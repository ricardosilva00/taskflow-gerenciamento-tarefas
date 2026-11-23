"""Testes do CRUD em memória (src/repository.py)."""

import pytest

from src.models import ValidationError
from src.repository import TaskNotFoundError, TaskRepository


@pytest.fixture
def repo():
    return TaskRepository()


def test_criar_gera_ids_sequenciais(repo):
    t1 = repo.criar("Primeira")
    t2 = repo.criar("Segunda")
    assert (t1.id, t2.id) == (1, 2)


def test_criar_com_dados_invalidos_nao_salva(repo):
    with pytest.raises(ValidationError):
        repo.criar("")
    assert repo.listar() == []


def test_obter_inexistente(repo):
    with pytest.raises(TaskNotFoundError):
        repo.obter(99)


def test_listar_filtrando_por_status(repo):
    repo.criar("A")
    repo.criar("B", status="done")
    assert [t.titulo for t in repo.listar(status="done")] == ["B"]


def test_atualizar_campos(repo):
    tarefa = repo.criar("Antigo")
    repo.atualizar(tarefa.id, titulo="Novo", status="in_progress")
    atual = repo.obter(tarefa.id)
    assert atual.titulo == "Novo"
    assert atual.status == "in_progress"


def test_atualizar_campo_desconhecido(repo):
    tarefa = repo.criar("X")
    with pytest.raises(ValidationError):
        repo.atualizar(tarefa.id, id=50)


def test_atualizacao_invalida_nao_altera_nada(repo):
    tarefa = repo.criar("Original")
    with pytest.raises(ValidationError):
        repo.atualizar(tarefa.id, titulo="Novo", status="invalido")
    assert repo.obter(tarefa.id).titulo == "Original"


def test_remover(repo):
    tarefa = repo.criar("Apagar")
    repo.remover(tarefa.id)
    with pytest.raises(TaskNotFoundError):
        repo.obter(tarefa.id)


def test_resumo_por_status(repo):
    repo.criar("A")
    repo.criar("B", status="done")
    repo.criar("C", status="done")
    assert repo.resumo() == {"todo": 1, "in_progress": 0, "done": 2}
