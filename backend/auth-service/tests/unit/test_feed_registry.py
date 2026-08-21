import pytest
from app.services.federation.source_reputation_engine import SourceReputationEngine


def test_feed_registry_list():
    engine = SourceReputationEngine()
    sources = engine.list_sources()
    assert len(sources) >= 2
    assert any(s.source_type == "STIX_TAXII" for s in sources)
    assert any(s.source_type == "INTERNAL" for s in sources)
