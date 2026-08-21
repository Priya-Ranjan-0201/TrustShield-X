"""Unit Tests — Lineage & Provenance Tracking (Phase 4.0 Part 2)."""

import pytest
from types import SimpleNamespace
from app.services.trust_narrative_engine import TrustNarrativeEngine


class TestNarrativeLineage:
    """Mandatory Test Case 18: Every statement has lineage to source data."""

    def setup_method(self):
        self.engine = TrustNarrativeEngine()

    def test_lineage_for_dataflow(self):
        risk_dto = SimpleNamespace(risk_score=50.0, risk_band="MODERATE_RISK", confidence_level="HIGH", evidence_sufficiency="SUFFICIENT", primary_risk_category="DATA_LEAK")
        dataflow = [SimpleNamespace(path_id="p1", source="contacts", sink="api.example.com", resolution_status="RESOLVED")]
        doc = self.engine.build_narrative("r1", "a1", risk_assessment_dto=risk_dto, dataflow_paths=dataflow)
        assert len(doc.lineage) >= 1
        assert doc.lineage[0].report_id == "r1"
        assert doc.lineage[0].source_type == "DATAFLOW_PATH"

    def test_lineage_for_threat_intel(self):
        risk_dto = SimpleNamespace(risk_score=80.0, risk_band="HIGH_RISK", confidence_level="HIGH", evidence_sufficiency="SUFFICIENT", primary_risk_category="MALWARE")
        threats = [SimpleNamespace(indicator="domain", freshness="CURRENT")]
        doc = self.engine.build_narrative("r2", "a2", risk_assessment_dto=risk_dto, threat_matches=threats)
        ti_lineage = [l for l in doc.lineage if l.source_type == "THREAT_MATCH"]
        assert len(ti_lineage) >= 1

    def test_lineage_all_statements_have_entries(self):
        risk_dto = SimpleNamespace(risk_score=50.0, risk_band="MODERATE_RISK", confidence_level="HIGH", evidence_sufficiency="SUFFICIENT", primary_risk_category="NETWORK_THREAT")
        mitigations = ["CertPin"]
        doc = self.engine.build_narrative("r3", "a3", risk_assessment_dto=risk_dto, mitigations=mitigations)
        stmt_ids = {s.statement_id for s in doc.statements}
        lineage_ids = {l.statement_id for l in doc.lineage}
        assert stmt_ids == lineage_ids
