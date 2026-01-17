import pytest
import respx
import httpx
from decimal import Decimal
from fastapi import HTTPException
from app_customer.services.customer_service import CustomerService
from app_customer.services.transaction_services import TransactionService

CUSTOMER_URL = 'http://127.0.0.1:8001/customers'
TRANSACTION_URL = 'http://127.0.0.1:8001/transactions'

@respx.mock
@pytest.mark.asyncio
async def test_customer_service_calculate_score():
    assert CustomerService.calculate_score(Decimal('100.00')) == Decimal('10.00')
    assert CustomerService.calculate_score(0) == 0

@respx.mock
@pytest.mark.asyncio
async def test_customer_service_create_success():
    respx.post(f'{CUSTOMER_URL}/').mock(return_value=httpx.Response(201, json={'id': 1}))
    result = await CustomerService.create({'name': 'Thiago'})
    assert result['id'] == 1

@respx.mock
@pytest.mark.asyncio
async def test_customer_service_create_fail():
    respx.post(f'{CUSTOMER_URL}/').mock(return_value=httpx.Response(400, json={'detail': 'Erro'}))
    with pytest.raises(HTTPException):
        await CustomerService.create({})

@respx.mock
@pytest.mark.asyncio
async def test_customer_service_get_by_id_success():
    respx.get(f'{CUSTOMER_URL}/1').mock(return_value=httpx.Response(200, json={'id': 1, 'account_balance': '500.00'}))
    result = await CustomerService.get_by_id(1)
    assert result['score'] == 50.0

@respx.mock
@pytest.mark.asyncio
async def test_customer_service_get_by_id_fail():
    respx.get(f'{CUSTOMER_URL}/1').mock(return_value=httpx.Response(404))
    with pytest.raises(HTTPException):
        await CustomerService.get_by_id(1)

@respx.mock
@pytest.mark.asyncio
async def test_customer_service_get_by_filter_success():
    respx.get(f'{CUSTOMER_URL}/filter').mock(return_value=httpx.Response(200, json={'id': 1}))
    result = await CustomerService.get_by_filter({'email': 't@t.com'})
    assert result['id'] == 1

@respx.mock
@pytest.mark.asyncio
async def test_customer_service_get_by_filter_none():
    respx.get(f'{CUSTOMER_URL}/filter').mock(return_value=httpx.Response(404))
    result = await CustomerService.get_by_filter({'email': 'x@x.com'})
    assert result is None

@respx.mock
@pytest.mark.asyncio
async def test_customer_service_update_success():
    respx.patch(f'{CUSTOMER_URL}/1').mock(return_value=httpx.Response(200, json={'id': 1}))
    result = await CustomerService.update(1, {'name': 'Novo'})
    assert result['id'] == 1

@respx.mock
@pytest.mark.asyncio
async def test_customer_service_update_fail():
    respx.patch(f'{CUSTOMER_URL}/1').mock(return_value=httpx.Response(400, json={'detail': 'Erro'}))
    with pytest.raises(HTTPException):
        await CustomerService.update(1, {})

@respx.mock
@pytest.mark.asyncio
async def test_customer_service_get_all_success():
    respx.get(f'{CUSTOMER_URL}/').mock(return_value=httpx.Response(200, json=[]))
    result = await CustomerService.get_all({})
    assert result == []

@respx.mock
@pytest.mark.asyncio
async def test_customer_service_get_all_fail():
    respx.get(f'{CUSTOMER_URL}/').mock(return_value=httpx.Response(500))
    with pytest.raises(HTTPException):
        await CustomerService.get_all({})

@respx.mock
@pytest.mark.asyncio
async def test_transaction_service_register_with_decimal():
    respx.post(f'{TRANSACTION_URL}/').mock(return_value=httpx.Response(201, json={'id': 1}))
    data = {'amount': Decimal('10.00'), 'customer_id': 1}
    await TransactionService.register(data)

@respx.mock
@pytest.mark.asyncio
async def test_transaction_service_register_with_float():
    respx.post(f'{TRANSACTION_URL}/').mock(return_value=httpx.Response(201, json={'id': 1}))
    data = {'amount': 10.0, 'customer_id': 1}
    await TransactionService.register(data)

@respx.mock
@pytest.mark.asyncio
async def test_transaction_service_register_fail():
    respx.post(f'{TRANSACTION_URL}/').mock(return_value=httpx.Response(400, json={'detail': 'Erro'}))
    with pytest.raises(HTTPException):
        await TransactionService.register({'amount': 10.0})

@respx.mock
@pytest.mark.asyncio
async def test_transaction_service_get_statement_success():
    respx.get(f'{TRANSACTION_URL}/customer/1').mock(return_value=httpx.Response(200, json=[]))
    result = await TransactionService.get_statement(1)
    assert result == []

@respx.mock
@pytest.mark.asyncio
async def test_transaction_service_get_statement_fail():
    respx.get(f'{TRANSACTION_URL}/customer/1').mock(return_value=httpx.Response(404))
    with pytest.raises(HTTPException):
        await TransactionService.get_statement(1)