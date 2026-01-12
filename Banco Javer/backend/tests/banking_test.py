import pytest

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


