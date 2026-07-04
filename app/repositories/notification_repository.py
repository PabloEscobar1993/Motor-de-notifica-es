"""Camada Repository: isola todo o acesso ao banco de dados."""

from sqlalchemy.orm import Session

from app.models.notification import NotificationModel


class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, recipient: str, message: str, type: str) -> NotificationModel:
        notification = NotificationModel(
            recipient=recipient, message=message, type=type
        )
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def get(self, notification_id: int) -> NotificationModel | None:
        return (
            self.db.query(NotificationModel)
            .filter(NotificationModel.id == notification_id)
            .first()
        )

    def list_all(self) -> list[NotificationModel]:
        return (
            self.db.query(NotificationModel)
            .order_by(NotificationModel.id.desc())
            .all()
        )

    def save(self, notification: NotificationModel) -> NotificationModel:
        self.db.commit()
        self.db.refresh(notification)
        return notification
