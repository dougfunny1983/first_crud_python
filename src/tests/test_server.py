from starlette.testclient import TestClient
from starlette.status import HTTP_200_OK
from api.server import app, arq


def test_quando_listar_tarefas_devo_ter_como_retorno_codigo_de_status_200():
    cliente = TestClient(app)
    resposta = cliente.get("/user")
    assert resposta.status_code == HTTP_200_OK


def test_quando_listar_tarefas_formato_de_retorno_deve_ser_json():
    cliente = TestClient(app)
    resposta = cliente.get("/user")
    assert resposta.headers["Content-Type"] == "application/json"


def test_quando_listar_tarefas_retorno_deve_ser_uma_lista():
    cliente = TestClient(app)
    resposta = cliente.get("/user")
    assert isinstance(resposta.json(), list)


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_id():
    arq.append({"id": 1})
    cliente = TestClient(app)
    resposta = cliente.get("/user")
    assert "id" in resposta.json().pop()
    arq.clear()


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_titulo():
    arq.append({"titulo": "titulo 1"})
    cliente = TestClient(app)
    resposta = cliente.get("/user")
    assert "titulo" in resposta.json().pop()
    arq.clear()


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_descricao():
    arq.append({"descricao": "descricao 1"})
    cliente = TestClient(app)
    resposta = cliente.get("/user")
    assert "descricao" in resposta.json().pop()
    arq.clear()


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_um_estado():
    arq.append({"estado": "finalizado"})
    cliente = TestClient(app)
    resposta = cliente.get("/user")
    assert "estado" in resposta.json().pop()
    arq.clear()


def test_recurso_tarefas_deve_aceitar_o_verbo_post():
    cliente = TestClient(app)
    resposta = cliente.post("/user")
    assert resposta.status_code != 405


def test_quando_uma_tarefa_e_submetida_deve_possuir_um_titulo():
    cliente = TestClient(app)
    resposta = cliente.post("/user", json={})
    assert resposta.status_code == 422


def test_titulo_da_tarefa_deve_conter_entre_3_e_50_caracteres():
    cliente = TestClient(app)
    resposta = cliente.post("/user", json={"titulo": 2 * "*"})
    assert resposta.status_code == 422
    resposta = cliente.post("/user", json={"titulo": 51 * "*"})
    assert resposta.status_code == 422


def test_descricao_da_tarefa_pode_conter_no_maximo_140_caracteres():
    cliente = TestClient(app)
    resposta = cliente.post("/user", json={"titulo": "titulo", "descricao": "*" * 141})
    assert resposta.status_code == 422


def test_quando_criar_uma_tarefa_a_mesma_deve_ser_retornada():
    cliente = TestClient(app)
    users = {"titulo": "titulo", "descricao": "descricao" * 130}
    resposta = cliente.post("/user", json=users)
    assert resposta.json() == users


def test_quando_criar_uma_tarefa_seu_id_deve_ser_unico():
    cliente = TestClient(app)
    tarefa_1 = {"titulo": "titulo1", "descricao": "*" * 139}
    tarefa_2 = {"titulo": "titulo2", "descricao": "*" * 138}
    resposta_1 = cliente.post("/users", json=tarefa_1)
    resposta_2 = cliente.post("/users", json=tarefa_2)
    assert resposta_1.json()["id"] != resposta_2.json()["id"]
