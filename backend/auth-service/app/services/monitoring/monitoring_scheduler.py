"""Monitoring Scheduler, Retry Policy & Rate Limiting Engine (Phase 4.0 Part 6 — Sections 23-27).

Manages synchronization schedules, executes feed runs with exponential backoff and jitter,
and tracks provider rate limit quotas.
"""

from typing import List, Dict, Any, Optional
import uuid
import random
from datetime import datetime, timezone, timedelta
from app.schemas.continuous_intelligence_models import (
    MonitoringJobDTO,
    MonitoringJobRunDTO,
    ThreatFeedConfigurationDTO,
)


class MonitoringScheduler:
    """Schedules, controls, and manages synchronization jobs across all configured threat feeds."""

    def __init__(self):
        self._jobs: Dict[str, MonitoringJobDTO] = {}
        self._runs: List[MonitoringJobRunDTO] = []
        self._rate_limits: Dict[str, Dict[str, Any]] = {}

    def register_feed(self, config: ThreatFeedConfigurationDTO) -> MonitoringJobDTO:
        """Create or update monitoring job schedule for a threat feed."""
        interval_secs = config.poll_interval_seconds or 3600
        job = MonitoringJobDTO(
            job_id=f"job_{config.feed_id}",
            feed_id=config.feed_id,
            job_type="SYNC",
            schedule_type=config.poll_interval,
            interval_seconds=interval_secs,
            enabled=config.enabled,
            next_run_at=datetime.now(timezone.utc).isoformat(),
        )
        self._jobs[job.job_id] = job
        return job

    def compute_retry_backoff(self, attempt: int, base_seconds: float = 2.0, max_seconds: float = 60.0) -> float:
        """Compute exponential backoff with jitter (Section 26)."""
        backoff = min(max_seconds, base_seconds * (2 ** (attempt - 1)))
        jitter = random.uniform(0.1, 0.5) * backoff
        return backoff + jitter

    def check_rate_limit(self, feed_id: str, max_requests_per_minute: int = 60) -> bool:
        """Check if requests are within provider rate limit quota (Section 27)."""
        now = datetime.now(timezone.utc)
        record = self._rate_limits.get(feed_id)

        if not record or record["reset_at"] < now:
            self._rate_limits[feed_id] = {
                "count": 1,
                "reset_at": now + timedelta(minutes=1),
            }
            return True

        if record["count"] >= max_requests_per_minute:
            return False

        record["count"] += 1
        return True

    def create_job_run(self, job_id: str, feed_id: str, attempt: int = 1) -> MonitoringJobRunDTO:
        """Start a new monitoring execution run."""
        run = MonitoringJobRunDTO(
            run_id=f"run_{uuid.uuid4().hex[:12]}",
            job_id=job_id,
            feed_id=feed_id,
            status="RUNNING",
            started_at=datetime.now(timezone.utc).isoformat(),
            attempt=attempt,
        )
        self._runs.append(run)
        return run

    def complete_job_run(
        self,
        run: MonitoringJobRunDTO,
        items_processed: int,
        items_failed: int = 0,
        error_code: Optional[str] = None,
        error_message: Optional[str] = None,
    ) -> MonitoringJobRunDTO:
        """Finalize job run and calculate next execution timestamp."""
        run.completed_at = datetime.now(timezone.utc).isoformat()
        run.items_processed = items_processed
        run.items_failed = items_failed
        run.error_code = error_code
        run.error_message = error_message
        run.status = "COMPLETED" if not error_code else ("FAILED" if run.attempt >= 3 else "RETRYING")

        # Update parent job
        job = self._jobs.get(run.job_id)
        if job:
            job.last_run_at = run.completed_at
            job.status = run.status
            next_secs = job.interval_seconds if run.status == "COMPLETED" else self.compute_retry_backoff(run.attempt)
            job.next_run_at = (datetime.now(timezone.utc) + timedelta(seconds=next_secs)).isoformat()

        return run

    def list_jobs(self) -> List[MonitoringJobDTO]:
        return list(self._jobs.values())

    def list_runs(self, limit: int = 50) -> List[MonitoringJobRunDTO]:
        return self._runs[-limit:]
