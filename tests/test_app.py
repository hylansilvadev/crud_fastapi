from fastapi.testclient import TestClient
from crud_fastapi.main import app


def test_carrega_lista_de_usuarios(deve_criar_um_novo_usuario_e_depois_excluir_lo):
    client = TestClient(app)
    
    url ='/users'
    
    resquest = client.get(url)
    
    assert resquest.status_code == 200
    
    
def test_deve_atualizar_usuario(deve_criar_um_novo_usuario_e_depois_excluir_lo):
    client = TestClient(app)
    
    user_update = {
       "nome":"Paciente Teste",
        "idade": 10,
        "logado": True
    }
    
    url = '/users/0'
    
    request = client.put(url, json=user_update)
    
    responseJSON = request.json()
    
    assert request.status_code == 200
    assert responseJSON["nome"] == user_update["nome"]
    assert responseJSON["idade"] == user_update["idade"]
    assert responseJSON["logado"] == user_update["logado"]


def test_deve_buscar_um_usuario_especifico(deve_criar_um_novo_usuario_e_depois_excluir_lo):
    client = TestClient(app)
    
    # esperamos como resposta
    user_data = {
        "nome":"Paciente Teste",
        "idade": 10,
        "logado": False
    }
    
    url = '/users/0'
    
    request = client.get(url)
    
    responseJSON = request.json()
    
    assert request.status_code == 200
    assert responseJSON["nome"] == user_data["nome"]
    assert responseJSON["idade"] == user_data["idade"]
    assert responseJSON["logado"] == user_data["logado"]