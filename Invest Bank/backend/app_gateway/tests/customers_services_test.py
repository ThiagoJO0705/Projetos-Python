import pytest
import uuid
from fastapi import HTTPException
from unittest.mock import patch, MagicMock
from app_gateway.services.customers_services import CustomerDataService

@pytest.mark.asyncio
@patch("httpx.AsyncClient")
class TestCustomerDataService:
    async def test_get_all_customers_success(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"name": "João"}]
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
        result = await CustomerDataService.get_all_customers(name="João")
        assert result == [{"name": "João"}]

    async def test_get_all_customers_error(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
        with pytest.raises(HTTPException) as exc:
            await CustomerDataService.get_all_customers()
        assert exc.value.status_code == 500

    async def test_get_customer_by_id_success(self, mock_client):
        customer_id = uuid.uuid4()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": str(customer_id)}
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
        result = await CustomerDataService.get_customer_by_id(customer_id)
        assert result["id"] == str(customer_id)

    async def test_get_customer_by_id_not_found(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
        with pytest.raises(HTTPException) as exc:
            await CustomerDataService.get_customer_by_id(uuid.uuid4())
        assert exc.value.status_code == 404

    async def test_get_customer_by_id_error(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
        with pytest.raises(HTTPException) as exc:
            await CustomerDataService.get_customer_by_id(uuid.uuid4())
        assert exc.value.status_code == 500

    async def test_create_customer_success(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": "123", "email": "a@a.com"}
        mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
        result = await CustomerDataService.create_customer({"email": "a@a.com"})
        assert result["email"] == "a@a.com"

    async def test_create_customer_validation_error(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"detail": "CPF inválido"}
        mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
        with pytest.raises(HTTPException) as exc:
            await CustomerDataService.create_customer({"cpf": "000"})
        assert exc.value.status_code == 400

    async def test_create_customer_internal_error(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
        with pytest.raises(HTTPException) as exc:
            await CustomerDataService.create_customer({"email": "a@a.com"})
        assert exc.value.status_code == 500

    async def test_update_customer_success(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"is_active": False}
        mock_client.return_value.__aenter__.return_value.patch.return_value = mock_response
        result = await CustomerDataService.update_customer(uuid.uuid4(), {"is_active": False})
        assert result["is_active"] is False

    async def test_update_customer_not_found(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_client.return_value.__aenter__.return_value.patch.return_value = mock_response
        with pytest.raises(HTTPException) as exc:
            await CustomerDataService.update_customer(uuid.uuid4(), {})
        assert exc.value.status_code == 404

    async def test_update_customer_error(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_client.return_value.__aenter__.return_value.patch.return_value = mock_response
        with pytest.raises(HTTPException) as exc:
            await CustomerDataService.update_customer(uuid.uuid4(), {})
        assert exc.value.status_code == 500

    async def test_get_customer_by_filter_success(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"email": "a@a.com"}
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
        result = await CustomerDataService.get_customer_by_filter(email="a@a.com")
        assert result["email"] == "a@a.com"

    async def test_get_customer_by_filter_not_found(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
        result = await CustomerDataService.get_customer_by_filter(email="x@x.com")
        assert result is None

    async def test_soft_delete_investor_success(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client.return_value.__aenter__.return_value.patch.return_value = mock_response
        result = await CustomerDataService.soft_delete_investor(uuid.uuid4())
        assert result is True

    async def test_soft_delete_investor_error(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_client.return_value.__aenter__.return_value.patch.return_value = mock_response
        with pytest.raises(HTTPException) as exc:
            await CustomerDataService.soft_delete_investor(uuid.uuid4())
        assert exc.value.status_code == 500