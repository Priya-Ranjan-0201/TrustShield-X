"""
TruthShield X — Campaign Evolution Engine (Phase 22).

Tracks campaign shifts across infrastructure, techniques, and targeting, labeling observed vs inferred evolution.
"""

from typing import Dict, List, Any
from datetime import datetime, timezone


class CampaignEvolutionEngine:
    """Detects campaign expansion and evolutionary changes."""

    def record_evolution(
        self,
        campaign_id: str,
        new_infrastructure: List[str],
        new_techniques: List[str],
        new_targets: List[str],
    ) -> Dict[str, Any]:
        what_changed = []
        if new_infrastructure:
            what_changed.append(f"Observed {len(new_infrastructure)} new infrastructure nodes: {', '.join(new_infrastructure[:3])}")
        if new_techniques:
            what_changed.append(f"Adopted {len(new_techniques)} new TTPs: {', '.join(new_techniques)}")
        if new_targets:
            what_changed.append(f"Expanded targeting into: {', '.join(new_targets)}")

        return {
            "campaign_id": campaign_id,
            "evolution_timestamp": datetime.now(timezone.utc).isoformat(),
            "what_changed": what_changed,
            "observed_changes": new_infrastructure + new_techniques,
            "inferred_intent": "Lateral expansion across related business verticals",
            "lifecycle_state": "EXPANDING" if (new_infrastructure or new_techniques) else "ACTIVE",
        }
