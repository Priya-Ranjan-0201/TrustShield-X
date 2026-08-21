"""
TruthShield X — Indicator Intelligence Engine (Phase 33).

Normalizes and governs atomic indicators (IOC), Indicators of Attack (IOA),
and Indicators of Behavior (IOB) with strict canonical hashing and lifecycle transitions.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import hashlib
import re

from app.schemas.threat_intelligence_fusion_models import IndicatorDTO


class IndicatorIntelligenceEngine:
    """Manages atomic, behavioral, and context-rich indicators."""

    def __init__(self):
        self._indicators: Dict[str, IndicatorDTO] = {}
        self._seed_default_indicators()

    def _seed_default_indicators(self):
        ind_c2 = self.register_indicator(
            raw_value="HTTP://Malicious-C2.Darkstorm-Threat.COM/beacon ",
            indicator_type="URL",
            sources=["src_fs_isac_feed"],
            related_campaigns=["cmp_darkstorm_apac"],
            related_actors=["act_apt_ember_bear"],
            related_malware=["mal_cobalt_beacon"],
            related_techniques=["T1071.001"],
            affected_assets=["ast_payment_gw_01"],
            confidence=0.92,
        )
        ind_hash = self.register_indicator(
            raw_value="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            indicator_type="HASH",
            sources=["src_cert_in_advisory"],
            related_malware=["mal_ransom_blackshadow"],
            confidence=0.98,
        )

    def normalize_value(self, raw_value: str, indicator_type: str) -> str:
        """Applies type-specific canonical normalization."""
        cleaned = raw_value.strip()
        if indicator_type in ("DOMAIN", "EMAIL"):
            return cleaned.lower()
        elif indicator_type == "URL":
            # Lowercase scheme and domain, strip trailing slashes
            url_norm = cleaned.lower()
            return re.sub(r"/+$", "", url_norm)
        elif indicator_type == "HASH":
            return cleaned.lower()
        elif indicator_type in ("IPv4", "IPv6"):
            return cleaned.lower()
        return cleaned

    def register_indicator(
        self,
        raw_value: str,
        indicator_type: str,
        sources: Optional[List[str]] = None,
        related_campaigns: Optional[List[str]] = None,
        related_actors: Optional[List[str]] = None,
        related_malware: Optional[List[str]] = None,
        related_techniques: Optional[List[str]] = None,
        affected_assets: Optional[List[str]] = None,
        confidence: float = 0.80,
        behavior_type: Optional[str] = None,
    ) -> IndicatorDTO:
        normalized = self.normalize_value(raw_value, indicator_type)
        canonical_hash = hashlib.sha256(f"{indicator_type}:{normalized}".encode("utf-8")).hexdigest()
        indicator_id = f"ind_{canonical_hash[:12]}"

        sources = sources or []
        dto = IndicatorDTO(
            indicator_id=indicator_id,
            indicator_type=indicator_type,
            raw_value=raw_value,
            normalized_value=normalized,
            canonical_hash=canonical_hash,
            status="ACTIVE",
            confidence=confidence,
            source_count=len(sources) if sources else 1,
            sources=sources,
            related_campaigns=related_campaigns or [],
            related_actors=related_actors or [],
            related_malware=related_malware or [],
            related_techniques=related_techniques or [],
            affected_assets=affected_assets or [],
            first_seen=datetime.now(timezone.utc).isoformat(),
            last_seen=datetime.now(timezone.utc).isoformat(),
            behavior_type=behavior_type,
        )
        self._indicators[indicator_id] = dto
        return dto

    def get_indicator(self, indicator_id: str) -> Optional[IndicatorDTO]:
        return self._indicators.get(indicator_id)

    def list_indicators(self, status: Optional[str] = None) -> List[IndicatorDTO]:
        inds = list(self._indicators.values())
        if status:
            inds = [i for i in inds if i.status == status]
        return inds

    def evaluate_indicator_quality(self, indicator_id: str, days_since_last_seen: int = 0) -> Dict[str, Any]:
        ind = self._indicators.get(indicator_id)
        if not ind:
            return {"status": "NOT_FOUND"}

        quality_state = "ACTIVE"
        if days_since_last_seen > 180:
            quality_state = "STALE"
            ind.status = "EXPIRED"
        elif ind.confidence < 0.50:
            quality_state = "LOW_CONFIDENCE"
        elif ind.confidence >= 0.90 and ind.source_count >= 2:
            quality_state = "VERIFIED"

        return {
            "indicator_id": indicator_id,
            "quality_state": quality_state,
            "confidence": ind.confidence,
            "source_count": ind.source_count,
            "status": ind.status,
        }
