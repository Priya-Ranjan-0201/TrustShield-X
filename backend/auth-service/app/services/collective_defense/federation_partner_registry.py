"""
TruthShield X — Federation Partner Registry & Poisoning Defense (Phase 16).

Manages federation partners, authentication, rate limiting, replay defense,
and detects coordinated threat intelligence poisoning attacks.
"""

from typing import Dict, List, Optional, Tuple, Set, Any
import hashlib
from datetime import datetime, timezone

from app.schemas.collective_defense_models import (
    FederationPartnerDTO,
    ThreatIntelligenceObjectDTO,
    PartnerStatusLiteral,
)


class FederationPartnerRegistry:
    """Registry of federated intelligence exchange partners with rate & poisoning guards."""

    def __init__(self):
        self._partners: Dict[str, FederationPartnerDTO] = {}
        self._seen_content_hashes: Set[str] = set()
        self._partner_submission_windows: Dict[str, List[float]] = {}
        self._poisoning_alerts: List[Dict[str, Any]] = []

    def register_partner(
        self,
        name: str,
        trust_level: float = 0.80,
        scopes: Optional[List[str]] = None,
        auth_key: str = "default_secret_key",
        rate_limit: int = 100,
    ) -> FederationPartnerDTO:
        """Registers a new federation exchange partner."""
        key_hash = hashlib.sha256(auth_key.encode()).hexdigest()
        partner = FederationPartnerDTO(
            name=name,
            trust_level=trust_level,
            scopes=scopes or ["threat_indicators", "campaigns"],
            auth_key_hash=key_hash,
            rate_limit_per_minute=rate_limit,
        )
        self._partners[partner.partner_id] = partner
        self._partner_submission_windows[partner.partner_id] = []
        return partner

    def authenticate_partner(self, partner_id: str, provided_key: str) -> bool:
        """Validates partner credentials against salted hash."""
        partner = self._partners.get(partner_id)
        if not partner or partner.status != "ACTIVE":
            return False
        return partner.auth_key_hash == hashlib.sha256(provided_key.encode()).hexdigest()

    def check_rate_limit(self, partner_id: str) -> bool:
        """Enforces sliding-window rate limiting."""
        partner = self._partners.get(partner_id)
        if not partner:
            return False

        now_ts = datetime.now(timezone.utc).timestamp()
        window = self._partner_submission_windows.get(partner_id, [])
        # Keep only events in last 60 seconds
        window = [t for t in window if now_ts - t < 60.0]
        self._partner_submission_windows[partner_id] = window

        if len(window) >= partner.rate_limit_per_minute:
            return False

        window.append(now_ts)
        partner.current_minute_requests = len(window)
        return True

    def check_replay_and_poisoning(
        self,
        partner_id: str,
        objects: List[ThreatIntelligenceObjectDTO],
    ) -> Tuple[List[ThreatIntelligenceObjectDTO], Optional[str]]:
        """Filters replayed items and checks for intelligence poisoning spikes."""
        partner = self._partners.get(partner_id)
        if not partner:
            return [], "UNKNOWN_PARTNER"

        # 1. Poisoning detection (Section 23 - Sudden flood or duplicate flooding)
        if len(objects) > 500:
            warning = f"INTELLIGENCE_POISONING_WARNING: Sudden anomalous surge of {len(objects)} indicators from partner {partner.name}"
            self._poisoning_alerts.append({
                "partner_id": partner_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "warning": warning,
            })
            partner.trust_level = max(0.1, partner.trust_level - 0.2)
            partner.status = "PROBATION"

        # 2. Replay detection (Section 25)
        new_objects: List[ThreatIntelligenceObjectDTO] = []
        for obj in objects:
            ident = obj.canonical_identifier or obj.raw_indicator
            h = obj.content_hash or hashlib.sha256(f"{obj.intelligence_type}:{ident}".encode()).hexdigest()
            if h in self._seen_content_hashes:
                # Replay detected — do not duplicate
                continue
            self._seen_content_hashes.add(h)
            new_objects.append(obj)

        partner.total_received += len(objects)
        partner.total_rejected += (len(objects) - len(new_objects))
        partner.last_sync = datetime.now(timezone.utc).isoformat()

        return new_objects, None

    def get_partner(self, partner_id: str) -> Optional[FederationPartnerDTO]:
        return self._partners.get(partner_id)

    def list_partners(self) -> List[FederationPartnerDTO]:
        return list(self._partners.values())

    def list_poisoning_alerts(self) -> List[Dict[str, Any]]:
        return self._poisoning_alerts
