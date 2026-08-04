import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


class RegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=10)
    phone: str | None = Field(default=None, max_length=20)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.lower().strip()

    @field_validator("phone")
    @classmethod
    def clean_phone(cls, v: str | None) -> str | None:
        if v:
            v = v.strip()
            return v if v else None
        return None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.lower().strip()


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 900  # 15 minutes


class UserResponse(BaseModel):
    id: uuid.UUID
    full_name: str
    email: str
    phone: str | None = None
    role: str
    status: str
    email_verified: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
