"""Testes unitários das regras de validação de entrada (src/models.py)."""

import pytest

from src.models import (
    DESCRICAO_MAX,
    TITULO_MAX,
    Task,
    ValidationError,
    validar_descricao,
    validar_status,
    validar_titulo,
)


def test_titulo_valido_remove_espacos():
    assert validar_titulo("  Entregar pedido  ") == "Entregar pedido"


@pytest.mark.parametrize("titulo", ["", "   ", None, 123])
def test_titulo_invalido(titulo):
    with pytest.raises(ValidationError):
        validar_titulo(titulo)


def test_titulo_muito_longo():
    with pytest.raises(ValidationError):
        validar_titulo("a" * (TITULO_MAX + 1))


def test_descricao_opcional():
    assert validar_descricao(None) == ""


def test_descricao_muito_longa():
    with pytest.raises(ValidationError):
        validar_descricao("a" * (DESCRICAO_MAX + 1))


@pytest.mark.parametrize("status", ["todo", "in_progress", "done"])
def test_status_validos(status):
    assert validar_status(status) == status


def test_status_invalido():
    with pytest.raises(ValidationError):
        validar_status("arquivado")


def test_task_to_dict():
    tarefa = Task(id=1, titulo="Teste")
    dados = tarefa.to_dict()
    assert dados["id"] == 1
    assert dados["status"] == "todo"
    assert "criada_em" in dados
