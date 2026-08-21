"""Unit tests for Rule Versioning (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import BehaviorRuleVersionDTO


def test_rule_version_dto():
    ver = BehaviorRuleVersionDTO(
        rule_id="RULE-DATAFLOW-001",
        rule_version="1.1.0",
        author="TruthShield Core Team",
    )

    assert ver.rule_version == "1.1.0"
