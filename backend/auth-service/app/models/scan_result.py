import uuid
from datetime import datetime, timezone
from sqlalchemy import Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class ScanResult(Base):
    __tablename__ = "scan_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True
    )
    module_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("scan_modules.id", ondelete="SET NULL"), nullable=True, index=True
    )
    trust_score: Mapped[int] = mapped_column(Integer, nullable=False)
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    findings_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    execution_time_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    scan: Mapped["ScanHistory"] = relationship("ScanHistory", backref="results")
    module: Mapped["ScanModule"] = relationship("ScanModule", backref="results")
