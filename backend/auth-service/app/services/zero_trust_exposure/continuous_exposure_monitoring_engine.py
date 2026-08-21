"""
Continuous Exposure Monitoring Engine (Phase 34)
================================================
Monitors external assets, certificates, open ports, and zero-trust policies
for drift (EXPOSURE_DRIFT, ZERO_TRUST_DRIFT, PRIVILEGE_DRIFT), triggering re-evaluation.
"""

from typing import Dict, Any, List, Optional
import datetime
from app.schemas.zero_trust_exposure_models import ExposureDriftDTO


class ContinuousExposureMonitoringEngine:
    def __init__(self):
        self._drift_events: List[Dict[str, Any]] = []

    def check_exposure_drift(
        self,
        drift_id: str,
        tenant_id: str,
        asset_id: str,
        previous_state: Dict[str, Any],
        current_state: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        # Detect delta
        diff = {}
        for k, v in current_state.items():
            if previous_state.get(k) != v:
                diff[k] = {"previous": previous_state.get(k), "current": v}

        if not diff:
            return None

        drift_type = "EXPOSURE_DRIFT"
        if "open_ports" in diff or "exposed_publicly" in diff or "exposed" in diff:
            drift_type = "EXPOSURE_DRIFT"
        elif "trust_state" in diff or "policy_version" in diff:
            drift_type = "ZERO_TRUST_DRIFT"
        elif "roles" in diff or "privileges" in diff:
            drift_type = "PRIVILEGE_DRIFT"

        record = {
            "drift_id": drift_id,
            "tenant_id": tenant_id,
            "asset_id": asset_id,
            "drift_type": drift_type,
            "previous_state": previous_state,
            "current_state": current_state,
            "detected_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        self._drift_events.append(record)
        return record

    def record_baseline(self, tenant_id: str, baseline_data: Dict[str, Any]) -> Dict[str, Any]:
        if not hasattr(self, "_baselines"):
            self._baselines = {}
        self._baselines[tenant_id] = {
            "tenant_id": tenant_id,
            "baseline_data": baseline_data,
            "status": "BASELINE_ACTIVE",
            "recorded_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        return self._baselines[tenant_id]

    def evaluate_drift(self, tenant_id: str, current_state: Dict[str, Any]) -> Dict[str, Any]:
        if not hasattr(self, "_baselines"):
            self._baselines = {}
        baseline_record = self._baselines.get(tenant_id)
        prev_data = baseline_record["baseline_data"] if baseline_record else {}
        
        drifts = []
        for k, curr_v in current_state.items():
            prev_v = prev_data.get(k)
            if prev_v != curr_v:
                drifts.append({
                    "attribute": k,
                    "previous": prev_v,
                    "current": curr_v,
                    "severity": "HIGH" if k in ["open_ports", "unapproved_admins"] else "MEDIUM"
                })

        drift_detected = (len(drifts) > 0)
        return {
            "tenant_id": tenant_id,
            "drift_detected": drift_detected,
            "drifts": drifts,
            "status": "DRIFT_CONFIRMED" if drift_detected else "NO_DRIFT",
            "evaluated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }


continuous_exposure_monitoring_engine = ContinuousExposureMonitoringEngine()

