import pytest
from jose import jwt
from passlib.context import CryptContext
from app_customer.app.api.dependencies import SECRET_KEY, ALGORITHM, generate_score
from app_customer.app.main import app
from app_customer.app.api.dependencies import verify_token
from fastapi import HTTPException

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

USER_DATA = {
    'name': 'Thiago Teste',
    'email': 'thiago@teste.com',
    'password': 'senha123',
    'phone_number': '11999999999',
    'cpf': '12345678901'
}

def test_signup_success(client, mocker):
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_filter', return_value=None)
    mocker.patch('app_customer.services.customer_service.CustomerService.create', return_value={
        'id': 1, 
        'name': 'Thiago Teste',
        'email': 'thiago@teste.com',
        'phone_number': '11999999999',
        'cpf': '12345678901',
        'account_balance': 0.0, 
        'is_active': True, 
        'is_admin': False,
        'is_account_holder': True
    })
    payload = {
        'name': 'Thiago Teste', 
        'email': 'thiago@teste.com', 
        'password': 'senha123', 
        'phone_number': '11999999999', 
        'cpf': '12345678901'
    }
    response = client.post('/auth/signup', json=payload)
    assert response.status_code == 201
    assert response.json()['is_account_holder'] is True

def test_signup_duplicate_email(client, mocker):
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_filter', return_value={'id': 1})
    response = client.post('/auth/signup', json=USER_DATA)
    assert response.status_code == 400
    assert 'Email' in response.json()['detail']

def test_signup_duplicate_cpf(client, mocker):
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_filter', side_effect=[None, {'id': 1}])
    response = client.post('/auth/signup', json=USER_DATA)
    assert response.status_code == 400
    assert 'CPF' in response.json()['detail']

def test_signup_duplicate_phone(client, mocker):
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_filter', side_effect=[None, None, {'id': 1}])
    response = client.post('/auth/signup', json=USER_DATA)
    assert response.status_code == 400
    assert 'Telefone' in response.json()['detail']

def test_signin_success(client, mocker):
    hash_senha = pwd_context.hash(USER_DATA['password'])
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_filter', return_value={'id': 1, 'email': USER_DATA['email'], 'password': hash_senha, 'is_active': True})
    response = client.post('/auth/signin', json={'email': USER_DATA['email'], 'password': USER_DATA['password']})
    assert response.status_code == 200
    assert 'access_token' in response.json()

def test_signin_wrong_password(client, mocker):
    hash_senha = pwd_context.hash('outra_senha')
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_filter', return_value={'id': 1, 'password': hash_senha})
    response = client.post('/auth/signin', json={'email': USER_DATA['email'], 'password': '123'})
    assert response.status_code == 400
    assert 'inválidas' in response.json()['detail']

def test_signin_inactive_user(client, mocker):
    hash_senha = pwd_context.hash(USER_DATA['password'])
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_filter', return_value={'id': 1, 'password': hash_senha, 'is_active': False})
    response = client.post('/auth/signin', json={'email': USER_DATA['email'], 'password': USER_DATA['password']})
    assert response.status_code == 401
    assert 'desativada' in response.json()['detail']

def test_signin_form_success(client, mocker):
    hash_senha = pwd_context.hash(USER_DATA['password'])
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_filter', return_value={'id': 1, 'password': hash_senha, 'is_active': True})
    response = client.post('/auth/signin-form', data={'username': USER_DATA['email'], 'password': USER_DATA['password']})
    assert response.status_code == 200

def test_refresh_token_success(client, mocker):
    mock_user = {'id': 1, 'is_active': True}
    app.dependency_overrides[verify_token] = lambda: mock_user 
    response = client.post('/auth/refresh', headers={'Authorization': 'Bearer fake'})
    assert response.status_code == 200
    assert 'access_token' in response.json()
    app.dependency_overrides = {}

def test_verify_token_user_not_found(client, mocker):
    payload = {'sub': '999', 'exp': 9999999999}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_id', return_value=None)
    response = client.post('/auth/refresh', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 401
    assert 'Acesso' in response.json()['detail']

def test_verify_token_malformed(client):
    response = client.post('/auth/refresh', headers={'Authorization': 'Bearer invalido'})
    assert response.status_code == 401

def test_generate_score_logic():
    assert generate_score(500) == 50.0
    assert generate_score(0) == 0.0
    assert generate_score(-10) == 0.0

def test_signin_user_not_found(client, mocker):
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_filter', return_value=None)
    response = client.post('/auth/signin', json={'email': 'errado@teste.com', 'password': '123'})
    assert response.status_code == 400
    assert 'não encontrado' in response.json()['detail']

def test_signin_form_fail(client, mocker):
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_filter', return_value=None)
    response = client.post('/auth_signin-form', data={'username': 'x', 'password': 'y'})
    response = client.post('/auth/signin-form', data={'username': 'errado', 'password': '123'})
    assert response.status_code == 400

def test_verify_token_inactive_user_error(client, mocker):
    payload = {'sub': '1', 'exp': 9999999999}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_id', return_value={'id': 1, 'is_active': False})
    
    response = client.post('/auth/refresh', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 401
    assert 'desativada' in response.json()['detail']

def test_verify_account_holder_fail(client, mocker):
    mock_not_holder = {'id': 1, 'is_active': True, 'is_account_holder': False}
    app.dependency_overrides[verify_token] = lambda: mock_not_holder
    from app_customer.app.api.dependencies import verify_account_holder
    with pytest.raises(HTTPException) as exc:
        verify_account_holder(mock_not_holder)
    assert exc.value.status_code == 403
    app.dependency_overrides = {}

def test_verify_admin_fail(client, mocker):
    mock_not_admin = {'id': 1, 'is_active': True, 'is_admin': False}
    from app_customer.app.api.dependencies import verify_admin
    with pytest.raises(HTTPException) as exc:
        verify_admin(mock_not_admin)
    assert exc.value.status_code == 403

def test_verify_token_malformed_payload(client, mocker):
    payload = {'sub': 'abc', 'exp': 9999999999}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    response = client.post('/auth/refresh', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 401

def test_verify_token_real_success_path(client, mocker):
    app.dependency_overrides = {}
    payload = {'sub': '1', 'exp': 9999999999}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_id', return_value={'id': 1, 'name': 'Thiago', 'is_active': True, 'account_balance': 100.0})
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/auth/refresh', headers=headers)
    assert response.status_code == 200
    assert 'access_token' in response.json()

def test_verify_account_holder_real_success_path(client, mocker):
    app.dependency_overrides = {} 
    payload = {'sub': '1', 'exp': 9999999999}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_id', return_value={'id': 1, 'is_active': True, 'is_account_holder': True, 'account_balance': 100.0})
    response = client.get('/banking/balance', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

def test_verify_admin_real_success_path(client, mocker):
    app.dependency_overrides = {}
    payload = {'sub': '99', 'exp': 9999999999}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    mocker.patch('app_customer.services.customer_service.CustomerService.get_by_id', return_value={'id': 99, 'is_active': True, 'is_admin': True})
    mocker.patch('app_customer.services.customer_service.CustomerService.get_all', return_value=[])
    response = client.get('/admin/customers', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

def test_get_current_user_success(client, mocker):
    mock_user = {
        "id": 1,
        "name": "Thiago Teste",
        "email": "thiago@teste.com",
        "account_balance": 1000.0,
        "is_active": True,
        "is_admin": False,
        "is_account_holder": True,
        "cpf": "12345678901",
        "phone_number": "11999999999"
    }

    from app_customer.app.api.dependencies import verify_token
    app.dependency_overrides[verify_token] = lambda: mock_user
    response = client.get("/auth/me", headers={"Authorization": "Bearer token-qualquer"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Thiago Teste"
    assert float(data["score"]) == 100.0
    app.dependency_overrides = {}