"""Unit tests for Canonical API Signature Normalization (Phase 3.7 Part 1A.16)."""

import pytest
from app.services.api_intelligence_service import APIIntelligenceService


def test_api_signature_normalization():
    service = APIIntelligenceService()

    cid, pkg, cls, method = service.normalize_signature("Landroid/net/ConnectivityManager;->getActiveNetworkInfo()Landroid/net/NetworkInfo;")
    assert cid == "android.net.ConnectivityManager.getActiveNetworkInfo"
    assert pkg == "android.net"
    assert cls == "ConnectivityManager"
    assert method == "getActiveNetworkInfo"
