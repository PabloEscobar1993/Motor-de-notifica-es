# Mini Motor de Notificações

API REST para **registrar** e **disparar** (envio simulado) notificações de
**E-mail** e **SMS**. Projeto de Laboratório de Engenharia de Software com foco
em **arquitetura em camadas** e nos padrões de projeto **Factory Method** e
**Strategy**.

## Tecnologias

- Python 3
- FastAPI (API REST + documentação Swagger automática)
- SQLAlchemy + SQLite (persistência relacional)
- Pytest (testes)

## Arquitetura em Camadas

```
┌─────────────────────────────────────────────┐
│  Controller  (app/controllers)              │  ← Endpoints REST (FastAPI)
├─────────────────────────────────────────────┤
│  Service     (app/services)                 │  ← Regras de negócio
│              usa Factory + Strategy         │
├─────────────────────────────────────────────┤
│  Repository  (app/repositories)             │  ← Acesso ao banco
├─────────────────────────────────────────────┤
│  Model       (app/models)  + SQLite         │  ← Persistência (ORM)
└─────────────────────────────────────────────┘

Design Patterns (app/patterns):
  Factory Method  ->  cria EmailNotification / SmsNotification pelo "tipo"
  Strategy        ->  EmailStrategy / SmsStrategy (algoritmos de envio)
```

Fluxo de um disparo: `Controller → Service → Factory (cria o objeto) →
Strategy (envia) → Repository (persiste)`.

## Estrutura de Pastas

```
app/
├── controllers/   # Camada Controller (rotas REST)
├── services/      # Camada Service (regras de negócio)
├── repositories/  # Camada Repository (acesso a dados)
├── models/        # Camada Model (ORM / tabela)
├── patterns/      # Factory Method e Strategy
├── database.py    # Conexão com o SQLite
├── schemas.py     # Schemas Pydantic (JSON)
└── main.py        # Aplicação FastAPI
tests/             # Testes com Pytest
```

## Como Rodar (Docker)

Com o **Docker Desktop** aberto, na pasta do projeto:

```bash
docker compose up --build
```

A API fica disponível em `http://127.0.0.1:8000/docs` (Swagger). Para parar,
`Ctrl+C` ou, em outro terminal, `docker compose down`.

Rodar os testes dentro do container:

```bash
docker compose exec api pytest -v
```

## Endpoints (Requisitos Funcionais)

| Método | Rota                                | Requisito | Descrição                       |
|--------|-------------------------------------|-----------|---------------------------------|
| POST   | `/notifications`                    | RF01      | Cria uma notificação            |
| POST   | `/notifications/{id}/dispatch`      | RF02      | Dispara (envio simulado)        |
| GET    | `/notifications`                    | RF03      | Lista o histórico               |

Exemplo de corpo para criar (RF01):

```json
{
  "recipient": "aluno@escola.com",
  "message": "Sua nota foi lançada",
  "type": "email"
}
```

## Como Rodar os Testes

```bash
docker compose exec api pytest -v
```

São 8 testes: 5 de padrões de projeto (Factory/Strategy) e 3 de
integração da API (RF01, RF02 e RF03).

## Onde estão os Padrões

- **Factory Method:** [`app/patterns/factory.py`](app/patterns/factory.py) —
  `NotificationFactory.create()` instancia `EmailNotification` ou
  `SmsNotification` conforme o `tipo`.
- **Strategy:** [`app/patterns/strategies.py`](app/patterns/strategies.py) —
  `EmailStrategy` e `SmsStrategy` implementam algoritmos de envio distintos,
  usados por `Notification.dispatch()`.
