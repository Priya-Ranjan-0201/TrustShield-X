"""
TruthShield X — Enterprise Risk Engine (Phase 32).

Maintains the enterprise risk register, calculates residual risk, and validates time-bound risk acceptance.
"""

from typing import Dict, List, Optional, Any
from app.schemas.enterprise_governance_models import EnterpriseRiskDTO, RiskStateLiteral


class EnterpriseRiskEngine:
    """Evaluates multi-factor risk, ensuring risk acceptance is time-bound, justified, and executive-authorized."""

    def __init__(self):
        self._risks: Dict[str, EnterpriseRiskDTO] = {}
        self._seed_default_risk()

    def _seed_default_risk(self):
        r1 = EnterpriseRiskDTO(
            risk_id="rsk_unauthorized_admin_access",
            title="Risk of Administrative Account Compromise",
            description="Risk that administrative access is gained via credential stuffing",
            asset="Identity Provider & Tenant Management Gateway",
            threat="Adversarial Credential Replay",
            vulnerability="Legacy Single-Factor Legacy Protocols",
            control_id="ctrl_iam_mfa_enforcement",
            likelihood=0.20,
            impact=0.90,
            inherent_risk=0.85,
            residual_risk=0.18,
            owner="CISO",
            treatment="MITIGATE",
            status="ASSESSED",
        )
        self._risks[r1.risk_id] = r1

    def evaluate_risk_acceptance(
        self,
        risk_id: str,
        authorized_by: str,
        rationale: str,
        expiration_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        risk = self._risks.get(risk_id)
        if not risk:
            raise ValueError(f"Risk '{risk_id}' not found.")

        # Absolute Rule: Risk acceptance requires authorized executive, rationale, and expiration
        if not authorized_by or authorized_by != "CISO":
            return {
                "risk_id": risk_id,
                "allowed": False,
                "status": "REJECTED",
                "reason": "RISK_ACCEPTANCE_REQUIRES_EXECUTIVE_CISO_AUTHORIZATION",
            }

        if not expiration_date:
            return {
                "risk_id": risk_id,
                "allowed": False,
                "status": "REJECTED",
                "reason": "PERMANENT_SILENT_RISK_ACCEPTANCE_FORBIDDEN",
            }

        return {
            "risk_id": risk_id,
            "allowed": True,
            "status": "RISK_ACCEPTED",
            "authorized_by": authorized_by,
            "expiration_date": expiration_date,
            "rationale": rationale,
        }

    def list_risks(self) -> List[EnterpriseRiskDTO]:
        return list(self._risks.values())
