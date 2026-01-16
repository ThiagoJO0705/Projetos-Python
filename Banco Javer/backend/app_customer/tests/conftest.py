import pytest
from fastapi.testclient import TestClient
from app_customer.app.main import app 
from app_customer.app.api.dependencies import verify_token, verify_admin

@pytest.fixture(scope="function")
def client():
    app.dependency_overrides = {}
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}

@pytest.fixture
def mock_user_auth(client):
    """Força o FastAPI a acreditar que um usuário comum está logado"""
    mock_user = {
        "id": 1, "name": "User", "email": "u@u.com", "is_active": True, 
        "is_admin": False, "is_account_holder": True, "account_balance": 100.0,
        "cpf": "123", "phone_number": "123"
    }
    app.dependency_overrides[verify_token] = lambda: mock_user
    return mock_user

@pytest.fixture
def mock_admin_auth(client):
    """Força o FastAPI a acreditar que um Admin está logado"""
    mock_admin = {
        "id": 99, "name": "Admin", "email": "a@a.com", "is_active": True, 
        "is_admin": True, "is_account_holder": True, "account_balance": 0.0,
        "cpf": "000", "phone_number": "000"
    }
    app.dependency_overrides[verify_token] = lambda: mock_admin
    app.dependency_overrides[verify_admin] = lambda: mock_admin
    return mock_admin