import pytest
from fastapi.testclient import TestClient

from fastapi_tdd.main import app


@pytest.fixture
def client():
    return TestClient(app)
