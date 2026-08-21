import uuid
from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.repositories.notification_repository import NotificationRepository
from app.schemas.envelope import ResponseEnvelope, ResponseMeta

router = APIRouter()


@router.get("", response_model=ResponseEnvelope[list[dict]])
async def get_notifications(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    notif_repo = NotificationRepository(db)
    notifications = await notif_repo.get_user_notifications(current_user.id, limit=50)

    data = [
        {
            "id": str(n.id),
            "title": n.title,
            "message": n.message,
            "read": n.read,
            "severity": n.severity,
            "created_at": n.created_at.isoformat(),
        }
        for n in notifications
    ]

    return ResponseEnvelope[list[dict]](
        success=True,
        message="Notifications retrieved.",
        data=data,
        meta=ResponseMeta(
            traceId=getattr(request.state, "trace_id", "trace-id-default"),
            version="v1",
        ),
    )


@router.put("/{notification_id}/read", response_model=ResponseEnvelope[dict])
async def mark_notification_read(
    notification_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    notif_repo = NotificationRepository(db)
    success = await notif_repo.mark_as_read(notification_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found.",
        )

    return ResponseEnvelope[dict](
        success=True,
        message="Notification marked as read.",
        data={"id": str(notification_id), "read": True},
        meta=ResponseMeta(
            traceId=getattr(request.state, "trace_id", "trace-id-default"),
            version="v1",
        ),
    )


@router.put("/read-all", response_model=ResponseEnvelope[dict])
async def mark_all_notifications_read(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    notif_repo = NotificationRepository(db)
    count = await notif_repo.mark_all_as_read(current_user.id)

    return ResponseEnvelope[dict](
        success=True,
        message=f"{count} notifications marked as read.",
        data={"marked_count": count},
        meta=ResponseMeta(
            traceId=getattr(request.state, "trace_id", "trace-id-default"),
            version="v1",
        ),
    )
