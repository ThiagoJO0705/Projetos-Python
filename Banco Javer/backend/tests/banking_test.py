import pytest
from app.models.customer import Customer

SENDER_DATA = {
    "name": "Sender User", 
    "email": "sender@banco.com", 
    "password": "123",
    "phone_number": "111111111", 
    "cpf": "11111111111"
}

RECEIVER_DATA = {
    "name": "Receiver User", 
    "email": "receiver@banco.com", 
    "password": "123",
    "phone_number": "222222222", 
    "cpf": "22222222222"
}

@pytest.fixture
def auth_headers(client):
    """
    Cadastra um usuário remetente e retorna o cabeçalho com o token de acesso.
    """
    client.post("/auth/signup", json=SENDER_DATA)
    login = client.post("/auth/signin", json={"email": SENDER_DATA["email"], "password": SENDER_DATA["password"]})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_get_balance_success(client, auth_headers):
    """
    Verifica se a consulta de saldo retorna os valores zerados para uma conta recém-criada.
    """
    response = client.get("/banking/balance", headers=auth_headers)
    assert response.status_code == 200
    assert float(response.json()["balance"]) == 0.0
    assert float(response.json()["score"]) == 0.0


def test_deposit_success(client, auth_headers):
    """
    Valida se um depósito de valor positivo atualiza corretamente o saldo e o score.
    """
    response = client.post("/banking/deposit", params={"deposit_value": 100.50}, headers=auth_headers)
    assert response.status_code == 200
    assert float(response.json()["new_balance"]) == 100.50
    assert float(response.json()["new_score"]) == 10.05


def test_deposit_invalid_value(client, auth_headers):
    """
    Garante que depósitos com valores negativos ou zero sejam rejeitados.
    """
    response = client.post("/banking/deposit", params={"deposit_value": -10}, headers=auth_headers)
    assert response.status_code == 400
    assert "positivo" in response.json()["detail"]


def test_payment_success(client, auth_headers):
    """
    Testa a realização de um pagamento com sucesso, verificando o abatimento no saldo.
    """
    client.post("/banking/deposit", params={"deposit_value": 100.0}, headers=auth_headers)
    payment_data = {"amount": 40.0, "method": "BANK SLIP", "description": "Luz"}
    response = client.post("/banking/payment", json=payment_data, headers=auth_headers)
    assert response.status_code == 200
    assert float(response.json()["new_balance"]) == 60.0
    assert "BANK SLIP" in response.json()["extract"]["description"]


def test_payment_invalid_amount(client, auth_headers):
    """
    Verifica se o sistema barra pagamentos com valor zero ou negativo.
    """
    payment_data = {"amount": 0, "method": "BANK SLIP", "description": "Nada"}
    response = client.post("/banking/payment", json=payment_data, headers=auth_headers)
    assert response.status_code == 400
    assert "maior que zero" in response.json()["detail"]


def test_payment_insufficient_funds(client, auth_headers):
    """
    Valida se um pagamento é negado quando o saldo do cliente é menor que o valor cobrado.
    """
    payment_data = {"amount": 1000.0, "method": "TED", "description": "Carro"}
    response = client.post("/banking/payment", json=payment_data, headers=auth_headers)
    assert response.status_code == 400
    assert "insuficiente" in response.json()["detail"]


def test_payment_with_deposit_method_forbidden(client, auth_headers):
    """
    Garante que o tipo DEPOSIT não possa ser usado indevidamente como método de saída no pagamento.
    """
    payment_data = {"amount": 10.0, "method": "DEPOSIT", "description": "Fraude"}
    response = client.post("/banking/payment", json=payment_data, headers=auth_headers)
    assert response.status_code == 400
    assert "Depósito" in response.json()["detail"]


def test_pix_success(client, auth_headers, session):
    """
    Valida uma transferência via Pix entre dois usuários, checando o saldo de ambos.
    """
    client.post("/auth/signup", json=RECEIVER_DATA)
    client.post("/banking/deposit", params={"deposit_value": 100.0}, headers=auth_headers)
    pix_data = {"pix_key": RECEIVER_DATA["cpf"], "pix_amount": 30.0}
    response = client.post("/banking/pix", json=pix_data, headers=auth_headers)
    assert response.status_code == 200
    assert float(response.json()["new_balance"]) == 70.0
    receiver = session.query(Customer).filter(Customer.cpf == RECEIVER_DATA["cpf"]).first()
    assert float(receiver.account_balance) == 30.0


def test_pix_invalid_amount(client, auth_headers):
    """
    Verifica se transferências Pix com valores inválidos são interrompidas precocemente.
    """
    pix_data = {"pix_key": RECEIVER_DATA["cpf"], "pix_amount": -5.0}
    response = client.post("/banking/pix", json=pix_data, headers=auth_headers)
    assert response.status_code == 400
    assert "maior que zero" in response.json()["detail"]


def test_pix_key_not_found(client, auth_headers):
    """
    Garante o retorno de erro 404 quando uma chave Pix não é localizada no sistema.
    """
    pix_data = {"pix_key": "99999999999", "pix_amount": 10.0}
    response = client.post("/banking/pix", json=pix_data, headers=auth_headers)
    assert response.status_code == 404


def test_pix_to_self(client, auth_headers):
    """
    Impede que um usuário realize uma transferência Pix para o próprio CPF/Email.
    """
    pix_data = {"pix_key": SENDER_DATA["cpf"], "pix_amount": 10.0}
    response = client.post("/banking/pix", json=pix_data, headers=auth_headers)
    assert response.status_code == 400
    assert "si mesmo" in response.json()["detail"]


def test_pix_insufficient_funds(client, auth_headers):
    """
    Valida a trava de segurança de saldo insuficiente especificamente para a operação de Pix.
    """
    client.post("/auth/signup", json=RECEIVER_DATA)
    pix_data = {"pix_key": RECEIVER_DATA["cpf"], "pix_amount": 1000.0}
    response = client.post("/banking/pix", json=pix_data, headers=auth_headers)
    assert response.status_code == 400
    assert "insuficiente" in response.json()["detail"]


def test_pix_to_inactive_receiver(client, auth_headers, session):
    """
    Testa o bloqueio de envio de Pix para destinatários que tiveram a conta desativada.
    """
    client.post("/auth/signup", json=RECEIVER_DATA)
    user = session.query(Customer).filter(Customer.email == RECEIVER_DATA["email"]).first()
    user.is_active = False
    session.commit()
    pix_data = {"pix_key": RECEIVER_DATA["cpf"], "pix_amount": 10.0}
    response = client.post("/banking/pix", json=pix_data, headers=auth_headers)
    assert response.status_code == 400
    assert "desativada" in response.json()["detail"]


def test_pix_to_non_holder_receiver(client, auth_headers, session):
    """
    Garante que o Pix não seja concluído se o destinatário não possuir uma conta corrente ativa.
    """
    client.post("/auth/signup", json=RECEIVER_DATA)
    user = session.query(Customer).filter(Customer.email == RECEIVER_DATA["email"]).first()
    user.is_account_holder = False
    session.commit()
    pix_data = {"pix_key": RECEIVER_DATA["cpf"], "pix_amount": 10.0}
    response = client.post("/banking/pix", json=pix_data, headers=auth_headers)
    assert response.status_code == 400
    assert "Correntista" in response.json()["detail"]


def test_get_statement(client, auth_headers):
    """
    Verifica se a rota de extrato retorna todas as transações em ordem cronológica decrescente.
    """
    client.post("/banking/deposit", params={"deposit_value": 100.0}, headers=auth_headers)
    client.post("/banking/payment", json={"amount": 20.0, "method": "PIX", "description": "Pizza"}, headers=auth_headers)
    response = client.get("/banking/statement", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["type"] == "DEPOSIT"
    assert data[1]["type"] == "PIX"


def test_banking_forbidden_for_non_holder(client, session):
    """
    Testa o isolamento de segurança que impede não-correntistas de acessarem funções financeiras.
    """
    client.post("/auth/signup", json=SENDER_DATA)
    user = session.query(Customer).filter(Customer.email == SENDER_DATA["email"]).first()
    user.is_account_holder = False
    session.commit()
    login = client.post("/auth/signin", json={"email": SENDER_DATA["email"], "password": SENDER_DATA["password"]})
    token = login.json()["access_token"]
    response = client.get("/banking/balance", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    assert "Correntista" in response.json()["detail"]