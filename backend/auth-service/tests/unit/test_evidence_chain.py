import pytest
from app.services.governance_fabric.evidence_chain_engine import EvidenceChainEngine


def test_evidence_chain_assembly():
    engine = EvidenceChainEngine()

    chain = engine.build_chain(
        requirement_id="req_soc2_cc6_1",
        control_id="ctrl_iso_01",
        assertion="ast_iso_01",
        test_execution_id="tst_exec_99",
        evidence_id="evi_iso_01",
    )

    assert chain.chain_id.startswith("chn_")
    assert chain.is_valid is True
    assert len(chain.chain_hash) == 64
