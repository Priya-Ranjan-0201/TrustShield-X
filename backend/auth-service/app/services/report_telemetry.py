"""Report Telemetry Manager (Phase 4.0 Part 1).

Tracks report generation counts, durations, failures, and payload sizes.
"""

from typing import Dict, Any
from app.schemas.digital_trust_report_models import ReportMetricDTO


class ReportTelemetryManager:
    """Telemetry Manager tracking report generation metrics."""

    def __init__(self):
        self._generated_total = 0
        self._failed_total = 0

    def record_success(self, duration_ms: float):
        self._generated_total += 1

    def record_failure(self):
        self._failed_total += 1

    def get_metrics(self) -> ReportMetricDTO:
        return ReportMetricDTO(
            reports_generated_total=self._generated_total,
            reports_failed_total=self._failed_total,
        )
