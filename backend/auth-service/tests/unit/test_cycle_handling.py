"""Unit tests for Cycle Handling (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorChainDTO


def test_cycle_handling_dto():
    chain = BehaviorChainDTO(
        chain_id="ch_cycle",
        chain_type="NETWORK_STORAGE_CYCLE",
        nodes=["Network", "Cache", "Network"],
        edges=["STORES", "LOADS"],
        start_node="Network",
        end_node="Network",
    )

    assert len(chain.nodes) == 3
