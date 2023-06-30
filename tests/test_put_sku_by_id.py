from fastapi.testclient import TestClient

"""
test_existing_unassigned_id_and_product_name_in_body_returns_assigned_sku
test_existing_assigned_id_and_product_name_in_body_returns_updated_assigned_sku
test_existing_assigned_id_and_None_product_name_in_body_unassigns_product_from_sku
test_existing_unassigned_id_and_None_product_name_in_body_returns_unassigned_sku
"""


def test_not_existing_id_returns_404_status_code_and_message_in_detail_field(
    client: TestClient,
):
    response = client.put("/sku/NOT_EXISTING", json={"product_nane": "product"})

    assert response.status_code == 404
    assert response.json() == {"detail": "SKU not found"}


def test_existing_id_and_product_name_in_body_returns_200_status_code(
    client: TestClient, single_SKU_in_DB
):
    response = client.put("/sku/TD:4321", json={"product_nane": "product"})
    assert response.status_code == 200
