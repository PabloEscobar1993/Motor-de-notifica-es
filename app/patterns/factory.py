"""FACTORY METHOD PATTERN.

Cria o objeto de Notificação correto com base no "tipo" recebido na
requisição (email ou sms). Cada Notificação já vem equipada com a
Strategy de envio correspondente.
"""

from abc import ABC

from app.patterns.strategies import EmailStrategy, SendStrategy, SmsStrategy


class Notification(ABC):
    """Produto abstrato do Factory Method.

    Guarda os dados da notificação e delega o envio para uma Strategy.
    """

    def __init__(self, recipient: str, message: str, strategy: SendStrategy):
        self.recipient = recipient
        self.message = message
        self._strategy = strategy

    def dispatch(self) -> str:
        """Dispara a notificação usando a Strategy de envio."""
        return self._strategy.send(self.recipient, self.message)


class EmailNotification(Notification):
    """Notificação de E-mail (usa EmailStrategy)."""

    def __init__(self, recipient: str, message: str):
        super().__init__(recipient, message, EmailStrategy())


class SmsNotification(Notification):
    """Notificação de SMS (usa SmsStrategy)."""

    def __init__(self, recipient: str, message: str):
        super().__init__(recipient, message, SmsStrategy())


class NotificationFactory:
    """Fábrica que decide qual Notificação instanciar a partir do tipo."""

    _registry = {
        "email": EmailNotification,
        "sms": SmsNotification,
    }

    @classmethod
    def create(cls, tipo: str, recipient: str, message: str) -> Notification:
        notification_cls = cls._registry.get((tipo or "").lower())
        if notification_cls is None:
            raise ValueError(f"Tipo de notificação inválido: {tipo}")
        return notification_cls(recipient, message)
