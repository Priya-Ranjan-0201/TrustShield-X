"""Inbound Threat Feed Validation & Normalization Pipeline (Phase 4.0 Part 6 — Sections 8, 14, 15, 90, 91).

Enforces schema validation, resource limits (MAX_FEED_SIZE), entity normalization,
and deterministic deduplication.
"""

from typing import List, Dict, Any, Tuple, Optional
import hashlib
from datetime import datetime, timezone
from app.schemas.continuous_intelligence_models import (
    IntelligenceObservationDTO,
    ThreatFeedConfigurationDTO,
)
from app.services.graph.entity_normalizer import EntityNormalizer

# Maximum payload size: 50MB (Section 91)
MAX_FEED_SIZE_BYTES = 50 * 1024 * 1024
MAX_BATCH_SIZE = 100000


class FeedValidationError(Exception):
    """Raised when an intelligence payload fails security or schema validation."""
    pass


class FeedValidator:
    """Validates, normalizes, and deduplicates incoming feed records."""

    @staticmethod
    def validate_feed_size(payload_bytes: bytes, max_bytes: int = MAX_FEED_SIZE_BYTES) -> None:
        """Reject maliciously oversized feeds."""
        if len(payload_bytes) > max_bytes:
            raise FeedValidationError(
                f"Feed payload size ({len(payload_bytes)} bytes) exceeds MAX_FEED_SIZE ({max_bytes} bytes)."
            )

    @staticmethod
    def validate_and_normalize_item(
        feed_config: ThreatFeedConfigurationDTO,
        raw_item: Dict[str, Any],
    ) -> Optional[IntelligenceObservationDTO]:
        """Validate an individual feed item, normalize it, and produce an IntelligenceObservationDTO."""
        indicator_id = raw_item.get("indicator_id") or raw_item.get("id")
        indicator_type = (raw_item.get("indicator_type") or raw_item.get("type") or "").upper()
        raw_value = raw_item.get("raw_value") or raw_item.get("value") or raw_item.get("indicator") or ""

        if not indicator_id or not indicator_type or not raw_value:
            return None

        # Re-use Phase 4.0 Part 5 EntityNormalizer (Section 14)
        normalized_value, display_value, value_hash = FeedValidator._normalize(indicator_type, str(raw_value))

        obs_type = raw_item.get("observation_type", "NEW")
        classification = raw_item.get("classification", "MALICIOUS")
        confidence = raw_item.get("confidence", "HIGH")
        feed_ver = raw_item.get("feed_version", "1.0.0")

        return IntelligenceObservationDTO(
            observation_id=f"obs_{hashlib.sha256(f'{feed_config.feed_id}:{indicator_type}:{value_hash}'.encode()).hexdigest()[:16]}",
            feed_id=feed_config.feed_id,
            indicator_id=str(indicator_id),
            indicator_type=indicator_type,
            indicator_value_hash=value_hash,
            normalized_value=normalized_value,
            raw_value=str(raw_value),
            observation_type=obs_type,
            classification=classification,
            confidence=confidence,
            feed_version=feed_ver,
            status="ACTIVE" if obs_type != "REVOKED" else "REVOKED",
        )

    @staticmethod
    def _normalize(indicator_type: str, raw_value: str) -> Tuple[str, str, str]:
        """Normalize using canonical entity normalizer."""
        if indicator_type in ("DOMAIN", "HOSTNAME"):
            return EntityNormalizer.normalize_domain(raw_value)
        elif indicator_type == "URL":
            return EntityNormalizer.normalize_url(raw_value)
        elif indicator_type in ("IPv4", "IPv6", "IP", "IP_ADDRESS"):
            return EntityNormalizer.normalize_ip(raw_value)
        elif indicator_type in ("HASH", "SHA256", "MD5", "SHA1"):
            return EntityNormalizer.normalize_hash(raw_value)
        elif indicator_type == "CERTIFICATE":
            return EntityNormalizer.normalize_certificate(raw_value)
        elif indicator_type in ("PACKAGE", "APPLICATION"):
            return EntityNormalizer.normalize_package(raw_value)
        elif indicator_type == "PHONE":
            return EntityNormalizer.normalize_phone(raw_value)
        elif indicator_type == "EMAIL":
            return EntityNormalizer.normalize_email(raw_value)
        elif indicator_type in ("UPI", "UPI_ID"):
            return EntityNormalizer.normalize_upi(raw_value)
        else:
            canon = raw_value.strip().lower()
            val_hash = hashlib.sha256(canon.encode()).hexdigest()
            return canon, raw_value.strip(), val_hash

    @staticmethod
    def deduplicate_observations(
        observations: List[IntelligenceObservationDTO],
    ) -> List[IntelligenceObservationDTO]:
        """Deterministic deduplication by (feed_id, indicator_type, indicator_value_hash) (Section 15)."""
        seen: Dict[str, IntelligenceObservationDTO] = {}
        for obs in observations:
            key = f"{obs.feed_id}:{obs.indicator_type}:{obs.indicator_value_hash}"
            if key not in seen:
                seen[key] = obs
            else:
                # Update observation last_seen
                seen[key].last_seen = obs.last_seen
        return list(seen.values())
