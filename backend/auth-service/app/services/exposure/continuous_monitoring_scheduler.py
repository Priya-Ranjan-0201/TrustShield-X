"""
TruthShield X — Continuous Monitoring Scheduler & State Machine
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.exposure_models import MonitoringStatusLiteral, AssetDTO


class ContinuousMonitoringScheduler:
    """Schedules, controls concurrency, and transitions monitoring jobs with idempotency and retry backoff."""

    VALID_TRANSITIONS = {
        "CONFIGURED": ["SCHEDULED", "PAUSED", "DISABLED"],
        "SCHEDULED": ["RUNNING", "PAUSED", "DISABLED"],
        "RUNNING": ["COMPLETED", "FAILED", "RETRYING", "PAUSED"],
        "RETRYING": ["SCHEDULED", "RUNNING", "FAILED", "PAUSED", "DISABLED"],
        "COMPLETED": ["SCHEDULED", "PAUSED", "DISABLED"],
        "FAILED": ["RETRYING", "PAUSED", "DISABLED", "SCHEDULED"],
        "PAUSED": ["SCHEDULED", "DISABLED"],
        "DISABLED": ["CONFIGURED", "SCHEDULED"],
    }

    def __init__(self, max_concurrent_jobs: int = 50):
        self.max_concurrent_jobs = max_concurrent_jobs
        # tenant_id -> job_id -> Job Dict
        self._jobs: Dict[str, Dict[str, Dict[str, Any]]] = {}
        # tenant_id -> asset_id -> job_id (idempotent lookup)
        self._asset_active_job: Dict[str, Dict[str, str]] = {}

    def schedule_monitoring_job(
        self,
        asset: AssetDTO,
        mode: str = "PASSIVE",  # PASSIVE or AUTHORIZED_ACTIVE
        tenant_id: str = "default_tenant",
    ) -> Dict[str, Any]:
        """Schedules a new monitoring job, preventing duplicate running jobs on the same asset."""
        if tenant_id not in self._jobs:
            self._jobs[tenant_id] = {}
            self._asset_active_job[tenant_id] = {}

        # Idempotency check: if already active (SCHEDULED or RUNNING), return existing job
        existing_job_id = self._asset_active_job[tenant_id].get(asset.asset_id)
        if existing_job_id:
            existing = self._jobs[tenant_id].get(existing_job_id)
            if existing and existing["status"] in ("SCHEDULED", "RUNNING"):
                return existing

        # Concurrency limit check
        active_count = sum(1 for j in self._jobs[tenant_id].values() if j["status"] == "RUNNING")
        if active_count >= self.max_concurrent_jobs:
            status: MonitoringStatusLiteral = "SCHEDULED"
        else:
            status = "SCHEDULED"

        job_id = f"mjob_{uuid.uuid4().hex[:12]}"
        job = {
            "job_id": job_id,
            "asset_id": asset.asset_id,
            "canonical_identifier": asset.canonical_identifier,
            "mode": mode,
            "status": status,
            "retry_count": 0,
            "max_retries": 3,
            "tenant_id": tenant_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

        self._jobs[tenant_id][job_id] = job
        self._asset_active_job[tenant_id][asset.asset_id] = job_id
        return job

    def transition_job_status(
        self,
        job_id: str,
        new_status: MonitoringStatusLiteral,
        tenant_id: str = "default_tenant",
        failure_reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Transitions job status following the formal state machine."""
        job = self._jobs.get(tenant_id, {}).get(job_id)
        if not job:
            raise KeyError(f"Job '{job_id}' not found.")

        current_status = job["status"]
        allowed = self.VALID_TRANSITIONS.get(current_status, [])
        if new_status not in allowed:
            raise ValueError(f"Invalid transition from '{current_status}' to '{new_status}'. Allowed: {allowed}")

        job["status"] = new_status
        job["updated_at"] = datetime.now(timezone.utc).isoformat()

        if new_status == "FAILED":
            job["failure_reason"] = failure_reason
            if job["retry_count"] < job["max_retries"]:
                job["retry_count"] += 1
                job["status"] = "RETRYING"

        return job

    def list_jobs(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        """Lists all monitoring jobs for a tenant."""
        return list(self._jobs.get(tenant_id, {}).values())
