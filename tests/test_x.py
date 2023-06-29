import pytest
from fastapi.testclient import TestClient

from fastapi_tdd.main import app, db

client = TestClient(app)


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


def test_get_sku_for_not_existing_id_returns_404_status_code_and_message_in_detail_field():
    response = client.get("/sku/NOT_EXISTING")

    assert response.status_code == 404
    assert response.json() == {"detail": "SKU not found"}


def test_get_sku_for_existing_id_returns_200_status_code(single_SKU_in_DB):
    response = client.get("/sku/TD:4321")

    assert response.status_code == 200


def test_get_sku_for_existing_id_returns_sku_id_and_name_v1(single_SKU_in_DB):
    response = client.get("/sku/TD:4321")
    assert response.json() == {
        "sku_id": "TD:4321",
        "name": "SKU name 1",
    }


def test_get_sku_for_existing_id_returns_sku_id_and_name_v2(single_SKU_in_DB):
    response = client.get("/sku/TD:4321")
    result_sku = response.json()

    assert result_sku["sku_id"] == "TD:4321"
    assert result_sku["name"] == "SKU name 1"


def test_make_sure_that_we_clean_up_the_db():
    response = client.get("/sku/TD:4321")

    assert response.status_code == 404
