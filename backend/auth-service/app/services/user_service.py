import uuid
import secrets
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.core.password_policy import validate_password_strength
from app.core.redis import blacklist_jti
from app.models.user import User, UserStatus
from app.repositories.user_repository import UserRepository
from app.repositories.token_repository import TokenRepository
from app.repositories.audit_repository import AuditRepository
from app.repositories.session_repository import SessionRepository
from app.schemas.auth import UserResponse
from app.schemas.session import SessionResponse
from app.schemas.user import (
    ProfileUpdateRequest,
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.token_repo = TokenRepository(db)
        self.audit_repo = AuditRepository(db)
        self.session_repo = SessionRepository(db)

    async def get_profile(self, user_id: uuid.UUID) -> UserResponse:
        user = await self.user_repo.get_by_id(user_id)
        if not user or user.status != UserStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User account not found or inactive.",
            )
        return UserResponse(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            phone=user.phone,
            role=user.role.name,
            status=user.status.value,
            email_verified=user.email_verified,
            created_at=user.created_at,
        )

    async def update_profile(
        self,
        user_id: uuid.UUID,
        request: ProfileUpdateRequest,
        ip_address: str,
        user_agent: str | None,
        trace_id: str,
    ) -> UserResponse:
        user = await self.user_repo.get_by_id(user_id)
        if not user or user.status != UserStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User account not found or inactive.",
            )

        if request.full_name is not None:
            user.full_name = request.full_name.strip()

        if request.phone is not None and request.phone != user.phone:
            existing_phone = await self.user_repo.get_by_phone(request.phone)
            if existing_phone and existing_phone.id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="This phone number is already registered to another account.",
                )
            user.phone = request.phone

        updated_user = await self.user_repo.update(user)

        await self.audit_repo.log_action(
            action="PROFILE_UPDATE_SUCCESS",
            user_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
            success=True,
            trace_id=trace_id,
        )

        return UserResponse(
            id=updated_user.id,
            full_name=updated_user.full_name,
            email=updated_user.email,
            phone=updated_user.phone,
            role=updated_user.role.name,
            status=updated_user.status.value,
            email_verified=updated_user.email_verified,
            created_at=updated_user.created_at,
        )

    async def change_password(
        self,
        user_id: uuid.UUID,
        request: ChangePasswordRequest,
        ip_address: str,
        user_agent: str | None,
        trace_id: str,
    ) -> None:
        user = await self.user_repo.get_by_id(user_id)
        if not user or user.status != UserStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User account not found or inactive.",
            )

        if not verify_password(request.current_password, user.password_hash):
            await self.audit_repo.log_action(
                action="PASSWORD_CHANGE_FAILED",
                user_id=user.id,
                ip_address=ip_address,
                user_agent=user_agent,
                success=False,
                trace_id=trace_id,
                metadata={"reason": "Current password incorrect"},
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect current password.",
            )

        is_valid_pw, pw_error = validate_password_strength(request.new_password)
        if not is_valid_pw:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=pw_error or "Invalid new password.",
            )

        user.password_hash = hash_password(request.new_password)
        await self.user_repo.update(user)

        # Revoke all sessions for security
        await self.token_repo.revoke_all_user_refresh_tokens(user.id)
        await self.session_repo.revoke_all_user_sessions(user.id)

        await self.audit_repo.log_action(
            action="PASSWORD_CHANGE_SUCCESS",
            user_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
            success=True,
            trace_id=trace_id,
        )

    async def get_active_sessions(
        self, user_id: uuid.UUID, current_jti: str | None = None
    ) -> list[SessionResponse]:
        sessions = await self.session_repo.get_active_sessions_by_user_id(user_id)
        response_list = []
        for s in sessions:
            res = SessionResponse.model_validate(s)
            if current_jti and s.refresh_token_jti == current_jti:
                res.is_current = True
            response_list.append(res)
        return response_list

    async def revoke_session(
        self, user_id: uuid.UUID, session_id: uuid.UUID, ip_address: str, trace_id: str
    ) -> None:
        session_obj = await self.session_repo.get_session_by_id(session_id)
        if not session_obj or session_obj.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session record not found.",
            )

        await self.session_repo.revoke_session_by_id(session_id, user_id)
        await self.token_repo.revoke_refresh_token(session_obj.refresh_token_jti)

        await self.audit_repo.log_action(
            action="SESSION_REVOKED",
            user_id=user_id,
            ip_address=ip_address,
            success=True,
            trace_id=trace_id,
            metadata={"session_id": str(session_id)},
        )

    async def revoke_all_sessions(
        self, user_id: uuid.UUID, current_jti: str | None, ip_address: str, trace_id: str
    ) -> None:
        await self.session_repo.revoke_all_user_sessions(user_id, except_jti=current_jti)
        await self.token_repo.revoke_all_user_refresh_tokens(user_id)

        await self.audit_repo.log_action(
            action="ALL_SESSIONS_REVOKED",
            user_id=user_id,
            ip_address=ip_address,
            success=True,
            trace_id=trace_id,
        )

    async def forgot_password_stub(
        self,
        request: ForgotPasswordRequest,
        ip_address: str,
        trace_id: str,
    ) -> dict:
        user = await self.user_repo.get_by_email(request.email)
        if user and user.status == UserStatus.ACTIVE:
            raw_token = secrets.token_urlsafe(32)
            token_hash = hash_password(raw_token)[:64]
            expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
            await self.token_repo.create_password_reset_token(
                user_id=user.id, token_hash=token_hash, expires_at=expires_at
            )
            await self.audit_repo.log_action(
                action="FORGOT_PASSWORD_REQUESTED",
                user_id=user.id,
                ip_address=ip_address,
                success=True,
                trace_id=trace_id,
            )

        return {
            "status": "pending_dispatch",
            "info": "If an account exists with this email, a password reset link has been prepared.",
        }

    async def reset_password_stub(
        self,
        request: ResetPasswordRequest,
        ip_address: str,
        trace_id: str,
    ) -> dict:
        is_valid_pw, pw_error = validate_password_strength(request.new_password)
        if not is_valid_pw:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=pw_error or "Invalid new password.",
            )

        await self.audit_repo.log_action(
            action="RESET_PASSWORD_STUB_EXECUTIVE",
            ip_address=ip_address,
            success=True,
            trace_id=trace_id,
        )

        return {
            "status": "structure_validated",
            "info": "Password reset token structure validated. Email dispatch service integration pending for future phase.",
        }
