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

## Task 11
Make data persistent. But first, refactor your code and instead direct access to the `db` dictionary, wrap it around the repository class. Use the code below as a starting point.

At the end of this task, you should access `db` dictionary only inside `SKURepo`. All other places should use the `SKURepo` methods.

```python
class SKU(BaseModel):
    sku_id: str
    name: str
    product_name: str | None


class SKURepo:
    def get(self, sku_id) -> SKU | None:
        pass

    def save(self, sku: SKU) -> SKU:
        pass
```

Run your tests frequently. In a perfect solution, they will never fail, even in the middle of refactoring!

## Task 12
Let's use an actual database! First, in `repo.py`` add the SqlAlchemy model definition for our table.

```python
# repo.py

from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class _DBSKU(Base):
    __tablename__ = "sku"
    sku_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    product_name: Mapped[str | None]
```

and init `SqlAlchemy` in `main.py`
```python
#main.py

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


BASE_DIR = Path(__file__).parent.parent.resolve()
engine = create_engine(f"sqlite:///{BASE_DIR/'db.sqlite'}", echo=True)
Base.metadata.create_all(engine)


def get_session():
    session = Session(engine)
    with session.begin():
        yield session

```

We can now prepare tests to run in SQLite in-memory DB
```python
# conftest.py

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
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def client(session):
    app.dependency_overrides[get_session] = lambda: session
    return TestClient(app)


@pytest.fixture
def sku_repo(session) -> SKURepo:
    return SKURepo(session)
```

Now having this ready and based on SqlAlchemy [documentation](https://docs.sqlalchemy.org/en/20/orm/quickstart.html#create-objects-and-persist), write queries for `SKURepo` methods (pass session via constructor). Don't modify returned types ([in Pydantic documentation](https://docs.pydantic.dev/1.10/usage/models/#orm-mode-aka-arbitrary-class-instances) is an example of how to create Pydantic `SKU` object from the orm model )

Then in `main.py` use `get_session` as a dependency to create `SKURepo` in `get_sku_repo`.