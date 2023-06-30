from fastapi import FastAPI, HTTPException

app = FastAPI()
db = {}


@app.get("/sku/{sku_id}")
def get_sku_by_id(sku_id: str):
    sku = db.get(sku_id)
    if sku is None:
        raise HTTPException(status_code=404, detail="SKU not found")
    return sku


@app.put("/sku/{sku_id}")
def update_sku_by_id(sku_id: str):
    raise HTTPException(status_code=404, detail="SKU not found")
