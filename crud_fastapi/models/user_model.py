from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class User(SQLModel):
    nome: str
    idade: int
    logado: bool = False


class UserDB(User, table=True):
    id: int = Field(primary_key=True)
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None


class UserView(User):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserUpdate(SQLModel):
    nome: Optional[str] = None
    idade: Optional[int] = None
    logado: Optional[bool] = None
    updated_at: datetime = datetime.now()