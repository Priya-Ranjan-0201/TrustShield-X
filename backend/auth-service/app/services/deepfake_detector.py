"""Master Deepfake Detection Pipeline Orchestrator for Phase 3.5 Part 2A.

Orchestrates complete deepfake preprocessing, vision, and neural inference pipeline:
1. Media Validation (MIME, size, corruption, resolution, codec)
2. Technical Metadata Extraction (Width, Height, FPS, Duration, Codec, Audio, EXIF)
3. Image/Video Quality Analysis (Blur, Noise, Brightness, Contrast, Sharpness, Quality Score)
4. Intelligent Frame Extraction & Sampling (Uniform, Adaptive, Key Frame, Scene-based)
5. Face Detection (OpenCV DNN / Pluggable BaseFaceDetector)
6. Face Alignment (Landmark rotation correction & 224x224 chip extraction)
7. Face Tracking across video frames (IoU identity tracking & track_id assignment)
8. Deepfake Model Selection & Device Auto-Detection (CPU/GPU)
9. Neural Mini-Batch Inference (EfficientNet-B0 / MesoNet / Xception / Swin / ViT / CLIP)
10. Temporal & Multi-Face Aggregation (AVERAGE, WEIGHTED_AVERAGE, MEDIAN, CONFIDENCE_WEIGHTED)
11. Confidence Calibration & False Positive Protection (LOW_CONFIDENCE)
12. Explainability & Evidence Generation

Returns structured explainable result with real fake_probability, calibrated_confidence, and evidence.
"""

import time
from typing import Dict, Any, List, Optional

from app.services.deepfake_validator import validate_media_file
from app.services.deepfake_metadata_extractor import extract_media_metadata
from app.services.deepfake_quality_analyzer import analyze_deepfake_media_quality
from app.services.frame_extractor import extract_and_sample_frames
from app.services.face_detector import OpenCVDNNFaceDetector
from app.services.face_aligner import align_and_crop_face
from app.services.face_tracker import FaceTrackerEngine
from app.services.deepfake_model_registry import DeepfakeModelRegistryExtended
from app.services.deepfake_aggregator import aggregate_multi_face_predictions
from app.services.deepfake_calibrator import calibrate_deepfake_confidence
from app.services.deepfake_explainability import (
    generate_deepfake_explainability,
    generate_deepfake_evidence_cards,
)


class DeepfakePipelineResult:
    def __init__(
        self,
        module: str,
        status: str,
        media_type: str,
        metadata: Dict[str, Any],
        quality_metrics: Dict[str, Any],
        frames_summary: List[Dict[str, Any]],
        total_frames_extracted: int,
        face_tracks: List[Dict[str, Any]],
        total_faces_detected: int,
        risk_score: int,
        confidence_score: float,
        fake_probability: float,
        severity: str,
        evidence: List[Dict[str, str]],
        recommendations: List[str],
        explainability: Dict[str, Any],
        pipeline_status: str,
        execution_time_ms: int,
        model_name: str = "EfficientNet-B0-Deepfake",
    ):
        self.module = module
        self.status = status
        self.media_type = media_type
        self.metadata = metadata
        self.quality_metrics = quality_metrics
        self.frames_summary = frames_summary
        self.total_frames_extracted = total_frames_extracted
        self.face_tracks = face_tracks
        self.total_faces_detected = total_faces_detected
        self.risk_score = risk_score
        self.confidence_score = confidence_score
        self.fake_probability = fake_probability
        self.severity = severity
        self.evidence = evidence
        self.recommendations = recommendations
        self.explainability = explainability
        self.pipeline_status = pipeline_status
        self.execution_time_ms = execution_time_ms
        self.model_name = model_name

    def to_dict(self) -> Dict[str, Any]:
        return {
            "module": self.module,
            "status": self.status,
            "media_type": self.media_type,
            "metadata": self.metadata,
            "quality_metrics": self.quality_metrics,
            "frames_summary": self.frames_summary,
            "total_frames_extracted": self.total_frames_extracted,
            "face_tracks": self.face_tracks,
            "total_faces_detected": self.total_faces_detected,
            "risk_score": self.risk_score,
            "confidence_score": round(self.confidence_score, 4),
            "fake_probability": round(self.fake_probability, 4),
            "severity": self.severity,
            "evidence": self.evidence,
            "recommendations": self.recommendations,
            "explainability": self.explainability,
            "pipeline_status": self.pipeline_status,
            "execution_time_ms": self.execution_time_ms,
            "model_name": self.model_name,
        }


class DeepfakePipelineOrchestrator:
    def __init__(self):
        self.face_detector = OpenCVDNNFaceDetector()
        self.model_registry = DeepfakeModelRegistryExtended()

    async def analyze_media(
        self,
        file_bytes: bytes,
        filename: str,
        content_type: Optional[str] = None,
        model_name: Optional[str] = None,
    ) -> DeepfakePipelineResult:
        start_time = time.time()

        evidence: List[Dict[str, str]] = []
        recommendations: List[str] = []

        # 1. Media Validation
        val_res = validate_media_file(file_bytes, filename, content_type)
        if not val_res.is_valid:
            execution_time_ms = int((time.time() - start_time) * 1000)
            return DeepfakePipelineResult(
                module="video-deepfake",
                status="failed",
                media_type="UNKNOWN",
                metadata={},
                quality_metrics={},
                frames_summary=[],
                total_frames_extracted=0,
                face_tracks=[],
                total_faces_detected=0,
                risk_score=100,
                confidence_score=0.0,
                fake_probability=1.0,
                severity="DANGEROUS",
                evidence=[{
                    "type": "MEDIA_VALIDATION",
                    "severity": "CRITICAL",
                    "title": f"Media Validation Failed ({val_res.error_code})",
                    "description": val_res.error_message or "Unsupported or corrupted media file.",
                }],
                recommendations=["Upload a valid MP4, MOV, AVI, WEBM video or PNG, JPG image under 25MB."],
                explainability={},
                pipeline_status="FAILED",
                execution_time_ms=execution_time_ms,
            )

        # 2. Technical Metadata Extraction
        meta_res = extract_media_metadata(file_bytes, val_res.media_type)
        meta_dict = meta_res.to_dict()

        # 3. Image & Video Quality Analysis
        quality_dict = analyze_deepfake_media_quality(
            file_bytes, val_res.media_type, meta_res.width, meta_res.height
        )

        # 4. Frame Extraction & Sampling
        extracted_frames = extract_and_sample_frames(
            file_bytes, val_res.media_type, sampling_strategy="ADAPTIVE", target_max_frames=16
        )

        # 5. Face Detection, Alignment, and Face Tracking across frames
        tracker = FaceTrackerEngine(iou_threshold=0.3)
        total_faces = 0
        face_chips_batch = []

        for frame in extracted_frames:
            detected_faces = self.face_detector.detect_faces(frame.image_bytes)
            frame.faces_detected_count = len(detected_faces)
            total_faces += len(detected_faces)

            for face in detected_faces:
                chip = align_and_crop_face(frame.image_bytes, face, target_size=(224, 224))
                face_chips_batch.append(chip.aligned_bytes)

            tracker.process_frame(frame.frame_index, frame.timestamp_sec, detected_faces)

        track_records = tracker.get_track_records()

        # 6. Model Selection & Neural Mini-Batch Inference
        active_adapter = self.model_registry.get_adapter(model_name)
        preprocessed_data = active_adapter.preprocess(face_chips_batch or [file_bytes[:5000]])
        inference_out = active_adapter.infer(preprocessed_data)

        # Update track entries with neural probabilities
        tracks_summary = []
        for tr in track_records:
            tr_dict = tr.to_dict()
            tr_dict["fake_probability"] = inference_out.fake_probability
            tr_dict["confidence"] = inference_out.confidence
            tracks_summary.append(tr_dict)

        frames_summary = [f.to_dict() for f in extracted_frames]

        # 7. Temporal & Multi-Face Aggregation Engine
        aggregated_res = aggregate_multi_face_predictions(
            tracks_summary, temporal_strategy="CONFIDENCE_WEIGHTED"
        )

        # 8. Confidence Calibration & False Positive Protection
        min_dim = min(meta_res.width, meta_res.height) if meta_res.width else 224
        verdict = calibrate_deepfake_confidence(
            fake_probability=aggregated_res.overall_fake_probability,
            model_confidence=aggregated_res.overall_confidence,
            quality_metrics=quality_dict,
            min_face_dimension=min_dim,
            frames_analyzed=len(extracted_frames),
        )

        # 9. Explainability & Evidence Generation
        explainability_dict = generate_deepfake_explainability(
            verdict=verdict,
            aggregated=aggregated_res,
            model_name=active_adapter.model_name,
            device_used=inference_out.device_used,
        )

        pipeline_evidence, pipeline_recs = generate_deepfake_evidence_cards(
            verdict=verdict,
            aggregated=aggregated_res,
            model_name=active_adapter.model_name,
        )
        evidence.extend(pipeline_evidence)
        recommendations.extend(pipeline_recs)

        execution_time_ms = int((time.time() - start_time) * 1000)

        return DeepfakePipelineResult(
            module="video-deepfake",
            status="completed",
            media_type=val_res.media_type,
            metadata=meta_dict,
            quality_metrics=quality_dict,
            frames_summary=frames_summary,
            total_frames_extracted=len(extracted_frames),
            face_tracks=tracks_summary,
            total_faces_detected=total_faces,
            risk_score=verdict.risk_score,
            confidence_score=verdict.calibrated_confidence,
            fake_probability=verdict.calibrated_fake_probability,
            severity=verdict.severity,
            evidence=evidence,
            recommendations=recommendations,
            explainability=explainability_dict,
            pipeline_status="INFERENCE_COMPLETED",
            execution_time_ms=execution_time_ms,
            model_name=active_adapter.model_name,
        )
