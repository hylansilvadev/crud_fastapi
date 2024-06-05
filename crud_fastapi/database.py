from sqlmodel import SQLModel, Session, create_engine

from crud_fastapi.config import settings


engine = create_engine(settings.DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
