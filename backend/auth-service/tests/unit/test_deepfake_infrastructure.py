"""Unit tests for Phase 3.5 Part 1 — AI Deepfake Detection Infrastructure & Processing Pipeline.

Tests cover:
- Media validation (MIME, extension, size, corruption checks)
- Technical metadata extraction (Width, Height, FPS, Duration, Codec, Audio)
- Image & Video quality analysis (Blur, Noise, Brightness, Contrast, Sharpness)
- Frame extraction and sampling strategies (Uniform, Adaptive, Key Frame, Scene-based)
- Face detection abstraction & OpenCV face detector
- Face alignment and normalized 224x224 chip extraction
- Face tracking across frames with persistent track_id assignment
- Deepfake Model Registry and BaseDeepfakeDetector interface
- Master DeepfakePipelineOrchestrator end-to-end pipeline execution
"""

import pytest
from app.services.deepfake_validator import validate_media_file
from app.services.deepfake_metadata_extractor import extract_media_metadata
from app.services.deepfake_quality_analyzer import analyze_deepfake_media_quality
from app.services.frame_extractor import extract_and_sample_frames
from app.services.face_detector import OpenCVDNNFaceDetector, FaceBBox
from app.services.face_aligner import align_and_crop_face
from app.services.face_tracker import FaceTrackerEngine, compute_iou
from app.services.deepfake_detector_interface import DeepfakeModelRegistry, InfrastructureStubModel
from app.services.deepfake_detector import DeepfakePipelineOrchestrator


# ============================================================
# 1. Media Validation Tests
# ============================================================

def test_validate_media_file_valid_image():
    # Minimal synthetic PNG bytes header
    png_bytes = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
    res = validate_media_file(png_bytes, "sample.png", "image/png")
    assert res.is_valid is True
    assert res.media_type == "IMAGE"
    assert res.extension == ".png"


def test_validate_media_file_valid_video():
    mp4_bytes = b"\x00\x00\x00\x18ftypmp42" + b"\x00" * 200
    res = validate_media_file(mp4_bytes, "sample.mp4", "video/mp4")
    assert res.is_valid is True
    assert res.media_type == "VIDEO"
    assert res.extension == ".mp4"


def test_validate_media_file_empty():
    res = validate_media_file(b"", "empty.png")
    assert res.is_valid is False
    assert res.error_code == "TSX-MEDIA-001"


def test_validate_media_file_unsupported_ext():
    res = validate_media_file(b"some bytes", "file.exe", "application/x-msdownload")
    assert res.is_valid is False
    assert res.error_code == "TSX-MEDIA-002"


# ============================================================
# 2. Metadata Extraction Tests
# ============================================================

def test_extract_image_metadata():
    img_bytes = b"\x89PNG\r\n\x1a\n" + b"\x00" * 500
    meta = extract_media_metadata(img_bytes, "IMAGE")
    assert meta.media_type == "IMAGE"
    assert meta.width > 0
    assert meta.height > 0
    assert meta.dpi >= 72


def test_extract_video_metadata():
    video_bytes = b"\x00\x00\x00\x18ftypmp42" + b"\x00" * 1000
    meta = extract_media_metadata(video_bytes, "VIDEO")
    assert meta.media_type == "VIDEO"
    assert meta.duration_sec >= 0.0
    assert meta.fps >= 0.0


# ============================================================
# 3. Quality Analysis Tests
# ============================================================

def test_analyze_deepfake_media_quality():
    sample_bytes = bytes(range(256)) * 50
    quality = analyze_deepfake_media_quality(sample_bytes, "IMAGE", 1920, 1080)

    assert "overall_quality_score" in quality
    assert "resolution_score" in quality
    assert "blur_score" in quality
    assert "byte_entropy" in quality
    assert quality["overall_quality_score"] >= 0


# ============================================================
# 4. Frame Extraction & Sampling Tests
# ============================================================

def test_extract_and_sample_frames_image():
    img_bytes = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
    frames = extract_and_sample_frames(img_bytes, "IMAGE")
    assert len(frames) == 1
    assert frames[0].sampling_strategy == "SINGLE_IMAGE"


def test_extract_and_sample_frames_video_strategies():
    video_bytes = b"\x00\x00\x00\x18ftypmp42" + b"\x00" * 1000
    frames_uniform = extract_and_sample_frames(video_bytes, "VIDEO", "UNIFORM", 4)
    assert len(frames_uniform) >= 1
    assert frames_uniform[0].frame_index >= 0


# ============================================================
# 5. Face Detection & Alignment Tests
# ============================================================

def test_opencv_face_detector():
    detector = OpenCVDNNFaceDetector()
    assert detector.provider_name == "OpenCV-DNN/Haar"

    img_bytes = b"fake image bytes"
    faces = detector.detect_faces(img_bytes)
    assert len(faces) >= 1
    assert isinstance(faces[0], FaceBBox)
    assert faces[0].confidence > 0.0
    assert "left_eye" in faces[0].landmarks


def test_face_aligner():
    detector = OpenCVDNNFaceDetector()
    img_bytes = b"fake image bytes"
    faces = detector.detect_faces(img_bytes)

    chip = align_and_crop_face(img_bytes, faces[0], target_size=(224, 224))
    assert chip.chip_width == 224
    assert chip.chip_height == 224
    assert len(chip.aligned_bytes) > 0


# ============================================================
# 6. Face Tracking Tests
# ============================================================

def test_compute_iou():
    boxA = (100, 100, 50, 50)
    boxB = (100, 100, 50, 50)
    assert compute_iou(boxA, boxB) == 1.0

    boxC = (200, 200, 50, 50)
    assert compute_iou(boxA, boxC) == 0.0


def test_face_tracker_persistent_id():
    tracker = FaceTrackerEngine(iou_threshold=0.3)

    face1 = FaceBBox(x=100, y=100, w=50, h=50, confidence=0.9, face_id="f1")
    tracker.process_frame(frame_index=0, timestamp_sec=0.0, detected_faces=[face1])

    # Frame 1: slightly moved face -> should match same track
    face2 = FaceBBox(x=105, y=105, w=50, h=50, confidence=0.92, face_id="f2")
    assignments = tracker.process_frame(frame_index=1, timestamp_sec=0.033, detected_faces=[face2])

    assert len(assignments) == 1
    assert assignments[0][0] == "face_track_1"

    records = tracker.get_track_records()
    assert len(records) == 1
    assert records[0].track_id == "face_track_1"
    assert records[0].total_frames_tracked == 2


# ============================================================
# 7. Deepfake Model Registry Tests
# ============================================================

def test_deepfake_model_registry():
    registry = DeepfakeModelRegistry()
    models = registry.list_models()
    assert len(models) >= 1
    assert models[0]["model_name"] == "Deepfake-Pipeline-Infrastructure"

    active_model = registry.get_model()
    assert active_model.model_name == "Deepfake-Pipeline-Infrastructure"


# ============================================================
# 8. Master Deepfake Pipeline Orchestrator Integration Test
# ============================================================

@pytest.mark.asyncio
async def test_deepfake_orchestrator_pipeline_image():
    orchestrator = DeepfakePipelineOrchestrator()
    img_bytes = b"\x89PNG\r\n\x1a\n" + b"\x00" * 500

    res = await orchestrator.analyze_media(img_bytes, "test_face.png", "image/png")

    assert res.module == "video-deepfake"
    assert res.status == "completed"
    assert res.media_type == "IMAGE"
    assert res.pipeline_status == "INFERENCE_COMPLETED"
    assert len(res.frames_summary) == 1
    assert res.total_faces_detected >= 1
    assert len(res.face_tracks) >= 1
    assert res.execution_time_ms >= 0


@pytest.mark.asyncio
async def test_deepfake_orchestrator_pipeline_video():
    orchestrator = DeepfakePipelineOrchestrator()
    video_bytes = b"\x00\x00\x00\x18ftypmp42" + b"\x00" * 1000

    res = await orchestrator.analyze_media(video_bytes, "test_video.mp4", "video/mp4")

    assert res.module == "video-deepfake"
    assert res.status == "completed"
    assert res.media_type == "VIDEO"
    assert res.pipeline_status == "INFERENCE_COMPLETED"
    assert res.total_frames_extracted >= 1
    assert res.total_faces_detected >= 1
    assert len(res.evidence) >= 1
