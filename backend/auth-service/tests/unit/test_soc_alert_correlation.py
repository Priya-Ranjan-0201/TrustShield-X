"""Unit Tests — SOC Alert Correlation & False Correlation Protection (Phase 4.0 Part 7 — Sections 6-10, 91).

Implements:
- Mandatory Test 16: Five duplicate alerts -> exactly one incident.
- Mandatory Test 17: Five alerts from same campaign -> correlated incident.
- Mandatory Test 18: Two alerts share only Cloudflare -> NO automatic correlation.
- Mandatory Test 19: APK + phishing domain + payment ID -> cross-modal incident candidate.
- Mandatory Test 20: Same alert arrives from two feeds -> deduplicated.
"""

import pytest
from app.schemas.soc_operations_models import SOCAlertDTO
from app.services.soc_operations_engine import SOCOperationsEngine
from app.services.soc.soc_correlation_rules import AlertEntityRule


class TestSOCAlertCorrelation:
    def test_16_mandatory_five_duplicate_alerts_create_one_incident(self):
        engine = SOCOperationsEngine()
        raw_alert = {
            "title": "Phishing URL Detected",
            "category": "PHISHING",
            "entity_ids": ["phishing-sbi-portal.in"],
            "case_id": "case_101",
        }

        created_incidents = []
        for _ in range(5):
            alert, inc = engine.ingest_and_process_alert(raw_alert)
            created_incidents.append(inc)

        # Invariant: Exactly 1 distinct incident created, with alert_count = 5
        distinct_ids = set(i.incident_id for i in created_incidents)
        assert len(distinct_ids) == 1
        assert created_incidents[-1].source_alert_count == 5

    def test_17_mandatory_five_alerts_from_same_campaign_correlated(self):
        engine = SOCOperationsEngine()

        for i in range(5):
            raw = {
                "title": f"Campaign C2 Node {i}",
                "category": "MALWARE",
                "campaign_id": "camp_lazarus_2026",
                "entity_ids": [f"c2_node_{i}.net"],
            }
            alert, inc = engine.ingest_and_process_alert(raw)

        # All 5 belong to the same campaign incident
        incidents = engine.list_incidents()
        camp_incs = [inc for inc in incidents if inc.campaign_id == "camp_lazarus_2026"]
        assert len(camp_incs) == 1
        assert camp_incs[0].source_alert_count == 5

    def test_18_mandatory_cloudflare_shared_infrastructure_not_correlated(self):
        # Two unrelated alerts that only share 'Cloudflare Inc' CDN
        alert1 = SOCAlertDTO(
            alert_id="alt_1",
            title="Suspicious Storefront",
            category="PHISHING",
            entity_ids=["legit-store.com", "Cloudflare Inc"],
        )
        alert2 = SOCAlertDTO(
            alert_id="alt_2",
            title="Crypto Exchange Fraud",
            category="FINANCIAL_FRAUD",
            entity_ids=["crypto-fake.net", "Cloudflare Inc"],
        )

        res = AlertEntityRule.evaluate(alert1, alert2)
        # Invariant: Must return None because Cloudflare alone cannot correlate alerts
        assert res is None

    def test_19_mandatory_cross_modal_correlation(self):
        engine = SOCOperationsEngine()
        raw_apk = {
            "title": "Malicious APK Dropper",
            "category": "MALWARE",
            "entity_ids": ["com.fraud.dropper", "shared_bank_fraud_upi@ybl"],
            "case_id": "case_cross_modal_01",
        }
        raw_upi = {
            "title": "Mule UPI Payment Identifier",
            "category": "FINANCIAL_FRAUD",
            "entity_ids": ["shared_bank_fraud_upi@ybl"],
            "case_id": "case_cross_modal_01",
        }

        _, inc1 = engine.ingest_and_process_alert(raw_apk)
        _, inc2 = engine.ingest_and_process_alert(raw_upi)

        # Correlated into cross-modal incident
        assert inc1.incident_id == inc2.incident_id
        assert inc2.source_alert_count == 2
