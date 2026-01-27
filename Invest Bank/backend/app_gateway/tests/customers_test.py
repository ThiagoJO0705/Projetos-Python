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

def test_get_customer_me_success():
    app.dependency_overrides[get_or_create_pyinvest_user] = mock_active_user
    response = client.get("/customer/me")
    assert response.status_code == 200
    assert response.json()["name"] == "Thiago"

@patch("app_gateway.services.customers_services.CustomerDataService.update_customer", new_callable=AsyncMock)
def test_update_customer_success(mock_update):
    app.dependency_overrides[get_or_create_pyinvest_user] = mock_active_user
    mock_update.return_value = {"id": USER_ID, "name": "Thiago", "investor_profile": "ARROJADO"}
    
    payload = {"investor_profile": "ARROJADO"}
    response = client.patch("/customer/me", json=payload)
    
    assert response.status_code == 200
    assert response.json()["user"]["investor_profile"] == "ARROJADO"

def test_update_customer_empty_payload():
    app.dependency_overrides[get_or_create_pyinvest_user] = mock_active_user
    response = client.patch("/customer/me", json={})
    assert response.status_code == 400
    assert response.json()["detail"] == "Nenhum dado fornecido para atualização."
