import pytest
from decimal import Decimal
from app_customer.app.main import app
from app_customer.app.api.dependencies import verify_token, verify_admin

MOCK_USER = {
    'id': 1, 'name': 'Thiago', 'email': 't@t.com', 'phone_number': '123', 'cpf': '123',
    'account_balance': Decimal('100.00'), 'is_account_holder': True, 'is_active': True, 'is_admin': False
}
MOCK_ADMIN = {
    'id': 99, 'name': 'Admin', 'email': 'admin@javer.com', 'phone_number': '0', 'cpf': '0',
    'account_balance': Decimal('0.00'), 'is_admin': True, 'is_active': True, 'is_account_holder': True
}

@pytest.fixture
def auth_admin():
    app.dependency_overrides[verify_token] = lambda: MOCK_ADMIN
    app.dependency_overrides[verify_admin] = lambda: MOCK_ADMIN
    yield MOCK_ADMIN
    app.dependency_overrides = {}

@pytest.fixture
def auth_user():
    app.dependency_overrides[verify_token] = lambda: MOCK_USER
    app.dependency_overrides[verify_admin] = None 
    yield MOCK_USER
    app.dependency_overrides = {}

def test_get_customers_success(client, auth_admin, mocker):
    mocker.patch('app_customer.services.customer_service.CustomerService.get_all', return_value=[MOCK_USER])
    response = client.get('/admin/customers', headers={'Authorization': 'Bearer fake'})
    assert response.status_code == 200
    assert float(response.json()[0]['score']) == 10.0

def test_update_customer_as_owner(client, auth_user, mocker):
    mocker.patch('app_customer.services.customer_service.CustomerService.update', return_value=MOCK_USER)
    response = client.patch('/admin/customers/1', json={'name': 'Novo Nome', 'is_admin': True}, headers={'Authorization': 'Bearer fake'})
    assert response.status_code == 200

def test_update_customer_forbidden(client, auth_user):
    response = client.patch('/admin/customers/99', json={'name': 'Hack'}, headers={'Authorization': 'Bearer fake'})
    assert response.status_code == 403

def test_disable_customer_forbidden(client, auth_user, mocker):
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_id', return_value=MOCK_ADMIN)
    response = client.delete('/admin/customers/disable/99', headers={'Authorization': 'Bearer fake'})
    assert response.status_code == 403

def test_disable_customer_high_balance(client, auth_admin, mocker):
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_id', return_value=MOCK_USER)
    response = client.delete('/admin/customers/disable/1', headers={'Authorization': 'Bearer fake'})
    assert response.status_code == 400

def test_disable_self_admin_error(client, auth_admin, mocker):
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_id', return_value=MOCK_ADMIN)
    response = client.delete('/admin/customers/disable/99', headers={'Authorization': 'Bearer fake'})
    assert response.status_code == 400
    assert 'Autodesativação' in response.json()['detail']

def test_disable_last_admin_error(client, auth_admin, mocker):
    target_admin = MOCK_ADMIN.copy()
    target_admin['id'] = 88
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_id', return_value=target_admin)
    mocker.patch('app_customer.services.customer_service.CustomerService.get_all', return_value=[MOCK_ADMIN])
    response = client.delete('/admin/customers/disable/88', headers={'Authorization': 'Bearer fake'})
    assert response.status_code == 400
    assert 'Último administrador' in response.json()['detail']

def test_disable_customer_success(client, auth_admin, mocker):
    user_zero = MOCK_USER.copy()
    user_zero['account_balance'] = 0
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_id', return_value=user_zero)
    mocker.patch('app_customer.services.customer_service.CustomerService.update', return_value=user_zero)
    
    response = client.delete('/admin/customers/disable/1', headers={'Authorization': 'Bearer fake'})
    assert response.status_code == 200

def test_activate_customer_not_found(client, auth_admin, mocker):
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_id', return_value=None)
    response = client.patch('/admin/customer/activate/999', headers={'Authorization': 'Bearer fake'})
    assert response.status_code == 404

def test_activate_already_active(client, auth_admin, mocker):
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_id', return_value=MOCK_USER)
    response = client.patch('/admin/customer/activate/1', headers={'Authorization': 'Bearer fake'})
    assert response.status_code == 400

def test_activate_success(client, auth_admin, mocker):
    user_inativo = MOCK_USER.copy()
    user_inativo['is_active'] = False
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_id', return_value=user_inativo)
    mocker.patch('app_customer.services.customer_service.CustomerService.update', return_value=MOCK_USER)
    
    response = client.patch('/admin/customer/activate/1', headers={'Authorization': 'Bearer fake'})
    assert response.status_code == 200