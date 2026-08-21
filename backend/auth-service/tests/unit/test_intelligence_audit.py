import pytest
import hashlib

def test_intelligence_audit_hashing():
    entry = {"action": "INGEST_FEED", "source_id": "src_global_exchange"}
    h = hashlib.sha256(str(entry).encode()).hexdigest()
    assert len(h) == 64
