"""Unit tests for Android Component Knowledge Base Catalog (Phase 3.7 Part 1A.9)."""

import pytest
from app.services.component_catalog import lookup_component_type, ANDROID_COMPONENT_CATALOG


def test_lookup_activity_component_type():
    meta = lookup_component_type("ACTIVITY")
    assert meta["is_known"] is True
    assert meta["type_name"] == "Activity"
    assert meta["supports_intent_filters"] is True


def test_lookup_service_component_type():
    meta = lookup_component_type("SERVICE")
    assert meta["is_known"] is True
    assert meta["type_name"] == "Service"
    assert meta["supports_foreground_mode"] is True


def test_lookup_unknown_component_type():
    meta = lookup_component_type("CUSTOM_TYPE")
    assert meta["is_known"] is False
    assert meta["type_name"] == "CUSTOM_TYPE"
