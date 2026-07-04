"""STRATEGY PATTERN.

Define algoritmos de envio intercambiáveis. Cada estratégia implementa
o mesmo contrato `send()`, mas com um comportamento de envio diferente.
"""

from abc import ABC, abstractmethod


class SendStrategy(ABC):
    """Interface comum das estratégias de envio."""

    @abstractmethod
    def send(self, recipient: str, message: str) -> str:
        """Executa o envio (simulado) e retorna uma descrição do resultado."""
        raise NotImplementedError


class EmailStrategy(SendStrategy):
    """Algoritmo de envio por E-mail."""

    def send(self, recipient: str, message: str) -> str:
        # Simulação: aqui entraria a integração real com um servidor SMTP.
        print(f"[EMAIL] Enviando para {recipient}: {message}")
        return f"E-mail enviado para {recipient}"


class SmsStrategy(SendStrategy):
    """Algoritmo de envio por SMS."""

    def send(self, recipient: str, message: str) -> str:
        # Simulação: aqui entraria a integração real com um gateway de SMS.
        print(f"[SMS] Enviando para {recipient}: {message}")
        return f"SMS enviado para {recipient}"
