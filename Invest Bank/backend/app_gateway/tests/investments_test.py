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
