from typing import List
from fastapi import FastAPI, status, HTTPException
from fastapi.concurrency import asynccontextmanager
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from crud_fastapi.models import User, UserDB, UserView, UserUpdate
from crud_fastapi.database import create_db_and_tables, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


kargs={
    "title":"Crud FastAPI Playlist",
    "lifespan":lifespan,
    "docs_url":"/",
    "version":"0.7.0"
}

app = FastAPI(**kargs, )


# CREATE


@app.post(
    "/users",
    response_model=UserView,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_new_user(user: User):
    async with AsyncSession(engine) as session:
        user_db = UserDB(**user.model_dump())
        session.add(user_db)
        await session.commit()
        await session.refresh(user_db)
        return user_db


# READ


@app.get(
    "/users",
    response_model=List[UserView],
    status_code=status.HTTP_200_OK,
)
async def get_all_users():
    async with AsyncSession(engine) as session:
        result = await session.exec(select(UserDB))
        users = result.all()
        return users



@app.get(
    "/users/{id}",
    response_model=UserView,
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def get_user_by_id(id: int):
    async with AsyncSession(engine) as session:
        user_db = await session.get(UserDB, id)
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
            )

        return user_db


# UPDATE


@app.patch("/users/{id}", response_model=UserView, response_model_by_alias=False)
async def update_user_by_id(id: int, user_data: UserUpdate):
    async with AsyncSession(engine) as session:
        user_db = await session.get(UserDB, id)
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
            )
        update_user = user_data.model_dump(exclude_none=True)
        user_db.sqlmodel_update(update_user)
        session.add(user_db)
        await session.commit()
        await session.refresh(user_db)

        return user_db


# DELETE


@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(id: int):
    async with AsyncSession(engine) as session:
        user_db = await session.get(UserDB, id)
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
            )

        await session.delete(user_db)
        await session.commit()
