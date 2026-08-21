"""Unit tests for Framework & Library Fingerprinting (Phase 3.7 Part 1A.16)."""

import pytest
from app.services.api_intelligence_service import APIIntelligenceService


def test_framework_detection():
    service = APIIntelligenceService()

    apis = [
        "com.google.firebase.auth.FirebaseAuth.getInstance",
        "io.flutter.embedding.engine.FlutterEngine",
        "okhttp3.OkHttpClient.newCall",
    ]
    packages = ["com.google.firebase", "io.flutter"]

    frameworks = service.detect_frameworks(apis, packages)
    names = [f.framework_name for f in frameworks]

    assert "Firebase" in names
    assert "Flutter" in names
    assert "OkHttp" in names
