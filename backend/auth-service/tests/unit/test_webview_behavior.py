"""Unit tests for WebView Behavior Correlation (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorFindingDTO


def test_webview_behavior_dto():
    f = BehaviorFindingDTO(
        finding_id="web_1",
        finding_type="WEBVIEW_JS_BRIDGE",
        category="REMOTE_CONFIGURATION",
        evidence_strength="STRONG",
        summary="addJavascriptInterface detected",
    )

    assert f.finding_type == "WEBVIEW_JS_BRIDGE"
