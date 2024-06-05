from datetime import datetime
from sqlmodel import SQLModel, Field

class User(SQLModel):
    nome: str
    idade: int
    logado: bool = False


class UserDB(User, table=True):
    __tablename__ = "user_table"
    id: int = Field(primary_key=True)
    created_at: datetime = datetime.now()


class UserView(User):
    id: int
    

class UserUpdate(SQLModel):
    nome: str | None = None
    idade: int | None = None
    logado: bool | None = None