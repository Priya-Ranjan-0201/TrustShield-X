"""
TruthShield X — Security Experiment Engine (Phase 25).

Orchestrates controlled hypothesis-driven experiments (A/B testing, threshold tuning) with safety limits.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.security_engineering_models import SecurityExperimentDTO


class SecurityExperimentEngine:
    """Safely executes defensive security experiments to test hypotheses against real telemetry."""

    def __init__(self):
        self._experiments: Dict[str, SecurityExperimentDTO] = {}
        self._seed_default_experiment()

    def _seed_default_experiment(self):
        e1 = SecurityExperimentDTO(
            experiment_id="exp_waf_sqli_tuning",
            tenant_id="default_tenant",
            hypothesis="Tuning regex threshold on SQL injection WAF decreases false alerts by 40% without missing true positives.",
            baseline={"false_positive_rate": 0.08, "missed_detections": 0.0},
            treatment={"false_positive_rate": 0.02, "missed_detections": 0.0},
            metrics=["false_positive_rate", "detection_coverage"],
            duration_hours=24,
            expected_result="Lower false positive rate with 0 missed true attacks.",
            actual_result="False positives reduced by 75%, 0 missed true attacks.",
            conclusion="Hypothesis validated. Recommended for production deployment.",
            status="COMPLETED",
        )
        self._experiments[e1.experiment_id] = e1

    def create_experiment(
        self,
        hypothesis: str,
        baseline: Dict[str, float],
        treatment: Dict[str, float],
        metrics: List[str],
        duration_hours: int = 24,
        target_scope: str = "INTERNAL_SANDBOX",
        tenant_id: str = "default_tenant",
    ) -> SecurityExperimentDTO:
        # Experiment Safety Invariant: Cannot target unauthorized or external systems
        if target_scope in ["EXTERNAL_UNAUTHORIZED", "THIRD_PARTY_SYSTEM", "UNCONTROLLED_PROD"]:
            raise ValueError(f"Experiment Rejected: Prohibited target scope '{target_scope}'. Experiments must be safely bounded to authorized internal or sandbox scopes.")

        dto = SecurityExperimentDTO(
            tenant_id=tenant_id,
            hypothesis=hypothesis,
            baseline=baseline,
            treatment=treatment,
            metrics=metrics,
            duration_hours=duration_hours,
            expected_result="Treatment improves metrics over baseline.",
            actual_result="Pending completion",
            conclusion=None,
            status="RUNNING",
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._experiments[dto.experiment_id] = dto
        return dto

    def get_experiment(self, experiment_id: str) -> Optional[SecurityExperimentDTO]:
        return self._experiments.get(experiment_id)

    def list_experiments(self, tenant_id: str = "default_tenant") -> List[SecurityExperimentDTO]:
        return list(self._experiments.values())
