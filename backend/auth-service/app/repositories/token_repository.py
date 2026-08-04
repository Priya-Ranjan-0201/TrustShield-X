import uuid
from datetime import datetime, timezone
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.token import RefreshToken
from app.models.password_reset import PasswordResetToken


class TokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # --- Refresh Tokens ---
    async def create_refresh_token(
        self, user_id: uuid.UUID, token_jti: str, expires_at: datetime
    ) -> RefreshToken:
        refresh_token = RefreshToken(
            user_id=user_id,
            token_jti=token_jti,
            expires_at=expires_at,
        )
        self.session.add(refresh_token)
        await self.session.commit()
        return refresh_token

    async def get_refresh_token_by_jti(self, token_jti: str) -> RefreshToken | None:
        stmt = select(RefreshToken).where(RefreshToken.token_jti == token_jti)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_jti(self, token_jti: str) -> RefreshToken | None:
        """Alias for get_refresh_token_by_jti."""
        return await self.get_refresh_token_by_jti(token_jti)

    async def revoke_refresh_token(self, token_jti: str) -> bool:
        stmt = select(RefreshToken).where(RefreshToken.token_jti == token_jti)
        result = await self.session.execute(stmt)
        token = result.scalar_one_or_none()
        if token and not token.revoked_at:
            token.revoked_at = datetime.now(timezone.utc)
            await self.session.commit()
            return True
        return False

    async def revoke_all_user_refresh_tokens(self, user_id: uuid.UUID) -> int:
        now = datetime.now(timezone.utc)
        stmt = (
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id, RefreshToken.revoked_at.is_(None))
            .values(revoked_at=now)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount

    # --- Password Reset Tokens (Structure Only) ---
    async def create_password_reset_token(
        self, user_id: uuid.UUID, token_hash: str, expires_at: datetime
    ) -> PasswordResetToken:
        reset_token = PasswordResetToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        self.session.add(reset_token)
        await self.session.commit()
        return reset_token

    async def get_password_reset_token(self, token_hash: str) -> PasswordResetToken | None:
        stmt = select(PasswordResetToken).where(PasswordResetToken.token_hash == token_hash)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
