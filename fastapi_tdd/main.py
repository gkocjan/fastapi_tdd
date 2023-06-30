from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from fastapi_tdd.repo import SKURepo

app = FastAPI()


def get_sku_repo():
    return SKURepo()


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
