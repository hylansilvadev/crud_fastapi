from typing import List
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    nome: str
    idade: int
    logado: bool
    
database = []
 

# CREATE 

@app.post(
    '/users',
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False
)
def create_new_user(user: User):
    database.append(user)
    return user

# READ

@app.get(
    '/users',
    response_model=List[User],
    status_code=status.HTTP_200_OK,
)
def get_all_users():
    return database


@app.get(
    '/users/{id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False
)
def get_user_by_id(id: int):
    if id <= -1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Id de usuário não permitido"
        )
    
    if not database[id] or len(database) < id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return database[id]


# UPDATE

@app.put(
    '/users/{id}',
    response_model=User,
    response_model_by_alias=False
)
def update_user_by_id(id: int, user_data: User):
    if id <= -1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Id de usuário não permitido"
        )
    
    if not database[id] or len(database) < id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    database[id] = user_data
    
    return user_data


# DELETE 

@app.delete(
    '/users/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user_by_id(id: int):
    if id <= -1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Id de usuário não permitido"
        )
    
    if not database[id] or len(database) < id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    database.pop(id)