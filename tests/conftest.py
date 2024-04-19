from pytest import fixture
from fastapi.testclient import TestClient
from crud_fastapi.main import app

@fixture()
def deve_criar_um_novo_usuario_e_depois_excluir_lo():
    client = TestClient(app)
    
    user_data = {
        "nome":"Paciente Teste",
        "idade": 10,
        "logado": False
    }
    
    url = '/users'
    
    request = client.post(url, json=user_data)
    
    responseJSON = request.json()
    
    assert request.status_code == 201
    assert responseJSON["nome"] == user_data["nome"]
    assert responseJSON["idade"] == user_data["idade"]
    assert responseJSON["logado"] == user_data["logado"]
    
    yield
    
    url = '/users/0'
    
    request = client.delete(url)
    
    assert request.status_code == 204