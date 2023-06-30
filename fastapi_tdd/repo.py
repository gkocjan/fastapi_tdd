from pydantic import BaseModel

_db = {}


class SKU(BaseModel):
    sku_id: str
    name: str
    product_name: str | None


class SKURepo:
    def get(self, sku_id) -> SKU | None:
        return _db.get(sku_id)

    def save(self, sku: SKU) -> SKU:
        _db[sku.sku_id] = sku
        return self.get(sku.sku_id)
