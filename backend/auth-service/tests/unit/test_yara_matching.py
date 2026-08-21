"""Unit tests for YARA Rule Matching (Phase 3.9 Part 1A.23)."""

import pytest
from app.schemas.threat_intelligence_models import YaraMatchDTO


def test_yara_match_dto():
    ym = YaraMatchDTO(
        rule_name="DEX_SUSPICIOUS_REFLECT",
        rule_namespace="android.malware",
        matched_file="classes.dex",
        offset=512,
    )

    assert ym.rule_name == "DEX_SUSPICIOUS_REFLECT"
    assert ym.offset == 512
