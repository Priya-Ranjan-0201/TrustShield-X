import uuid
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class SessionResponse(BaseModel):
    id: uuid.UUID
    device_name: str | None = None
    browser: str | None = None
    operating_system: str | None = None
    ip_address: str
    country: str | None = "Unknown"
    last_activity: datetime
    is_active: bool
    created_at: datetime
    expires_at: datetime
    is_current: bool = False

    model_config = ConfigDict(from_attributes=True)


class VerifyEmailRequest(BaseModel):
    token: str = Field(..., description="Email verification token received via email link")


class ResendVerificationRequest(BaseModel):
    email: str = Field(..., description="Email address to resend verification link to")
