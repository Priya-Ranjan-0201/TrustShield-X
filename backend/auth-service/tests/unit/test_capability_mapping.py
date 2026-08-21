"""Unit tests for Semantic Capability Taxonomy Mapping (Phase 3.7 Part 1A.16)."""

import pytest
from app.services.api_intelligence_service import APIIntelligenceService
from app.schemas.api_intelligence_models import APICapabilityEnum


def test_capability_mapping():
    service = APIIntelligenceService()

    assert service.classify_capability("javax.crypto.Cipher.getInstance") == APICapabilityEnum.CRYPTO
    assert service.classify_capability("android.location.LocationManager.getLastKnownLocation") == APICapabilityEnum.LOCATION
    assert service.classify_capability("android.hardware.Camera.open") == APICapabilityEnum.CAMERA
    assert service.classify_capability("android.telephony.SmsManager.sendTextMessage") == APICapabilityEnum.SMS
    assert service.classify_capability("java.lang.reflect.Method.invoke") == APICapabilityEnum.REFLECTION
    assert service.classify_capability("dalvik.system.DexClassLoader") == APICapabilityEnum.DYNAMIC_LOADING
    assert service.classify_capability("android.webkit.WebView.loadUrl") == APICapabilityEnum.WEBVIEW
