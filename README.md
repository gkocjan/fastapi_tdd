# FastAPI service written in TDD
During this workshop, we will create a small service using FastAPI that will be responsible for maintaining a mapping of SKUs to products. This is part of a larger product that processes game sales data.

An SKU represents a single game/DLC that can be purchased (i.e. on Steam). In contrast, a product refers to a group of many SKUs related to each other (e.g., a game and all its DLCs).

![product to sku example](img/product_sku_example.png)

## Task 1
Write your first test. Don't bother naming things, creating API or setting up a database. Just write a simple test with `assert False` in it.

## Task 2
Search for an example of how to write a test for FastAPI. (hint: documentation is your best friend!)

## Acceptance criteria #1
- User can get SKU by it's id (example id: `TD:4321`, `XC:653`)
- User can add new SKU with sku_id and it's name

## Task 3
Write list of tests for `GET /sku/{sku_id}` endpoint.

Example:
Bad name example:
- `test_user`
- `test_get_user`

Good name example:
- `test_update_user_with_invalid_data_returns_400_status_code`
- `test_update_user_with_invalid_data_returns_list_of_invalid_fields_with_reason_and_error_type`

## Task 4
Write your first failing test. Try to use as few lines of code as possible while still adhering to PEP8/Black coding standards.

Example test from [FastAPI docs](https://fastapi.tiangolo.com/tutorial/testing/):

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

## Task 5
Make the test green! Let it be ugly, don't organize your code. Find the simplest way to pass the test (hint: you can return specific status code and message in FastAPI with [HTTPException](https://fastapi.tiangolo.com/tutorial/handling-errors/)).


## Task 6
Write a test that checks if `GET /sku/{sku_id}` returns status 200 for existing sku_id.

How to add existing SKU? Implement your database and add it at the beginning of the test.

Example database implementation:
```python
db = {}
db["TD:4321"] = {
    "sku_id": "TD:4321",
    "name": "SKU name 1",
}
```

## Task 7
Make the test green!

## Task 8
Write a test that checks if `GET /sku/{sku_id}` returns `sku_id` and `name` with expected values. Run the test, and verify that it fails.

Then, and only then, write code to passes the test.

## Task 9
Refactor your tests to use [pytest.fixtures](https://docs.pytest.org/en/latest/how-to/fixtures.html#fixtures-can-request-other-fixtures) for creating existing SKUs in the database.

If you didn't move your API code to a separate module, then it's a good time to do it also :)

## Acceptance criteria #2
- User can set SKU product_name
- User can unset SKU product assignment

## Task 10
Write a list of tests fulfilling those acceptance criteria (at least 3). For simplification, assume that from now SKU will have a third field, `product_name`. Use `PUT /sku/{sku_id}` for those operations. Rember about edge cases.

Work to fulfil those new acceptance criteria for product assignments. Flow stays the same. Pick one test from the list, write it, check if it is failing and make it green.

Writing new tests in a separate file would be a good idea. To do so, first, move your fixtures to `conftest.py` file. `TestClient` instance should also be returned by fixture in that common `conftest.py` file. Avoid creating utilities for tests that are not fixtures!

```python
tests/
    conftest.py
        # content of tests/conftest.py
        import pytest
        from fastapi.testclient import TestClient

        from fastapi_tdd.main import app


        @pytest.fixture
        def client():
            return TestClient(app)

    test_get_sku_by_id.py
        # content of tests/test_get_sku_by_id.py
        def test_not_existing_id_returns_404_status_code_and_message_in_detail_field(client):
            response = client.get("/sku/NOT_EXISTING")

            assert response.status_code == 404
            assert response.json() == {"detail": "SKU not found"}

```