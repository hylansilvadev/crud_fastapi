import random
from faker import Faker
from fastapi.testclient import TestClient
from crud_fastapi.main import app

faker = Faker("pt_BR")

# GET
def test_carrega_lista_de_usuarios(deve_criar_uma_lista_de_usuarios_e_depois_excluir):
    client = TestClient(app)
    
    url ='/users'
    
    request = client.get(url)
    
    responseJSON = request.json()
    
    assert request.status_code == 200
    assert isinstance(responseJSON, list)
    
# GET (id)
def test_deve_buscar_um_usuario_especifico(deve_criar_um_novo_usuario):
    user = deve_criar_um_novo_usuario
    
    client = TestClient(app)
    
    url = f'/users/{user['id']}'
    
    request = client.get(url)
    
    responseJSON = request.json()
    
    assert request.status_code == 200
    assert responseJSON["nome"] == user["nome"]
    assert responseJSON["idade"] == user["idade"]
    assert responseJSON["logado"] == user["logado"]
    
    request = client.delete(url)

    assert request.status_code == 204

# PATCH (id)
def test_deve_atualizar_usuario(deve_criar_um_novo_usuario):
    user = deve_criar_um_novo_usuario
    
    client = TestClient(app)
    
    user_update = {
       "nome": faker.name(), 
        "idade": random.randint(18,99), 
        "logado": faker.boolean()
    }
    
    url = f'/users/{user['id']}'
    
    request = client.patch(url, json=user_update)
    
    responseJSON = request.json()
    
    assert request.status_code == 200
    assert responseJSON["nome"] == user_update["nome"]
    assert responseJSON["idade"] == user_update["idade"]
    assert responseJSON["logado"] == user_update["logado"]

    request = client.delete(url)

    assert request.status_code == 204

# DELETE (id)
def test_deve_criar_um_novo_usuario_e_depois_excluir_lo():
    client = TestClient(app)

    user_data = {
       "nome": faker.name(), 
        "idade": random.randint(18,99), 
        "logado": faker.boolean()
    }

    url = "/users"

    request = client.post(url, json=user_data)

    responseJSON = request.json()

    assert request.status_code == 201
    assert responseJSON["nome"] == user_data["nome"]
    assert responseJSON["idade"] == user_data["idade"]
    assert responseJSON["logado"] == user_data["logado"]

    url = f"/users/{responseJSON["id"]}"

    request = client.delete(url)

    assert request.status_code == 204