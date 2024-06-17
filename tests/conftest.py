import random
from faker import Faker
from pytest import fixture
from fastapi.testclient import TestClient
from crud_fastapi.main import app

faker = Faker("pt_BR")

# POST
@fixture()
def deve_criar_uma_lista_de_usuarios_e_depois_excluir():
    client = TestClient(app)
    url = "/users"
    ids = []

    for i in range(10):
        user_data = {
            "nome": faker.name(), 
            "idade": random.randint(18,99), 
            "logado": faker.boolean()
            }
        request = client.post(url, json=user_data)
        
        responseJSON = request.json()
        
        assert request.status_code == 201
        ids.append(responseJSON["id"])
        
    yield
    
    
    
    for id in ids:
        url = f"/users/{id}"
        
        request = client.delete(url)
        
        assert request.status_code == 204

# POST
@fixture()
def deve_criar_um_novo_usuario():
    client = TestClient(app)

    user_data = {"nome": faker.name(), "idade": random.randint(18,99), "logado": faker.boolean()}

    url = "/users"

    request = client.post(url, json=user_data)

    responseJSON = request.json()

    assert request.status_code == 201
    assert responseJSON["nome"] == user_data["nome"]
    assert responseJSON["idade"] == user_data["idade"]
    assert responseJSON["logado"] == user_data["logado"]

    return responseJSON
