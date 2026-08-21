"""
TruthShield X — Adaptive Detection Engine (Phase 17).

Manages dynamic detection rule tuning, versioning, automated rollback, and false-positive spike protection.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid


class AdaptiveDetectionRuleDTO:
    def __init__(
        self,
        rule_id: str,
        name: str,
        pattern: str,
        version: int = 1,
        owner: str = "SOC_DETECTION",
        status: str = "ACTIVE",
        previous_version: Optional[int] = None,
    ):
        self.rule_id = rule_id
        self.name = name
        self.pattern = pattern
        self.version = version
        self.owner = owner
        self.status = status
        self.previous_version = previous_version
        self.created_at = datetime.now(timezone.utc).isoformat()


class AdaptiveDetectionEngine:
    """Manages versioned detection rule adaptations and rollback safety."""

    def __init__(self):
        # rule_id -> AdaptiveDetectionRuleDTO
        self._rules: Dict[str, AdaptiveDetectionRuleDTO] = {}
        self._version_history: Dict[str, List[AdaptiveDetectionRuleDTO]] = {}
        self._alert_volume_spikes: List[Dict[str, Any]] = []

    def deploy_rule(self, name: str, pattern: str, rule_id: Optional[str] = None) -> AdaptiveDetectionRuleDTO:
        """Deploys a new or updated versioned detection rule."""
        rid = rule_id or f"rule_{uuid.uuid4().hex[:8]}"

        # Syntax check (Section 26)
        if not pattern or len(pattern) < 3:
            raise ValueError("Invalid detection pattern syntax.")

        existing = self._rules.get(rid)
        prev_ver = existing.version if existing else None
        new_ver = (existing.version + 1) if existing else 1

        rule = AdaptiveDetectionRuleDTO(
            rule_id=rid,
            name=name,
            pattern=pattern,
            version=new_ver,
            previous_version=prev_ver,
        )

        self._rules[rid] = rule
        history = self._version_history.setdefault(rid, [])
        history.append(rule)
        return rule

    def rollback_rule(self, rule_id: str) -> Optional[AdaptiveDetectionRuleDTO]:
        """Rolls back a detection rule to its previous version."""
        history = self._version_history.get(rule_id, [])
        if len(history) < 2:
            return None

        # Previous version is second-to-last
        prev = history[-2]
        self._rules[rule_id] = prev
        return prev

    def check_alert_volume(self, rule_id: str, hourly_alerts: int) -> Optional[str]:
        """Monitors for abnormal alert volume spikes (Section 27)."""
        if hourly_alerts > 100:
            warning = f"ADAPTATION_WARNING: Abnormal alert volume spike ({hourly_alerts}/hr) on rule {rule_id}"
            self._alert_volume_spikes.append({
                "rule_id": rule_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "warning": warning,
            })
            return warning
        return None

    def get_rule(self, rule_id: str) -> Optional[AdaptiveDetectionRuleDTO]:
        return self._rules.get(rule_id)

    def list_rules(self) -> List[AdaptiveDetectionRuleDTO]:
        return list(self._rules.values())
