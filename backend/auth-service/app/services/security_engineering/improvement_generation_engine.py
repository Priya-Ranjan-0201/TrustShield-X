"""
TruthShield X — Improvement Generation Engine (Phase 25).

Generates evidence-grounded defensive recommendations and automatically screens for malicious or destabilizing inputs.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.security_engineering_models import SecurityImprovementDTO, ImprovementCategoryLiteral


class ImprovementGenerationEngine:
    """Creates structured defensive improvements with strict safety guardrails."""

    def __init__(self):
        self._improvements: Dict[str, SecurityImprovementDTO] = {}
        self._seed_default_improvements()

    def _seed_default_improvements(self):
        i1 = SecurityImprovementDTO(
            improvement_id="imp_sigma_t1055_rule",
            tenant_id="default_tenant",
            category="DETECTION",
            title="Deploy Sigma Rule for Reflective DLL Injection",
            description="Adds detection rule targeting reflective DLL memory allocations used by campaign AP-44.",
            problem="Reflective DLL injection not alerted by current ruleset.",
            evidence=["ev_threat_intel_AP44", "ev_sigma_coverage_matrix"],
            proposed_change="Add sigma_rule_reflective_dll_injection.yml to active SIEM engine.",
            expected_benefit="Increases MITRE T1055 detection coverage to 100%.",
            expected_risk="Minor increase in false alerts (< 0.5%).",
            confidence=0.96,
            impact_score=0.88,
            reversibility="FULLY_REVERSIBLE",
            approval_required=False,
            simulation_status="SIMULATED",
            validation_status="PASSED",
            deployment_status="CANARY_DEPLOYED",
            outcome_status="IMPROVED",
        )
        self._improvements[i1.improvement_id] = i1

    def generate_improvement(
        self,
        category: ImprovementCategoryLiteral,
        title: str,
        description: str,
        problem: str,
        proposed_change: str,
        expected_benefit: str,
        expected_risk: str,
        evidence: Optional[List[str]] = None,
        confidence: float = 0.95,
        impact_score: float = 0.85,
        reversibility: str = "FULLY_REVERSIBLE",
        tenant_id: str = "default_tenant",
    ) -> SecurityImprovementDTO:
        # Malicious Recommendation Filter
        prohibited_phrases = [
            "disable auth",
            "disable authentication",
            "bypass four-eyes",
            "bypass approval",
            "modify audit",
            "disable audit",
            "remove tenant isolation",
            "grant wildcard admin",
        ]
        combined_text = f"{title} {description} {proposed_change}".lower()
        for phrase in prohibited_phrases:
            if phrase in combined_text:
                raise ValueError(f"Malicious Recommendation Rejected: Cannot propose actions that weaken security controls ('{phrase}').")

        dto = SecurityImprovementDTO(
            tenant_id=tenant_id,
            category=category,
            title=title,
            description=description,
            problem=problem,
            evidence=evidence or ["ev_system_telemetry_baseline"],
            proposed_change=proposed_change,
            expected_benefit=expected_benefit,
            expected_risk=expected_risk,
            confidence=confidence,
            impact_score=impact_score,
            reversibility=reversibility,  # type: ignore
            approval_required=(impact_score > 0.9 or reversibility == "IRREVERSIBLE"),
            simulation_status="PENDING",
            validation_status="NOT_VERIFIED",
            deployment_status="PENDING",
            outcome_status="NOT_VERIFIED",
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._improvements[dto.improvement_id] = dto
        return dto

    def get_improvement(self, improvement_id: str) -> Optional[SecurityImprovementDTO]:
        return self._improvements.get(improvement_id)

    def list_improvements(self, tenant_id: str = "default_tenant") -> List[SecurityImprovementDTO]:
        return [i for i in self._improvements.values() if i.tenant_id == tenant_id or i.tenant_id == "default_tenant"]
