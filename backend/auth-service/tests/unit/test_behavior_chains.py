"""Unit tests for Multi-Stage Behavior Chains (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorChainDTO


def test_behavior_chain_dto():
    chain = BehaviorChainDTO(
        chain_id="ch_1",
        chain_type="SMS_TO_NETWORK",
        nodes=["READ_SMS", "SmsManager.receive", "DataflowPath", "OkHttpClient.post"],
        edges=["USES_PERMISSION", "CARRIES_DATA", "SENDS"],
        start_node="READ_SMS",
        end_node="OkHttpClient.post",
    )

    assert chain.chain_id == "ch_1"
    assert len(chain.nodes) == 4
