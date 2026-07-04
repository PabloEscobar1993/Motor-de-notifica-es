"""Configuração da conexão com o banco relacional (SQLite)."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./notifications.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos ORM (camada Model)
Base = declarative_base()


def get_db():
    """Fornece uma sessão de banco por requisição (injeção de dependência)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
