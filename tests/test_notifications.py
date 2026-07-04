"""Testes unitários e de integração do Mini Motor de Notificações."""

import pytest

from app.patterns.factory import (
    EmailNotification,
    NotificationFactory,
    SmsNotification,
)
from app.patterns.strategies import EmailStrategy, SmsStrategy

# --------------------------------------------------------------------------
# Testes dos Design Patterns (Factory Method e Strategy)
# --------------------------------------------------------------------------


def test_factory_cria_email():
    """Factory deve criar uma EmailNotification para o tipo 'email'."""
    obj = NotificationFactory.create("email", "aluno@escola.com", "Olá")
    assert isinstance(obj, EmailNotification)


def test_factory_cria_sms():
    """Factory deve criar uma SmsNotification para o tipo 'sms'."""
    obj = NotificationFactory.create("sms", "11999998888", "Olá")
    assert isinstance(obj, SmsNotification)


def test_factory_tipo_invalido():
    """Factory deve recusar tipos desconhecidos."""
    with pytest.raises(ValueError):
        NotificationFactory.create("fax", "x", "y")


def test_email_strategy_envia():
    """EmailStrategy deve simular o envio e citar o destinatário."""
    resultado = EmailStrategy().send("aluno@escola.com", "Olá")
    assert "aluno@escola.com" in resultado


def test_sms_strategy_envia():
    """SmsStrategy deve simular o envio e citar o destinatário."""
    resultado = SmsStrategy().send("11999998888", "Olá")
    assert "11999998888" in resultado


# --------------------------------------------------------------------------
# Testes da API (integração das camadas Controller/Service/Repository)
# --------------------------------------------------------------------------


def test_criar_notificacao(client):
    """RF01 - Criar notificação retorna 201 com status inicial CRIADA."""
    resp = client.post(
        "/notifications",
        json={"recipient": "aluno@escola.com", "message": "Bem-vindo", "type": "email"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["id"] > 0
    assert body["status"] == "CRIADA"


def test_disparar_notificacao(client):
    """RF02 - Disparar notificação muda o status para ENVIADA."""
    criado = client.post(
        "/notifications",
        json={"recipient": "aluno@escola.com", "message": "Bem-vindo", "type": "email"},
    ).json()
    resp = client.post(f"/notifications/{criado['id']}/dispatch")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ENVIADA"


def test_listar_historico(client):
    """RF03 - Listar retorna o histórico de notificações."""
    client.post(
        "/notifications",
        json={"recipient": "11999998888", "message": "Oi", "type": "sms"},
    )
    resp = client.get("/notifications")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1
