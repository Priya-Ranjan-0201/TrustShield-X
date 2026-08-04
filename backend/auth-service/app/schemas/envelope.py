from datetime import datetime, timezone
from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field

T = TypeVar("T")


class ResponseMeta(BaseModel):
    traceId: str = Field(..., description="Unique transaction correlation ID")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO-8601 UTC timestamp",
    )
    version: str = Field(default="v1", description="API Version")


class StandardResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str
    data: Optional[T] = None
    meta: Optional[ResponseMeta] = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: str = Field(..., description="Standardized TSX-AUTH error code")
    meta: Optional[ResponseMeta] = None
    trace_id: Optional[str] = None  # Preserved for backward compatibility
