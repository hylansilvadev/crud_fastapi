from fastapi import APIRouter, status
from typing import List

from crud_fastapi.models.user_model import UserView, User, UserUpdate
from crud_fastapi.service.user_service import UserService


route = APIRouter(prefix="api/v1/user", tags=["User"])
user_service = UserService()


@route.post(
    "/",
    response_model=UserView,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
def create_new_user(user: User):
    return user_service.create_user_new(user)


@route.get(
    "/",
    response_model=List[UserView],
    status_code=status.HTTP_200_OK,
)
def get_all_users():
    return user_service.get_all_users()


@route.get(
    "/{id}",
    response_model=UserView,
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
def get_user_by_id(id: int):
    return user_service.get_user_by_id(id)


@route.patch("/{id}", response_model=UserView, response_model_by_alias=False)
def update_user_by_id(id: int, user_data: UserUpdate):
    return user_service.update_user_by_id(id, user_data)


@route.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_id(id: int):
    user_service.delete_user_by_id(id)
