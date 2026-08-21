"""Unit tests for WebView Security Behavior Rules (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import BehaviorRuleEvaluationDTO


def test_webview_rule_eval_dto():
    eval_dto = BehaviorRuleEvaluationDTO(
        evaluation_id="eval_web1",
        rule_id="RULE-WEBVIEW-001",
        rule_version="1.0.0",
        namespace="WEBVIEW",
        state="MATCHED",
        confidence="HIGH",
        evidence_provenance="WebView Remote Content Loading",
    )

    assert eval_dto.namespace == "WEBVIEW"
