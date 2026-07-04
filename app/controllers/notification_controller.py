"""Camada Controller: expõe os endpoints da API."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.notification_repository import NotificationRepository
from app.schemas import NotificationCreate, NotificationOut
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notificações"])

"""Monta a cadeia de camadas: Repository -> Service."""
def get_service(db: Session = Depends(get_db)) -> NotificationService:
    
    return NotificationService(NotificationRepository(db))


@router.post(
    "", response_model=NotificationOut, status_code=status.HTTP_201_CREATED
)
def create_notification(
    payload: NotificationCreate,
    service: NotificationService = Depends(get_service),
):
    """RF01 - Cria uma notificação (Destinatário, Mensagem, Tipo)."""
    return service.create_notification(payload)

"""RF02 - Dispara (simula o envio) da notificação."""
@router.post("/{notification_id}/dispatch", response_model=NotificationOut)
def dispatch_notification(
    notification_id: int,
    service: NotificationService = Depends(get_service),
):
    
    try:
        return service.dispatch_notification(notification_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        )

"""RF03 - Lista o histórico de notificações enviadas."""
@router.get("", response_model=list[NotificationOut])
def list_notifications(service: NotificationService = Depends(get_service)):
    
    return service.list_notifications()
