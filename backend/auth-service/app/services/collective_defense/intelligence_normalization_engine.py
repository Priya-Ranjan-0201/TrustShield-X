"""
TruthShield X — Intelligence Normalization & Deduplication Engine (Phase 16).

Transforms threat indicators into canonical format, computes deterministic hashes,
and deduplicates objects while preserving multi-source provenance.
"""

from typing import Dict, Any, Optional, Tuple, List
import hashlib
import re
from datetime import datetime, timezone
from urllib.parse import urlparse

from app.schemas.collective_defense_models import (
    ThreatIntelligenceObjectDTO,
    IntelligenceTypeLiteral,
)


class IntelligenceNormalizationEngine:
    """Canonicalizes indicators, creates deterministic hashes, and merges provenance."""

    def __init__(self):
        # Index: content_hash -> ThreatIntelligenceObjectDTO
        self._canonical_store: Dict[str, ThreatIntelligenceObjectDTO] = {}

    def normalize_indicator(self, indicator_type: IntelligenceTypeLiteral, raw_value: str) -> str:
        """Normalizes an indicator value to its canonical representation."""
        val = raw_value.strip()

        if indicator_type == "DOMAIN":
            return val.lower().rstrip(".")
        elif indicator_type == "URL":
            parsed = urlparse(val)
            netloc = parsed.netloc.lower()
            path = parsed.path.rstrip("/") if parsed.path != "/" else "/"
            scheme = parsed.scheme.lower() if parsed.scheme else "https"
            return f"{scheme}://{netloc}{path}"
        elif indicator_type == "IP":
            return val.split(":")[0].strip() if ":" in val and not val.count(":") > 1 else val
        elif indicator_type in ("FILE_HASH", "APK_SIGNATURE", "CERTIFICATE"):
            return val.lower().replace(":", "").replace(" ", "")
        elif indicator_type == "EMAIL_INDICATOR":
            return val.lower()
        elif indicator_type == "PHONE_IDENTIFIER":
            return re.sub(r"[^\d+]", "", val)
        elif indicator_type == "PAYMENT_IDENTIFIER":
            return val.lower().strip()
        elif indicator_type == "QR_INDICATOR":
            return val.strip()
        else:
            return val.strip()

    def compute_content_hash(self, indicator_type: IntelligenceTypeLiteral, canonical_id: str) -> str:
        """Computes deterministic SHA-256 content hash."""
        seed = f"{indicator_type}:{canonical_id}".encode("utf-8")
        return hashlib.sha256(seed).hexdigest()

    def ingest_or_merge(
        self,
        raw_obj: ThreatIntelligenceObjectDTO,
        source_id: str,
        source_reliability: float = 0.85,
    ) -> Tuple[ThreatIntelligenceObjectDTO, bool]:
        """Normalizes and either stores new or merges into existing object with provenance preservation.

        Returns: (object, is_new)
        """
        canonical_id = self.normalize_indicator(raw_obj.intelligence_type, raw_obj.raw_indicator or raw_obj.canonical_identifier)
        content_hash = self.compute_content_hash(raw_obj.intelligence_type, canonical_id)

        raw_obj.canonical_identifier = canonical_id
        raw_obj.content_hash = content_hash

        if content_hash in self._canonical_store:
            existing = self._canonical_store[content_hash]
            # Merge provenance (Section 9, 10)
            history = existing.provenance.get("source_history", [])
            history.append({
                "source_id": source_id,
                "submitted_at": datetime.now(timezone.utc).isoformat(),
                "reliability": source_reliability,
                "initial_confidence": raw_obj.confidence,
            })
            existing.provenance["source_history"] = history

            # Update multi-source confidence without blind overwriting
            existing.confidence = min(0.99, max(existing.confidence, raw_obj.confidence) + 0.05)
            existing.version += 1
            existing.validation_state = "CORRELATED"
            return existing, False

        # First-time submission
        raw_obj.provenance = {
            "origin_source_id": source_id,
            "first_submitted_at": datetime.now(timezone.utc).isoformat(),
            "source_history": [{
                "source_id": source_id,
                "submitted_at": datetime.now(timezone.utc).isoformat(),
                "reliability": source_reliability,
                "initial_confidence": raw_obj.confidence,
            }],
        }
        self._canonical_store[content_hash] = raw_obj
        return raw_obj, True

    def get_by_hash(self, content_hash: str) -> Optional[ThreatIntelligenceObjectDTO]:
        """Retrieves an object by its canonical content hash."""
        return self._canonical_store.get(content_hash)

    def list_all(self) -> List[ThreatIntelligenceObjectDTO]:
        """Lists all canonical normalized intelligence objects."""
        return list(self._canonical_store.values())
