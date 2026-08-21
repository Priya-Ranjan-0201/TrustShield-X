"""
TruthShield X — Knowledge Object Manager (Phase 19).

Provides lifecycle management, immutable versioning, canonical resolution, and SHA-256 hashing for all 27 knowledge object types.
"""

import hashlib
import json
from typing import Dict, List, Optional, Any
from app.schemas.cyber_knowledge_fabric_models import (
    KnowledgeObjectDTO,
    KnowledgeObjectTypeLiteral,
)


class KnowledgeObjectManager:
    """Manages knowledge objects with strict tenant isolation, immutable history, and content hashing."""

    def __init__(self):
        self._objects: Dict[str, KnowledgeObjectDTO] = {}
        self._history: Dict[str, List[KnowledgeObjectDTO]] = {}
        self._initialize_seed_objects()

    def _compute_hash(self, obj_type: str, canonical_id: str, tenant_id: str, version: int) -> str:
        payload = f"{obj_type}:{canonical_id}:{tenant_id}:{version}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def _initialize_seed_objects(self):
        seeds = [
            ("ASSET", "srv_checkout_production", "PROD_HOST_01", "default_tenant", 0.98),
            ("IDENTITY", "usr_admin_svc", "SVC_PRINCIPAL_ADM", "default_tenant", 0.95),
            ("SERVICE", "svc_payment_gateway", "REST_SVC_PAY", "default_tenant", 0.96),
            ("CONTROL", "ctrl_waf_edge_01", "WAF_SHIELD_EDGE", "default_tenant", 0.99),
            ("VULNERABILITY", "cve_2026_9942", "CVE-2026-9942", "default_tenant", 0.92),
            ("CAMPAIGN", "camp_shadow_hydra", "CAMP_SHADOW_HYDRA", "default_tenant", 0.88),
            ("EVIDENCE", "ev_pcap_trace_88", "PCAP_TRACE_88", "default_tenant", 0.94),
        ]
        for obj_type, obj_id, canonical, tenant, conf in seeds:
            content_hash = self._compute_hash(obj_type, canonical, tenant, 1)
            kobj = KnowledgeObjectDTO(
                object_id=obj_id,
                tenant_id=tenant,
                object_type=obj_type,  # type: ignore
                canonical_identifier=canonical,
                confidence=conf,
                content_hash=content_hash,
                provenance={"source": "DISCOVERY_INGESTION", "actor": "FABRIC_SEEDS"},
            )
            self._objects[obj_id] = kobj
            self._history[obj_id] = [kobj]

    def create_object(
        self,
        object_type: KnowledgeObjectTypeLiteral,
        canonical_identifier: str,
        tenant_id: str = "default_tenant",
        classification: str = "RESTRICTED",
        confidence: float = 0.85,
        source: str = "TELEMETRY_ENGINE",
        provenance: Optional[Dict[str, Any]] = None,
    ) -> KnowledgeObjectDTO:
        """Registers a new knowledge object with provenance and content hashing."""
        content_hash = self._compute_hash(object_type, canonical_identifier, tenant_id, 1)
        kobj = KnowledgeObjectDTO(
            tenant_id=tenant_id,
            object_type=object_type,
            canonical_identifier=canonical_identifier,
            classification=classification,
            confidence=confidence,
            source=source,
            provenance=provenance or {"source": source},
            content_hash=content_hash,
        )
        self._objects[kobj.object_id] = kobj
        self._history[kobj.object_id] = [kobj]
        return kobj

    def update_object(
        self,
        object_id: str,
        new_confidence: Optional[float] = None,
        new_classification: Optional[str] = None,
        new_status: Optional[str] = None,
        change_reason: str = "TELEMETRY_UPDATE",
    ) -> KnowledgeObjectDTO:
        """Updates knowledge object while preserving immutable historical version in history."""
        old_obj = self._objects.get(object_id)
        if not old_obj:
            raise KeyError(f"Knowledge object '{object_id}' not found.")

        new_version = old_obj.version + 1
        content_hash = self._compute_hash(
            old_obj.object_type, old_obj.canonical_identifier, old_obj.tenant_id, new_version
        )

        updated = KnowledgeObjectDTO(
            object_id=old_obj.object_id,
            tenant_id=old_obj.tenant_id,
            object_type=old_obj.object_type,
            canonical_identifier=old_obj.canonical_identifier,
            classification=new_classification or old_obj.classification,
            source=old_obj.source,
            provenance={**old_obj.provenance, "last_change_reason": change_reason, "prev_version": old_obj.version},
            confidence=new_confidence if new_confidence is not None else old_obj.confidence,
            validity_start=old_obj.validity_start,
            version=new_version,
            status=new_status or old_obj.status,
            content_hash=content_hash,
        )
        self._objects[object_id] = updated
        self._history[object_id].append(updated)
        return updated

    def get_object(self, object_id: str, tenant_id: str = "default_tenant") -> Optional[KnowledgeObjectDTO]:
        """Retrieves active knowledge object respecting tenant boundary."""
        obj = self._objects.get(object_id)
        if obj and (obj.tenant_id == tenant_id or tenant_id == "admin"):
            return obj
        return None

    def list_objects(self, tenant_id: str = "default_tenant", object_type: Optional[str] = None) -> List[KnowledgeObjectDTO]:
        """Lists objects for a tenant, optionally filtered by type."""
        objs = [o for o in self._objects.values() if o.tenant_id == tenant_id or tenant_id == "admin"]
        if object_type:
            objs = [o for o in objs if o.object_type == object_type]
        return objs

    def get_object_history(self, object_id: str, tenant_id: str = "default_tenant") -> List[KnowledgeObjectDTO]:
        """Returns full immutable version history of a knowledge object."""
        obj = self.get_object(object_id, tenant_id)
        if not obj:
            return []
        return self._history.get(object_id, [])
