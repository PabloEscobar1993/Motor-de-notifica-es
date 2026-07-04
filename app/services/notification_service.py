"""Camada Service: regras de negócio.

Orquestra o Factory Method, a Strategy e o Repository.
"""

from app.models.notification import NotificationModel
from app.patterns.factory import NotificationFactory
from app.repositories.notification_repository import NotificationRepository
from app.schemas import NotificationCreate


class NotificationService:
    def __init__(self, repository: NotificationRepository):
        self.repository = repository

    def create_notification(self, data: NotificationCreate) -> NotificationModel:
        """RF01 - Registra a notificação (ainda não enviada)."""
        return self.repository.create(
            recipient=data.recipient,
            message=data.message,
            type=data.type.value,
        )

    def dispatch_notification(self, notification_id: int) -> NotificationModel:
        """RF02 - Dispara a notificação (envio simulado via Factory + Strategy)."""
        notification = self.repository.get(notification_id)
        if notification is None:
            raise ValueError("Notificação não encontrada")

        # Factory Method escolhe o objeto certo; dispatch() aplica a Strategy.
        domain_notification = NotificationFactory.create(
            notification.type, notification.recipient, notification.message
        )
        domain_notification.dispatch()

        notification.status = "ENVIADA"
        return self.repository.save(notification)

    def list_notifications(self) -> list[NotificationModel]:
        """RF03 - Retorna o histórico de notificações."""
        return self.repository.list_all()
