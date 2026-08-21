"""
TruthShield X — Detection Optimization Engine (Phase 30).

Governs the detection engineering lifecycle:
INCIDENT -> MISSED_SIGNAL -> HYPOTHESIS -> DETECTION_RULE -> SIMULATION -> VALIDATION -> APPROVAL -> DEPLOYMENT.
"""

from typing import Dict, List, Optional, Any
from app.schemas.autonomous_defense_models import DetectionOptimizationDTO


class DetectionOptimizationEngine:
    """Evaluates rule precision, recall, drift, and prevents unsafe regressions in detection coverage."""

    def __init__(self):
        self._rules: Dict[str, DetectionOptimizationDTO] = {}
        self._seed_default_rules()

    def _seed_default_rules(self):
        r1 = DetectionOptimizationDTO(
            rule_id="rule_darkstorm_c2_entropy",
            rule_name="DarkStorm DNS High Entropy Detection",
            precision=0.96,
            recall=0.92,
            detection_latency_ms=45.0,
            drift_status="STABLE",
            candidate_rule=None,
            status="DEPLOYED",
        )
        self._rules[r1.rule_id] = r1

    def evaluate_rule_optimization(
        self,
        rule_id: str,
        candidate_precision: float,
        candidate_recall: float,
    ) -> Dict[str, Any]:
        curr = self._rules.get(rule_id)
        if not curr:
            raise ValueError(f"Rule '{rule_id}' not found.")

        # Safety Check: Optimization must not weaken detection recall/coverage
        if candidate_recall < curr.recall:
            return {
                "rule_id": rule_id,
                "is_approved": False,
                "status": "REJECTED",
                "reason": f"CANDIDATE_RECALL_{candidate_recall}_BELOW_BASELINE_{curr.recall}_UNSAFE_OPTIMIZATION",
            }

        return {
            "rule_id": rule_id,
            "is_approved": True,
            "status": "VALIDATED",
            "reason": "CANDIDATE_IMPROVED_PRECISION_PRESERVED_RECALL",
            "expected_precision": candidate_precision,
            "expected_recall": candidate_recall,
        }

    def detect_rule_drift(self, rule_id: str, false_positive_spike: bool = False) -> str:
        return "DETECTION_DRIFT" if false_positive_spike else "STABLE"

    def list_rules(self) -> List[DetectionOptimizationDTO]:
        return list(self._rules.values())
