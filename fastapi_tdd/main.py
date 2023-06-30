from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapi_tdd.repo import Base, SKURepo

app = FastAPI()

BASE_DIR = Path(__file__).parent.parent.resolve()
engine = create_engine(f"sqlite:///{BASE_DIR/'db.sqlite'}", echo=True)
Base.metadata.create_all(engine)


def get_session():
    session = Session(engine)
    with session.begin():
        yield session


def get_sku_repo(session: Session = Depends(get_session)):
    return SKURepo(session)


@app.get("/sku/{sku_id}")
def get_sku_by_id(sku_id: str, sku_repo: SKURepo = Depends(get_sku_repo)):
    sku = sku_repo.get(sku_id)
    if sku is None:
        raise HTTPException(status_code=404, detail="SKU not found")
    return sku


class SKUProductAssignment(BaseModel):
    product_name: str | None = None


@app.put("/sku/{sku_id}")
def update_sku_by_id(
    sku_id: str,
    sku_product_assignement: SKUProductAssignment,
    sku_repo: SKURepo = Depends(get_sku_repo),
):
    sku = sku_repo.get(sku_id)
    if sku is None:
        raise HTTPException(status_code=404, detail="SKU not found")
    sku.product_name = sku_product_assignement.product_name
    return sku_repo.save(sku)
