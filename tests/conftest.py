import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi_tdd.main import app, get_session
from fastapi_tdd.repo import SKU, Base, SKURepo


@pytest.fixture(scope="session")
def engine():
    _engine = create_engine(
        "sqlite://",
        echo=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(_engine)
    return _engine


@pytest.fixture()
def session(engine):
    session = Session(engine)
    session.begin()

    yield session

    session.rollback()
    session.close()


@pytest.fixture
def client(session):
    app.dependency_overrides[get_session] = lambda: session
    return TestClient(app)


@pytest.fixture
def sku_repo(session) -> SKURepo:
    return SKURepo(session)


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
