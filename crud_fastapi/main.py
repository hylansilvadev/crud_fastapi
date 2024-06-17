from typing import List
from fastapi import FastAPI, status, HTTPException
from sqlmodel import Session, select

from crud_fastapi.models import User, UserDB, UserView, UserUpdate
from crud_fastapi.database import create_db_and_tables, engine


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# CREATE 

@app.post(
    '/users',
    response_model=UserView,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False
)
def create_new_user(user: User):
    with Session(engine) as session:
        user_db = UserDB(**user.model_dump())
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        return user_db

# READ

@app.get(
    '/users',
    response_model=List[UserView],
    status_code=status.HTTP_200_OK,
)
def get_all_users():
    with Session(engine) as session:
        users = session.exec(select(UserDB)).all()
        return users


@app.get(
    '/users/{id}',
    response_model=UserView,
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False
)
def get_user_by_id(id: int):
    with Session(engine) as session:
        user_db = session.get(UserDB, id)
        if not user_db:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
        
        return user_db
# UPDATE

@app.patch(
    '/users/{id}',
    response_model=UserView,
    response_model_by_alias=False
)
def update_user_by_id(id: int, user_data: UserUpdate):
    with Session(engine) as session:
        user_db = session.get(UserDB, id)
        if not user_db:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
        update_user = user_data.model_dump(exclude_none=True)
        user_db.sqlmodel_update(update_user)
        session.add(user_db)
        session.commit()
        session.refresh(user_db)

        return user_db

# DELETE 

@app.delete(
    '/users/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user_by_id(id: int):
    with Session(engine) as session:
        user_db = session.get(UserDB, id)
        if not user_db:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
        
        session.delete(user_db)
        session.commit()