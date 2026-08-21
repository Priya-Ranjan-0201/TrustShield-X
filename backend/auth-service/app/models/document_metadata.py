import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class DocumentMetadata(Base):
    __tablename__ = "document_metadata"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True
    )
    document_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    extracted_fields: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    ocr_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    image_quality_metrics: Mapped[dict | None] = mapped_column(JSON, nullable=True, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    scan: Mapped["ScanHistory"] = relationship("ScanHistory", backref="document_metadata")
