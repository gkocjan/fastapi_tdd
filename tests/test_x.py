"""
test_get_sku_for_existing_id_returns_200_status_code
test_get_sku_for_existing_id_returns_sku_id_and_name  # can split into 2 tests

in case of auth:
test_get_sku_returns_401_for_unauthorized_user
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

client = TestClient(app)


def test_get_sku_for_not_existing_id_returns_404_status_code_and_message_in_detail_field():
    response = client.get("/sku/NOT_EXISTING")

    assert response.status_code == 404
    assert response.json() == {"detail": "SKU not found"}
