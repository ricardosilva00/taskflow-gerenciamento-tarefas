"""Testes de integração da API REST (src/app.py) usando o cliente de testes do Flask."""

import pytest

from src.app import create_app
from src.repository import TaskRepository


@pytest.fixture
def client():
    app = create_app(TaskRepository())
    app.config["TESTING"] = True
    return app.test_client()


def test_pagina_inicial(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"TaskFlow" in resp.data


def test_fluxo_crud_completo(client):
    # Create
    resp = client.post("/api/tasks", json={"titulo": "Separar carga", "descricao": "Doca 3"})
    assert resp.status_code == 201
    tarefa_id = resp.get_json()["id"]
    # Read
    assert client.get(f"/api/tasks/{tarefa_id}").get_json()["titulo"] == "Separar carga"
    assert len(client.get("/api/tasks").get_json()) == 1
    # Update
    resp = client.put(f"/api/tasks/{tarefa_id}", json={"status": "done"})
    assert resp.get_json()["status"] == "done"
    # Delete
    assert client.delete(f"/api/tasks/{tarefa_id}").status_code == 204
    assert client.get(f"/api/tasks/{tarefa_id}").status_code == 404


def test_criar_sem_titulo_retorna_400(client):
    resp = client.post("/api/tasks", json={"descricao": "sem título"})
    assert resp.status_code == 400
    assert "título" in resp.get_json()["erro"]


def test_corpo_nao_json_retorna_400(client):
    resp = client.post("/api/tasks", data="texto", content_type="text/plain")
    assert resp.status_code == 400


def test_status_invalido_no_filtro(client):
    assert client.get("/api/tasks?status=xyz").status_code == 400


def test_resumo(client):
    client.post("/api/tasks", json={"titulo": "A"})
    assert client.get("/api/resumo").get_json()["todo"] == 1
