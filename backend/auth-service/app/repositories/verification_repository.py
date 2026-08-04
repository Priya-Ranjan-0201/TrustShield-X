import uuid
from datetime import datetime, timezone
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.email_verification import EmailVerificationToken


class VerificationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_verification_token(
        self, user_id: uuid.UUID, token_hash: str, expires_at: datetime
    ) -> EmailVerificationToken:
        record = EmailVerificationToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        self.session.add(record)
        await self.session.flush()
        return record

    async def get_by_token_hash(self, token_hash: str) -> EmailVerificationToken | None:
        stmt = select(EmailVerificationToken).where(
            EmailVerificationToken.token_hash == token_hash,
            EmailVerificationToken.used_at.is_(None),
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def mark_used(self, record_id: uuid.UUID) -> None:
        now = datetime.now(timezone.utc)
        stmt = (
            update(EmailVerificationToken)
            .where(EmailVerificationToken.id == record_id)
            .values(used_at=now)
        )
        await self.session.execute(stmt)
