import pytest
from fastapi.testclient import TestClient

from fastapi_tdd.main import app
from fastapi_tdd.repo import _db as db


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
        "product_name": None,
    }

    yield  # run the test

    db.clear()  # clean up after the test


@pytest.fixture
def single_assigned_SKU_in_DB():
    # prepare data for the test
    db.clear()
    db["XC:653"] = {
        "sku_id": "XC:653",
        "name": "SKU name 1",
        "product_name": "existing_assignment",
    }

    yield  # run the test

    db.clear()  # clean up after the test
