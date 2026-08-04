import uuid
from typing import Callable
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_token
from app.core.redis import is_jti_blacklisted, get_user_revocation_cutoff
from app.core.error_codes import AuthErrorCode
from app.models.user import User, UserStatus
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"


def get_trace_id(request: Request) -> str:
    trace_id = request.headers.get("X-Trace-ID")
    if not trace_id:
        trace_id = str(uuid.uuid4())
        request.state.trace_id = trace_id
    return trace_id


async def get_current_user(
    request: Request,
    token: str | None = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not token:
        exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token required.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        setattr(exc, "error_code", AuthErrorCode.UNAUTHORIZED)
        raise exc

    try:
        payload = decode_token(token)
    except ValueError:
        exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token signature.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        setattr(exc, "error_code", AuthErrorCode.TOKEN_EXPIRED)
        raise exc

    if payload.get("type") != "access":
        exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token type.",
        )
        setattr(exc, "error_code", AuthErrorCode.UNAUTHORIZED)
        raise exc

    jti = payload.get("jti")
    if jti and await is_jti_blacklisted(jti):
        exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token has been revoked.",
        )
        setattr(exc, "error_code", AuthErrorCode.TOKEN_REVOKED)
        raise exc

    user_id_str = payload.get("sub")
    if not user_id_str:
        exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims.",
        )
        setattr(exc, "error_code", AuthErrorCode.UNAUTHORIZED)
        raise exc

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token.",
        )
        setattr(exc, "error_code", AuthErrorCode.UNAUTHORIZED)
        raise exc

    iat = payload.get("iat")
    cutoff = await get_user_revocation_cutoff(user_id_str)
    if cutoff and iat and iat < cutoff:
        exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session revoked. Please log in again.",
        )
        setattr(exc, "error_code", AuthErrorCode.TOKEN_REVOKED)
        raise exc

    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    if not user or user.status != UserStatus.ACTIVE:
        exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive or disabled.",
        )
        setattr(exc, "error_code", AuthErrorCode.ACCOUNT_DISABLED)
        raise exc

    return user


def require_roles(*allowed_roles: str) -> Callable:
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        user_role_name = current_user.role.name.upper()
        allowed_upper = [r.upper() for r in allowed_roles]
        if user_role_name not in allowed_upper and "ADMIN" not in allowed_upper:
            exc = HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{user_role_name}' does not have permission to access this resource.",
            )
            setattr(exc, "error_code", AuthErrorCode.FORBIDDEN)
            raise exc
        return current_user

    return role_checker
