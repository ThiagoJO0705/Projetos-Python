import pytest
from app.models.customer import Customer

ADMIN_DATA = {
    'name': 'Admin User',
    'email': 'admin@javer.com',
    'password': 'adminpassword',
    'phone_number': '000000000',
    'cpf': '00000000000'
}

USER_DATA = {
    'name': 'Common User',
    'email': 'user@javer.com',
    'password': 'userpassword',
    'phone_number': '111111111',
    'cpf': '11111111111'
}

@pytest.fixture
def admin_headers(client, session):
    '''Cria um administrador no banco de dados e retorna os headers com o token de acesso.'''
    client.post('/auth/signup', json=ADMIN_DATA)
    db_admin = session.query(Customer).filter(Customer.email == ADMIN_DATA['email']).first()
    db_admin.is_admin = True
    session.commit()
    
    login = client.post('/auth/signin', json={'email': ADMIN_DATA['email'], 'password': ADMIN_DATA['password']})
    return {'Authorization': f'Bearer {login.json()['access_token']}'}

@pytest.fixture
def user_headers(client):
    '''Cria um usuário comum e retorna os headers com o token de acesso.'''
    client.post('/auth/signup', json=USER_DATA)
    login = client.post('/auth/signin', json={'email': USER_DATA['email'], 'password': USER_DATA['password']})
    return {'Authorization': f'Bearer {login.json()['access_token']}'}
