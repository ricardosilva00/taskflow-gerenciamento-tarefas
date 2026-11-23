"""
Repositório de tarefas em memória.

Implementa as operações CRUD (Create, Read, Update, Delete). Foi mantido
em memória para simplificar a execução e os testes; trocar por um banco
de dados exigiria alterar apenas esta classe.
"""

from threading import Lock

from src.models import (
    Task,
    ValidationError,
    _agora,
    validar_descricao,
    validar_status,
    validar_titulo,
)


class TaskNotFoundError(LookupError):
    """Erro lançado quando a tarefa procurada não existe."""


class TaskRepository:
    """Armazena e manipula tarefas."""

    def __init__(self):
        self._tarefas = {}
        self._proximo_id = 1
        self._lock = Lock()  # evita conflitos de id com requisições simultâneas

    # ---------- CREATE ----------
    def criar(self, titulo, descricao=None, status="todo"):
        """Cria uma nova tarefa após validar todos os campos."""
        tarefa_validada = dict(
            titulo=validar_titulo(titulo),
            descricao=validar_descricao(descricao),
            status=validar_status(status),
        )
        with self._lock:
            tarefa = Task(id=self._proximo_id, **tarefa_validada)
            self._tarefas[tarefa.id] = tarefa
            self._proximo_id += 1
        return tarefa

    # ---------- READ ----------
    def listar(self, status=None):
        """Lista as tarefas em ordem de criação, opcionalmente filtrando por status."""
        tarefas = list(self._tarefas.values())
        if status is not None:
            validar_status(status)
            tarefas = [t for t in tarefas if t.status == status]
        return sorted(tarefas, key=lambda t: t.id)

    def obter(self, tarefa_id):
        """Retorna uma tarefa pelo id ou lança TaskNotFoundError."""
        try:
            return self._tarefas[tarefa_id]
        except KeyError:
            raise TaskNotFoundError(f"Tarefa {tarefa_id} não encontrada.") from None

    # ---------- UPDATE ----------
    def atualizar(self, tarefa_id, **campos):
        """Atualiza apenas os campos informados de uma tarefa existente."""
        tarefa = self.obter(tarefa_id)
        validadores = {
            "titulo": validar_titulo,
            "descricao": validar_descricao,
            "status": validar_status,
        }
        desconhecidos = set(campos) - set(validadores)
        if desconhecidos:
            raise ValidationError(f"Campos não permitidos: {', '.join(sorted(desconhecidos))}.")
        # Valida tudo antes de alterar, para não deixar a tarefa pela metade.
        novos_valores = {nome: validadores[nome](valor) for nome, valor in campos.items()}
        for nome, valor in novos_valores.items():
            setattr(tarefa, nome, valor)
        tarefa.atualizada_em = _agora()
        return tarefa

    # ---------- DELETE ----------
    def remover(self, tarefa_id):
        """Remove uma tarefa existente."""
        self.obter(tarefa_id)
        del self._tarefas[tarefa_id]

    def resumo(self):
        """Contagem de tarefas por status, usada para monitorar o desempenho da equipe."""
        contagem = {status: 0 for status in ("todo", "in_progress", "done")}
        for tarefa in self._tarefas.values():
            contagem[tarefa.status] += 1
        return contagem
