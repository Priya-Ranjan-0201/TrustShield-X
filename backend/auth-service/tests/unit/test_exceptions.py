"""Unit tests for Scoped Rule Exception Auditing (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import RuleExceptionDTO


def test_rule_exception_dto():
    exc = RuleExceptionDTO(
        exception_id="exc_1",
        rule_id="RULE-NETWORK-003",
        scope="com.bank.sdk",
    )

    assert exc.scope == "com.bank.sdk"
