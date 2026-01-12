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

def test_admin_access_denied_for_common_user(client, user_headers):
    '''Garante que usuários sem privilégios de administrador recebam erro 403 ao acessar rotas restritas.'''
    response = client.get('/admin/customers', headers=user_headers)
    assert response.status_code == 403

def test_get_customers_listing_and_filters(client, admin_headers):
    '''Testa a listagem de clientes e a aplicação de filtros de busca por nome e status ativo.'''
    client.post('/auth/signup', json=USER_DATA)
    response = client.get('/admin/customers?name=Common&is_active=true', headers=admin_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_get_customers_filter_is_account_holder(client, admin_headers):
    '''Valida o funcionamento dos filtros para correntistas e não correntistas no painel administrativo.'''
    response = client.get('/admin/customers?is_account_holder=true', headers=admin_headers)
    assert response.status_code == 200
    
    response = client.get('/admin/customers?is_account_holder=false', headers=admin_headers)
    assert response.status_code == 200

def test_get_customers_name_filter_no_results(client, admin_headers):
    '''Verifica se a listagem retorna uma lista vazia quando o filtro de nome não encontra correspondências.'''
    response = client.get('/admin/customers?name=NomeQueNaoExiste', headers=admin_headers)
    assert response.status_code == 200
    assert len(response.json()) == 0
