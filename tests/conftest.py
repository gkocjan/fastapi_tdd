import pytest
from fastapi.testclient import TestClient

from fastapi_tdd.main import app
from fastapi_tdd.repo import SKU, SKURepo, _db


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db():
    _db.clear()
    yield _db
    _db.clear()


@pytest.fixture
def sku_repo(db) -> SKURepo:
    return SKURepo()


@pytest.fixture
def single_SKU_in_DB(sku_repo: SKURepo):
    sku_repo.save(
        SKU(
            sku_id="TD:4321",
            name="SKU name 1",
            product_name=None,
        )
    )


@pytest.fixture
def single_assigned_SKU_in_DB(sku_repo: SKURepo):
    sku_repo.save(
        SKU(
            sku_id="XC:653",
            name="SKU name 1",
            product_name="existing_assignment",
        )
    )
