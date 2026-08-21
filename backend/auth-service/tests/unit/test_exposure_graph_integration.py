import pytest
from app.services.exposure.asset_inventory_service import AssetInventoryService
from app.services.knowledge.knowledge_fabric_service import KnowledgeFabricService


def test_exposure_knowledge_fabric_graph_linkage():
    inventory = AssetInventoryService()
    fabric = KnowledgeFabricService()

    # 1. Register asset in inventory
    asset = inventory.register_asset(
        asset_type="DOMAIN",
        raw_identifier="auth.truthshield.io",
        ownership_status="VERIFIED_OWNER",
        criticality="CRITICAL",
        tenant_id="tenant_graph",
    )

    # 2. Register knowledge object in fabric
    k_obj = fabric.register_object(
        object_type="ENTITY",
        canonical_reference=asset.canonical_identifier,
        tenant_id="tenant_graph",
        confidence=0.98,
        classification="RESTRICTED",
    )
    assert k_obj.canonical_reference == "auth.truthshield.io"

    # 3. Link to campaign object in graph
    camp_obj = fabric.register_object(
        object_type="CAMPAIGN",
        canonical_reference="CAMP-2026-0891",
        tenant_id="tenant_graph",
    )

    rel = fabric.link_objects(
        source_id=k_obj.knowledge_object_id,
        target_id=camp_obj.knowledge_object_id,
        relationship_type="ASSOCIATED_WITH",
        confidence=0.90,
        tenant_id="tenant_graph",
    )
    assert rel.relationship_type == "ASSOCIATED_WITH"
