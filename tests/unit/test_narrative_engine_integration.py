"""Unit Tests — Trust Narrative Engine Integration (Phase 4.0 Part 2)."""

import pytest
from types import SimpleNamespace
from app.services.trust_narrative_engine import TrustNarrativeEngine


class TestTrustNarrativeEngineIntegration:
    """Mandatory Test Case 16: Full engine builds complete NarrativeDocument."""

    def setup_method(self):
        self.engine = TrustNarrativeEngine()

    def test_build_minimal_narrative(self):
        risk_dto = SimpleNamespace(risk_score=25.0, risk_band="LOW_RISK", confidence_level="HIGH", evidence_sufficiency="SUFFICIENT", primary_risk_category="NETWORK_THREAT")
        doc = self.engine.build_narrative("r1", "a1", risk_assessment_dto=risk_dto)
        assert doc.narrative_id == "narr_r1"
        assert doc.report_id == "r1"
        assert "Low Risk" in doc.executive_summary.headline
        assert "25.0" in doc.risk_narrative.risk_statement

    def test_build_with_findings(self):
        risk_dto = SimpleNamespace(risk_score=75.0, risk_band="HIGH_RISK", confidence_level="HIGH", evidence_sufficiency="SUFFICIENT", primary_risk_category="DATA_LEAK")
        findings = [SimpleNamespace(finding_id="f1", title="Domain Leak", description="Data leak", confidence_level="HIGH", finding_category="NETWORK")]
        doc = self.engine.build_narrative("r2", "a2", risk_assessment_dto=risk_dto, findings=findings)
        assert len(doc.finding_narratives) == 1
        assert doc.finding_narratives[0].finding_id == "f1"

    def test_build_with_all_generators(self):
        risk_dto = SimpleNamespace(risk_score=90.0, risk_band="CRITICAL_RISK", confidence_level="HIGH", evidence_sufficiency="SUFFICIENT", primary_risk_category="MALWARE")
        findings = [SimpleNamespace(finding_id="f1", title="Malware", description="Malware detected", confidence_level="HIGH", finding_category="MALWARE")]
        evidence = [SimpleNamespace(evidence_id="e1", observation="Binary", evidence_strength="STRONG", source="DEXEngine")]
        dataflow = [SimpleNamespace(path_id="p1", source="contacts", sink="api.evil.com", resolution_status="RESOLVED")]
        behavior = [SimpleNamespace(nodes=["READ_SMS", "SEND"])]
        threats = [SimpleNamespace(indicator="domain", freshness="CURRENT")]
        contradictions = [SimpleNamespace(evidence_a="A", evidence_b="B")]
        mitigations = ["Certificate Pinning"]
        doc = self.engine.build_narrative(
            "r3", "a3", risk_assessment_dto=risk_dto, findings=findings, evidence=evidence,
            dataflow_paths=dataflow, behavior_chains=behavior, threat_matches=threats,
            contradictions=contradictions, mitigations=mitigations,
        )
        assert len(doc.finding_narratives) == 1
        assert len(doc.evidence_narratives) == 1
        assert len(doc.contradiction_narratives) == 1
        assert len(doc.statements) > 0
        assert len(doc.lineage) > 0

    def test_deterministic_mode(self):
        risk_dto = SimpleNamespace(risk_score=25.0, risk_band="LOW_RISK", confidence_level="HIGH", evidence_sufficiency="SUFFICIENT", primary_risk_category="NETWORK_THREAT")
        doc = self.engine.build_narrative("r1", "a1", risk_assessment_dto=risk_dto)
        assert doc.mode == "DETERMINISTIC_MODE"

    def test_schema_version(self):
        risk_dto = SimpleNamespace(risk_score=25.0, risk_band="LOW_RISK", confidence_level="HIGH", evidence_sufficiency="SUFFICIENT", primary_risk_category="NETWORK_THREAT")
        doc = self.engine.build_narrative("r1", "a1", risk_assessment_dto=risk_dto)
        assert doc.schema_version == "4.0.0"
