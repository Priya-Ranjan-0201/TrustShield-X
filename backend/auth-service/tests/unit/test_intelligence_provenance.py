import pytest
from app.services.global_intelligence.provenance_chain_engine import ProvenanceChainEngine

def test_intelligence_provenance_chaining():
    engine = ProvenanceChainEngine()
    chain = engine.attach_provenance([], "INGEST", "ingest_gateway", {"source": "feed_a"})
    chain = engine.attach_provenance(chain, "ENRICH", "enrichment_svc", {"vt_score": 92})
    assert len(chain) == 2
    assert engine.verify_provenance(chain) is True
