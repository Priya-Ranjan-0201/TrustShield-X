"""
TruthShield X — Continuous Change Detection Engine
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.exposure_models import (
    AssetChangeDTO,
    AssetBaselineDTO,
    AssetObservationDTO,
    ChangeClassificationLiteral,
)


class ChangeDetectionEngine:
    """Compares incoming observations against established baselines to detect and classify changes."""

    def __init__(self):
        # tenant_id -> change_id -> AssetChangeDTO
        self._changes: Dict[str, Dict[str, AssetChangeDTO]] = {}
        # tenant_id -> asset_id -> List[change_id]
        self._asset_changes: Dict[str, Dict[str, List[str]]] = {}

    def evaluate_observation(
        self,
        observation: AssetObservationDTO,
        baseline: Optional[AssetBaselineDTO],
    ) -> List[AssetChangeDTO]:
        """Evaluates an observation against a baseline, returning all detected changes."""
        tenant_id = observation.tenant_id
        asset_id = observation.asset_id
        detected_changes: List[AssetChangeDTO] = []

        if not baseline:
            # First observation, no prior baseline exists -> Informational Initial State
            return detected_changes

        obs_data = observation.observed_data

        # 1. Check DNS changes
        if "dns_records" in obs_data and baseline.dns_records:
            if obs_data["dns_records"] != baseline.dns_records:
                cls: ChangeClassificationLiteral = "SUSPICIOUS" if "nameserver" in str(obs_data["dns_records"]) else "INFORMATIONAL"
                chg = self._create_change(
                    asset_id=asset_id,
                    tenant_id=tenant_id,
                    change_type="DNS_RECORD_MUTATION",
                    classification=cls,
                    previous_state=baseline.dns_records,
                    new_state=obs_data["dns_records"],
                    confidence=observation.confidence,
                )
                detected_changes.append(chg)

        # 2. Check TLS Certificate changes
        if "tls_certificate" in obs_data and baseline.tls_certificate:
            obs_cert = obs_data["tls_certificate"]
            base_cert = baseline.tls_certificate
            if obs_cert.get("fingerprint_sha256") != base_cert.get("fingerprint_sha256"):
                # Is it an unexpected issuer or self-signed?
                is_suspicious = obs_cert.get("issuer") != base_cert.get("issuer")
                cls = "SUSPICIOUS" if is_suspicious else "BENIGN"
                chg = self._create_change(
                    asset_id=asset_id,
                    tenant_id=tenant_id,
                    change_type="TLS_CERTIFICATE_ROTATION",
                    classification=cls,
                    previous_state=base_cert,
                    new_state=obs_cert,
                    confidence=observation.confidence,
                )
                detected_changes.append(chg)

        # 3. Check Newly Exposed Ports
        if "exposed_ports" in obs_data and baseline.exposed_ports is not None:
            obs_ports = set(obs_data["exposed_ports"])
            base_ports = set(baseline.exposed_ports)
            new_ports = list(obs_ports - base_ports)
            if new_ports:
                cls = "HIGH_RISK" if any(p in (22, 3389, 445, 1433, 27017) for p in new_ports) else "SUSPICIOUS"
                chg = self._create_change(
                    asset_id=asset_id,
                    tenant_id=tenant_id,
                    change_type="NEW_EXPOSED_PORTS_DETECTED",
                    classification=cls,
                    previous_state={"exposed_ports": list(base_ports)},
                    new_state={"exposed_ports": list(obs_ports), "newly_opened": new_ports},
                    confidence=observation.confidence,
                )
                detected_changes.append(chg)

        # 4. Check Campaign Association Emergence
        if "associated_campaign" in obs_data:
            chg = self._create_change(
                asset_id=asset_id,
                tenant_id=tenant_id,
                change_type="NEW_CAMPAIGN_ASSOCIATION",
                classification="CRITICAL",
                previous_state={"associated_campaign": None},
                new_state={"associated_campaign": obs_data["associated_campaign"]},
                confidence=observation.confidence,
            )
            detected_changes.append(chg)

        return detected_changes

    def _create_change(
        self,
        asset_id: str,
        tenant_id: str,
        change_type: str,
        classification: ChangeClassificationLiteral,
        previous_state: Dict[str, Any],
        new_state: Dict[str, Any],
        confidence: float,
    ) -> AssetChangeDTO:
        change_id = f"chg_{uuid.uuid4().hex[:12]}"
        evidence_id = f"ev_chg_{uuid.uuid4().hex[:8]}"

        change = AssetChangeDTO(
            change_id=change_id,
            asset_id=asset_id,
            tenant_id=tenant_id,
            change_type=change_type,
            classification=classification,
            previous_state=previous_state,
            new_state=new_state,
            evidence_id=evidence_id,
            confidence=confidence,
            detected_at=datetime.now(timezone.utc).isoformat(),
        )

        if tenant_id not in self._changes:
            self._changes[tenant_id] = {}
            self._asset_changes[tenant_id] = {}
        if asset_id not in self._asset_changes[tenant_id]:
            self._asset_changes[tenant_id][asset_id] = []

        self._changes[tenant_id][change_id] = change
        self._asset_changes[tenant_id][asset_id].append(change_id)
        return change

    def get_changes_for_asset(self, asset_id: str, tenant_id: str = "default_tenant") -> List[AssetChangeDTO]:
        """Retrieves all detected changes for an asset."""
        change_ids = self._asset_changes.get(tenant_id, {}).get(asset_id, [])
        return [self._changes[tenant_id][cid] for cid in change_ids if cid in self._changes.get(tenant_id, {})]
