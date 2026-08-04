from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.api.deps import get_client_ip, get_trace_id, get_current_user
from app.models.user import User
from app.services.auth_service import AuthService
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.schemas.session import VerifyEmailRequest, ResendVerificationRequest
from app.schemas.envelope import StandardResponse, ResponseMeta

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _make_meta(trace_id: str) -> ResponseMeta:
    return ResponseMeta(traceId=trace_id)


@router.post(
    "/register",
    response_model=StandardResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
)
async def register(
    request_data: RegisterRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    ip_address: str = Depends(get_client_ip),
    trace_id: str = Depends(get_trace_id),
):
    auth_service = AuthService(db)
    user_response = await auth_service.register(
        request=request_data,
        ip_address=ip_address,
        user_agent=request.headers.get("User-Agent"),
        trace_id=trace_id,
    )
    return StandardResponse(
        success=True,
        message="User account created successfully.",
        data=user_response,
        meta=_make_meta(trace_id),
    )


@router.post(
    "/login",
    response_model=StandardResponse[TokenResponse],
    status_code=status.HTTP_200_OK,
    summary="Authenticate user & receive access token",
)
async def login(
    request_data: LoginRequest,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    ip_address: str = Depends(get_client_ip),
    trace_id: str = Depends(get_trace_id),
):
    auth_service = AuthService(db)
    token_response, refresh_token_str, refresh_expires_at = await auth_service.login(
        request=request_data,
        ip_address=ip_address,
        user_agent=request.headers.get("User-Agent"),
        trace_id=trace_id,
    )

    is_secure = settings.ENVIRONMENT.lower() == "production"
    response.set_cookie(
        key="tsx_refresh_token",
        value=refresh_token_str,
        httponly=True,
        secure=is_secure,
        samesite="lax" if not is_secure else "strict",
        expires=refresh_expires_at,
        path="/api/v1/auth",
    )

    return StandardResponse(
        success=True,
        message="Login successful.",
        data=token_response,
        meta=_make_meta(trace_id),
    )


@router.post(
    "/refresh",
    response_model=StandardResponse[TokenResponse],
    status_code=status.HTTP_200_OK,
    summary="Rotate refresh token & receive new access token",
)
async def refresh(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    ip_address: str = Depends(get_client_ip),
    trace_id: str = Depends(get_trace_id),
):
    refresh_token_str = request.cookies.get("tsx_refresh_token") or request.headers.get("X-Refresh-Token")
    if not refresh_token_str:
        return Response(
            content='{"success": false, "message": "Refresh token cookie missing.", "error_code": "TSX-AUTH-010", "meta": {"traceId": "' + trace_id + '"}}',
            status_code=status.HTTP_401_UNAUTHORIZED,
            media_type="application/json",
        )

    auth_service = AuthService(db)
    token_response, new_refresh_str, new_expires_at = await auth_service.refresh(
        refresh_token_str=refresh_token_str,
        ip_address=ip_address,
        user_agent=request.headers.get("User-Agent"),
        trace_id=trace_id,
    )

    is_secure = settings.ENVIRONMENT.lower() == "production"
    response.set_cookie(
        key="tsx_refresh_token",
        value=new_refresh_str,
        httponly=True,
        secure=is_secure,
        samesite="lax" if not is_secure else "strict",
        expires=new_expires_at,
        path="/api/v1/auth",
    )

    return StandardResponse(
        success=True,
        message="Token refreshed successfully.",
        data=token_response,
        meta=_make_meta(trace_id),
    )


@router.post(
    "/logout",
    response_model=StandardResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Log out user & revoke refresh session",
)
async def logout(
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    ip_address: str = Depends(get_client_ip),
    trace_id: str = Depends(get_trace_id),
):
    refresh_token_str = request.cookies.get("tsx_refresh_token") or request.headers.get("X-Refresh-Token")
    auth_service = AuthService(db)
    await auth_service.logout(
        user_id=current_user.id,
        refresh_token_str=refresh_token_str,
        ip_address=ip_address,
        user_agent=request.headers.get("User-Agent"),
        trace_id=trace_id,
    )

    response.delete_cookie(key="tsx_refresh_token", path="/api/v1/auth")

    return StandardResponse(
        success=True,
        message="Logged out successfully.",
        data={"logged_out": True},
        meta=_make_meta(trace_id),
    )


@router.post(
    "/verify-email",
    response_model=StandardResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Verify user email address using verification token",
)
async def verify_email(
    request_data: VerifyEmailRequest,
    db: AsyncSession = Depends(get_db),
    ip_address: str = Depends(get_client_ip),
    trace_id: str = Depends(get_trace_id),
):
    auth_service = AuthService(db)
    result = await auth_service.verify_email(
        token=request_data.token,
        ip_address=ip_address,
        trace_id=trace_id,
    )
    return StandardResponse(
        success=True,
        message="Email verification processed.",
        data=result,
        meta=_make_meta(trace_id),
    )


@router.post(
    "/resend-verification",
    response_model=StandardResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Resend email verification link",
)
async def resend_verification(
    request_data: ResendVerificationRequest,
    db: AsyncSession = Depends(get_db),
    ip_address: str = Depends(get_client_ip),
    trace_id: str = Depends(get_trace_id),
):
    auth_service = AuthService(db)
    result = await auth_service.resend_verification(
        email=request_data.email,
        ip_address=ip_address,
        trace_id=trace_id,
    )
    return StandardResponse(
        success=True,
        message="Verification resend request processed.",
        data=result,
        meta=_make_meta(trace_id),
    )
