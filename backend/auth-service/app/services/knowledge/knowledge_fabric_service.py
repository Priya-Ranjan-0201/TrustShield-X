"""Digital Trust Knowledge Fabric Service (Phase 7 - Sections 2-9, 21, 36-39).

Unifies canonical entities, evidence, incidents, campaigns, predictions, threat signals,
responses, reports, and audit events into a versioned, snapshot-capable knowledge fabric.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import copy
import uuid

from app.schemas.knowledge_fabric_models import (
    KnowledgeObjectDTO,
    KnowledgeRelationshipDTO,
    EvidenceLineageDTO,
    EvidenceChainDTO,
    KnowledgeVersionDTO,
    KnowledgeSnapshotDTO,
    KnowledgeDiffDTO,
    KnowledgeObjectTypeLiteral,
    RelationshipTypeLiteral,
)


class KnowledgeFabricService:
    """Core knowledge fabric managing knowledge objects, relationships, lineage, versioning, snapshots, and diffs."""

    def __init__(self):
        # In-memory stores partitioned by tenant_id
        self._objects: Dict[str, Dict[str, KnowledgeObjectDTO]] = {}  # tenant_id -> object_id -> object
        self._relationships: Dict[str, Dict[str, KnowledgeRelationshipDTO]] = {}  # tenant_id -> rel_id -> rel
        self._lineages: Dict[str, Dict[str, EvidenceLineageDTO]] = {}  # tenant_id -> lineage_id -> lineage
        self._versions: Dict[str, List[KnowledgeVersionDTO]] = {}  # object_id -> versions
        self._snapshots: Dict[str, Dict[str, KnowledgeSnapshotDTO]] = {}  # tenant_id -> snapshot_id -> snapshot

    # -----------------------------------------------------------------------
    # Section 3: Canonical Knowledge Object Management
    # -----------------------------------------------------------------------

    def register_object(
        self,
        object_type: KnowledgeObjectTypeLiteral,
        canonical_reference: str,
        tenant_id: str = "default_tenant",
        classification: str = "RESTRICTED",
        confidence: float = 0.85,
        provenance: Optional[Dict[str, Any]] = None,
        first_seen: Optional[str] = None,
        last_seen: Optional[str] = None,
    ) -> KnowledgeObjectDTO:
        """Registers or updates a canonical knowledge object."""
        if tenant_id not in self._objects:
            self._objects[tenant_id] = {}

        now_iso = datetime.now(timezone.utc).isoformat()
        kobj_id = f"kobj_{uuid.uuid4().hex[:12]}"

        obj = KnowledgeObjectDTO(
            knowledge_object_id=kobj_id,
            object_type=object_type,
            canonical_reference=canonical_reference,
            tenant_id=tenant_id,
            classification=classification,
            confidence=confidence,
            provenance=provenance or {},
            first_seen=first_seen or now_iso,
            last_seen=last_seen or now_iso,
            version=1,
            created_at=now_iso,
            updated_at=now_iso,
        )

        self._objects[tenant_id][kobj_id] = obj

        # Initialize version history
        ver = KnowledgeVersionDTO(
            knowledge_object_id=kobj_id,
            version=1,
            previous_version=None,
            changed_fields=["initial_registration"],
            change_reason="Initial registration in knowledge fabric",
            changed_by="KNOWLEDGE_FABRIC_ENGINE",
            snapshot_data=obj.model_dump(),
            timestamp=now_iso,
        )
        self._versions[kobj_id] = [ver]

        return obj

    def get_object(self, object_id: str, tenant_id: str = "default_tenant") -> Optional[KnowledgeObjectDTO]:
        """Retrieves a knowledge object within tenant boundaries."""
        return self._objects.get(tenant_id, {}).get(object_id)

    def find_objects_by_reference(
        self,
        canonical_reference: str,
        tenant_id: str = "default_tenant",
    ) -> List[KnowledgeObjectDTO]:
        """Finds knowledge objects matching a canonical reference within tenant context."""
        tenant_objs = self._objects.get(tenant_id, {})
        return [o for o in tenant_objs.values() if o.canonical_reference == canonical_reference]

    def update_object_confidence(
        self,
        object_id: str,
        new_confidence: float,
        reason: str,
        updated_by: str,
        tenant_id: str = "default_tenant",
    ) -> KnowledgeObjectDTO:
        """Updates confidence of a knowledge object, recording version history without silent overwrite."""
        obj = self.get_object(object_id, tenant_id)
        if not obj:
            raise KeyError(f"Knowledge object '{object_id}' not found for tenant '{tenant_id}'.")

        now_iso = datetime.now(timezone.utc).isoformat()
        new_version_num = obj.version + 1

        updated_obj = KnowledgeObjectDTO(
            knowledge_object_id=obj.knowledge_object_id,
            object_type=obj.object_type,
            canonical_reference=obj.canonical_reference,
            tenant_id=obj.tenant_id,
            classification=obj.classification,
            confidence=new_confidence,
            provenance=obj.provenance,
            first_seen=obj.first_seen,
            last_seen=now_iso,
            version=new_version_num,
            created_at=obj.created_at,
            updated_at=now_iso,
        )

        self._objects[tenant_id][object_id] = updated_obj

        # Record version
        ver = KnowledgeVersionDTO(
            knowledge_object_id=object_id,
            version=new_version_num,
            previous_version=obj.version,
            changed_fields=["confidence", "last_seen", "updated_at"],
            change_reason=reason,
            changed_by=updated_by,
            snapshot_data=updated_obj.model_dump(),
            timestamp=now_iso,
        )
        self._versions.setdefault(object_id, []).append(ver)

        return updated_obj

    # -----------------------------------------------------------------------
    # Section 4: Knowledge Relationships
    # -----------------------------------------------------------------------

    def link_objects(
        self,
        source_id: str,
        target_id: str,
        relationship_type: RelationshipTypeLiteral,
        confidence: float = 0.85,
        evidence_ids: Optional[List[str]] = None,
        causality_verified: bool = False,
        tenant_id: str = "default_tenant",
    ) -> KnowledgeRelationshipDTO:
        """Establishes an explicit relationship between knowledge objects."""
        # Validate that both objects exist within tenant context
        source_obj = self.get_object(source_id, tenant_id)
        target_obj = self.get_object(target_id, tenant_id)

        if not source_obj:
            raise KeyError(f"Source object '{source_id}' does not exist for tenant '{tenant_id}'.")
        if not target_obj:
            raise KeyError(f"Target object '{target_id}' does not exist for tenant '{tenant_id}'.")

        # Invariant: If relationship is CAUSED_BY, causality_verified MUST be true
        if relationship_type == "CAUSED_BY" and not causality_verified:
            # Downgrade to ASSOCIATED_WITH if causality is uncertain
            relationship_type = "ASSOCIATED_WITH"

        rel_id = f"krel_{uuid.uuid4().hex[:12]}"
        rel = KnowledgeRelationshipDTO(
            relationship_id=rel_id,
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            confidence=confidence,
            evidence_ids=evidence_ids or [],
            causality_verified=causality_verified,
            tenant_id=tenant_id,
        )

        if tenant_id not in self._relationships:
            self._relationships[tenant_id] = {}
        self._relationships[tenant_id][rel_id] = rel

        return rel

    def get_object_relationships(
        self,
        object_id: str,
        tenant_id: str = "default_tenant",
    ) -> List[KnowledgeRelationshipDTO]:
        """Retrieves all incoming and outgoing relationships for a knowledge object."""
        tenant_rels = self._relationships.get(tenant_id, {})
        return [
            r for r in tenant_rels.values()
            if r.source_id == object_id or r.target_id == object_id
        ]

    # -----------------------------------------------------------------------
    # Section 5 & 6: Evidence Lineage & Provenance Graph
    # -----------------------------------------------------------------------

    def record_evidence_lineage(
        self,
        knowledge_object_id: str,
        original_artifact_id: str,
        extraction_module: str,
        detector_id: str,
        detector_version: str = "1.0.0",
        algorithm_version: str = "1.0.0",
        transformation_steps: Optional[List[str]] = None,
        confidence: float = 0.90,
        source: str = "CANONICAL_DETECTOR",
        tenant_id: str = "default_tenant",
    ) -> EvidenceLineageDTO:
        """Records full evidence lineage preserving all transforms and provenance."""
        lineage_id = f"lin_{uuid.uuid4().hex[:12]}"
        lineage = EvidenceLineageDTO(
            lineage_id=lineage_id,
            knowledge_object_id=knowledge_object_id,
            original_artifact_id=original_artifact_id,
            extraction_module=extraction_module,
            detector_id=detector_id,
            detector_version=detector_version,
            algorithm_version=algorithm_version,
            transformation_steps=transformation_steps or [],
            confidence=confidence,
            source=source,
        )

        if tenant_id not in self._lineages:
            self._lineages[tenant_id] = {}
        self._lineages[tenant_id][lineage_id] = lineage

        return lineage

    def get_evidence_chain(self, object_id: str, tenant_id: str = "default_tenant") -> EvidenceChainDTO:
        """Traces backward from conclusion to underlying evidence and root artifacts."""
        obj = self.get_object(object_id, tenant_id)
        if not obj:
            raise KeyError(f"Object '{object_id}' not found.")

        chain_elements: List[Dict[str, Any]] = [{"object": obj.model_dump()}]
        root_artifacts: List[str] = []

        # Find lineages
        tenant_lineages = self._lineages.get(tenant_id, {})
        for lin in tenant_lineages.values():
            if lin.knowledge_object_id == object_id:
                chain_elements.append({"lineage": lin.model_dump()})
                root_artifacts.append(lin.original_artifact_id)

        # Trace outgoing relationships
        rels = self.get_object_relationships(object_id, tenant_id)
        for r in rels:
            chain_elements.append({"relationship": r.model_dump()})

        return EvidenceChainDTO(
            conclusion_id=object_id,
            chain_elements=chain_elements,
            root_artifacts=list(set(root_artifacts)),
            verified_at=datetime.now(timezone.utc).isoformat(),
        )

    # -----------------------------------------------------------------------
    # Section 7: Knowledge Versioning
    # -----------------------------------------------------------------------

    def get_version_history(self, object_id: str) -> List[KnowledgeVersionDTO]:
        """Retrieves full version history for an object."""
        return self._versions.get(object_id, [])

    # -----------------------------------------------------------------------
    # Section 8 & 9: Knowledge Snapshots & Diff Engine
    # -----------------------------------------------------------------------

    def create_snapshot(self, label: str, tenant_id: str = "default_tenant") -> KnowledgeSnapshotDTO:
        """Creates an immutable point-in-time snapshot of tenant knowledge state."""
        objs = copy.deepcopy(self._objects.get(tenant_id, {}))
        rels = copy.deepcopy(list(self._relationships.get(tenant_id, {}).values()))

        snap_id = f"ksnap_{uuid.uuid4().hex[:12]}"
        now_iso = datetime.now(timezone.utc).isoformat()

        snapshot = KnowledgeSnapshotDTO(
            snapshot_id=snap_id,
            tenant_id=tenant_id,
            label=label,
            snapshot_timestamp=now_iso,
            object_count=len(objs),
            relationship_count=len(rels),
            objects={k: v.model_dump() for k, v in objs.items()},
            relationships=[r.model_dump() for r in rels],
            created_at=now_iso,
        )

        if tenant_id not in self._snapshots:
            self._snapshots[tenant_id] = {}
        self._snapshots[tenant_id][snap_id] = snapshot

        return snapshot

    def get_snapshot(self, snapshot_id: str, tenant_id: str = "default_tenant") -> Optional[KnowledgeSnapshotDTO]:
        """Retrieves a point-in-time knowledge snapshot."""
        return self._snapshots.get(tenant_id, {}).get(snapshot_id)

    def list_snapshots(self, tenant_id: str = "default_tenant") -> List[KnowledgeSnapshotDTO]:
        """Lists all snapshots for a tenant."""
        return list(self._snapshots.get(tenant_id, {}).values())

    def compute_diff(self, snapshot_a_id: str, snapshot_b_id: str, tenant_id: str = "default_tenant") -> KnowledgeDiffDTO:
        """Compares two snapshots and computes additions, deletions, confidence shifts, and new campaigns."""
        snap_a = self.get_snapshot(snapshot_a_id, tenant_id)
        snap_b = self.get_snapshot(snapshot_b_id, tenant_id)

        if not snap_a:
            raise KeyError(f"Snapshot A '{snapshot_a_id}' not found.")
        if not snap_b:
            raise KeyError(f"Snapshot B '{snapshot_b_id}' not found.")

        objs_a = snap_a.objects
        objs_b = snap_b.objects

        new_evidence = [
            k for k, v in objs_b.items()
            if k not in objs_a and v.get("object_type") == "EVIDENCE"
        ]
        removed_evidence = [
            k for k, v in objs_a.items()
            if k not in objs_b and v.get("object_type") == "EVIDENCE"
        ]

        changed_confidence = []
        for k, v_b in objs_b.items():
            if k in objs_a:
                v_a = objs_a[k]
                if v_a.get("confidence") != v_b.get("confidence"):
                    changed_confidence.append({
                        "object_id": k,
                        "old_confidence": v_a.get("confidence"),
                        "new_confidence": v_b.get("confidence"),
                    })

        new_campaigns = [
            k for k, v in objs_b.items()
            if k not in objs_a and v.get("object_type") == "CAMPAIGN"
        ]

        rels_a_ids = {r.get("relationship_id") for r in snap_a.relationships}
        new_rels = [r for r in snap_b.relationships if r.get("relationship_id") not in rels_a_ids]
        rels_b_ids = {r.get("relationship_id") for r in snap_b.relationships}
        rem_rels = [r for r in snap_a.relationships if r.get("relationship_id") not in rels_b_ids]

        summary_parts = []
        if new_evidence:
            summary_parts.append(f"{len(new_evidence)} new evidence items added.")
        if removed_evidence:
            summary_parts.append(f"{len(removed_evidence)} evidence items removed.")
        if changed_confidence:
            summary_parts.append(f"{len(changed_confidence)} confidence scores updated.")
        if new_campaigns:
            summary_parts.append(f"{len(new_campaigns)} new threat campaigns identified.")
        if new_rels:
            summary_parts.append(f"{len(new_rels)} new relationships formed.")

        summary = " ".join(summary_parts) if summary_parts else "Snapshots are identical."

        return KnowledgeDiffDTO(
            snapshot_a_id=snapshot_a_id,
            snapshot_b_id=snapshot_b_id,
            new_evidence=new_evidence,
            removed_evidence=removed_evidence,
            changed_confidence=changed_confidence,
            new_relationships=new_rels,
            removed_relationships=rem_rels,
            new_campaigns=new_campaigns,
            summary=summary,
        )

    # -----------------------------------------------------------------------
    # Section 21: Unified Knowledge Search
    # -----------------------------------------------------------------------

    def search_knowledge(
        self,
        query: str,
        object_types: Optional[List[KnowledgeObjectTypeLiteral]] = None,
        min_confidence: float = 0.0,
        tenant_id: str = "default_tenant",
    ) -> List[KnowledgeObjectDTO]:
        """Performs exact, token, and keyword search across authorized tenant knowledge objects."""
        import re
        tenant_objs = self._objects.get(tenant_id, {}).values()
        q_lower = query.lower().strip()
        tokens = [t for t in re.split(r'[\s\?\.,!]+', q_lower) if len(t) > 3]

        results = []
        for obj in tenant_objs:
            if object_types and obj.object_type not in object_types:
                continue
            if obj.confidence < min_confidence:
                continue

            ref_lower = obj.canonical_reference.lower()
            prov_str = str(obj.provenance).lower()

            match = False
            if q_lower in ref_lower or (ref_lower and ref_lower in q_lower):
                match = True
            elif q_lower in prov_str or any(t in ref_lower or t in prov_str for t in tokens):
                match = True

            if match:
                results.append(obj)

        return results
