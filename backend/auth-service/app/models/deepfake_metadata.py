import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class DeepfakeMetadata(Base):
    __tablename__ = "deepfake_metadata"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True
    )
    media_type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)  # IMAGE, VIDEO
    duration_sec: Mapped[float | None] = mapped_column(Float, nullable=True)
    fps: Mapped[float | None] = mapped_column(Float, nullable=True)
    width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    codec: Mapped[str | None] = mapped_column(String(50), nullable=True)
    has_audio: Mapped[bool | None] = mapped_column(Boolean, default=False, nullable=True)
    quality_metrics: Mapped[dict | None] = mapped_column(JSON, nullable=True, default=dict)
    exif_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True, default=dict)

    # Production Inference & Telemetry columns
    fake_probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    real_probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    inference_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    model_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    model_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    processing_device: Mapped[str | None] = mapped_column(String(50), nullable=True)
    total_frame_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    manipulated_frame_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    highest_risk_frame: Mapped[int | None] = mapped_column(Integer, nullable=True)
    average_frame_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    explanation_available: Mapped[bool | None] = mapped_column(Boolean, default=True, nullable=True)
    heatmap_available: Mapped[bool | None] = mapped_column(Boolean, default=True, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    scan: Mapped["ScanHistory"] = relationship("ScanHistory", backref="deepfake_metadata")


class MediaFrame(Base):
    __tablename__ = "media_frames"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True
    )
    frame_index: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp_sec: Mapped[float] = mapped_column(Float, nullable=False)
    width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sampling_strategy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    quality_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    faces_detected_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Frame-level inference persistence
    prediction: Mapped[float | None] = mapped_column(Float, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    risk_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    face_track_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    processing_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    explanation_ref: Mapped[dict | None] = mapped_column(JSON, nullable=True, default=dict)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    scan: Mapped["ScanHistory"] = relationship("ScanHistory", backref="media_frames")


class FaceTrack(Base):
    __tablename__ = "face_tracks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True
    )
    track_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    total_frames_tracked: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    avg_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    bounding_boxes_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    scan: Mapped["ScanHistory"] = relationship("ScanHistory", backref="face_tracks")
