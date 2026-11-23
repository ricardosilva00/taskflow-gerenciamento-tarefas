"""
Modelo de domínio do TaskFlow.

Define a entidade Tarefa (Task) e as regras de validação dos dados de
entrada. Toda validação fica concentrada aqui para que a API e o
repositório compartilhem as mesmas regras.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone

# Status possíveis de uma tarefa, espelhando as colunas do quadro Kanban.
STATUS_VALIDOS = ("todo", "in_progress", "done")

TITULO_MAX = 100
DESCRICAO_MAX = 500


class ValidationError(ValueError):
    """Erro lançado quando os dados de uma tarefa são inválidos."""


def validar_titulo(titulo):
    """Garante que o título é um texto não vazio com até TITULO_MAX caracteres."""
    if not isinstance(titulo, str) or not titulo.strip():
        raise ValidationError("O título é obrigatório.")
    titulo = titulo.strip()
    if len(titulo) > TITULO_MAX:
        raise ValidationError(f"O título deve ter no máximo {TITULO_MAX} caracteres.")
    return titulo


def validar_descricao(descricao):
    """A descrição é opcional, mas se informada deve ser texto curto."""
    if descricao is None:
        return ""
    if not isinstance(descricao, str):
        raise ValidationError("A descrição deve ser um texto.")
    descricao = descricao.strip()
    if len(descricao) > DESCRICAO_MAX:
        raise ValidationError(f"A descrição deve ter no máximo {DESCRICAO_MAX} caracteres.")
    return descricao


def validar_status(status):
    """O status deve ser uma das colunas do Kanban."""
    if status not in STATUS_VALIDOS:
        raise ValidationError(f"Status inválido. Use um de: {', '.join(STATUS_VALIDOS)}.")
    return status


def _agora():
    """Data/hora atual em UTC no formato ISO 8601."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class Task:
    """Representa uma tarefa do quadro de trabalho."""

    id: int
    titulo: str
    descricao: str = ""
    status: str = "todo"
    criada_em: str = field(default_factory=_agora)
    atualizada_em: str = field(default_factory=_agora)

    def to_dict(self):
        """Converte a tarefa em dicionário (usado nas respostas JSON)."""
        return asdict(self)
