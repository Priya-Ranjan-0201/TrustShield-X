"""Unit tests for Intent Dataflow (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import IntentDataflowDTO


def test_intent_dataflow_dto():
    intent_df = IntentDataflowDTO(
        source_component="com.bank.LoginActivity",
        target_component="com.bank.MainActivity",
        extra_key="user_token",
        extra_type="STRING",
    )

    assert intent_df.source_component == "com.bank.LoginActivity"
    assert intent_df.extra_key == "user_token"
