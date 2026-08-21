import pytest
from app.services.knowledge_fabric.cyber_security_knowledge_fabric import CyberSecurityKnowledgeFabric


def test_knowledge_fabric_graceful_missing_query_handling():
    fabric = CyberSecurityKnowledgeFabric()

    # Query for nonexistent object
    nonexistent = fabric.objects.get_object("kobj_missing_404")
    assert nonexistent is None

    # Lineage for unrecorded conclusion
    lineage = fabric.lineage.get_lineage("conc_unrecorded")
    assert lineage is None
