import os
from typing import List, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "TruthShield X - Auth Service"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = Field(default="development")

    # PostgreSQL Database
    POSTGRES_SERVER: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_USER: str = Field(default="tsx_admin")
    POSTGRES_PASSWORD: str = Field(default="tsx_password")
    POSTGRES_DB: str = Field(default="truthshield_db")
    DATABASE_URL: str | None = None

    # Redis Cache & Token Management
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_PASSWORD: str = Field(default="")
    REDIS_DB: int = Field(default=0)
    REDIS_URL: str | None = None

    # JWT & Auth Security
    JWT_SECRET: str = Field(default="super_secret_jwt_key_truthshield_x_change_in_production_123456789")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS Configuration
    ALLOWED_ORIGINS: Union[str, List[str]] = Field(default="http://localhost:5173,http://localhost:3000")

    # Email Verification Enforcement Policy
    REQUIRE_EMAIL_VERIFICATION: bool = False
    VERIFICATION_TOKEN_EXPIRE_HOURS: int = 24

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    @property
    def async_database_url(self) -> str:
        if self.DATABASE_URL:
            if self.DATABASE_URL.startswith("postgresql://"):
                return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
            return self.DATABASE_URL
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def sync_database_url(self) -> str:
        if self.DATABASE_URL:
            if self.DATABASE_URL.startswith("postgresql+asyncpg://"):
                return self.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://", 1)
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def redis_connection_url(self) -> str:
        if self.REDIS_URL:
            return self.REDIS_URL
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    async def validate_on_startup(self) -> None:
        """Validate critical environment variables, PostgreSQL, and Redis connectivity on startup."""
        if len(self.JWT_SECRET_KEY) < 32 and self.ENVIRONMENT.lower() == "production":
            raise ValueError("JWT_SECRET_KEY must be at least 32 characters long in production.")

        try:
            from app.core.database import AsyncSessionLocal
            from sqlalchemy import text
            async with AsyncSessionLocal() as session:
                await session.execute(text("SELECT 1"))
        except Exception as e:
            raise RuntimeError(f"Database startup validation failed: {str(e)}")

        try:
            from app.core.redis import get_redis_client
            redis = await get_redis_client()
            await redis.ping()
        except Exception as e:
            raise RuntimeError(f"Redis startup validation failed: {str(e)}")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


settings = Settings()
