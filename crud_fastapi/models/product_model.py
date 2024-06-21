from datetime import datetime
from typing import Optional
from sqlmodel import Relationship, SQLModel, Field

from crud_fastapi.models.label_model import LabelDB, LabelView


class Product(SQLModel):
    title: str
    short_description: str
    description: str
    image_url: str
    quantity: int
    value: float
    label_id: Optional[int] = Field(default=None, foreign_key="labeldb.id")


class ProductDB(Product, table=True):
    id: int = Field(primary_key=True)
    label_id: Optional[int] = Field(default=None, foreign_key="labeldb.id")
    label: Optional[LabelDB] = Relationship(back_populates="products")
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None


class ProductView(SQLModel):
    id: int
    title: str
    short_description: str
    description: str
    image_url: str
    quantity: int
    value: float
    label: LabelView | None = None
    created_at: datetime
    updated_at: Optional[datetime] = None



class ProductUpdate(SQLModel):
    title: Optional[str] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    quantity: Optional[int] = None
    value: Optional[float] = None
    label_id: Optional[int] = None
    updated_at: datetime = datetime.now()
