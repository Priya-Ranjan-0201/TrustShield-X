"""Database Repository for Deepfake Detection Infrastructure & Production Integration.

Persists deepfake_metadata, media_frames, and face_tracks records.
"""

import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.deepfake_metadata import DeepfakeMetadata, MediaFrame, FaceTrack


class DeepfakeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_deepfake_record(
        self,
        scan_id: uuid.UUID,
        media_type: str,
        metadata_dict: Dict[str, Any],
        quality_metrics: Dict[str, Any],
        frames_list: List[Dict[str, Any]],
        face_tracks_list: List[Dict[str, Any]],
        inference_results: Optional[Dict[str, Any]] = None,
    ) -> DeepfakeMetadata:
        """Saves deepfake_metadata, media_frames, and face_tracks records with neural inference details."""

        inf = inference_results or {}

        # Calculate manipulated frame statistics
        manipulated_frames = [f for f in frames_list if f.get("fake_probability", 0.0) >= 0.50]
        manipulated_count = len(manipulated_frames)

        highest_risk_frame_idx = 0
        if frames_list:
            highest_risk_frame = max(frames_list, key=lambda f: f.get("fake_probability", 0.0))
            highest_risk_frame_idx = highest_risk_frame.get("frame_index", 0)

        avg_frame_score = 0.0
        if frames_list:
            scores = [f.get("fake_probability", 0.0) for f in frames_list]
            avg_frame_score = sum(scores) / len(scores)

        # 1. DeepfakeMetadata
        meta = DeepfakeMetadata(
            scan_id=scan_id,
            media_type=media_type,
            duration_sec=metadata_dict.get("duration_sec"),
            fps=metadata_dict.get("fps"),
            width=metadata_dict.get("width"),
            height=metadata_dict.get("height"),
            codec=metadata_dict.get("codec"),
            has_audio=metadata_dict.get("has_audio", False),
            quality_metrics=quality_metrics,
            exif_metadata=metadata_dict.get("exif_metadata", {}),
            # Neural Inference & Telemetry Columns
            fake_probability=inf.get("fake_probability", 0.0),
            real_probability=inf.get("real_probability", 1.0),
            confidence=inf.get("confidence", 0.90),
            inference_time_ms=inf.get("execution_time_ms", 0),
            model_name=inf.get("model_name", "EfficientNet-B0-Deepfake"),
            model_version=inf.get("model_version", "2.0-Production"),
            processing_device=inf.get("explainability", {}).get("device_used", "cpu"),
            total_frame_count=len(frames_list),
            manipulated_frame_count=manipulated_count,
            highest_risk_frame=highest_risk_frame_idx,
            average_frame_score=avg_frame_score,
            explanation_available=True,
            heatmap_available=inf.get("explainability", {}).get("heatmap_available", True),
        )
        self.session.add(meta)

        # 2. MediaFrames (with frame-level prediction persistence)
        for frame in frames_list:
            mf = MediaFrame(
                scan_id=scan_id,
                frame_index=frame.get("frame_index", 0),
                timestamp_sec=frame.get("timestamp_sec", 0.0),
                width=frame.get("width"),
                height=frame.get("height"),
                sampling_strategy=frame.get("sampling_strategy"),
                quality_score=frame.get("quality_score"),
                faces_detected_count=frame.get("faces_detected_count", 0),
                prediction=frame.get("fake_probability", 0.0),
                confidence=inf.get("confidence", 0.90),
                risk_score=int(frame.get("fake_probability", 0.0) * 100),
                face_track_id=face_tracks_list[0].get("track_id") if face_tracks_list else "face_track_0",
                processing_time_ms=frame.get("processing_time_ms", 5),
                explanation_ref={"status": "analyzed"},
            )
            self.session.add(mf)

        # 3. FaceTracks
        for track in face_tracks_list:
            ft = FaceTrack(
                scan_id=scan_id,
                track_id=track.get("track_id", "face_track_0"),
                total_frames_tracked=track.get("total_frames_tracked", 0),
                avg_confidence=track.get("avg_confidence"),
                bounding_boxes_json=track.get("frame_entries", []),
            )
            self.session.add(ft)

        await self.session.commit()
        return meta

    async def get_by_scan_id(self, scan_id: uuid.UUID) -> Optional[DeepfakeMetadata]:
        stmt = select(DeepfakeMetadata).where(DeepfakeMetadata.scan_id == scan_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
