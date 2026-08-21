"""
TruthShield X — Asset Baseline Engine
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.exposure_models import AssetBaselineDTO


class AssetBaselineEngine:
    """Establishes, versions, and manages known-good operational baselines for monitored assets."""

    def __init__(self):
        # tenant_id -> asset_id -> List[AssetBaselineDTO] (history)
        self._baselines: Dict[str, Dict[str, List[AssetBaselineDTO]]] = {}

    def establish_baseline(
        self,
        asset_id: str,
        dns_records: Optional[Dict[str, Any]] = None,
        tls_certificate: Optional[Dict[str, Any]] = None,
        http_headers: Optional[Dict[str, Any]] = None,
        exposed_ports: Optional[List[int]] = None,
        technologies: Optional[List[str]] = None,
        trust_score: float = 85.0,
        risk_score: float = 15.0,
        exposure_score: float = 20.0,
        known_relationships: Optional[List[str]] = None,
        tenant_id: str = "default_tenant",
    ) -> AssetBaselineDTO:
        """Establishes or increments an asset's known-good configuration baseline."""
        if tenant_id not in self._baselines:
            self._baselines[tenant_id] = {}
        if asset_id not in self._baselines[tenant_id]:
            self._baselines[tenant_id][asset_id] = []

        history = self._baselines[tenant_id][asset_id]
        next_version = len(history) + 1
        baseline_id = f"base_{uuid.uuid4().hex[:12]}"

        baseline = AssetBaselineDTO(
            baseline_id=baseline_id,
            asset_id=asset_id,
            tenant_id=tenant_id,
            version=next_version,
            dns_records=dns_records or {},
            tls_certificate=tls_certificate or {},
            http_headers=http_headers or {},
            exposed_ports=exposed_ports or [],
            technologies=technologies or [],
            trust_score_baseline=trust_score,
            risk_score_baseline=risk_score,
            exposure_score_baseline=exposure_score,
            known_relationships=known_relationships or [],
            established_at=datetime.now(timezone.utc).isoformat(),
        )

        history.append(baseline)
        return baseline

    def get_latest_baseline(self, asset_id: str, tenant_id: str = "default_tenant") -> Optional[AssetBaselineDTO]:
        """Retrieves the most recent baseline for an asset."""
        history = self._baselines.get(tenant_id, {}).get(asset_id, [])
        return history[-1] if history else None

    def get_baseline_history(self, asset_id: str, tenant_id: str = "default_tenant") -> List[AssetBaselineDTO]:
        """Retrieves all historical baselines for an asset."""
        return self._baselines.get(tenant_id, {}).get(asset_id, [])
