import pytest
from decimal import Decimal
from app_data.models.transaction import Transaction

CUSTOMER_PAYLOAD = {
    'name': 'User Transacao', 
    'email': 'tx@teste.com', 
    'password': 'h', 
    'phone_number': '111', 
    'cpf': '111', 
    'account_balance': 100.0
}

def test_post_transaction_credit_success(client):
    client.post('/customers/', json=CUSTOMER_PAYLOAD)
    payload = {
        'customer_id': 1,
        'type': 'DEPOSIT',
        'direction': 'CREDIT',
        'amount': 50.0,
        'description': 'Deposito Teste'
    }
    response = client.post('/transactions/', json=payload)
    assert response.status_code == 201
    user = client.get('/customers/1').json()
    assert float(user['account_balance']) == 150.0

def test_post_transaction_debit_success(client):
    client.post('/customers/', json=CUSTOMER_PAYLOAD)
    payload = {
        'customer_id': 1,
        'type': 'PIX',
        'direction': 'DEBIT',
        'amount': 30.0,
        'description': 'Pix Teste'
    }
    response = client.post('/transactions/', json=payload)
    
    assert response.status_code == 201
    user = client.get('/customers/1').json()
    assert float(user['account_balance']) == 70.0

def test_post_transaction_user_not_found(client):
    payload = {
        'customer_id': 999,
        'type': 'DEPOSIT',
        'direction': 'CREDIT',
        'amount': 10.0
    }
    response = client.post('/transactions/', json=payload)
    assert response.status_code == 404

def test_post_transaction_db_error(client, mocker):
    client.post('/customers/', json=CUSTOMER_PAYLOAD)
    mocker.patch('sqlalchemy.orm.Session.commit', side_effect=Exception('Erro financeiro'))
    payload = {'customer_id': 1, 'type': 'DEPOSIT', 'direction': 'CREDIT', 'amount': 10.0}
    response = client.post('/transactions/', json=payload)
    assert response.status_code == 400

def test_get_customer_transactions_success(client):
    client.post('/customers/', json=CUSTOMER_PAYLOAD)
    client.post('/transactions/', json={'customer_id': 1, 'type': 'DEPOSIT', 'direction': 'CREDIT', 'amount': 10.0})
    client.post('/transactions/', json={'customer_id': 1, 'type': 'PIX', 'direction': 'DEBIT', 'amount': 5.0})
    response = client.get('/transactions/customer/1')
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_customer_transactions_not_found(client):
    response = client.get('/transactions/customer/999')
    assert response.status_code == 404

def test_transaction_model_constructor():
    t = Transaction(
        customer_id=1, 
        type='PIX', 
        amount=50.0, 
        direction='DEBIT', 
        related_customer_id=2, 
        description='Teste'
    )
    assert t.customer_id == 1
    assert t.amount == 50.0