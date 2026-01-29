import pytest
import uuid
from datetime import datetime
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from app_gateway.app.main import app
from app_gateway.app.dependencies import validate_active_investor
from fastapi.security import HTTPAuthorizationCredentials
from app_data.schemas.enums import InvestmentType

client = TestClient(app)

HEADERS = {"Authorization": "Bearer fake_token"}
USER_UUID = str(uuid.uuid4())
ASSET_UUID = str(uuid.uuid4())
INVESTMENT_UUID = str(uuid.uuid4())
NOW_ISO = datetime.utcnow().isoformat()

MOCK_USER_CONTEXT = {
    'javer': {'balance': 5000.0, 'cpf': '123', 'name': 'Thiago'},
    'pyinvest': {'id': USER_UUID, 'is_active': True, 'investor_profile': 'MODERADO', 'total_assets': 1000.0}
}

def get_full_investment_mock(ticker="AAPL", currency="USD", inv_type="AÇÕES"):
    return {
        'id': INVESTMENT_UUID,
        'customer_id': USER_UUID,
        'asset_id': ASSET_UUID,
        'quantity': 10.0,
        'purchase_price': 100.0,
        'is_active': True,
        'application_date': NOW_ISO,
        'asset': {
            'id': ASSET_UUID,
            'ticker': ticker,
            'name': 'Empresa Teste',
            'type': inv_type,
            'currency': currency,
            'current_price': 150.0,
            'last_updated': NOW_ISO
        },
        'customer': {
            'id': USER_UUID,
            'name': 'Thiago',
            'email': 't@t.com',
            'phone_number': '123',
            'cpf': '123',
            'total_assets': 1000.0,
            'is_active': True
        }
    }

@pytest.fixture(autouse=True)
def setup_dependency_overrides():
    app.dependency_overrides[validate_active_investor] = lambda: MOCK_USER_CONTEXT
    from app_gateway.app.api.routes.investments import security
    app.dependency_overrides[security] = lambda: HTTPAuthorizationCredentials(scheme="Bearer", credentials="fake")
    yield
    app.dependency_overrides = {}

@patch("app_gateway.services.investments_services.InvestmentDataService.get_customer_investments", new_callable=AsyncMock)
@patch("app_gateway.services.yfinance_services.YahooService.get_usd_brl_rate", return_value=5.0)
@patch("app_gateway.services.yfinance_services.YahooService.get_current_price", return_value=150.0)
def test_get_my_investments_success(mock_price, mock_usd, mock_get_inv):
    mock_get_inv.return_value = [
        get_full_investment_mock("AAPL", "USD", "AÇÕES"),
        get_full_investment_mock("CDB-1", "BRL", "RENDA_FIXA"),
        get_full_investment_mock("PETR4.SA", "BRL", "AÇÕES")
    ]
    response = client.get("/investments/me", headers=HEADERS)
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert "current_value_brl" in response.json()[0]

@patch("app_gateway.services.yfinance_services.YahooService.get_asset_details")
@patch("app_gateway.services.assets_services.AssetDataService.get_asset_by_ticker", new_callable=AsyncMock)
@patch("app_gateway.services.investments_services.InvestmentDataService.create_investment", new_callable=AsyncMock)
@patch("app_gateway.services.javer_services.JaverService.debit_account", new_callable=AsyncMock)
@patch("app_gateway.services.customers_services.CustomerDataService.update_customer", new_callable=AsyncMock)
@patch("app_gateway.services.yfinance_services.YahooService.get_usd_brl_rate", return_value=5.0)
def test_buy_stock_usd_success(mock_usd, mock_up, mock_debit, mock_create, mock_get_asset, mock_yahoo):
    mock_yahoo.return_value = {'current_price': 100.0, 'currency': 'USD', 'ticker': 'AAPL'}
    mock_get_asset.return_value = {'id': ASSET_UUID}
    mock_create.return_value = get_full_investment_mock()
    response = client.post("/investments/buy", json={"ticker": "AAPL", "quantity": 1}, headers=HEADERS)
    assert response.status_code == 200
    mock_debit.assert_called_once()
    mock_up.assert_called_once()

@patch("app_gateway.services.assets_services.AssetDataService.get_asset_by_ticker", new_callable=AsyncMock, return_value=None)
@patch("app_gateway.services.assets_services.AssetDataService.create_asset", new_callable=AsyncMock, return_value={'id': ASSET_UUID})
@patch("app_gateway.services.investments_services.InvestmentDataService.create_investment", new_callable=AsyncMock)
@patch("app_gateway.services.javer_services.JaverService.debit_account", new_callable=AsyncMock)
@patch("app_gateway.services.customers_services.CustomerDataService.update_customer", new_callable=AsyncMock)
def test_buy_fixed_income_success(mock_up, mock_debit, mock_create, mock_create_asset, mock_get_asset):
    mock_create.return_value = {'id': INVESTMENT_UUID}
    response = client.post("/investments/buy", json={"ticker": "CDB123", "quantity": 10}, headers=HEADERS)
    assert response.status_code == 200
    mock_create_asset.assert_called_once()

@patch("app_gateway.services.yfinance_services.YahooService.get_asset_details")
def test_buy_errors(mock_yahoo):
    mock_yahoo.return_value = None
    assert client.post("/investments/buy", json={"ticker": "ERRO", "quantity": 1}, headers=HEADERS).status_code == 404
    mock_yahoo.return_value = {'current_price': 10000.0, 'currency': 'BRL'}
    assert client.post("/investments/buy", json={"ticker": "CARO", "quantity": 1}, headers=HEADERS).status_code == 400

@patch("app_gateway.services.javer_services.JaverService.debit_account", side_effect=Exception("Erro"))
@patch("app_gateway.services.investments_services.InvestmentDataService.create_investment", new_callable=AsyncMock, return_value={'id': 'id'})
@patch("app_gateway.services.investments_services.InvestmentDataService.delete_investment", new_callable=AsyncMock)
@patch("app_gateway.services.customers_services.CustomerDataService.update_customer", new_callable=AsyncMock)
@patch("app_gateway.services.assets_services.AssetDataService.get_asset_by_ticker", new_callable=AsyncMock, return_value={'id': 'id'})
@patch("app_gateway.services.yfinance_services.YahooService.get_asset_details", return_value={'current_price': 1, 'currency': 'BRL'})
def test_buy_rollback(mock_yahoo, mock_ga, mock_up, mock_delete, mock_create, mock_debit):
    response = client.post("/investments/buy", json={"ticker": "TEST", "quantity": 1}, headers=HEADERS)
    assert response.status_code == 500
    mock_delete.assert_called_once()
