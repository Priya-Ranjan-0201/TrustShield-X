import uuid
from datetime import datetime, timezone
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.session import UserSession


class SessionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_session(
        self,
        user_id: uuid.UUID,
        device_name: str | None,
        browser: str | None,
        operating_system: str | None,
        ip_address: str,
        country: str | None,
        refresh_token_jti: str,
        expires_at: datetime,
    ) -> UserSession:
        user_session = UserSession(
            user_id=user_id,
            device_name=device_name,
            browser=browser,
            operating_system=operating_system,
            ip_address=ip_address,
            country=country or "Unknown",
            refresh_token_jti=refresh_token_jti,
            is_active=True,
            expires_at=expires_at,
        )
        self.session.add(user_session)
        await self.session.flush()
        return user_session

    async def get_active_sessions_by_user_id(self, user_id: uuid.UUID) -> list[UserSession]:
        stmt = (
            select(UserSession)
            .where(UserSession.user_id == user_id, UserSession.is_active.is_(True))
            .order_by(UserSession.last_activity.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_session_by_jti(self, refresh_token_jti: str) -> UserSession | None:
        stmt = select(UserSession).where(UserSession.refresh_token_jti == refresh_token_jti)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_session_by_id(self, session_id: uuid.UUID) -> UserSession | None:
        stmt = select(UserSession).where(UserSession.id == session_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def touch_session(self, refresh_token_jti: str) -> None:
        now = datetime.now(timezone.utc)
        stmt = (
            update(UserSession)
            .where(UserSession.refresh_token_jti == refresh_token_jti, UserSession.is_active.is_(True))
            .values(last_activity=now)
        )
        await self.session.execute(stmt)

    async def revoke_session_by_id(self, session_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        stmt = (
            update(UserSession)
            .where(UserSession.id == session_id, UserSession.user_id == user_id, UserSession.is_active.is_(True))
            .values(is_active=False)
        )
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def revoke_session_by_jti(self, refresh_token_jti: str) -> None:
        stmt = (
            update(UserSession)
            .where(UserSession.refresh_token_jti == refresh_token_jti)
            .values(is_active=False)
        )
        await self.session.execute(stmt)

    async def revoke_all_user_sessions(self, user_id: uuid.UUID, except_jti: str | None = None) -> None:
        stmt = update(UserSession).where(UserSession.user_id == user_id, UserSession.is_active.is_(True))
        if except_jti:
            stmt = stmt.where(UserSession.refresh_token_jti != except_jti)
        stmt = stmt.values(is_active=False)
        await self.session.execute(stmt)
