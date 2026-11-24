"""Testes da funcionalidade de prioridade (mudança de escopo - ver README)."""

import pytest

from src.app import create_app
from src.models import ValidationError, validar_prioridade
from src.repository import TaskRepository


@pytest.mark.parametrize("valor,esperado", [("alta", "alta"), ("BAIXA", "baixa"), (None, "media")])
def test_validar_prioridade(valor, esperado):
    assert validar_prioridade(valor) == esperado


def test_prioridade_invalida():
    with pytest.raises(ValidationError):
        validar_prioridade("urgentissima")


def test_listagem_ordenada_por_prioridade():
    repo = TaskRepository()
    repo.criar("Baixa", prioridade="baixa")
    repo.criar("Alta", prioridade="alta")
    repo.criar("Media")
    assert [t.titulo for t in repo.listar()] == ["Alta", "Media", "Baixa"]


def test_filtro_por_prioridade_na_api():
    client = create_app(TaskRepository()).test_client()
    client.post("/api/tasks", json={"titulo": "Urgente", "prioridade": "alta"})
    client.post("/api/tasks", json={"titulo": "Normal"})
    resp = client.get("/api/tasks?prioridade=alta")
    assert [t["titulo"] for t in resp.get_json()] == ["Urgente"]


def test_atualizar_prioridade():
    repo = TaskRepository()
    tarefa = repo.criar("X")
    assert repo.atualizar(tarefa.id, prioridade="alta").prioridade == "alta"
