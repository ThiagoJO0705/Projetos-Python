import uuid
from app_data.schemas.enums import InvestorProfile

def create_customer_payload(**overrides):
    payload = {
        "name": "João Teste",
        "email": "joao@test.com",
        "password": "123456",
        "phone_number": "11999999999",
        "cpf": "12345678901",
        "investor_profile": InvestorProfile.UNDEFINED,
        "total_assets": 0.0,
        "is_active": True
    }
    payload.update(overrides)
    return payload

def test_create_customer_success(client):
    response = client.post(
        "/customers/",
        json=create_customer_payload()
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "João Teste"
    assert data["email"] == "joao@test.com"
    assert data["cpf"] == "12345678901"
    assert data["is_active"] is True

def test_create_customer_db_error(client, monkeypatch):
    from app_data.models.customer import Customer
    def mock_add(*args, **kwargs):
        raise Exception("DB error")
    monkeypatch.setattr("sqlalchemy.orm.Session.add", mock_add)
    response = client.post(
        "/customers/",
        json=create_customer_payload()
    )
    assert response.status_code == 400
    assert "erro ao tentar salvar" in response.json()["detail"].lower()

def test_get_all_customers(client):
    client.post("/customers/", json=create_customer_payload())
    client.post(
        "/customers/",
        json=create_customer_payload(
            email="outro123@test.com",
            cpf="99999999900",
            phone_number="11999000999",
            name="Maria"
        )
    )
    response = client.get("/customers/")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_all_customers_with_filters(client):
    client.post(
        "/customers/",
        json=create_customer_payload(is_active=True)
    )
    client.post(
        "/customers/",
        json=create_customer_payload(
            email="outro123@test.com",
            cpf="99999999900",
            phone_number="11999000999",
            name="Maria",
            is_active=False
        )
    )
    response = client.get("/customers/?is_active=false")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["email"] == "outro123@test.com"

def test_filter_customer_by_email(client):
    client.post("/customers/", json=create_customer_payload())
    response = client.get("/customers/filter?email=joao@test.com")
    assert response.status_code == 200
    assert response.json()["email"] == "joao@test.com"

def test_filter_customer_without_params(client):
    response = client.get("/customers/filter")
    assert response.status_code == 400

def test_filter_customer_not_found(client):
    response = client.get("/customers/filter?email=naoexiste@test.com")
    assert response.status_code == 404

def test_get_customer_by_id_success(client):
    create_response = client.post("/customers/", json=create_customer_payload())
    customer_id = create_response.json()["id"]
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 200
    assert response.json()["id"] == customer_id

def test_get_customer_by_id_not_found(client):
    random_id = str(uuid.uuid4())
    response = client.get(f"/customers/{random_id}")
    assert response.status_code == 404

def test_update_customer_success(client):
    create_response = client.post("/customers/", json=create_customer_payload())
    customer_id = create_response.json()["id"]
    response = client.patch(
        f"/customers/{customer_id}",
        json={"name": "Nome Atualizado"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Nome Atualizado"

def test_update_customer_duplicate_email(client):
    client.post(
        "/customers/",
        json=create_customer_payload()
    )
    second = client.post(
        "/customers/",
        json=create_customer_payload(
            email="segundo@test.com",
            cpf="22222222222",
            phone_number="11222222222"
        )
    )
    customer_id = second.json()["id"]
    response = client.patch(
        f"/customers/{customer_id}",
        json={"email": "joao@test.com"}
    )
    assert response.status_code == 400
    assert "email já está em uso" in response.json()["detail"].lower()

def test_update_customer_not_found(client):
    response = client.patch(
        f"/customers/{uuid.uuid4()}",
        json={"name": "Teste"}
    )
    assert response.status_code == 404
    
def test_get_all_customers_filter_by_name(client):
    client.post(
        "/customers/",
        json=create_customer_payload(name="João Silva")
    )
    client.post(
        "/customers/",
        json=create_customer_payload(
            email="maria@test.com",
            cpf="99999919999",
            phone_number="11888888188",
            name="Maria"
        )
    )
    response = client.get("/customers/?name=Maria")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Maria"

def test_update_customer_db_error(client, monkeypatch):
    create_response = client.post("/customers/", json=create_customer_payload())
    customer_id = create_response.json()["id"]
    def mock_commit(*args, **kwargs):
        raise Exception("DB error")
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_commit)
    response = client.patch(
        f"/customers/{customer_id}",
        json={"name": "Erro Update"}
    )
    assert response.status_code == 400
    assert "erro ao tentar atualizar" in response.json()["detail"].lower()