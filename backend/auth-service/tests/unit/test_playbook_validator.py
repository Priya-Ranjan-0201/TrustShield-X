import pytest
from app.services.soc.playbook_validator import PlaybookValidator
from app.schemas.autonomous_soc_models import SecurePlaybookDTO, PlaybookNodeDTO


def test_playbook_validator_unreachable_node_detection():
    validator = PlaybookValidator()

    # Create playbook with an orphaned unreachable node 'n_orphan'
    nodes = [
        PlaybookNodeDTO(node_id="n1", node_type="TRIGGER", name="Start", next_node_ids=["n2"]),
        PlaybookNodeDTO(node_id="n2", node_type="END", name="End"),
        PlaybookNodeDTO(node_id="n_orphan", node_type="ACTION", name="Orphan Action"),
    ]
    pb = SecurePlaybookDTO(playbook_id="pb_orphan", name="Orphan Playbook", nodes=nodes)
    val = validator.validate_playbook(pb)

    assert val.is_valid is False
    assert "n_orphan" in val.unreachable_nodes
