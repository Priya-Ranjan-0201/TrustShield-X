"""SOC Alert Correlation Rules & False Correlation Protection (Phase 4.0 Part 7 — Sections 6-10)."""

from typing import List, Dict, Any, Optional, Set
from datetime import datetime, timezone, timedelta
from app.schemas.soc_operations_models import SOCAlertDTO

POPULAR_INFRASTRUCTURE = {
    "cloudflare",
    "aws",
    "amazon",
    "azure",
    "google cloud",
    "gcp",
    "akamai",
    "fastly",
    "let's encrypt",
    "digicert",
    "firebase",
    "google play services",
}


def is_generic_infrastructure(identifier: str) -> bool:
    low = identifier.lower().strip()
    return any(infra in low for infra in POPULAR_INFRASTRUCTURE)


class AlertEntityRule:
    """Correlates alerts that share concrete malicious entities while rejecting generic CDN/CA overlap."""

    @staticmethod
    def evaluate(alert1: SOCAlertDTO, alert2: SOCAlertDTO) -> Optional[Dict[str, Any]]:
        shared_entities = set(alert1.entity_ids).intersection(set(alert2.entity_ids))
        if not shared_entities:
            return None

        # Filter out generic infrastructure (Section 10)
        valid_shared = [e for e in shared_entities if not is_generic_infrastructure(e)]
        if not valid_shared:
            return None  # Only generic cloud/CDN overlap; false correlation protected!

        return {
            "rule_id": "SOC_RULE_ENTITY_OVERLAP",
            "cluster_type": "SAME_ENTITY",
            "confidence": 0.95,
            "shared_entities": valid_shared,
            "reason": f"Alerts share non-generic entities: {', '.join(valid_shared)}",
        }


class CampaignRule:
    """Correlates alerts that belong to the same threat campaign."""

    @staticmethod
    def evaluate(alert1: SOCAlertDTO, alert2: SOCAlertDTO) -> Optional[Dict[str, Any]]:
        if alert1.campaign_id and alert2.campaign_id and alert1.campaign_id == alert2.campaign_id:
            return {
                "rule_id": "SOC_RULE_CAMPAIGN_OVERLAP",
                "cluster_type": "SAME_CAMPAIGN",
                "confidence": 0.98,
                "campaign_id": alert1.campaign_id,
                "reason": f"Alerts belong to the same coordinated threat campaign {alert1.campaign_id}",
            }
        return None


class AttackChainRule:
    """Correlates alerts that represent consecutive steps in an attack chain."""

    @staticmethod
    def evaluate(alert1: SOCAlertDTO, alert2: SOCAlertDTO) -> Optional[Dict[str, Any]]:
        if alert1.attack_chain_id and alert2.attack_chain_id and alert1.attack_chain_id == alert2.attack_chain_id:
            return {
                "rule_id": "SOC_RULE_ATTACK_CHAIN_OVERLAP",
                "cluster_type": "SAME_ATTACK_CHAIN",
                "confidence": 0.95,
                "attack_chain_id": alert1.attack_chain_id,
                "reason": f"Alerts belong to attack chain {alert1.attack_chain_id}",
            }
        return None


class TemporalRule:
    """Evaluates temporal proximity between alerts on related cases."""

    @staticmethod
    def evaluate(alert1: SOCAlertDTO, alert2: SOCAlertDTO, max_window_minutes: int = 60) -> Optional[Dict[str, Any]]:
        if not alert1.case_id or not alert2.case_id or alert1.case_id != alert2.case_id:
            return None

        try:
            t1 = datetime.fromisoformat(alert1.created_at)
            t2 = datetime.fromisoformat(alert2.created_at)
            diff = abs((t1 - t2).total_seconds()) / 60.0
            if diff <= max_window_minutes:
                return {
                    "rule_id": "SOC_RULE_TEMPORAL_PROXIMITY",
                    "cluster_type": "TEMPORALLY_RELATED",
                    "confidence": 0.85,
                    "reason": f"Alerts occurred within {diff:.1f} minutes on case {alert1.case_id}",
                }
        except Exception:
            pass
        return None


class CrossModalRule:
    """Correlates cross-modal alerts (e.g. APK + Phishing URL + Payment ID)."""

    @staticmethod
    def evaluate(alert1: SOCAlertDTO, alert2: SOCAlertDTO) -> Optional[Dict[str, Any]]:
        if alert1.category != alert2.category:
            # Check if they share a case or non-generic entity
            shared_entities = set(alert1.entity_ids).intersection(set(alert2.entity_ids))
            valid_entities = [e for e in shared_entities if not is_generic_infrastructure(e)]
            if valid_entities or (alert1.case_id and alert1.case_id == alert2.case_id):
                return {
                    "rule_id": "SOC_RULE_CROSS_MODAL",
                    "cluster_type": "CROSS_MODAL",
                    "confidence": 0.90,
                    "reason": f"Cross-modal correlation between {alert1.category} and {alert2.category}",
                }
        return None
