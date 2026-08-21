import pytest
from app.services.global_intelligence.provenance_chain_engine import ProvenanceChainEngine

def test_intelligence_evidence_tamper_detection():
    engine = ProvenanceChainEngine()
    chain = engine.attach_provenance([], "STAGE_1", "svc_1", {})
    chain = engine.attach_provenance(chain, "STAGE_2", "svc_2", {})
    
    # Tamper with chain
    chain[1]["prev_hash"] = "TAMPERED_HASH"
    assert engine.verify_provenance(chain) is False
