from app.models.customer import Customer
from jose import jwt
from app.main import SECRET_KEY, ALGORITHM


USER_DATA = {
    'name': 'Thiago Teste',
    'email': 'thiago@teste.com',
    'password': 'senha123',
    'phone_number': '11999999999',
    'cpf': '12345678901'
}

def test_signup_success(client):
    '''Testa o cadastro de um novo usuário com sucesso'''
    response = client.post('/auth/signup', json=USER_DATA)
    assert response.status_code == 201
    data = response.json()
    assert data['email'] == USER_DATA['email']
    assert 'id' in data
    assert 'password' not in data


def test_signup_duplicate_email(client):
    '''Testa se a API barra e-mails duplicados'''
    client.post('/auth/signup', json=USER_DATA)
    user_2 = USER_DATA.copy()
    user_2['cpf'] = '00000000000'
    response = client.post('/auth/signup', json=user_2)
    assert response.status_code == 400
    assert response.json()['detail'] == 'Email do usuário já cadastrado!'


def test_signup_duplicate_cpf(client):
    '''Testa se a API barra CPFs duplicados'''
    client.post('/auth/signup', json=USER_DATA)
    user_2 = USER_DATA.copy()
    user_2['email'] = 'outro@email.com'
    response = client.post('/auth/signup', json=user_2)
    assert response.status_code == 400
    assert 'CPF' in response.json()['detail']


def test_signup_duplicate_phone(client):
    '''Testa se a API barra CPFs duplicados'''
    client.post('/auth/signup', json=USER_DATA)
    user_2 = USER_DATA.copy()
    user_2['email'] = 'outro@email.com'
    user_2['cpf'] = '2134'
    response = client.post('/auth/signup', json=user_2)
    assert response.status_code == 400
    assert 'Telefone' in response.json()['detail']


def test_signup_invalid_email(client):
    '''Testa se o Pydantic barra e-mail mal formatado'''
    invalid_data = USER_DATA.copy()
    invalid_data['email'] = 'email_sem_arroba.com'
    response = client.post('/auth/signup', json=invalid_data)
    assert response.status_code == 422


def test_signin_success(client):
    '''Testa o login com credenciais corretas'''
    client.post('/auth/signup', json=USER_DATA)
    login_data = {'email': USER_DATA['email'], 'password': USER_DATA['password']}
    response = client.post('/auth/signin', json=login_data)
    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert 'refresh_token' in response.json()
    assert response.json()['token_type'] == 'Bearer'


def test_signin_wrong_password(client):
    '''Testa erro de senha incorreta'''
    client.post('/auth/signup', json=USER_DATA)
    login_data = {'email': USER_DATA['email'], 'password': 'senha_errada'}
    response = client.post('/auth/signin', json=login_data)
    assert response.status_code == 400
    assert 'inválidas' in response.json()['detail']


def test_signin_user_not_found(client):
    '''Testa erro de usuário inexistente'''
    login_data = {'email': 'naoexiste@banco.com', 'password': '123'}
    response = client.post('/auth/signin', json=login_data)
    assert response.status_code == 400


def test_signin_inactive_user(client, session):
    '''Testa se usuário desativado consegue logar'''
    client.post('/auth/signup', json=USER_DATA)
    user = session.query(Customer).filter(Customer.email == USER_DATA['email']).first()
    user.is_active = False
    session.commit()
    login_data = {'email': USER_DATA['email'], 'password': USER_DATA['password']}
    response = client.post('/auth/signin', json=login_data)
    assert response.status_code == 401 
    assert 'desativada' in response.json()['detail']


def test_signin_form_success(client):
    '''Testa o login via formulário (OAuth2), usado pelo Swagger'''
    client.post('/auth/signup', json=USER_DATA)
    form_data = {
        'username': USER_DATA['email'], 
        'password': USER_DATA['password']
    }
    response = client.post('/auth/signin-form', data=form_data)
    assert response.status_code == 200
    assert 'access_token' in response.json()

def test_signin_form_fail(client):
    '''Testa falha no login via formulário'''
    form_data = {'username': 'errado@banco.com', 'password': '123'}
    response = client.post('/auth/signin-form', data=form_data)
    assert response.status_code == 400


def test_customer_score_calculation():
    '''Testa se a lógica de 10% do score no modelo está correta'''
    customer = Customer(
        name='Teste', email='t@t.com', password='1', 
        phone_number='1', cpf='1', account_balance='500.0'
    )
    assert float(customer.score) == 50.0
    customer.account_balance = 0
    assert float(customer.score) == 0.0


def test_refresh_token_success(client):
    '''Testa se o refresh token gera um novo access token com sucesso'''
    client.post('/auth/signup', json=USER_DATA)
    login_res = client.post('/auth/signin', json={'email': USER_DATA['email'], 'password': USER_DATA['password']})
    refresh_token = login_res.json()['refresh_token']
    headers = {'Authorization': f'Bearer {refresh_token}'}
    response = client.post('/auth/refresh', headers=headers)
    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert response.json()['token_type'] == 'Bearer'


def test_refresh_token_with_inactive_user(client, session):
    '''Testa se um usuário desativado consegue usar o refresh token'''
    client.post('/auth/signup', json=USER_DATA)
    login_res = client.post('/auth/signin', json={'email': USER_DATA['email'], 'password': USER_DATA['password']})
    refresh_token = login_res.json()['refresh_token']
    from app.models.customer import Customer
    user = session.query(Customer).filter(Customer.email == USER_DATA['email']).first()
    user.is_active = False
    session.commit()
    headers = {'Authorization': f'Bearer {refresh_token}'}
    response = client.post('/auth/refresh', headers=headers)
    assert response.status_code == 401
    assert 'desativada' in response.json()['detail']


def test_refresh_token_malformed(client):
    '''Testa acesso com token que não é um JWT real'''
    headers = {'Authorization': 'Bearer token_que_nao_existe'}
    response = client.post('/auth/refresh', headers=headers)
    assert response.status_code == 401
    assert 'Acesso Negado' in response.json()['detail']


def test_verify_token_invalid_jwt(client):
    '''Testa um token que não é um JWT válido'''
    headers = {'Authorization': 'Bearer token_completamente_errado'}
    response = client.post('/auth/refresh', headers=headers)
    assert response.status_code == 401
    assert 'Acesso Negado' in response.json()['detail']


def test_verify_token_user_not_found(client):
    '''Testa um token que tem um ID de usuário que não existe no banco'''
    payload = {'sub': '999', 'exp': 9999999999}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/auth/refresh', headers=headers)
    assert response.status_code == 401
    assert 'Inválido' in response.json()['detail']


def test_verify_token_no_sub_payload(client):
    '''Testa um token válido mas que não tem a claim 'sub'''
    payload = {'foo': 'bar', 'exp': 9999999999}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/auth/refresh', headers=headers)
    assert response.status_code == 401