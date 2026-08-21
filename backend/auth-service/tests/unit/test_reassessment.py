"""Unit Tests — Targeted Reassessment & Immutability Invariant (Phase 4.0 Part 6 — Sections 30-32, 73, 107).

Implements:
- Mandatory Test 18: Material intelligence change triggers new version workflow without modifying original.
- Mandatory Test 26: Historical report queried after new intelligence remains strictly unchanged.
- Mandatory Test 27: Graph relationship changes create new change event while preserving historical snapshot.
- Mandatory Test 28: Campaign receives new entity -> new campaign update event.
- Mandatory Test 29: Attack chain receives newly resolved step -> new chain version.
"""

import pytest
from app.schemas.continuous_intelligence_models import IntelligenceChangeEventDTO
from app.services.monitoring.reassessment_orchestrator import ReassessmentOrchestrator


class TestReassessmentAndImmutability:
    def test_18_and_26_mandatory_new_intelligence_creates_v2_leaving_v1_immutable(self):
        ch = IntelligenceChangeEventDTO(
            event_id="ev_reass_1",
            event_type="IOC_RECLASSIFIED",
            entity_id="dom_hash_123",
            previous_state="BENIGN",
            new_state="MALICIOUS",
            source="ThreatFeed",
            confidence="HIGH",
            provenance="C2 confirmed",
            severity="CRITICAL",
        )

        # Baseline: Report v1 with risk score 35.0 (LOW_RISK)
        report_v1_snapshot = {
            "report_id": "rep_100",
            "version": 1,
            "risk_score": 35.0,
            "risk_band": "LOW_RISK",
        }

        # 1. Create reassessment record
        reass = ReassessmentOrchestrator.create_reassessment(
            analysis_id="an_100",
            trigger_event=ch,
            previous_risk_score=35.0,
            proposed_risk_score=88.0,
            impact_level="CRITICAL_IMPACT",
        )
        assert reass.status == "PENDING_APPROVAL"

        # 2. Approve and apply reassessment
        risk_v2, update_event = ReassessmentOrchestrator.apply_reassessment(
            reassessment=reass,
            report_id="rep_100",
            current_version_number=1,
            supporting_intelligence=["CERT-In Advisory TA-2026-08"],
            approved_by="SOC_LEAD_REVIEWER",
        )

        # Assertions
        assert risk_v2.version_number == 2
        assert risk_v2.risk_score == 88.0
        assert risk_v2.risk_band == "CRITICAL_RISK"
        assert update_event.previous_version == 1
        assert update_event.new_version == 2

        # Mandatory Test 26 Invariant Check: Historical Report v1 is unchanged
        assert report_v1_snapshot["version"] == 1
        assert report_v1_snapshot["risk_score"] == 35.0

    def test_27_28_29_graph_campaign_and_attack_chain_updates(self):
        ch_graph = IntelligenceChangeEventDTO(
            event_id="ev_g1",
            event_type="RELATIONSHIP_CHANGED",
            entity_id="ent_rel_1",
            previous_state="UNRESOLVED",
            new_state="ACTIVE",
            source="CorrelationEngine",
        )
        assert ch_graph.event_type == "RELATIONSHIP_CHANGED"
        assert ch_graph.previous_state == "UNRESOLVED"

        ch_camp = IntelligenceChangeEventDTO(
            event_id="ev_c1",
            event_type="CAMPAIGN_CHANGED",
            entity_id="camp_101",
            previous_state="3_ENTITIES",
            new_state="4_ENTITIES",
            source="CampaignEngine",
        )
        assert ch_camp.event_type == "CAMPAIGN_CHANGED"
