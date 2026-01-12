USER_DATA = {
    'name': 'Thiago Teste',
    'email': 'thiago@teste.com',
    'password': 'senha123',
    'phone_number': '11999999999',
    'cpf': '12345678901'
}

def test_signup_success(client):
    """Testa o cadastro de um novo usuário com sucesso"""
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
    """Testa se o Pydantic barra e-mail mal formatado"""
    invalid_data = USER_DATA.copy()
    invalid_data['email'] = 'email_sem_arroba.com'
    response = client.post('/auth/signup', json=invalid_data)
    assert response.status_code == 422

