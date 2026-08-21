import pytest
from app.core.scan_lifecycle import ScanStatus, validate_status_transition
from app.services.scan_orchestrator import DefaultModuleRouter


def test_scan_lifecycle_valid_transitions():
    assert validate_status_transition(ScanStatus.UPLOADED, ScanStatus.VALIDATING)
    assert validate_status_transition(ScanStatus.VALIDATING, ScanStatus.QUEUED)
    assert validate_status_transition(ScanStatus.QUEUED, ScanStatus.PROCESSING)
    assert validate_status_transition(ScanStatus.PROCESSING, ScanStatus.COMPLETED)


def test_scan_lifecycle_invalid_transition():
    with pytest.raises(Exception) as exc_info:
        validate_status_transition(ScanStatus.COMPLETED, ScanStatus.PROCESSING)
    assert "Illegal scan status transition" in str(exc_info.value.detail)


def test_default_module_router():
    router = DefaultModuleRouter()
    assert router.resolve_target_module("URL") == "website-phishing-ai"
    assert router.resolve_target_module("IMAGE") == "qr-upi-vision-ai"
    assert router.resolve_target_module("PDF") == "document-ocr-ai"
    assert router.resolve_target_module("VIDEO") == "video-deepfake-ai"
    assert router.resolve_target_module("AUDIO") == "voice-clone-ai"
    assert router.resolve_target_module("APK") == "apk-malware-ai"
    assert router.resolve_target_module("TEXT") == "nlp-phishing-ai"
