"""Ponto de entrada da aplicação FastAPI (Mini Motor de Notificações)."""

from fastapi import FastAPI

from app.controllers.notification_controller import router as notification_router
from app.database import Base, engine

# Cria as tabelas no banco SQLite ao subir a aplicação.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mini Motor de Notificações",
    description=(
        "API REST para registrar e disparar notificações (E-mail e SMS), "
        "demonstrando os padrões Factory Method e Strategy em uma "
        "arquitetura em camadas."
    ),
    version="1.0.0",
)

app.include_router(notification_router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Mini Motor de Notificações. Acesse /docs para o Swagger."}
