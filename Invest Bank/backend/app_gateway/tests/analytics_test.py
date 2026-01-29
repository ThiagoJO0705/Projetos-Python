import pytest
import uuid
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from app_gateway.app.main import app
from app_gateway.app.dependencies import validate_active_investor
from app_data.schemas.enums import InvestmentType, InvestorProfile

client = TestClient(app)

HEADERS = {"Authorization": "Bearer fake_token"}
USER_UUID = str(uuid.uuid4())
INVESTMENT_UUID = str(uuid.uuid4())

MOCK_USER_CONTEXT = {
    'javer': {'balance': 5000.0, 'cpf': '123', 'name': 'Thiago'},
    'pyinvest': {'id': USER_UUID, 'is_active': True, 'investor_profile': InvestorProfile.MODERATE, 'total_assets': 1000.0}
}

MOCK_STOCK = {
    'id': INVESTMENT_UUID,
    'quantity': 10.0,
    'purchase_price': 100.0,
    'asset': {
        'ticker': 'AAPL',
        'type': InvestmentType.STOCKS,
        'currency': 'USD'
    }
}

MOCK_FIXED = {
    'id': str(uuid.uuid4()),
    'quantity': 1000.0,
    'purchase_price': 1.0,
    'is_active': True,
    'asset': {
        'ticker': 'CDB-TEST',
        'type': InvestmentType.FIXED_INCOME,
        'currency': 'BRL'
    }
}

@pytest.fixture(autouse=True)
def setup_dependency_overrides():
    app.dependency_overrides[validate_active_investor] = lambda: MOCK_USER_CONTEXT
    yield
    app.dependency_overrides = {}
