import pytest
import uuid
from unittest.mock import patch, AsyncMock
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from app_gateway.app.dependencies import get_or_create_pyinvest_user, validate_active_investor
from app_data.schemas.enums import InvestorProfile

def fake_auth(token="valid-token", scheme="Bearer"):
    return HTTPAuthorizationCredentials(scheme=scheme, credentials=token)

def fake_javer_user():
    return {
        "cpf": "12345678900",
        "name": "Thiago",
        "email": "thiago@email.com",
        "phone_number": "11999999999",
        "is_admin": False,
        "balance": 1000.0,
        "id": 1
    }

def fake_pyinvest_user(active=True):
    return {
        "id": str(uuid.uuid4()),
        "name": "Thiago",
        "email": "thiago@email.com",
        "cpf": "12345678900",
        "investor_profile": InvestorProfile.UNDEFINED,
        "total_assets": 0.0,
        "is_active": active
    }

@pytest.mark.asyncio
@patch("app_gateway.app.dependencies.JaverService.get_user_data_from_javer", new_callable=AsyncMock)
@patch("app_gateway.app.dependencies.CustomerDataService.get_customer_by_filter", new_callable=AsyncMock)
@patch("app_gateway.app.dependencies.CustomerDataService.create_customer", new_callable=AsyncMock)
async def test_auto_signup_new_user(mock_create, mock_get, mock_javer):
    mock_javer.return_value = fake_javer_user()
    mock_get.return_value = None
    mock_create.return_value = fake_pyinvest_user()
    result = await get_or_create_pyinvest_user(fake_auth())
    assert result["javer"]["cpf"] == "12345678900"
    mock_create.assert_called_once()

@pytest.mark.asyncio
@patch("app_gateway.app.dependencies.JaverService.get_user_data_from_javer", new_callable=AsyncMock)
@patch("app_gateway.app.dependencies.CustomerDataService.get_customer_by_filter", new_callable=AsyncMock)
@patch("app_gateway.app.dependencies.CustomerDataService.update_customer", new_callable=AsyncMock)
async def test_sync_user_data_mismatch(mock_update, mock_get, mock_javer):
    javer_data = fake_javer_user()
    javer_data["name"] = "Thiago Novo"
    javer_data["email"] = "novo@email.com"
    py_data = fake_pyinvest_user()
    mock_javer.return_value = javer_data
    mock_get.return_value = py_data
    mock_update.return_value = {**py_data, "name": "Thiago Novo", "email": "novo@email.com"}
    result = await get_or_create_pyinvest_user(fake_auth())
    assert result["pyinvest"]["name"] == "Thiago Novo"
    assert mock_update.called 

@pytest.mark.asyncio
@patch("app_gateway.app.dependencies.JaverService.get_user_data_from_javer", new_callable=AsyncMock)
@patch("app_gateway.app.dependencies.CustomerDataService.get_customer_by_filter", new_callable=AsyncMock)
async def test_existing_user_no_changes(mock_get, mock_javer):
    mock_javer.return_value = fake_javer_user()
    mock_get.return_value = fake_pyinvest_user()
    result = await get_or_create_pyinvest_user(fake_auth())
    assert result["pyinvest"]["name"] == "Thiago"

@pytest.mark.asyncio
async def test_validate_active_ok():
    context = {"pyinvest": {"is_active": True}}
    result = await validate_active_investor(context)
    assert result == context

@pytest.mark.asyncio
async def test_validate_active_forbidden():
    context = {"pyinvest": {"is_active": False}}
    with pytest.raises(HTTPException) as exc:
        await validate_active_investor(context)
    assert exc.value.status_code == 403