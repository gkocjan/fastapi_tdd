import pytest
from fastapi.testclient import TestClient

from fastapi_tdd.main import app, get_sku_repo
from fastapi_tdd.repo import SKU, SKURepo


@pytest.fixture
def client(sku_repo):
    app.dependency_overrides[get_sku_repo] = lambda: sku_repo
    return TestClient(app)


@pytest.fixture
def db():
    return {}


@pytest.fixture
def sku_repo(db) -> SKURepo:
    return SKURepo(db)


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
