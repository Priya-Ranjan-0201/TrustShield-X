import pytest
from app.services.knowledge.knowledge_fabric_service import KnowledgeFabricService
from app.services.knowledge.investigator_copilot_service import InvestigatorCopilotService
from app.schemas.knowledge_fabric_models import CopilotQueryRequestDTO


def test_retrieval_authorization_enforced():
    fabric = KnowledgeFabricService()
    fabric.register_object("ENTITY", "confidential-tenant-a.com", "tenant_a")
    copilot = InvestigatorCopilotService(fabric)

    # Query from Tenant B must NOT retrieve Tenant A's confidential object
    req_b = CopilotQueryRequestDTO(
        query="confidential-tenant-a.com",
        tenant_id="tenant_b",
    )
    res_b = copilot.process_query(req_b)
    assert len(res_b.citations) == 0
    assert "Insufficient evidence" in res_b.answer
