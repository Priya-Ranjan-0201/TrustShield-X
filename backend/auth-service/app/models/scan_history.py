import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Integer, BigInteger, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class ScanHistory(Base):
    __tablename__ = "scan_history"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    target: Mapped[str] = mapped_column(String(512), nullable=False)
    scan_type: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    trust_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    risk_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    confidence_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="UPLOADED", nullable=False, index=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Storage & File Security Metadata
    file_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    file_size_bytes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    sha256_checksum: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Telemetry & AI Pipeline Readiness
    processing_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    queue_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    module_used: Mapped[str | None] = mapped_column(String(100), nullable=True)
    result_version: Mapped[str | None] = mapped_column(String(30), default="v1", nullable=True)

    scanned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    user: Mapped["User"] = relationship("User", backref="scans")
