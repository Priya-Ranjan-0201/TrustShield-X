"""
TruthShield X — Twin State Differencing Engine (Phase 18).

Compares sequential digital twin state snapshots to calculate precise entity and control deltas.
"""

from typing import Dict, Any, Optional
from app.schemas.cyber_resilience_twin_models import TwinStateSnapshotDTO


class TwinDiffEngine:
    """Computes high-fidelity differential deltas between snapshots."""

    def compare_snapshots(
        self,
        previous_snapshot: Optional[TwinStateSnapshotDTO],
        current_snapshot: TwinStateSnapshotDTO,
    ) -> Dict[str, Any]:
        """Calculates state changes between two snapshots."""
        if not previous_snapshot:
            return {
                "diff_type": "INITIAL_SNAPSHOT",
                "asset_delta": current_snapshot.asset_count,
                "service_delta": current_snapshot.service_count,
                "control_delta": current_snapshot.control_count,
                "exposure_delta": current_snapshot.exposure_count,
                "summary": "Baseline digital twin snapshot established.",
            }

        asset_diff = current_snapshot.asset_count - previous_snapshot.asset_count
        serv_diff = current_snapshot.service_count - previous_snapshot.service_count
        ctrl_diff = current_snapshot.control_count - previous_snapshot.control_count
        exp_diff = current_snapshot.exposure_count - previous_snapshot.exposure_count

        return {
            "diff_type": "SEQUENTIAL_DELTA",
            "previous_snapshot_id": previous_snapshot.snapshot_id,
            "current_snapshot_id": current_snapshot.snapshot_id,
            "asset_delta": asset_diff,
            "service_delta": serv_diff,
            "control_delta": ctrl_diff,
            "exposure_delta": exp_diff,
            "has_changes": any(d != 0 for d in (asset_diff, serv_diff, ctrl_diff, exp_diff)),
        }
