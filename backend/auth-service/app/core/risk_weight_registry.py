"""Versioned Risk Weight Registry (Phase 3.9 Part 1B).

Maps canonical finding types to risk categories and base weights.
"""

from typing import Dict, Any, Optional


class RiskWeightRegistry:
    """Versioned Weight Registry mapping finding types to base risk weights."""

    def __init__(self):
        self._weights: Dict[str, Dict[str, Any]] = {
            "NETWORK_ENDPOINT_OBSERVED": {
                "category": "NETWORK_THREAT",
                "base_weight": 5.0,
                "max_weight": 15.0,
            },
            "SMS_DATA_NETWORK_TRANSFER": {
                "category": "DATA_EXFILTRATION",
                "base_weight": 25.0,
                "max_weight": 40.0,
            },
            "CREDENTIAL_PHISHING_EXFILTRATION": {
                "category": "CREDENTIAL_THEFT",
                "base_weight": 35.0,
                "max_weight": 50.0,
            },
        }

    def get_weight_config(self, finding_type: str) -> Optional[Dict[str, Any]]:
        return self._weights.get(finding_type)
