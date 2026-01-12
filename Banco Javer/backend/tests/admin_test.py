import pytest
from app.models.customer import Customer
from jose import jwt
from app.api.dependencies import SECRET_KEY, ALGORITHM, verify_admin, generate_score, get_session
from app.main import app

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

def test_update_customer_success(client, admin_headers, session):
    '''Valida a atualização parcial dos dados de um cliente via método PATCH.'''
    client.post('/auth/signup', json=USER_DATA)
    user = session.query(Customer).filter(Customer.email == USER_DATA['email']).first()
    
    response = client.patch(f'/admin/customers/{user.id}', json={'name': 'Novo Nome'}, headers=admin_headers)
    assert response.status_code == 200
    assert response.json()['name'] == 'Novo Nome'

def test_update_customer_no_changes(client, admin_headers, session):
    '''Garante que o endpoint de atualização responda com sucesso mesmo que nenhum dado novo seja enviado.'''
    client.post('/auth/signup', json=USER_DATA)
    user = session.query(Customer).filter(Customer.email == USER_DATA['email']).first()
    
    response = client.patch(f'/admin/customers/{user.id}', json={}, headers=admin_headers)
    assert response.status_code == 200

def test_update_customer_full_fields(client, admin_headers, session):
    '''Cobre a atualização simultânea de múltiplos campos do cliente, incluindo E-mail e CPF.'''
    client.post('/auth/signup', json=USER_DATA)
    user = session.query(Customer).filter(Customer.email == USER_DATA['email']).first()
    
    new_data = {
        'name': 'Novo Nome',
        'email': 'novissimo@email.com',
        'cpf': '99999999998',
        'is_active': True,
        'is_account_holder': False
    }
    response = client.patch(f'/admin/customers/{user.id}', json=new_data, headers=admin_headers)
    assert response.status_code == 200
    assert response.json()['email'] == 'novissimo@email.com'

def test_update_customer_duplicate_email(client, admin_headers, session):
    '''Testa o impedimento de atualização de e-mail quando o novo valor já está em uso por outro usuário.'''
    client.post('/auth/signup', json=USER_DATA) 
    user_target = session.query(Customer).filter(Customer.email == USER_DATA['email']).first()
    
    response = client.patch(f'/admin/customers/{user_target.id}', json={'email': ADMIN_DATA['email']}, headers=admin_headers)
    assert response.status_code == 400

def test_update_customer_duplicate_cpf(client, admin_headers, session):
    '''Testa o impedimento de atualização de CPF quando o novo valor já está cadastrado no sistema.'''
    client.post('/auth/signup', json=USER_DATA)
    user_target = session.query(Customer).filter(Customer.email == USER_DATA['email']).first()
    
    response = client.patch(f'/admin/customers/{user_target.id}', json={'cpf': ADMIN_DATA['cpf']}, headers=admin_headers)
    assert response.status_code == 400

def test_update_customer_not_found(client, admin_headers):
    '''Garante erro 404 ao tentar atualizar um cliente com ID inexistente.'''
    response = client.patch('/admin/customers/999', json={'name': 'X'}, headers=admin_headers)
    assert response.status_code == 404

def test_disable_customer_success(client, admin_headers, session):
    '''Valida o processo de desativação (soft delete) de um cliente e confirma a alteração no banco de dados.'''
    client.post('/auth/signup', json=USER_DATA)
    user = session.query(Customer).filter(Customer.email == USER_DATA['email']).first()
    user_id = user.id

    response = client.delete(f'/admin/customers/disable/{user_id}', headers=admin_headers)
    assert response.status_code == 200
    
    updated_user = session.query(Customer).filter(Customer.id == user_id).first()
    assert updated_user.is_active is False

def test_disable_customer_already_inactive(client, admin_headers, session):
    '''Garante que o sistema retorne erro 400 ao tentar desativar um cliente que já está inativo.'''
    client.post('/auth/signup', json=USER_DATA)
    user = session.query(Customer).filter(Customer.email == USER_DATA['email']).first()
    user.is_active = False
    session.commit()
    
    response = client.delete(f'/admin/customers/disable/{user.id}', headers=admin_headers)
    assert response.status_code == 400

def test_disable_self_forbidden(client, admin_headers, session):
    '''Testa a regra de negócio que impede que um administrador desative a própria conta.'''
    admin = session.query(Customer).filter(Customer.email == ADMIN_DATA['email']).first()
    response = client.delete(f'/admin/customers/disable/{admin.id}', headers=admin_headers)
    assert response.status_code == 400
    assert 'Autodesativação de conta' in response.json()['detail']

def test_disable_customer_not_found(client, admin_headers):
    '''Valida o retorno de erro 404 ao tentar desativar um ID de cliente inexistente.'''
    response = client.delete('/admin/customers/disable/999', headers=admin_headers)
    assert response.status_code == 404

def test_activate_customer_success(client, admin_headers, session):
    '''Valida o sucesso da reativação de um cliente previamente desativado.'''
    client.post('/auth/signup', json=USER_DATA)
    user = session.query(Customer).filter(Customer.email == USER_DATA['email']).first()
    client.delete(f'/admin/customers/disable/{user.id}', headers=admin_headers)
    
    response = client.patch(f'/admin/customer/activate/{user.id}', headers=admin_headers)
    assert response.status_code == 200
    assert 'ativada' in response.json()['message']

def test_activate_customer_already_active(client, admin_headers, session):
    '''Garante erro 400 ao tentar ativar um cliente que já se encontra em estado ativo.'''
    client.post('/auth/signup', json=USER_DATA)
    user = session.query(Customer).filter(Customer.email == USER_DATA['email']).first()
    
    response = client.patch(f'/admin/customer/activate/{user.id}', headers=admin_headers)
    assert response.status_code == 400
    assert 'já está ativa' in response.json()['detail']

def test_activate_customer_not_found(client, admin_headers):
    '''Valida o retorno de erro 404 ao tentar ativar um cliente inexistente.'''
    response = client.patch('/admin/customer/activate/999', headers=admin_headers)
    assert response.status_code == 404

def test_disable_last_admin_logic(client, admin_headers, session):
    '''Verifica se o sistema permite desativar um administrador quando ainda resta outro administrador ativo no banco.'''
    client.post('/auth/signup', json={'name':'Admin2','email':'a2@a.com','password':'1','phone_number':'5','cpf':'5'})
    admin2 = session.query(Customer).filter(Customer.email == 'a2@a.com').first()
    admin2.is_admin = True
    session.commit()
    
    res = client.delete(f'/admin/customers/disable/{admin2.id}', headers=admin_headers)
    assert res.status_code == 200
    
def test_disable_last_admin_trigger(client, admin_headers, session):
    '''Força o disparo da exceção de segurança que impede a desativação do último administrador ativo do sistema.'''
    admin_no_banco = session.query(Customer).filter(Customer.is_admin == True).first()
    usuario_fantasma = Customer(
        name='Fantasma', email='f@f.com', password='1', 
        phone_number='9', cpf='9', is_admin=True
    )
    
    app.dependency_overrides[verify_admin] = lambda: usuario_fantasma
    
    response = client.delete(f'/admin/customers/disable/{admin_no_banco.id}', headers=admin_headers)
    
    assert response.status_code == 400
    assert 'último administrador' in response.json()['detail']
    app.dependency_overrides.clear()

def test_generate_score_with_zero_or_negative():
    '''Valida se a função de geração de score retorna 0.0 para entradas zeradas ou negativas.'''
    assert generate_score(0) == 0.0
    assert generate_score(-100) == 0.0

def test_verify_admin_fail_not_admin(client):
    '''Garante que a dependência de verificação de admin bloqueie usuários comuns com erro 403.'''
    client.post('/auth/signup', json={'name':'X','email':'x@x.com','password':'1','phone_number':'2','cpf':'3'})
    login = client.post('/auth/signin', json={'email': 'x@x.com', 'password': '1'})
    token = login.json()['access_token']
    
    response = client.get('/admin/customers', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 403
    assert 'necessário ser Admin' in response.json()['detail']

def test_real_get_session():
    '''Testa manualmente o gerador de sessão para garantir a cobertura dos blocos try/finally de conexão com o banco.'''
    gen = get_session()
    session = next(gen)
    assert session is not None
    try:
        next(gen)
    except StopIteration:
        pass

def test_verify_token_missing_sub_claim(client):
    '''Testa a falha de autenticação quando um token JWT é válido mas não contém a claim de identificação do usuário.'''
    payload = {'nome': 'teste', 'exp': 9999999999, 'sub': None}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    response = client.get('/banking/balance', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 401
    assert 'Acesso Negado' in response.json()['detail']
