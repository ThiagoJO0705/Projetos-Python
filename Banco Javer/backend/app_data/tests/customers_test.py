import pytest
from app_data.models.customer import Customer

PAYLOAD = {
    'name': 'Thiago Teste',
    'email': 'thiago@teste.com',
    'password': 'hash_password',
    'phone_number': '123456789',
    'cpf': '12345678901'
}

def test_create_customer_success(client):
    response = client.post('/customers/', json=PAYLOAD)
    assert response.status_code == 201
    assert response.json()['email'] == PAYLOAD['email']

def test_create_customer_db_error(client, mocker):
    mocker.patch('sqlalchemy.orm.Session.commit', side_effect=Exception('Erro de Banco'))
    response = client.post('/customers/', json=PAYLOAD)
    assert response.status_code == 400
    assert 'erro ao tentar salvar' in response.json()['detail'].lower()

def test_get_all_customers_with_all_filters(client):
    client.post('/customers/', json=PAYLOAD)
    url = '/customers/?is_active=true&is_account_holder=true&is_admin=false&name=Thiago'
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_get_all_customers_no_filters(client):
    client.post('/customers/', json=PAYLOAD)
    response = client.get('/customers/')
    assert response.status_code == 200

def test_filter_customer_by_email_success(client):
    client.post('/customers/', json=PAYLOAD)
    response = client.get(f'/customers/filter?email={PAYLOAD['email']}')
    assert response.status_code == 200

def test_filter_customer_by_cpf_success(client):
    client.post('/customers/', json=PAYLOAD)
    response = client.get(f'/customers/filter?cpf={PAYLOAD['cpf']}')
    assert response.status_code == 200

def test_filter_customer_by_phone_success(client):
    client.post('/customers/', json=PAYLOAD)
    response = client.get(f'/customers/filter?phone_number={PAYLOAD['phone_number']}')
    assert response.status_code == 200

def test_filter_customer_not_found(client):
    response = client.get('/customers/filter?email=inexistente@teste.com')
    assert response.status_code == 404

def test_filter_customer_no_params_error(client):
    response = client.get('/customers/filter')
    assert response.status_code == 400

def test_get_customer_by_id_success(client):
    client.post('/customers/', json=PAYLOAD)
    response = client.get('/customers/1')
    assert response.status_code == 200
    assert response.json()['id'] == 1

def test_get_customer_by_id_not_found(client):

    response = client.get('/customers/999')
    assert response.status_code == 404

def test_update_customer_success(client):
    client.post('/customers/', json=PAYLOAD)
    response = client.patch('/customers/1', json={'name': 'Novo Nome', 'is_active': False})
    assert response.status_code == 200
    assert response.json()['name'] == 'Novo Nome'
    assert response.json()['is_active'] is False

def test_update_customer_conflict_email(client):
    client.post('/customers/', json=PAYLOAD)
    user2 = PAYLOAD.copy()
    user2.update({'email': 'user2@t.com', 'cpf': '000', 'phone_number': '000'})
    client.post('/customers/', json=user2) 
    response = client.patch('/customers/2', json={'email': PAYLOAD['email']})
    assert response.status_code == 400

def test_update_customer_conflict_cpf(client):
    client.post('/customers/', json=PAYLOAD)
    client.post('/customers/', json={'name':'A','email':'a@a.com','cpf':'2','phone_number':'2','password':'x'})
    
    response = client.patch('/customers/2', json={'cpf': PAYLOAD['cpf']})
    assert response.status_code == 400

def test_update_customer_conflict_phone(client):
    client.post('/customers/', json=PAYLOAD)
    client.post('/customers/', json={'name':'A','email':'a@a.com','cpf':'2','phone_number':'2','password':'x'})
    
    response = client.patch('/customers/2', json={'phone_number': PAYLOAD['phone_number']})
    assert response.status_code == 400

def test_update_customer_not_found(client):
    response = client.patch('/customers/999', json={'name': 'X'})
    assert response.status_code == 404

def test_update_customer_db_error(client, mocker):
    client.post('/customers/', json=PAYLOAD)
    mocker.patch('sqlalchemy.orm.Session.commit', side_effect=Exception('Erro'))
    response = client.patch('/customers/1', json={'name': 'X'})
    assert response.status_code == 400

def test_customer_model_constructor():
    c = Customer(name='T', email='e', password='p', phone_number='1', cpf='1')
    assert c.name == 'T'


from app_data.app.dbconfig import get_session

def test_db_config_session_generator():
    generator = get_session()
    db_session = next(generator)
    assert db_session is not None
    try:
        next(generator)
    except StopIteration:
        pass