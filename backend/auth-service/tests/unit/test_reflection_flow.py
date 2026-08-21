"""Unit tests for Reflection Dataflow (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import ReflectionDataflowDTO


def test_reflection_flow_dto():
    r = ReflectionDataflowDTO(
        caller_method="com.bank.Dynamic.load",
        reflection_target="com.bank.hidden.SecretMethod",
        resolution_status="RESOLVED",
    )

    assert r.reflection_target == "com.bank.hidden.SecretMethod"
