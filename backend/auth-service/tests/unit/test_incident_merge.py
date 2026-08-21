"""Unit Tests — Incident Creation, Merge & Split (Phase 4.0 Part 7 — Sections 11-16, 60-61)."""

import pytest
from app.services.soc.incident_creation_engine import IncidentCreationEngine
from app.schemas.soc_operations_models import SOCAlertDTO


class TestIncidentLifecycleOperations:
    def test_incident_merge_preserves_audit_trail(self):
        engine = IncidentCreationEngine()
        alert1 = SOCAlertDTO(
            alert_id="alt_m1",
            title="Phishing Site A",
            category="PHISHING",
            entity_ids=["site-a.com"],
        )
        alert2 = SOCAlertDTO(
            alert_id="alt_m2",
            title="Phishing Site B",
            category="PHISHING",
            entity_ids=["site-b.com"],
        )

        inc1 = engine.create_or_update_incident_from_alert(alert1)
        inc2 = engine.create_or_update_incident_from_alert(alert2)
        assert inc1.incident_id != inc2.incident_id

        # Merge inc2 into inc1
        primary, merge_rec = engine.merge_incidents(
            primary_incident_id=inc1.incident_id,
            merged_incident_ids=[inc2.incident_id],
            merged_by="lead_analyst@trustshield.internal",
            reason="Confirmed same adversary infrastructure",
        )

        assert primary.incident_id == inc1.incident_id
        assert primary.source_alert_count == 2
        assert inc2.status == "CANCELLED"
        assert merge_rec.primary_incident_id == inc1.incident_id

    def test_incident_split_creates_new_auditable_records(self):
        engine = IncidentCreationEngine()
        alert = SOCAlertDTO(
            alert_id="alt_s1",
            title="Multi-Branch Incident",
            category="PHISHING",
            entity_ids=["branch-1.com", "branch-2.com"],
        )
        inc = engine.create_or_update_incident_from_alert(alert)

        orig, new_incs, split_rec = engine.split_incident(
            original_incident_id=inc.incident_id,
            split_by="analyst@trustshield.internal",
            reason="Distinct attack actors identified on branch 2",
            new_incident_titles=["Branch 1 Investigation", "Branch 2 Adversary Investigation"],
        )

        assert len(new_incs) == 2
        assert split_rec.original_incident_id == inc.incident_id
        assert len(split_rec.new_incident_ids) == 2
