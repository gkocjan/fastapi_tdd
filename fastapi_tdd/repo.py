from pydantic import BaseModel


class SKU(BaseModel):
    sku_id: str
    name: str
    product_name: str | None


class SKURepo:
    def __init__(self, db) -> None:
        self._db = db

    def get(self, sku_id) -> SKU | None:
        return self._db.get(sku_id)

    def save(self, sku: SKU) -> SKU:
        self._db[sku.sku_id] = sku
        return self.get(sku.sku_id)
