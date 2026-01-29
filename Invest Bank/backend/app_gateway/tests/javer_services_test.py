import pytest
import httpx
from fastapi import HTTPException
from unittest.mock import MagicMock, patch
from app_gateway.services.javer_services import JaverService

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_get_user_data_from_javer_success(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "cpf": "123",
        "account_balance": 5000,
        "name": "Thiago",
        "email": "t@t.com",
        "phone_number": "9999",
        "is_admin": True,
        "id": "user-id"
    }
    mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
    result = await JaverService.get_user_data_from_javer("fake-token")
    assert result["cpf"] == "123"
    assert result["balance"] == 5000.0
    assert result["is_admin"] is True

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_get_user_data_from_javer_invalid_token(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
    with pytest.raises(HTTPException) as exc:
        await JaverService.get_user_data_from_javer("invalid-token")
    assert exc.value.status_code == 401

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_get_user_data_from_javer_connection_error(mock_client):
    mock_client.return_value.__aenter__.return_value.get.side_effect = httpx.ConnectError("fail")
    with pytest.raises(HTTPException) as exc:
        await JaverService.get_user_data_from_javer("token")
    assert exc.value.status_code == 503

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_get_user_data_from_javer_generic_error(mock_client):
    mock_client.return_value.__aenter__.return_value.get.side_effect = Exception("boom")
    with pytest.raises(HTTPException) as exc:
        await JaverService.get_user_data_from_javer("token")
    assert exc.value.status_code == 500

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_debit_account_success(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "ok"}
    mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
    result = await JaverService.debit_account("token", 100, "AAPL")
    assert result["status"] == "ok"

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_debit_account_business_error(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"detail": "Saldo insuficiente"}
    mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
    with pytest.raises(HTTPException) as exc:
        await JaverService.debit_account("token", 10000, "AAPL")
    assert exc.value.status_code == 400
    assert "Saldo insuficiente" in exc.value.detail

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_debit_account_exception(mock_client):
    mock_client.return_value.__aenter__.return_value.post.side_effect = Exception("timeout")
    with pytest.raises(HTTPException) as exc:
        await JaverService.debit_account("token", 100, "AAPL")
    assert exc.value.status_code == 500

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_credit_account_success(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"credited": True}
    mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
    result = await JaverService.credit_account("token", 500)
    assert result["credited"] is True

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_credit_account_error(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
    with pytest.raises(HTTPException) as exc:
        await JaverService.credit_account("token", 500)
    assert exc.value.status_code == 400