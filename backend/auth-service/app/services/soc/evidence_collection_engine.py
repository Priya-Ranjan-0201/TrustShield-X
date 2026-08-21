"""Evidence Collection & Chain-of-Custody Engine (Phase 4.0 Part 7 — Sections 63-65).

Collects digital forensic evidence with SHA-256 integrity hashing and auditable custody tracking.
"""

from typing import List, Dict, Any, Optional, Tuple
import hashlib
import uuid
from datetime import datetime, timezone
from app.schemas.soc_operations_models import EvidenceCollectionRecordDTO


class EvidenceCollectionEngine:
    """Collects and verifies digital evidence records for SOC investigations."""

    def __init__(self):
        self._records: Dict[str, EvidenceCollectionRecordDTO] = {}
        self._raw_evidence: Dict[str, bytes] = {}

    def collect_evidence(
        self,
        incident_id: str,
        source: str,
        collector_id: str,
        evidence_type: str,
        raw_data: bytes,
        collection_method: str = "SECURE_API_PULL",
    ) -> EvidenceCollectionRecordDTO:
        sha256 = hashlib.sha256(raw_data).hexdigest()
        storage_ref = f"evidence/{incident_id}/{uuid.uuid4().hex[:8]}.dat"

        now_str = datetime.now(timezone.utc).isoformat()
        rec = EvidenceCollectionRecordDTO(
            collection_id=f"evc_{uuid.uuid4().hex[:12]}",
            incident_id=incident_id,
            source=source,
            collector_id=collector_id,
            evidence_type=evidence_type,
            sha256_hash=sha256,
            storage_reference=storage_ref,
            integrity_status="VERIFIED",
            collection_method=collection_method,
            access_log=[{
                "actor": collector_id,
                "action": "COLLECT",
                "timestamp": now_str,
            }],
        )

        self._records[rec.collection_id] = rec
        self._raw_evidence[rec.collection_id] = raw_data
        return rec

    def verify_evidence_integrity(self, collection_id: str, current_data: bytes) -> bool:
        """Verifies current evidence bytes against stored SHA-256 hash (Section 65, Mandatory Test 38)."""
        rec = self._records.get(collection_id)
        if not rec:
            raise KeyError(f"Evidence {collection_id} not found.")

        current_hash = hashlib.sha256(current_data).hexdigest()
        is_valid = (current_hash == rec.sha256_hash)
        rec.integrity_status = "VERIFIED" if is_valid else "INTEGRITY_MISMATCH"
        return is_valid

    def access_evidence(self, collection_id: str, reader_id: str) -> Optional[EvidenceCollectionRecordDTO]:
        rec = self._records.get(collection_id)
        if rec:
            rec.access_log.append({
                "actor": reader_id,
                "action": "READ",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
        return rec

    def get_evidence_record(self, collection_id: str) -> Optional[EvidenceCollectionRecordDTO]:
        return self._records.get(collection_id)

    def list_incident_evidence(self, incident_id: str) -> List[EvidenceCollectionRecordDTO]:
        return [r for r in self._records.values() if r.incident_id == incident_id]
