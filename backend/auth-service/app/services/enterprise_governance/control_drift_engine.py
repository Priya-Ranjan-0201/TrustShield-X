"""
TruthShield X — Control Drift Engine (Phase 32).

Detects divergence between expected baseline configuration and live operating reality.
"""

from typing import Dict, Any


class ControlDriftEngine:
    """Computes differential configuration drift across security controls and policies."""

    def detect_control_drift(
        self,
        control_id: str,
        expected_config: Dict[str, Any],
        actual_config: Dict[str, Any],
    ) -> Dict[str, Any]:
        differences = []
        for k, v in expected_config.items():
            if actual_config.get(k) != v:
                differences.append({
                    "parameter": k,
                    "expected": v,
                    "actual": actual_config.get(k),
                })

        if differences:
            return {
                "control_id": control_id,
                "has_drift": True,
                "status": "CONTROL_DRIFT",
                "differences_count": len(differences),
                "differences": differences,
                "severity": "HIGH",
            }

        return {
            "control_id": control_id,
            "has_drift": False,
            "status": "IN_SYNC",
            "differences_count": 0,
            "differences": [],
            "severity": "NONE",
        }
