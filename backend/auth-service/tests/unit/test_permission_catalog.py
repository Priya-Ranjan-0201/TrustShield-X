"""Unit tests for Android Permission Catalog Knowledge Base (Phase 3.7 Part 1A.8)."""

import pytest
from app.services.permission_catalog import lookup_permission, ANDROID_PERMISSION_CATALOG


def test_lookup_official_camera_permission():
    meta = lookup_permission("android.permission.CAMERA")
    assert meta["is_known"] is True
    assert meta["category"] == "Camera"
    assert meta["protection_level"] == "DANGEROUS"
    assert meta["is_runtime"] is True


def test_lookup_google_system_permission():
    meta = lookup_permission("com.google.android.providers.gsf.permission.READ_GSERVICES")
    assert meta["is_known"] is False
    assert meta["protection_level"] == "SIGNATURE"


def test_lookup_custom_vendor_permission():
    meta = lookup_permission("com.example.app.permission.CUSTOM_PERM")
    assert meta["is_known"] is False
    assert meta["category"] == "Custom"
    assert meta["protection_level"] == "CUSTOM"


def test_lookup_unknown_permission():
    meta = lookup_permission("invalid_permission_format")
    assert meta["is_known"] is False
    assert meta["category"] == "Unknown"
    assert meta["protection_level"] == "UNKNOWN"
