import pytest
from app.services.threat_intelligence.intelligence_source_manager import IntelligenceSourceManager


def test_taxii_security_source_trust():
    mgr = IntelligenceSourceManager()
    taxii_src = mgr.get_source("src_cisa_ais")

    assert taxii_src is not None
    assert taxii_src.format == "TAXII2"
    assert taxii_src.trust_level >= 0.90
