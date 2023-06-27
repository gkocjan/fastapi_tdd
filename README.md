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
