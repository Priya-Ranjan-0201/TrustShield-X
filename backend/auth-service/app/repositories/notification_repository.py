import uuid
from datetime import datetime, timezone
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notification import Notification


class NotificationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_notification(
        self,
        user_id: uuid.UUID,
        title: str,
        message: str,
        severity: str = "info",
    ) -> Notification:
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            severity=severity,
        )
        self.session.add(notif)
        await self.session.commit()
        return notif

    async def get_user_notifications(
        self, user_id: uuid.UUID, limit: int = 50
    ) -> list[Notification]:
        stmt = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def mark_as_read(self, notification_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        stmt = (
            update(Notification)
            .where(Notification.id == notification_id, Notification.user_id == user_id)
            .values(read=True)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def mark_all_as_read(self, user_id: uuid.UUID) -> int:
        stmt = (
            update(Notification)
            .where(Notification.user_id == user_id, Notification.read.is_(False))
            .values(read=True)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount
