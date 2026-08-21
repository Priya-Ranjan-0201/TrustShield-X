import uuid
import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.password_policy import validate_password_strength
from app.core.redis import (
    check_rate_limit,
    blacklist_jti,
    is_jti_blacklisted,
    revoke_user_sessions,
    get_user_revocation_cutoff,
)
from app.core.user_agent import parse_user_agent
from app.core.error_codes import AuthErrorCode
from app.core.logger import security_logger, audit_logger

from app.models.user import User, UserStatus
from app.repositories.user_repository import UserRepository
from app.repositories.token_repository import TokenRepository
from app.repositories.audit_repository import AuditRepository
from app.repositories.session_repository import SessionRepository
from app.repositories.verification_repository import VerificationRepository

from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.token_repo = TokenRepository(db)
        self.audit_repo = AuditRepository(db)
        self.session_repo = SessionRepository(db)
        self.verification_repo = VerificationRepository(db)

    async def register(
        self,
        request: RegisterRequest,
        ip_address: str,
        user_agent: str | None,
        trace_id: str,
    ) -> UserResponse:
        # Rate limiting (3 registration attempts per hour per IP)
        allowed, retry_after = await check_rate_limit(
            key_prefix="ratelimit:register",
            identifier=ip_address,
            max_attempts=3,
            window_seconds=3600,
        )
        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Registration rate limit exceeded. Retry after {retry_after} seconds.",
                headers={"Retry-After": str(retry_after)},
            )

        # 1. Check if email already registered
        existing_user = await self.user_repo.get_by_email(request.email)
        if existing_user:
            await self.audit_repo.log_action(
                action="REGISTER_FAILED_DUPLICATE_EMAIL",
                ip_address=ip_address,
                user_agent=user_agent,
                success=False,
                trace_id=trace_id,
                metadata={"email": request.email},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email address already exists.",
            )

        # 2. Check if phone already registered (if provided)
        if request.phone:
            existing_phone = await self.user_repo.get_by_phone(request.phone)
            if existing_phone:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="An account with this phone number already exists.",
                )

        # 3. Password policy validation
        is_valid_pw, pw_error = validate_password_strength(request.password)
        if not is_valid_pw:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=pw_error or "Password does not meet strength requirements.",
            )

        # 4. Fetch CITIZEN default role
        citizen_role = await self.user_repo.get_role_by_name("CITIZEN")
        if not citizen_role:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Default system role CITIZEN not configured.",
            )

        # 5. Create user record
        hashed_pw = hash_password(request.password)
        user = await self.user_repo.create_user(
            full_name=request.full_name,
            email=request.email,
            password_hash=hashed_pw,
            role_id=citizen_role.id,
            phone=request.phone,
            email_verified=False,
        )

        # 6. Generate Initial Verification Token
        raw_verification_token = secrets.token_urlsafe(32)
        v_token_hash = hashlib.sha256(raw_verification_token.encode()).hexdigest()
        v_expires_at = datetime.now(timezone.utc) + timedelta(hours=settings.VERIFICATION_TOKEN_EXPIRE_HOURS)
        await self.verification_repo.create_verification_token(
            user_id=user.id,
            token_hash=v_token_hash,
            expires_at=v_expires_at,
        )

        # 7. Seed Welcome Notification (Step 7 requirement)
        from app.repositories.notification_repository import NotificationRepository
        notif_repo = NotificationRepository(self.db)
        await notif_repo.create_notification(
            user_id=user.id,
            title="Welcome to TruthShield X",
            message="Your National Digital Trust account is active. Explore the Unified AI Scanner to verify links, documents, and UPI QR codes.",
            severity="info",
        )

        await self.audit_repo.log_action(
            action="USER_REGISTERED_SUCCESS",
            user_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
            success=True,
            trace_id=trace_id,
        )

        security_logger.info(
            f"New user registered: email={user.email}, id={user.id}",
            extra={"trace_id": trace_id, "user_id": str(user.id)}
        )

        return UserResponse(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            phone=user.phone,
            role=citizen_role.name,
            status=user.status.value,
            email_verified=user.email_verified,
            created_at=user.created_at,
        )

    async def login(
        self,
        request: LoginRequest,
        ip_address: str,
        user_agent: str | None,
        trace_id: str,
    ) -> tuple[TokenResponse, str, datetime]:
        # Rate Limiting (5 login attempts per 15 mins per IP+Email)
        rate_key = f"{ip_address}:{request.email.lower()}"
        allowed, retry_after = await check_rate_limit(
            key_prefix="ratelimit:login",
            identifier=rate_key,
            max_attempts=5,
            window_seconds=900,
        )
        if not allowed:
            await self.audit_repo.log_action(
                action="LOGIN_RATE_LIMITED",
                ip_address=ip_address,
                user_agent=user_agent,
                success=False,
                trace_id=trace_id,
                metadata={"email": request.email},
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Too many failed login attempts. Retry after {retry_after} seconds.",
                headers={"Retry-After": str(retry_after)},
            )

        # 1. Fetch user by email
        user = await self.user_repo.get_by_email(request.email)
        if not user or not verify_password(request.password, user.password_hash):
            await self.audit_repo.log_action(
                action="LOGIN_FAILED_INVALID_CREDENTIALS",
                user_id=user.id if user else None,
                ip_address=ip_address,
                user_agent=user_agent,
                success=False,
                trace_id=trace_id,
                metadata={"email": request.email},
            )
            security_logger.warning(
                f"Failed login attempt for email={request.email} from IP={ip_address}",
                extra={"trace_id": trace_id}
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        # 2. Check if user active
        if user.status != UserStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your user account is suspended or disabled.",
            )

        # 3. Check Email Verification Enforcement Policy
        if settings.REQUIRE_EMAIL_VERIFICATION and not user.email_verified:
            await self.audit_repo.log_action(
                action="LOGIN_BLOCKED_UNVERIFIED_EMAIL",
                user_id=user.id,
                ip_address=ip_address,
                user_agent=user_agent,
                success=False,
                trace_id=trace_id,
            )
            exc = HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email address is not verified. Please verify your email before logging in.",
            )
            setattr(exc, "error_code", AuthErrorCode.EMAIL_NOT_VERIFIED)
            raise exc

        # 4. Issue Access Token & Refresh Token Pair
        access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role.name}
        )
        refresh_token_str, jti, refresh_expires_at = create_refresh_token(user_id=user.id)

        # 5. Store Refresh Token in DB
        await self.token_repo.create_refresh_token(
            user_id=user.id,
            token_jti=jti,
            expires_at=refresh_expires_at,
        )

        # 6. Parse User-Agent & Store User Session
        ua_info = parse_user_agent(user_agent)
        await self.session_repo.create_session(
            user_id=user.id,
            device_name=ua_info["device_name"],
            browser=ua_info["browser"],
            operating_system=ua_info["operating_system"],
            ip_address=ip_address,
            country="Unknown",
            refresh_token_jti=jti,
            expires_at=refresh_expires_at,
        )

        # 7. Audit log & analytics
        await self.audit_repo.log_action(
            action="LOGIN_SUCCESS",
            user_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
            success=True,
            trace_id=trace_id,
            metadata={
                "browser": ua_info["browser"],
                "device": ua_info["device_name"],
                "os": ua_info["operating_system"],
            },
        )

        security_logger.info(
            f"Successful login: user_id={user.id}, browser={ua_info['browser']}",
            extra={"trace_id": trace_id, "user_id": str(user.id)}
        )

        token_response = TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        return token_response, refresh_token_str, refresh_expires_at

    async def refresh(
        self,
        refresh_token_str: str,
        ip_address: str,
        user_agent: str | None,
        trace_id: str,
    ) -> tuple[TokenResponse, str, datetime]:
        # 1. Decode & Validate Refresh JWT
        try:
            payload = decode_token(refresh_token_str)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token signature.",
            )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type for refresh.",
            )

        jti = payload.get("jti")
        user_id_str = payload.get("sub")
        if not jti or not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token claims.",
            )

        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID format in token.",
            )

        # 2. Check Redis JTI Blacklist & User Revocation Cutoff
        if await is_jti_blacklisted(jti):
            await self._handle_token_theft(user_id=user_id, jti=jti, ip=ip_address, trace_id=trace_id)

        cutoff = await get_user_revocation_cutoff(user_id_str)
        iat = payload.get("iat")
        if cutoff and iat and iat < cutoff:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session revoked. Please log in again.",
            )

        # 3. Check DB RefreshToken Record
        token_record = await self.token_repo.get_by_jti(jti)
        if not token_record:
            await self._handle_token_theft(user_id=user_id, jti=jti, ip=ip_address, trace_id=trace_id)

        if token_record.revoked_at is not None:
            await self._handle_token_theft(user_id=user_id, jti=jti, ip=ip_address, trace_id=trace_id)

        now = datetime.now(timezone.utc)
        expires_at = token_record.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if expires_at <= now:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired. Please log in again.",
            )

        # 4. Fetch User
        user = await self.user_repo.get_by_id(user_id)
        if not user or user.status != UserStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is inactive or disabled.",
            )

        # 5. Rotate Refresh Token (Revoke old token & issue new pair)
        await self.token_repo.revoke_refresh_token(jti)
        remaining_seconds = int((expires_at - now).total_seconds())
        if remaining_seconds > 0:
            await blacklist_jti(jti, remaining_seconds)

        await self.session_repo.revoke_session_by_jti(jti)

        # Issue new Access & Refresh Pair
        new_access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role.name}
        )
        new_refresh_str, new_jti, new_expires_at = create_refresh_token(user_id=user.id)

        await self.token_repo.create_refresh_token(
            user_id=user.id,
            token_jti=new_jti,
            expires_at=new_expires_at,
        )

        ua_info = parse_user_agent(user_agent)
        await self.session_repo.create_session(
            user_id=user.id,
            device_name=ua_info["device_name"],
            browser=ua_info["browser"],
            operating_system=ua_info["operating_system"],
            ip_address=ip_address,
            country="Unknown",
            refresh_token_jti=new_jti,
            expires_at=new_expires_at,
        )

        await self.audit_repo.log_action(
            action="TOKEN_REFRESH_SUCCESS",
            user_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
            success=True,
            trace_id=trace_id,
        )

        token_response = TokenResponse(
            access_token=new_access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        return token_response, new_refresh_str, new_expires_at

    async def logout(
        self,
        user_id: uuid.UUID,
        refresh_token_str: str | None,
        ip_address: str,
        user_agent: str | None,
        trace_id: str,
    ) -> None:
        if refresh_token_str:
            try:
                payload = decode_token(refresh_token_str)
                jti = payload.get("jti")
                exp = payload.get("exp")
                if jti:
                    await self.token_repo.revoke_refresh_token(jti)
                    await self.session_repo.revoke_session_by_jti(jti)
                    if exp:
                        now_ts = int(datetime.now(timezone.utc).timestamp())
                        ttl = exp - now_ts
                        if ttl > 0:
                            await blacklist_jti(jti, ttl)
            except ValueError:
                pass

        await self.audit_repo.log_action(
            action="LOGOUT_SUCCESS",
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            success=True,
            trace_id=trace_id,
        )

    async def verify_email(self, token: str, ip_address: str, trace_id: str) -> dict:
        v_token_hash = hashlib.sha256(token.encode()).hexdigest()
        record = await self.verification_repo.get_by_token_hash(v_token_hash)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or already used email verification token.",
            )

        now = datetime.now(timezone.utc)
        expires_at = record.expires_at.replace(tzinfo=timezone.utc) if record.expires_at.tzinfo is None else record.expires_at
        if expires_at <= now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email verification token has expired. Please request a new link.",
            )

        # Mark user email as verified
        user = await self.user_repo.get_by_id(record.user_id)
        if user:
            user.email_verified = True
            await self.user_repo.update(user)

        await self.verification_repo.mark_used(record.id)

        await self.audit_repo.log_action(
            action="EMAIL_VERIFIED_SUCCESS",
            user_id=record.user_id,
            ip_address=ip_address,
            success=True,
            trace_id=trace_id,
        )

        return {"verified": True, "info": "Email address verified successfully."}

    async def resend_verification(self, email: str, ip_address: str, trace_id: str) -> dict:
        user = await self.user_repo.get_by_email(email)
        if user and not user.email_verified:
            raw_token = secrets.token_urlsafe(32)
            token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
            expires_at = datetime.now(timezone.utc) + timedelta(hours=settings.VERIFICATION_TOKEN_EXPIRE_HOURS)
            await self.verification_repo.create_verification_token(
                user_id=user.id, token_hash=token_hash, expires_at=expires_at
            )

            await self.audit_repo.log_action(
                action="RESEND_VERIFICATION_REQUESTED",
                user_id=user.id,
                ip_address=ip_address,
                success=True,
                trace_id=trace_id,
            )

        return {
            "status": "pending_dispatch",
            "info": "If an unverified account exists for this email, a verification link has been prepared.",
        }

    async def _handle_token_theft(self, user_id: uuid.UUID, jti: str, ip: str, trace_id: str):
        await self.token_repo.revoke_all_user_refresh_tokens(user_id)
        await self.session_repo.revoke_all_user_sessions(user_id)
        await revoke_user_sessions(str(user_id))

        await self.audit_repo.log_action(
            action="TOKEN_THEFT_DETECTED",
            user_id=user_id,
            ip_address=ip,
            success=False,
            trace_id=trace_id,
            metadata={"revoked_jti": jti},
        )

        security_logger.critical(
            f"TOKEN THEFT DETECTED for user_id={user_id}. Revoked all active tokens & sessions.",
            extra={"trace_id": trace_id, "user_id": str(user_id)}
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Security alert: Token reuse detected. All sessions have been revoked.",
        )
