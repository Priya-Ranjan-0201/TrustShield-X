import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class VoiceCloneResult(Base):
    __tablename__ = "voice_clone_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True
    )
    speaker_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    segment_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    clone_probability: Mapped[float] = mapped_column(Float, nullable=False)
    similarity_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    verdict: Mapped[str] = mapped_column(String(50), nullable=False)
    evidence_json: Mapped[list] = mapped_column(JSON, nullable=True, default=list)
    recommendation_json: Mapped[list] = mapped_column(JSON, nullable=True, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    scan: Mapped["ScanHistory"] = relationship("ScanHistory", backref="voice_clone_results")


class ConversationAnalysis(Base):
    __tablename__ = "conversation_analysis"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True
    )
    total_speakers: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    conversation_duration: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    conversation_quality: Mapped[int | None] = mapped_column(Integer, nullable=True)
    conversation_risk: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    conversation_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    dominant_speaker: Mapped[str | None] = mapped_column(String(50), nullable=True)
    summary_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    scan: Mapped["ScanHistory"] = relationship("ScanHistory", backref="conversation_analysis")
