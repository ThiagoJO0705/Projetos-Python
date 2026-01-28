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

