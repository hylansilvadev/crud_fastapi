from datetime import datetime
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field

from crud_fastapi.models.product_model import ProductDB


class Label(SQLModel):
    title: str


class LabelDB(Label, table=True):
    id: int = Field(primary_key=True)
    products: List[ProductDB] = Relationship(back_populates="label")
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None


class LabelView(SQLModel):
    title: str


class LabelUpdate(SQLModel):
    title: Optional[str] = None
    updated_at: datetime = datetime.now()