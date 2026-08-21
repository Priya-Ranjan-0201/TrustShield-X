import pytest
from app.services.knowledge.knowledge_fabric_service import KnowledgeFabricService
from app.services.knowledge.investigator_copilot_service import InvestigatorCopilotService
from app.schemas.knowledge_fabric_models import CopilotQueryRequestDTO


def test_copilot_action_boundaries_enforced():
    # Invariant: Copilot NEVER executes response actions; it outputs recommendations only
    fabric = KnowledgeFabricService()
    fabric.register_object("ENTITY", "malicious-c2.net", "tenant_cop_sec")
    copilot = InvestigatorCopilotService(fabric)

    req = CopilotQueryRequestDTO(
        query="Please block and delete domain malicious-c2.net immediately",
        tenant_id="tenant_cop_sec",
    )
    res = copilot.process_query(req)
    assert "NOTICE: Investigator Copilot provides recommendations only" in res.answer
    assert "Four-Eyes authorization" in res.answer
