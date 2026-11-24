# TaskFlow — Sistema Ágil de Gerenciamento de Tarefas

[![CI](https://github.com/ricardosilva00/taskflow-gerenciamento-tarefas/actions/workflows/ci.yml/badge.svg)](https://github.com/ricardosilva00/taskflow-gerenciamento-tarefas/actions/workflows/ci.yml)

Projeto acadêmico da disciplina de **Engenharia de Software**: *Construindo um Projeto Ágil no GitHub — da Gestão ao Controle de Qualidade*.

## Objetivo

A **TechFlow Solutions** (empresa fictícia) foi contratada por uma startup de logística para desenvolver um sistema de gerenciamento de tarefas baseado em metodologias ágeis. O sistema permite **acompanhar o fluxo de trabalho em tempo real**, **priorizar tarefas críticas** e **monitorar o desempenho da equipe**.

## Escopo

**Escopo inicial (Sprint 1 e 2)**

- CRUD completo de tarefas (criar, listar, consultar, atualizar e excluir) via API REST.
- Quadro web no estilo Kanban com as colunas *A Fazer*, *Em Progresso* e *Concluído*.
- Validação dos dados de entrada (título obrigatório, limites de tamanho, status válidos).
- Resumo de tarefas por status para acompanhar o desempenho da equipe.
- Testes automatizados e pipeline de integração contínua (GitHub Actions).

**Fora do escopo:** autenticação de usuários, persistência em banco de dados (os dados ficam em memória) e notificações.

**Adicionado por mudança de escopo (Sprint 3):** prioridade das tarefas — ver [Gestão de Mudanças](#gestão-de-mudanças).

## Metodologia

Foi adotado um modelo **híbrido Scrum + Kanban (Scrumban)**:

- **Kanban** — o trabalho é visualizado no [GitHub Projects](../../projects) com as colunas **To Do (A Fazer)**, **In Progress (Em Progresso)** e **Done (Concluído)**, limitando o trabalho em andamento e deixando gargalos visíveis.
- **Scrum** — as entregas foram organizadas em 3 sprints curtas, cada uma com um incremento funcional:
  1. *Sprint 1* — documentação, estrutura do repositório, modelo e CRUD.
  2. *Sprint 2* — interface web, testes automatizados e CI.
  3. *Sprint 3* — mudança de escopo (prioridades) e documentação UML.
- **Commits semânticos** ([Conventional Commits](https://www.conventionalcommits.org/pt-br/)): `feat`, `fix`, `test`, `docs`, `ci`, `chore`.
- **Integração contínua** — todo push na `main` dispara lint + testes.

## Estrutura do repositório

```
.
├── .github/workflows/ci.yml   # Pipeline de CI (flake8 + pytest)
├── docs/uml.md                # Diagramas UML (casos de uso e classes)
├── src/
│   ├── models.py              # Entidade Task e regras de validação
│   ├── repository.py          # CRUD em memória
│   ├── app.py                 # API REST + página web (Flask)
│   └── templates/index.html   # Interface do quadro Kanban
├── tests/                     # Testes automatizados (pytest)
├── requirements.txt
└── setup.cfg                  # Configuração do flake8 e do pytest
```

## Como executar

Pré-requisito: Python 3.11+.

```bash
git clone https://github.com/ricardosilva00/taskflow-gerenciamento-tarefas.git
cd taskflow-gerenciamento-tarefas
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.app
```

Acesse **http://127.0.0.1:5000** no navegador.

### Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/tasks?status=&prioridade=` | Lista tarefas (filtros opcionais), ordenadas por prioridade |
| POST | `/api/tasks` | Cria tarefa — `{"titulo", "descricao", "status", "prioridade"}` |
| GET | `/api/tasks/<id>` | Consulta uma tarefa |
| PUT | `/api/tasks/<id>` | Atualiza campos de uma tarefa |
| DELETE | `/api/tasks/<id>` | Exclui uma tarefa |
| GET | `/api/resumo` | Quantidade de tarefas por status |

Exemplo:

```bash
curl -X POST http://127.0.0.1:5000/api/tasks \
     -H "Content-Type: application/json" \
     -d '{"titulo": "Conferir carga da doca 3", "prioridade": "alta"}'
```

## Testes e controle de qualidade

```bash
flake8 src tests   # análise estática / padrão de código (PEP 8)
pytest -v          # testes automatizados
```

- `tests/test_models.py` — testes unitários de **validação de entradas**.
- `tests/test_repository.py` — testes do CRUD em memória.
- `tests/test_api.py` — testes de integração da API REST.
- `tests/test_prioridade.py` — testes da funcionalidade adicionada na mudança de escopo.

O workflow [`.github/workflows/ci.yml`](.github/workflows/ci.yml) roda o **flake8** e o **pytest** em Python 3.11 e 3.12 a cada push e pull request. Se algum teste ou regra de qualidade falhar, o commit fica marcado com ❌ e a falha aparece na aba **Actions**.

## Gestão de Mudanças

### Mudança de escopo: priorização de tarefas

| Item | Descrição |
|---|---|
| **Solicitante** | Cliente (startup de logística), na revisão da Sprint 2 |
| **Pedido** | Permitir marcar tarefas como **alta, média ou baixa** prioridade, com as críticas aparecendo primeiro |
| **Justificativa** | Na operação logística, entregas com prazo crítico (ex.: carga perecível, janela de doca) se perdiam no meio das demais tarefas. Sem prioridade, a equipe não conseguia cumprir o objetivo de "priorizar tarefas críticas" definido no início do projeto. |
| **Impacto** | Novo campo `prioridade` no modelo (padrão `media`, sem quebrar clientes antigos da API), ordenação e filtro por prioridade, destaque por cor no quadro, novos testes. |
| **Como foi gerenciada** | 1) Novo card criado no Kanban — issue [#9](../../issues/9) — e movido de *To Do* → *In Progress* → *Done*; 2) implementação em commits pequenos (`feat:` / `test:`) referenciando a issue (`Refs #9`); 3) CI validando que nada existente quebrou; 4) README e UML atualizados. |

**Lições:** a mudança foi absorvida com baixo risco porque a validação estava centralizada em `models.py` e os testes existentes funcionaram como rede de segurança — exatamente o que o Manifesto Ágil propõe com *"responder a mudanças mais que seguir um plano"*.

## Questões norteadoras

**1. Principais causas de falhas em projetos ágeis e como o GitHub ajuda a mitigá-las.** Falhas comuns são tarefas mal definidas, falta de visibilidade do andamento, comunicação fragmentada, retrabalho por regressões e mudanças sem rastreio. O GitHub mitiga com o quadro Projects (visibilidade e WIP), issues/cards (tarefas descritas e atribuídas), histórico de commits (rastreabilidade), pull requests (revisão de código) e Actions (detecção automática de regressões).

**2. Quem se beneficia e como.** Operadores de logística usam o quadro para saber o que fazer a seguir; gestores usam prioridades e o resumo por status para redistribuir o trabalho e medir o fluxo; o cliente acompanha a evolução em tempo real; a equipe de desenvolvimento ganha um processo previsível.

**3. Como o GitHub Actions garante software confiável.** Cada alteração é verificada automaticamente (lint + testes em mais de uma versão do Python) antes de ser considerada pronta. Erros aparecem minutos após o push, quando são baratos de corrigir, e ninguém depende de "lembrar" de rodar os testes.

**4. Desafios ao implementar mudanças e como lidar.** Riscos de regressão, estouro de prazo e escopo crescendo sem controle. Mitigação: registrar a mudança como card, avaliar impacto, manter compatibilidade (valor padrão), implementar em incrementos pequenos e confiar na suíte de testes.

**5. Aplicação das metodologias ágeis.** Sprints curtas com incrementos funcionais (Scrum), fluxo visual com colunas e limite de trabalho em andamento (Kanban), feedback do cliente gerando mudança de escopo, entrega contínua e documentação suficiente — não excessiva.

## Autor

Projeto desenvolvido para fins acadêmicos — disciplina de Engenharia de Software.
