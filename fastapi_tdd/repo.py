from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class _DBSKU(Base):
    __tablename__ = "sku"
    sku_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    product_name: Mapped[str | None]


class SKU(BaseModel):
    sku_id: str
    name: str
    product_name: str | None

    class Config:
        orm_mode = True


class SKURepo:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, sku_id) -> SKU | None:
        orm_sku = self._session.execute(
            select(_DBSKU).where(_DBSKU.sku_id == sku_id)
        ).first()
        return SKU.from_orm(orm_sku[0]) if orm_sku is not None else None

    def save(self, sku: SKU) -> SKU:
        db_sku = self._session.get(_DBSKU, ident=sku.sku_id) or _DBSKU(
            sku_id=sku.sku_id
        )

        db_sku.name = sku.name
        db_sku.product_name = sku.product_name

        self._session.add(db_sku)
        self._session.flush()
        return self.get(sku.sku_id)
