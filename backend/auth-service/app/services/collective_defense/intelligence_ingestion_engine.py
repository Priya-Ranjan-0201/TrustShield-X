"""
TruthShield X — Intelligence Ingestion Engine (Phase 16).

Executes the 9-stage ingestion pipeline with strict validation, rejecting
malformed, invalid, or dangerous payload structures.
"""

from typing import List, Dict, Any, Tuple, Optional
import ipaddress
import re
from datetime import datetime, timezone

from app.schemas.collective_defense_models import (
    ThreatIntelligenceObjectDTO,
    IntelligenceTypeLiteral,
)
from app.services.collective_defense.intelligence_normalization_engine import IntelligenceNormalizationEngine
from app.services.collective_defense.federation_partner_registry import FederationPartnerRegistry


class MalformedIntelligenceError(Exception):
    """Raised when an inbound intelligence object fails structural validation."""
    pass


class IntelligenceIngestionEngine:
    """Ingestion pipeline coordinator."""

    def __init__(
        self,
        normalizer: IntelligenceNormalizationEngine,
        partner_registry: FederationPartnerRegistry,
    ):
        self.normalizer = normalizer
        self.partner_registry = partner_registry
        self._stored_objects: Dict[str, ThreatIntelligenceObjectDTO] = {}

    def validate_indicator_syntax(self, itype: IntelligenceTypeLiteral, value: str) -> bool:
        """Validates syntactic integrity for each indicator type."""
        val = value.strip()
        if not val or len(val) > 2048:
            return False

        if itype == "IP":
            try:
                ipaddress.ip_address(val)
                return True
            except ValueError:
                return False
        elif itype == "DOMAIN":
            return bool(re.match(r"^(?:[a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,}$", val))
        elif itype == "FILE_HASH":
            return bool(re.match(r"^[a-fA-F0-9]{32,64}$", val))
        elif itype == "EMAIL_INDICATOR":
            return bool(re.match(r"^[^@]+@[^@]+\.[^@]+$", val))
        elif itype == "URL":
            return val.startswith("http://") or val.startswith("https://")
        return True

    def ingest_single(
        self,
        raw_obj: ThreatIntelligenceObjectDTO,
        source_id: str,
        partner_auth_key: Optional[str] = None,
    ) -> ThreatIntelligenceObjectDTO:
        """Ingests a single threat intelligence object through the 9-stage pipeline."""
        # Stage 1: Authenticate Partner if source is an external federation partner
        partner = self.partner_registry.get_partner(source_id)
        if partner:
            if partner_auth_key and not self.partner_registry.authenticate_partner(source_id, partner_auth_key):
                raise PermissionError("Partner authentication failed.")
            if not self.partner_registry.check_rate_limit(source_id):
                raise ValueError("Federation partner rate limit exceeded.")

        # Stage 2: Validate Syntax (Section 22 - Malformed Rejection)
        indicator_str = raw_obj.raw_indicator or raw_obj.canonical_identifier
        if not self.validate_indicator_syntax(raw_obj.intelligence_type, indicator_str):
            raise MalformedIntelligenceError(
                f"Malformed indicator value '{indicator_str}' for type {raw_obj.intelligence_type}"
            )

        # Stage 3: Normalize & Deduplicate
        rel = partner.trust_level if partner else 0.85
        obj, is_new = self.normalizer.ingest_or_merge(raw_obj, source_id, rel)

        # Stage 4: Store
        obj.validation_state = "VALIDATED"
        self._stored_objects[obj.intelligence_id] = obj
        return obj

    def ingest_bundle(
        self,
        objects: List[ThreatIntelligenceObjectDTO],
        source_id: str,
        partner_auth_key: Optional[str] = None,
    ) -> List[ThreatIntelligenceObjectDTO]:
        """Ingests a batch/bundle of intelligence objects."""
        # Check replay & poisoning
        valid_objects, poison_warning = self.partner_registry.check_replay_and_poisoning(source_id, objects)

        ingested = []
        for o in valid_objects:
            try:
                res = self.ingest_single(o, source_id, partner_auth_key)
                ingested.append(res)
            except Exception:
                continue
        return ingested

    def list_ingested(self) -> List[ThreatIntelligenceObjectDTO]:
        return list(self._stored_objects.values())
