# Modelagem UML do TaskFlow

Os diagramas abaixo usam [Mermaid](https://mermaid.js.org/), que o GitHub
renderiza automaticamente.

## Diagrama de Casos de Uso

Atores:

- **Membro da equipe** (operador de logística): cria, consulta e move tarefas.
- **Gestor do projeto**: além do que o membro faz, prioriza tarefas e acompanha o resumo de desempenho.

```mermaid
flowchart LR
    membro(["👤 Membro da equipe"])
    gestor(["👤 Gestor do projeto"])

    subgraph TaskFlow["Sistema TaskFlow"]
        UC1(("Criar tarefa"))
        UC2(("Listar / filtrar tarefas"))
        UC3(("Atualizar tarefa"))
        UC4(("Mover tarefa no quadro"))
        UC5(("Excluir tarefa"))
        UC6(("Definir prioridade"))
        UC7(("Consultar resumo por status"))
        UC8(("Validar dados de entrada"))
    end

    membro --- UC1
    membro --- UC2
    membro --- UC3
    membro --- UC4
    gestor --- UC5
    gestor --- UC6
    gestor --- UC7
    gestor -. herda .-> membro

    UC1 -. include .-> UC8
    UC3 -. include .-> UC8
    UC4 -. extend .-> UC3
```

## Diagrama de Classes

```mermaid
classDiagram
    class Task {
        +int id
        +str titulo
        +str descricao
        +str status
        +str prioridade
        +str criada_em
        +str atualizada_em
        +to_dict() dict
    }

    class TaskRepository {
        -dict _tarefas
        -int _proximo_id
        -Lock _lock
        +criar(titulo, descricao, status, prioridade) Task
        +listar(status, prioridade) list~Task~
        +obter(tarefa_id) Task
        +atualizar(tarefa_id, campos) Task
        +remover(tarefa_id) None
        +resumo() dict
    }

    class FlaskApp {
        <<create_app>>
        +GET /
        +GET /api/tasks
        +POST /api/tasks
        +GET /api/tasks/id
        +PUT /api/tasks/id
        +DELETE /api/tasks/id
        +GET /api/resumo
    }

    class ValidationError {
        <<exception>>
    }
    class TaskNotFoundError {
        <<exception>>
    }

    FlaskApp --> TaskRepository : usa
    TaskRepository "1" o-- "0..*" Task : armazena
    TaskRepository ..> ValidationError : lança
    TaskRepository ..> TaskNotFoundError : lança
    ValueError <|-- ValidationError
    LookupError <|-- TaskNotFoundError
```

> O atributo `prioridade` e o caso de uso **Definir prioridade** foram
> incluídos na mudança de escopo descrita no [README](../README.md#gestão-de-mudanças).
