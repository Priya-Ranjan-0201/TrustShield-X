"""Response Decision Engine & Safety Classification (Phase 5).

Evaluates threats, risk, confidence, legal hold, and asset criticality
to deterministically decide appropriate defensive response strategy.
"""

from typing import List, Dict, Any, Optional
from app.schemas.autonomous_defense_models import (
    DecisionContextDTO,
    DecisionResultDTO,
    DecisionTypeLiteral,
    SafetyClassificationLiteral,
)

READ_ONLY_ACTIONS = {
    "COLLECT_EVIDENCE",
    "ENRICH_IOC",
    "INSPECT_ARTIFACT",
    "QUERY_THREAT_GRAPH",
    "GET_DEVICE_INFO",
}

LOW_RISK_MUTATION_ACTIONS = {
    "MARK_INDICATOR",
    "ADD_INTERNAL_TAG",
    "NOTIFY_ANALYST",
    "NOTIFY_USER",
    "OPEN_INVESTIGATION_CASE",
    "CREATE_ALERT",
}

HIGH_RISK_MUTATION_ACTIONS = {
    "BLOCK_DOMAIN",
    "BLOCK_IP",
    "BLOCK_URL",
    "QUARANTINE_FILE",
    "ISOLATE_DEVICE",
    "DISABLE_ACCOUNT",
    "FREEZE_UPI_HANDLE",
    "ISOLATE_S3_BUCKET",
}

DESTRUCTIVE_ACTIONS = {
    "DELETE_RESOURCE",
    "REVOKE_INFRASTRUCTURE",
    "TERMINATE_ALL_SESSIONS",
    "REVOKE_TOKEN",
    "RESET_CREDENTIAL",
}

IRREVERSIBLE_ACTIONS = {
    "PERMANENT_DELETE_DATA",
    "HARD_PURGE_RECORDS",
    "REVOKE_ROOT_CERTIFICATE",
}


class ResponseDecisionEngine:
    """Evaluates cyber threat context and policies to determine the safest response decision."""

    @staticmethod
    def classify_action_safety(action_type: str) -> SafetyClassificationLiteral:
        """Categorize action into formal 5-tier safety levels."""
        act = action_type.upper()
        if act in READ_ONLY_ACTIONS:
            return "READ_ONLY"
        if act in LOW_RISK_MUTATION_ACTIONS:
            return "LOW_RISK_MUTATION"
        if act in HIGH_RISK_MUTATION_ACTIONS:
            return "HIGH_RISK_MUTATION"
        if act in DESTRUCTIVE_ACTIONS:
            return "DESTRUCTIVE"
        if act in IRREVERSIBLE_ACTIONS:
            return "IRREVERSIBLE"
        return "HIGH_RISK_MUTATION"

    def evaluate_decision(self, ctx: DecisionContextDTO) -> DecisionResultDTO:
        """Determines the appropriate defensive action decision."""
        safety = self.classify_action_safety(ctx.action_type)
        limitations: List[str] = []
        evidence_refs = list(ctx.evidence_ids)

        # 1. LEGAL HOLD OVERRIDE (Critical Governance Invariant)
        if ctx.legal_hold and safety in ("DESTRUCTIVE", "IRREVERSIBLE"):
            return DecisionResultDTO(
                decision="NO_ACTION",
                safety_classification=safety,
                confidence=1.0,
                required_approval=True,
                policy_basis="GOVERNANCE_LEGAL_HOLD_BLOCK",
                evidence_ids=evidence_refs,
                recommended_action=f"DENIED({ctx.action_type})",
                target=ctx.target,
                target_type=ctx.target_type,
                reason="Destructive actions strictly prohibited on assets subject to active legal hold.",
                limitations=["Legal preservation order overrides automated eradication playbooks."],
            )

        # 2. ASSET CRITICALITY OVERRIDE
        if ctx.asset_criticality == "MISSION_CRITICAL" and safety in ("HIGH_RISK_MUTATION", "DESTRUCTIVE", "IRREVERSIBLE"):
            return DecisionResultDTO(
                decision="REQUEST_APPROVAL",
                safety_classification=safety,
                confidence=ctx.confidence,
                required_approval=True,
                policy_basis="MISSION_CRITICAL_ASSET_PROTECTION",
                evidence_ids=evidence_refs,
                recommended_action=ctx.action_type,
                target=ctx.target,
                target_type=ctx.target_type,
                reason="Target asset is classified as MISSION_CRITICAL. Mandatory four-eyes approval required before containment.",
                limitations=["Automated containment disabled for tier-1 production systems."],
            )

        # 3. LOW-RISK / READ-ONLY ACTIONS (Automated allowed if confidence high)
        if safety in ("READ_ONLY", "LOW_RISK_MUTATION"):
            if ctx.confidence >= 0.70:
                decision: DecisionTypeLiteral = "EXECUTE"
                req_appr = False
                reason = f"Low-risk automated action '{ctx.action_type}' permitted by standard policy with confidence {ctx.confidence:.2f}."
            else:
                decision = "MONITOR"
                req_appr = False
                reason = f"Confidence {ctx.confidence:.2f} below threshold (0.70) for automated tagging. Placed in monitoring."
                limitations.append("Low statistical confidence in threat indicators.")

            return DecisionResultDTO(
                decision=decision,
                safety_classification=safety,
                confidence=ctx.confidence,
                required_approval=req_appr,
                policy_basis="LOW_RISK_AUTOMATION_POLICY",
                evidence_ids=evidence_refs,
                recommended_action=ctx.action_type,
                target=ctx.target,
                target_type=ctx.target_type,
                reason=reason,
                limitations=limitations,
            )

        # 4. HIGH-RISK / DESTRUCTIVE ACTIONS — EVALUATE RISK SCORE BANDS
        risk = ctx.risk_score

        if risk < 20.0:
            dec: DecisionTypeLiteral = "MONITOR"
            req_appr = False
            reason = f"Risk score ({risk:.1f}) within benign baseline (<20). Continued monitoring."
        elif 20.0 <= risk < 40.0:
            dec = "INVESTIGATE"
            req_appr = False
            reason = f"Risk score ({risk:.1f}) indicates anomalous activity. Automated investigation opened."
        elif 40.0 <= risk < 60.0:
            dec = "ALERT"
            req_appr = False
            reason = f"Moderate risk threat ({risk:.1f}). Security alert dispatched to SOC queue."
        elif 60.0 <= risk < 80.0:
            dec = "REQUEST_APPROVAL"
            req_appr = True
            reason = f"Elevated threat risk ({risk:.1f}). Containment action '{ctx.action_type}' requires four-eyes authorization."
        else:  # 80.0 <= risk <= 100.0 (CRITICAL)
            if ctx.confidence >= 0.90:
                dec = "REQUEST_APPROVAL"
                req_appr = True
                reason = f"Critical risk ({risk:.1f}) verified with high confidence ({ctx.confidence:.2f}). Emergency four-eyes approval requested."
            else:
                dec = "ESCALATE"
                req_appr = True
                reason = f"Critical risk ({risk:.1f}) with moderate confidence ({ctx.confidence:.2f}). Escalated to Tier-3 SOC for manual triage."
                limitations.append("High risk requires senior analyst verification before execution.")

        return DecisionResultDTO(
            decision=dec,
            safety_classification=safety,
            confidence=ctx.confidence,
            required_approval=req_appr,
            policy_basis="ENTERPRISE_RISK_GOVERNANCE_MATRIX",
            evidence_ids=evidence_refs,
            recommended_action=ctx.action_type,
            target=ctx.target,
            target_type=ctx.target_type,
            reason=reason,
            limitations=limitations,
        )
