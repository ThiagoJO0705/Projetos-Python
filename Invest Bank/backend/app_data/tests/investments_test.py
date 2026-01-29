import uuid
from unittest.mock import patch
from sqlalchemy.exc import SQLAlchemyError
from app_data.schemas.enums import InvestorProfile, InvestmentType
from app_data.models.customer import Customer
from app_data.models.asset import Asset

def create_customer(session):
    customer = Customer(
        name="Thiago",
        email=f"teste_{uuid.uuid4()}@teste.com",
        password="123",
        phone_number=str(uuid.uuid4())[:11],
        cpf=str(uuid.uuid4())[:11],
        investor_profile=InvestorProfile.UNDEFINED
    )
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

def create_asset(session):
    asset = Asset(
        ticker=f"TICK{str(uuid.uuid4())[:4]}",
        name="Ativo Teste",
        type=InvestmentType.STOCKS,
        currency="BRL"
    )
    session.add(asset)
    session.commit()
    session.refresh(asset)
    return asset

def test_create_investment_success(client, session):
    c = create_customer(session)
    a = create_asset(session)
    payload = {
        "customer_id": str(c.id),
        "asset_id": str(a.id),
        "quantity": 10,
        "purchase_price": 50.0,
        "is_active": True
    }
    response = client.post("/investments/", json=payload)
    assert response.status_code == 201

def test_create_investment_customer_not_found(client, session):
    a = create_asset(session)
    payload = {"customer_id": str(uuid.uuid4()), "asset_id": str(a.id), "quantity": 1, "purchase_price": 10}
    response = client.post("/investments/", json=payload)
    assert response.status_code == 404

def test_create_investment_asset_not_found(client, session):
    c = create_customer(session)
    payload = {"customer_id": str(c.id), "asset_id": str(uuid.uuid4()), "quantity": 1, "purchase_price": 10}
    response = client.post("/investments/", json=payload)
    assert response.status_code == 404

def test_create_investment_db_error(client, session):
    c = create_customer(session)
    a = create_asset(session)
    payload = {"customer_id": str(c.id), "asset_id": str(a.id), "quantity": 1, "purchase_price": 10}
    with patch.object(session, 'commit', side_effect=SQLAlchemyError("DB Error")):
        response = client.post("/investments/", json=payload)
        assert response.status_code == 400
        assert "erro" in response.json()["detail"].lower()

def test_get_all_investments_filter_branches(client, session):
    c = create_customer(session)
    a = create_asset(session)
    client.post("/investments/", json={"customer_id": str(c.id), "asset_id": str(a.id), "quantity": 1, "purchase_price": 10, "is_active": True})
    res_active = client.get("/investments/?is_active=true")
    assert res_active.status_code == 200
    res_inactive = client.get("/investments/?is_active=false")
    assert res_inactive.status_code == 200

def test_get_customer_investments_logic(client, session):
    c = create_customer(session)
    response = client.get(f"/investments/customer/{c.id}")
    assert response.status_code == 404
    response_none = client.get(f"/investments/customer/{uuid.uuid4()}")
    assert response_none.status_code == 404

def test_get_investment_by_id_logic(client, session):
    c = create_customer(session)
    a = create_asset(session)
    inv = client.post("/investments/", json={"customer_id": str(c.id), "asset_id": str(a.id), "quantity": 1, "purchase_price": 10}).json()
    res = client.get(f"/investments/investment/{inv['id']}")
    assert res.status_code == 200
    res_not_found = client.get(f"/investments/investment/{uuid.uuid4()}")
    assert res_not_found.status_code == 404

def test_update_investment_success(client, session):
    c = create_customer(session)
    a = create_asset(session)
    inv = client.post("/investments/", json={"customer_id": str(c.id), "asset_id": str(a.id), "quantity": 1, "purchase_price": 10}).json()
    res = client.patch(f"/investments/investment/{inv['id']}", json={"quantity": 20})
    assert res.status_code == 200
    assert res.json()["quantity"] == "20.00000000"

def test_update_investment_db_error(client, session):
    c = create_customer(session)
    a = create_asset(session)
    inv = client.post("/investments/", json={"customer_id": str(c.id), "asset_id": str(a.id), "quantity": 1, "purchase_price": 10}).json()
    with patch.object(session, 'commit', side_effect=SQLAlchemyError("DB Error")):
        res = client.patch(f"/investments/investment/{inv['id']}", json={"quantity": 20})
        assert res.status_code == 400

def test_delete_investment_success(client, session):
    c = create_customer(session)
    a = create_asset(session)
    inv = client.post("/investments/", json={"customer_id": str(c.id), "asset_id": str(a.id), "quantity": 1, "purchase_price": 10}).json()
    res = client.delete(f"/investments/investment/{inv['id']}")
    assert res.status_code == 204

def test_delete_investment_db_error(client, session):
    c = create_customer(session)
    a = create_asset(session)
    inv = client.post("/investments/", json={"customer_id": str(c.id), "asset_id": str(a.id), "quantity": 1, "purchase_price": 10}).json()
    with patch.object(session, 'commit', side_effect=SQLAlchemyError("DB Error")):
        res = client.delete(f"/investments/investment/{inv['id']}")
        assert res.status_code == 400

def test_get_customer_investments_without_investments(client, session):
    c = create_customer(session)
    response = client.get(f"/investments/customer/{c.id}")
    assert response.status_code == 404
    assert "não possui investimentos" in response.json()["detail"].lower()

def test_update_investment_not_found(client, session):
    response = client.patch(
        f"/investments/investment/{uuid.uuid4()}",
        json={"quantity": 5}
    )
    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"].lower()

def test_delete_investment_not_found(client, session):
    response = client.delete(
        f"/investments/investment/{uuid.uuid4()}"
    )
    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"].lower()

def test_get_customer_investments_success(client, session):
    c = create_customer(session)
    a = create_asset(session)
    client.post(
        "/investments/",
        json={
            "customer_id": str(c.id),
            "asset_id": str(a.id),
            "quantity": 5,
            "purchase_price": 100
        }
    )
    response = client.get(f"/investments/customer/{c.id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["customer_id"] == str(c.id)
