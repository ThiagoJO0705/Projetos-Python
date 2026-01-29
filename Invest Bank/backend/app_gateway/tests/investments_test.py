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
