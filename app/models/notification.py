"""Camada Model: mapeamento ORM da tabela de notificações."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from app.database import Base


class NotificationModel(Base):
    """Notificação persistida no banco relacional."""

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    recipient = Column(String, nullable=False)
    message = Column(String, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False, default="CRIADA")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
