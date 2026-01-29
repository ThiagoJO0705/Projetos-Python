import pytest
import uuid
from fastapi import HTTPException
from unittest.mock import MagicMock, patch
from app_gateway.services.investments_services import InvestmentDataService

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_get_all_investments_success(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": "1"}]
    mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
    result = await InvestmentDataService.get_all_investments()
    assert result == [{"id": "1"}]

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_get_all_investments_error(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
    with pytest.raises(HTTPException) as exc:
        await InvestmentDataService.get_all_investments()
    assert exc.value.status_code == 500

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_get_customer_investments_success(mock_client):
    customer_id = uuid.uuid4()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"asset": "PETR4"}]
    mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
    result = await InvestmentDataService.get_customer_investments(customer_id)
    assert result == [{"asset": "PETR4"}]

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_get_customer_investments_not_found(mock_client):
    customer_id = uuid.uuid4()
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
    result = await InvestmentDataService.get_customer_investments(customer_id)
    assert result == []

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_get_customer_investments_error(mock_client):
    customer_id = uuid.uuid4()
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
    with pytest.raises(HTTPException) as exc:
        await InvestmentDataService.get_customer_investments(customer_id)
    assert exc.value.status_code == 500

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_get_investment_by_id_success(mock_client):
    investment_id = uuid.uuid4()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": str(investment_id)}
    mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
    result = await InvestmentDataService.get_investment_by_id(investment_id)
    assert result["id"] == str(investment_id)

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_get_investment_by_id_not_found(mock_client):
    investment_id = uuid.uuid4()
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
    with pytest.raises(HTTPException) as exc:
        await InvestmentDataService.get_investment_by_id(investment_id)
    assert exc.value.status_code == 404

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_create_investment_success(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": "123"}
    mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
    result = await InvestmentDataService.create_investment({"quantity": 10})
    assert result["id"] == "123"

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_create_investment_bad_request(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"detail": "Dados inválidos"}
    mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
    with pytest.raises(HTTPException) as exc:
        await InvestmentDataService.create_investment({})
    assert exc.value.status_code == 400

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_create_investment_internal_error(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
    with pytest.raises(HTTPException) as exc:
        await InvestmentDataService.create_investment({})
    assert exc.value.status_code == 500

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_update_investment_success(mock_client):
    investment_id = uuid.uuid4()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"quantity": 5}
    mock_client.return_value.__aenter__.return_value.patch.return_value = mock_response
    result = await InvestmentDataService.update_investment(investment_id, {"quantity": 5})
    assert result["quantity"] == 5

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_update_investment_not_found(mock_client):
    investment_id = uuid.uuid4()
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_client.return_value.__aenter__.return_value.patch.return_value = mock_response
    with pytest.raises(HTTPException) as exc:
        await InvestmentDataService.update_investment(investment_id, {})
    assert exc.value.status_code == 404

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_delete_investment_success(mock_client):
    investment_id = uuid.uuid4()
    mock_response = MagicMock()
    mock_response.status_code = 204
    mock_client.return_value.__aenter__.return_value.delete.return_value = mock_response
    result = await InvestmentDataService.delete_investment(investment_id)
    assert result is True

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
async def test_delete_investment_not_found(mock_client):
    investment_id = uuid.uuid4()
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_client.return_value.__aenter__.return_value.delete.return_value = mock_response
    with pytest.raises(HTTPException) as exc:
        await InvestmentDataService.delete_investment(investment_id)
    assert exc.value.status_code == 404