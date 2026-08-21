import pytest
from app.services.knowledge_fabric.knowledge_object_manager import KnowledgeObjectManager


def test_knowledge_admin_authorization():
    manager = KnowledgeObjectManager()
    obj = manager.create_object("POLICY", "pol_pci_34", tenant_id="tenant_pci")

    # Admin can view all tenants
    admin_view = manager.get_object(obj.object_id, tenant_id="admin")
    assert admin_view is not None
    assert admin_view.canonical_identifier == "pol_pci_34"
