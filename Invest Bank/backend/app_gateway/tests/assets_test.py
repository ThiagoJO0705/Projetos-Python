from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from app_gateway.app.main import app

client = TestClient(app)

MOCK_ASSET_DETAILS = {
    'ticker': 'AAPL',
    'name': 'Apple Inc.',
    'type': 'AÇÕES',
    'current_price': 240.50,
    'currency': 'USD'
}

MOCK_DB_ASSETS = [
    {'ticker': 'PETR4.SA', 'name': 'Petrobras', 'type': 'AÇÕES'},
    {'ticker': 'BTC-USD', 'name': 'Bitcoin', 'type': 'CRIPTO'}
]

@patch("app_gateway.services.yfinance_services.YahooService.get_asset_details")
@patch("app_gateway.services.yfinance_services.YahooService.get_market_variation")
def test_search_by_ticker_success(mock_variation, mock_details):
    mock_details.return_value = MOCK_ASSET_DETAILS.copy()
    mock_variation.return_value = 1.5
    response = client.get("/assets/search/ticker/AAPL")
    assert response.status_code == 200
    assert response.json()["ticker"] == "AAPL"
    assert response.json()["variation_24h"] == "1.5%"

@patch("app_gateway.services.yfinance_services.YahooService.get_asset_details")
def test_search_by_ticker_not_found(mock_details):
    mock_details.return_value = None
    response = client.get("/assets/search/ticker/INVALIDO")
    assert response.status_code == 404
    assert "não foi encontrado" in response.json()["detail"]

@patch("yfinance.Search")
def test_search_by_name_success(mock_yf_search):
    mock_instance = MagicMock()
    mock_instance.quotes = [{'symbol': 'AAPL', 'shortname': 'Apple Inc.', 'quoteType': 'EQUITY'}]
    mock_yf_search.return_value = mock_instance
    response = client.get("/assets/search/name/Apple")
    assert response.status_code == 200
    assert response.json()[0]["ticker"] == "AAPL"

@patch("yfinance.Search")
def test_search_by_name_not_found(mock_yf_search):
    mock_instance = MagicMock()
    mock_instance.quotes = []
    mock_yf_search.return_value = mock_instance
    response = client.get("/assets/search/name/Inexistente")
    assert response.status_code == 404
    assert "Nenhum ativo encontrado" in response.json()["detail"]

@patch("yfinance.Search")
def test_search_by_name_exception(mock_yf_search):
    mock_yf_search.side_effect = Exception("Falha no Yahoo")
    response = client.get("/assets/search/name/Apple")    
    assert response.status_code == 500
    assert "Erro ao realizar busca" in response.json()["detail"]
