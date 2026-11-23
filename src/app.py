"""
Aplicação web (Flask) do TaskFlow.

Expõe uma API REST para o CRUD de tarefas e uma página web simples que
consome essa API. Execute com:  python -m src.app
"""

from flask import Flask, jsonify, render_template, request

from src.models import ValidationError
from src.repository import TaskNotFoundError, TaskRepository


def create_app(repositorio=None):
    """Fábrica da aplicação: permite injetar um repositório limpo nos testes."""
    app = Flask(__name__)
    repo = repositorio or TaskRepository()

    # ---------- Tratamento de erros padronizado ----------
    @app.errorhandler(ValidationError)
    def erro_validacao(erro):
        return jsonify({"erro": str(erro)}), 400

    @app.errorhandler(TaskNotFoundError)
    def erro_nao_encontrado(erro):
        return jsonify({"erro": str(erro)}), 404

    def corpo_json():
        """Lê o corpo da requisição exigindo um objeto JSON."""
        dados = request.get_json(silent=True)
        if not isinstance(dados, dict):
            raise ValidationError("O corpo da requisição deve ser um objeto JSON.")
        return dados

    # ---------- Página web ----------
    @app.get("/")
    def index():
        return render_template("index.html")

    # ---------- API REST ----------
    @app.get("/api/tasks")
    def listar():
        # Filtro opcional: /api/tasks?status=todo
        tarefas = repo.listar(status=request.args.get("status"))
        return jsonify([t.to_dict() for t in tarefas])

    @app.post("/api/tasks")
    def criar():
        dados = corpo_json()
        tarefa = repo.criar(
            titulo=dados.get("titulo"),
            descricao=dados.get("descricao"),
            status=dados.get("status", "todo"),
        )
        return jsonify(tarefa.to_dict()), 201

    @app.get("/api/tasks/<int:tarefa_id>")
    def obter(tarefa_id):
        return jsonify(repo.obter(tarefa_id).to_dict())

    @app.put("/api/tasks/<int:tarefa_id>")
    def atualizar(tarefa_id):
        tarefa = repo.atualizar(tarefa_id, **corpo_json())
        return jsonify(tarefa.to_dict())

    @app.delete("/api/tasks/<int:tarefa_id>")
    def remover(tarefa_id):
        repo.remover(tarefa_id)
        return "", 204

    @app.get("/api/resumo")
    def resumo():
        return jsonify(repo.resumo())

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
