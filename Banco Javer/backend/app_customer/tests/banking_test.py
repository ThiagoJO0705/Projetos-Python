import pytest
from decimal import Decimal
from app_customer.app.main import app
from app_customer.app.api.dependencies import verify_token, verify_account_holder

MOCK_SENDER = {
    'id': 1, 'name': 'Sender', 'email': 's@s.com', 'account_balance': Decimal('100.00'),
    'is_active': True, 'is_account_holder': True, 'cpf': '111', 'phone_number': '111'
}

MOCK_RECEIVER = {
    'id': 2, 'name': 'Receiver', 'email': 'r@r.com', 'account_balance': Decimal('0.00'),
    'is_active': True, 'is_account_holder': True, 'cpf': '222', 'phone_number': '222'
}

MOCK_TX_FULL = {
    'id': 99, 'amount': Decimal('30.00'), 'type': 'PIX', 'direction': 'DEBIT',
    'description': 'Teste', 'created_at': '2024-01-01T10:00:00'
}

@pytest.fixture
def auth_sender():
    app.dependency_overrides[verify_token] = lambda: MOCK_SENDER
    app.dependency_overrides[verify_account_holder] = lambda: MOCK_SENDER
    yield MOCK_SENDER
    app.dependency_overrides = {}

def test_get_balance_success(client, auth_sender):
    response = client.get('/banking/balance', headers={'Authorization': 'Bearer x'})
    assert response.status_code == 200
    assert float(response.json()['balance']) == 100.0

def test_deposit_success(client, auth_sender, mocker):
    mocker.patch('app_customer.services.transaction_services.TransactionService.register', return_value=MOCK_TX_FULL)
    updated_user = MOCK_SENDER.copy()
    updated_user['account_balance'] = Decimal('150.00')
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_id', return_value=updated_user)
    response = client.post('/banking/deposit', params={'deposit_value': 50.0}, headers={'Authorization': 'Bearer x'})
    assert response.status_code == 200
    assert float(response.json()['new_balance']) == 150.0

def test_payment_success(client, auth_sender, mocker):
    mocker.patch('app_customer.services.transaction_services.TransactionService.register', return_value=MOCK_TX_FULL)
    payment_data = {'amount': 40.0, 'method': 'BANK SLIP', 'description': 'Luz'}
    response = client.post('/banking/payment', json=payment_data, headers={'Authorization': 'Bearer x'})
    assert response.status_code == 200
    assert float(response.json()['new_balance']) == 60.0

def test_pix_success(client, auth_sender, mocker):
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_filter', return_value=MOCK_RECEIVER)
    mocker.patch('app_customer.services.transaction_services.TransactionService.register', return_value=MOCK_TX_FULL)
    pix_data = {'pix_key': '222', 'pix_amount': 30.0}
    response = client.post('/banking/pix', json=pix_data, headers={'Authorization': 'Bearer x'})
    assert response.status_code == 200
    assert float(response.json()['new_balance']) == 70.0

def test_get_statement_success(client, auth_sender, mocker):
    mocker.patch('app_customer.services.transaction_services.TransactionService.get_statement', return_value=[MOCK_TX_FULL])
    response = client.get('/banking/statement', headers={'Authorization': 'Bearer x'})
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_deposit_invalid_value(client, auth_sender):
    response = client.post('/banking/deposit', params={'deposit_value': 0}, headers={'Authorization': 'Bearer x'})
    assert response.status_code == 400

def test_payment_invalid_method(client, auth_sender):
    data = {'amount': 10, 'method': 'DEPOSIT', 'description': 'x'}
    response = client.post('/banking/payment', json=data, headers={'Authorization': 'Bearer x'})
    assert response.status_code == 400

def test_payment_zero_amount(client, auth_sender):
    data = {'amount': 0, 'method': 'PIX', 'description': 'x'}
    response = client.post('/banking/payment', json=data, headers={'Authorization': 'Bearer x'})
    assert response.status_code == 400

def test_payment_insufficient_funds(client, auth_sender):
    data = {'amount': 9999, 'method': 'PIX', 'description': 'x'}
    response = client.post('/banking/payment', json=data, headers={'Authorization': 'Bearer x'})
    assert response.status_code == 400

def test_pix_invalid_amount(client, auth_sender):
    data = {'pix_key': '222', 'pix_amount': -1}
    response = client.post('/banking/pix', json=data, headers={'Authorization': 'Bearer x'})
    assert response.status_code == 400

def test_pix_key_not_found(client, auth_sender, mocker):
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_filter', return_value=None)
    response = client.post('/banking/pix', json={'pix_key': '000', 'pix_amount': 10}, headers={'Authorization': 'Bearer x'})
    assert response.status_code == 404

def test_pix_to_self(client, auth_sender, mocker):
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_filter', return_value=MOCK_SENDER)
    response = client.post('/banking/pix', json={'pix_key': '111', 'pix_amount': 10}, headers={'Authorization': 'Bearer x'})
    assert response.status_code == 400

def test_pix_to_inactive_receiver(client, auth_sender, mocker):
    inactive = MOCK_RECEIVER.copy()
    inactive['is_active'] = False
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_filter', return_value=inactive)
    response = client.post('/banking/pix', json={'pix_key': '222', 'pix_amount': 10}, headers={'Authorization': 'Bearer x'})
    assert response.status_code == 400

def test_pix_to_non_holder(client, auth_sender, mocker):
    non_holder = MOCK_RECEIVER.copy()
    non_holder['is_account_holder'] = False
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_filter', return_value=non_holder)
    response = client.post('/banking/pix', json={'pix_key': '222', 'pix_amount': 10}, headers={'Authorization': 'Bearer x'})
    assert response.status_code == 400

def test_pix_insufficient_funds(client, auth_sender, mocker):
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_filter', return_value=MOCK_RECEIVER)
    response = client.post('/banking/pix', json={'pix_key': '222', 'pix_amount': 9999}, headers={'Authorization': 'Bearer x'})
    assert response.status_code == 400

def test_forbidden_banking(client):
    non_holder = MOCK_SENDER.copy()
    non_holder['is_account_holder'] = False
    app.dependency_overrides[verify_token] = lambda: non_holder
    response = client.get('/banking/balance', headers={'Authorization': 'Bearer x'})
    assert response.status_code == 403