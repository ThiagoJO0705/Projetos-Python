import pytest
import uuid
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app_gateway.app.main import app
from app_gateway.app.dependencies import get_or_create_pyinvest_user

client = TestClient(app)
USER_ID = str(uuid.uuid4())

def mock_active_user():
    return {
        "javer": {"name": "Thiago", "cpf": "123", "balance": 1000.0, "is_admin": False},
        "pyinvest": {"id": USER_ID, "name": "Thiago", "is_active": True, "investor_profile": "MODERATE"},
        "is_admin": False
    }

def mock_admin_user():
    return {
        "javer": {"name": "Admin", "cpf": "000", "balance": 9999.0, "is_admin": True},
        "pyinvest": {"id": str(uuid.uuid4()), "name": "Admin", "is_active": True, "investor_profile": "BOLD"},
        "is_admin": True
    }

def mock_inactive_user():
    return {
        "javer": {"name": "Inativo", "cpf": "456", "balance": 0.0, "is_admin": False},
        "pyinvest": {"id": USER_ID, "name": "Inativo", "is_active": False, "investor_profile": "UNDEFINED"},
        "is_admin": False
    }

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    app.dependency_overrides = {}
    yield
    app.dependency_overrides = {}
