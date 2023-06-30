import pytest
from fastapi.testclient import TestClient

from fastapi_tdd.main import app, db


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def single_SKU_in_DB():
    # prepare data for the test
    db.clear()
    db["TD:4321"] = {
        "sku_id": "TD:4321",
        "name": "SKU name 1",
    }

    yield  # run the test

    db.clear()  # clean up after the test
