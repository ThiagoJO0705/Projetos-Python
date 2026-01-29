import uuid
from unittest.mock import patch
from sqlalchemy.exc import SQLAlchemyError
from app_data.schemas.enums import InvestmentType
from app_data.models.asset import Asset

def test_create_asset_success(client):
    payload = {
        "ticker": "PETR4",
        "name": "Petrobras",
        "type": InvestmentType.STOCKS,
        "currency": "BRL"
    }
    response = client.post("/assets/", json=payload)
    assert response.status_code == 201
    assert response.json()["ticker"] == "PETR4"

def test_create_asset_already_exists(client, session):
    asset = Asset(
        ticker="VALE3",
        name="Vale",
        type=InvestmentType.STOCKS,
        currency="BRL"
    )
    session.add(asset)
    session.commit()
    payload = {
        "ticker": "vale3",
        "name": "Vale",
        "type": InvestmentType.STOCKS,
        "currency": "BRL"
    }
    response = client.post("/assets/", json=payload)
    assert response.status_code == 400
    assert "já está cadastrado" in response.json()["detail"].lower()

def test_create_asset_db_error(client, session):
    payload = {
        "ticker": f"ERR{uuid.uuid4().hex[:4]}",
        "name": "Erro",
        "type": InvestmentType.STOCKS,
        "currency": "BRL"
    }
    with patch.object(session, "commit", side_effect=SQLAlchemyError("DB Error")):
        response = client.post("/assets/", json=payload)
        assert response.status_code == 400

def test_get_assets_success(client, session):
    asset = Asset(
        ticker="ITUB4",
        name="Itaú",
        type=InvestmentType.STOCKS,
        currency="BRL"
    )
    session.add(asset)
    session.commit()
    response = client.get("/assets/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1

def test_get_asset_by_ticker_success(client, session):
    asset = Asset(
        ticker="BBAS3",
        name="Banco do Brasil",
        type=InvestmentType.STOCKS,
        currency="BRL"
    )
    session.add(asset)
    session.commit()
    response = client.get("/assets/BBAS3")
    assert response.status_code == 200
    assert response.json()["ticker"] == "BBAS3"

def test_get_asset_by_ticker_not_found(client):
    response = client.get("/assets/NAOEXISTE")
    assert response.status_code == 404

from app_data.app.dbconfig import get_session

def test_db_config_session_generator():
    generator = get_session()
    db_session = next(generator)
    assert db_session is not None
    try:
        next(generator)
    except StopIteration:
        pass