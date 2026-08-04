import uuid
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.core.error_codes import AuthErrorCode
from app.api.v1.router import api_router
from app.schemas.envelope import ErrorResponse, ResponseMeta

logger = logging.getLogger("auth-service.app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager validating configuration and infrastructure connectivity on startup."""
    try:
        await settings.validate_on_startup()
        logger.info("Startup validation successful: Database and Redis connectivity verified.")
    except Exception as e:
        logger.critical(f"STARTUP FAILED: {str(e)}", exc_info=True)
        # Suppress startup hard break in non-production local pytest runs if Postgres/Redis container absent
        if settings.ENVIRONMENT.lower() == "production":
            raise e
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)

# 1. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 2. Security Headers & Trace ID Middleware
@app.middleware("http")
async def add_security_headers_and_trace_id(request: Request, call_next):
    trace_id = request.headers.get("X-Trace-ID") or str(uuid.uuid4())
    request.state.trace_id = trace_id

    response = await call_next(request)

    response.headers["X-Trace-ID"] = trace_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; object-src 'none'; frame-ancestors 'none';"
    if settings.ENVIRONMENT.lower() == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


# Helper to determine TSX-AUTH error code from HTTP status
def _resolve_error_code(exc: StarletteHTTPException) -> str:
    if hasattr(exc, "error_code") and getattr(exc, "error_code"):
        return getattr(exc, "error_code")
    
    code_map = {
        400: AuthErrorCode.WEAK_PASSWORD,
        401: AuthErrorCode.UNAUTHORIZED,
        403: AuthErrorCode.FORBIDDEN,
        404: AuthErrorCode.NOT_FOUND,
        409: AuthErrorCode.WEAK_PASSWORD,
        429: AuthErrorCode.RATE_LIMIT_EXCEEDED,
    }
    return code_map.get(exc.status_code, f"TSX-AUTH-{exc.status_code}")


# 3. Custom Exception Handlers for Uniform Error Envelopes with Meta
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    trace_id = getattr(request.state, "trace_id", str(uuid.uuid4()))
    error_code = _resolve_error_code(exc)

    error_env = ErrorResponse(
        success=False,
        message=str(exc.detail),
        error_code=error_code,
        meta=ResponseMeta(traceId=trace_id),
        trace_id=trace_id,
    )
    headers = getattr(exc, "headers", None)
    return JSONResponse(
        status_code=exc.status_code,
        content=error_env.model_dump(),
        headers=headers,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    trace_id = getattr(request.state, "trace_id", str(uuid.uuid4()))
    errors = exc.errors()
    detail_msg = errors[0].get("msg") if errors else "Request validation error"

    error_env = ErrorResponse(
        success=False,
        message=f"Validation failed: {detail_msg}",
        error_code=AuthErrorCode.VALIDATION_ERROR,
        meta=ResponseMeta(traceId=trace_id),
        trace_id=trace_id,
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_env.model_dump(),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    trace_id = getattr(request.state, "trace_id", str(uuid.uuid4()))
    logger.error(f"[TraceID: {trace_id}] Unhandled server exception: {str(exc)}", exc_info=True)

    error_env = ErrorResponse(
        success=False,
        message="An internal server error occurred. Please contact support with the trace ID.",
        error_code=AuthErrorCode.INTERNAL_ERROR,
        meta=ResponseMeta(traceId=trace_id),
        trace_id=trace_id,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_env.model_dump(),
    )


# 4. Include Routers
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health"], summary="Root healthcheck")
async def root_health():
    return {"status": "UP", "service": settings.PROJECT_NAME}
