import pytest
from fastapi.testclient import TestClient
from app_customer.app.main import app 

@pytest.fixture(scope='function')
def client():
    app.dependency_overrides = {}
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}
