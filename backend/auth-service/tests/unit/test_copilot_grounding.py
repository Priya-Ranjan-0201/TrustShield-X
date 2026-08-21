import pytest
from app.services.knowledge.knowledge_fabric_service import KnowledgeFabricService
from app.services.knowledge.investigator_copilot_service import InvestigatorCopilotService
from app.schemas.knowledge_fabric_models import CopilotQueryRequestDTO


def test_copilot_grounded_answer_with_citations():
    fabric = KnowledgeFabricService()
    fabric.register_object(
        object_type="ENTITY",
        canonical_reference="secure-verification-hdfc-portal.net",
        tenant_id="tenant_cop",
        confidence=0.94,
        provenance={"detector": "dex_static_parser", "rule_id": "DEX_RULE_09"},
    )

    copilot = InvestigatorCopilotService(fabric)
    req = CopilotQueryRequestDTO(
        query="Why is secure-verification-hdfc-portal.net suspicious?",
        tenant_id="tenant_cop",
    )
    res = copilot.process_query(req)
    assert res.confidence >= 0.85
    assert len(res.citations) >= 1
    assert "secure-verification-hdfc-portal.net" in res.answer
    assert res.citations[0].target_id.startswith("kobj_")
