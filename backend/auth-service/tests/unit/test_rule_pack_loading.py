"""Unit tests for Rule Pack Loading (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import BehaviorRulePackDTO


def test_rule_pack_dto():
    pack = BehaviorRulePackDTO(
        pack_id="pack_v1",
        pack_version="1.0.0",
        rules_count=10,
        checksum="sha256_mock_checksum",
    )

    assert pack.pack_id == "pack_v1"
    assert pack.rules_count == 10
