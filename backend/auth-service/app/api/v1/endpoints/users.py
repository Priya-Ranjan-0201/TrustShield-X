import uuid
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_client_ip, get_trace_id, get_current_user
from app.core.security import decode_token
from app.models.user import User
from app.services.user_service import UserService
from app.schemas.auth import UserResponse
from app.schemas.session import SessionResponse
from app.schemas.user import (
    ProfileUpdateRequest,
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.schemas.envelope import StandardResponse, ResponseMeta

router = APIRouter(prefix="/users", tags=["User Management"])


def _make_meta(trace_id: str) -> ResponseMeta:
    return ResponseMeta(traceId=trace_id)


def _get_current_jti(request: Request) -> str | None:
    cookie_token = request.cookies.get("tsx_refresh_token") or request.headers.get("X-Refresh-Token")
    if cookie_token:
        try:
            payload = decode_token(cookie_token)
            return payload.get("jti")
        except ValueError:
            pass
    return None


@router.get(
    "/me",
    response_model=StandardResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
)
async def get_me(
    current_user: User = Depends(get_current_user),
    trace_id: str = Depends(get_trace_id),
):
    user_response = UserResponse(
        id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
        phone=current_user.phone,
        role=current_user.role.name,
        status=current_user.status.value,
        email_verified=current_user.email_verified,
        created_at=current_user.created_at,
    )
    return StandardResponse(
        success=True,
        message="User profile fetched successfully.",
        data=user_response,
        meta=_make_meta(trace_id),
    )


@router.put(
    "/me",
    response_model=StandardResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Update current user profile",
)
async def update_me(
    request_data: ProfileUpdateRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    ip_address: str = Depends(get_client_ip),
    trace_id: str = Depends(get_trace_id),
):
    user_service = UserService(db)
    updated_user = await user_service.update_profile(
        user_id=current_user.id,
        request=request_data,
        ip_address=ip_address,
        user_agent=request.headers.get("User-Agent"),
        trace_id=trace_id,
    )
    return StandardResponse(
        success=True,
        message="User profile updated successfully.",
        data=updated_user,
        meta=_make_meta(trace_id),
    )


@router.put(
    "/change-password",
    response_model=StandardResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Change password for current user",
)
async def change_password(
    request_data: ChangePasswordRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    ip_address: str = Depends(get_client_ip),
    trace_id: str = Depends(get_trace_id),
):
    user_service = UserService(db)
    await user_service.change_password(
        user_id=current_user.id,
        request=request_data,
        ip_address=ip_address,
        user_agent=request.headers.get("User-Agent"),
        trace_id=trace_id,
    )
    return StandardResponse(
        success=True,
        message="Password updated successfully. Please log in again with your new password.",
        data={"password_changed": True},
        meta=_make_meta(trace_id),
    )


@router.get(
    "/sessions",
    response_model=StandardResponse[list[SessionResponse]],
    status_code=status.HTTP_200_OK,
    summary="Get active user sessions",
)
async def get_sessions(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    trace_id: str = Depends(get_trace_id),
):
    user_service = UserService(db)
    current_jti = _get_current_jti(request)
    sessions = await user_service.get_active_sessions(
        user_id=current_user.id, current_jti=current_jti
    )
    return StandardResponse(
        success=True,
        message="Active sessions retrieved.",
        data=sessions,
        meta=_make_meta(trace_id),
    )


@router.delete(
    "/sessions/{session_id}",
    response_model=StandardResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Revoke selected active session",
)
async def revoke_session(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    ip_address: str = Depends(get_client_ip),
    trace_id: str = Depends(get_trace_id),
):
    user_service = UserService(db)
    await user_service.revoke_session(
        user_id=current_user.id,
        session_id=session_id,
        ip_address=ip_address,
        trace_id=trace_id,
    )
    return StandardResponse(
        success=True,
        message="Session revoked successfully.",
        data={"session_revoked": True},
        meta=_make_meta(trace_id),
    )


@router.delete(
    "/sessions",
    response_model=StandardResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Revoke all active user sessions",
)
async def revoke_all_sessions(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    ip_address: str = Depends(get_client_ip),
    trace_id: str = Depends(get_trace_id),
):
    user_service = UserService(db)
    current_jti = _get_current_jti(request)
    await user_service.revoke_all_sessions(
        user_id=current_user.id,
        current_jti=current_jti,
        ip_address=ip_address,
        trace_id=trace_id,
    )
    return StandardResponse(
        success=True,
        message="All active sessions revoked.",
        data={"all_sessions_revoked": True},
        meta=_make_meta(trace_id),
    )


@router.post(
    "/forgot-password",
    response_model=StandardResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Initiate forgot password reset flow",
)
async def forgot_password(
    request_data: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
    ip_address: str = Depends(get_client_ip),
    trace_id: str = Depends(get_trace_id),
):
    user_service = UserService(db)
    result = await user_service.forgot_password_stub(
        request=request_data,
        ip_address=ip_address,
        trace_id=trace_id,
    )
    return StandardResponse(
        success=True,
        message="Password reset request received.",
        data=result,
        meta=_make_meta(trace_id),
    )


@router.post(
    "/reset-password",
    response_model=StandardResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Reset password using token",
)
async def reset_password(
    request_data: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
    ip_address: str = Depends(get_client_ip),
    trace_id: str = Depends(get_trace_id),
):
    user_service = UserService(db)
    result = await user_service.reset_password_stub(
        request=request_data,
        ip_address=ip_address,
        trace_id=trace_id,
    )
    return StandardResponse(
        success=True,
        message="Password reset structure validated.",
        data=result,
        meta=_make_meta(trace_id),
    )
