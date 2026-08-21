import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, Boolean, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class AudioMetadata(Base):
    __tablename__ = "audio_metadata"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True
    )
    duration_sec: Mapped[float | None] = mapped_column(Float, nullable=True)
    sample_rate: Mapped[int | None] = mapped_column(Integer, nullable=True)
    channels: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bit_depth: Mapped[int | None] = mapped_column(Integer, nullable=True)
    codec: Mapped[str | None] = mapped_column(String(50), nullable=True)
    bitrate: Mapped[int | None] = mapped_column(Integer, nullable=True)
    loudness_lufs: Mapped[float | None] = mapped_column(Float, nullable=True)
    quality_metrics: Mapped[dict | None] = mapped_column(JSON, nullable=True, default=dict)

    # Production Inference & Version Tracking Columns
    clone_probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    real_probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    calibrated_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    prediction: Mapped[str | None] = mapped_column(String(50), nullable=True)
    prediction_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    model_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    model_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    inference_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    embedding_dimension: Mapped[int | None] = mapped_column(Integer, nullable=True)
    embedding_model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    device_used: Mapped[str | None] = mapped_column(String(50), nullable=True)
    explanation_available: Mapped[bool | None] = mapped_column(Boolean, default=True, nullable=True)
    evidence_available: Mapped[bool | None] = mapped_column(Boolean, default=True, nullable=True)
    recommendation_available: Mapped[bool | None] = mapped_column(Boolean, default=True, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    scan: Mapped["ScanHistory"] = relationship("ScanHistory", backref="audio_metadata")


class SpeechSegment(Base):
    __tablename__ = "speech_segments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True
    )
    segment_index: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time_sec: Mapped[float] = mapped_column(Float, nullable=False)
    end_time_sec: Mapped[float] = mapped_column(Float, nullable=False)
    duration_sec: Mapped[float] = mapped_column(Float, nullable=False)
    speaker_id: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    is_speech: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    scan: Mapped["ScanHistory"] = relationship("ScanHistory", backref="speech_segments")


class SpeakerTrack(Base):
    __tablename__ = "speaker_tracks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True
    )
    speaker_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    total_speaking_duration: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    segment_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    timeline_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    scan: Mapped["ScanHistory"] = relationship("ScanHistory", backref="speaker_tracks")
