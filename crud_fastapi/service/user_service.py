from typing import List
from fastapi import HTTPException, status
from sqlmodel import Session, select

from crud_fastapi.core.database import engine
from crud_fastapi.models.user_model import User, UserDB, UserUpdate


class UserService:
    def create_user_new(self, user: User) -> UserDB:
        with Session(engine) as session:
            user_db = UserDB(**user.model_dump())
            session.add(user_db)
            session.commit()
            session.refresh(user_db)
            return user_db

    def get_all_users(self) -> List[UserDB]:
        with Session(engine) as session:
            users = session.exec(select(UserDB)).all()
            return users

    def get_user_by_id(self, id: int) -> UserDB:
        with Session(engine) as session:
            user_db = session.get(UserDB, id)
            if not user_db:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuário não encontrado",
                )

            return user_db

    def update_user_by_id(self, id: int, user_data: UserUpdate) -> UserDB:
        with Session(engine) as session:
            user_db = session.get(UserDB, id)
            if not user_db:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuário não encontrado",
                )
            update_user = user_data.model_dump(exclude_none=True)
            user_db.sqlmodel_update(update_user)
            session.add(user_db)
            session.commit()
            session.refresh(user_db)

            return user_db

    def delete_user_by_id(serf, id: int) -> None:
        with Session(engine) as session:
            user_db = session.get(UserDB, id)
            if not user_db:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuário não encontrado",
                )

            session.delete(user_db)
            session.commit()
