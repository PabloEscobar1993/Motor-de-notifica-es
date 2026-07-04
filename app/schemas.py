"""Schemas de entrada/saída da API (validação com Pydantic)."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class NotificationType(str, Enum):
    """Tipos de notificação suportados."""

    EMAIL = "email"
    SMS = "sms"


class NotificationCreate(BaseModel):
    """Corpo da requisição para criar uma notificação (RF01)."""

    recipient: str
    message: str
    type: NotificationType


class NotificationOut(BaseModel):
    """Representação da notificação retornada pela API (JSON)."""

    id: int
    recipient: str
    message: str
    type: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
