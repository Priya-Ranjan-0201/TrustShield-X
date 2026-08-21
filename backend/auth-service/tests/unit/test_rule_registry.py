"""Unit tests for Rule Registry (Phase 3.9 Part 1A.24)."""

import pytest
from app.services.rule_registry import RuleRegistry


def test_rule_registry_list_active():
    registry = RuleRegistry()
    active_rules = registry.list_active_rules()

    assert len(active_rules) >= 2
    assert active_rules[0].status == "ACTIVE"
