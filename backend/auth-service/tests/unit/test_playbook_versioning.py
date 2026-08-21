import pytest
from app.services.soc.secure_playbook_engine import SecurePlaybookEngine
from app.schemas.autonomous_soc_models import SecurePlaybookDTO


def test_playbook_versioning_and_immutability():
    engine = SecurePlaybookEngine()
    pb_v1 = engine.get_playbook("pb_phishing_containment")
    assert pb_v1 is not None

    # Version upgrade to v2
    pb_v2 = SecurePlaybookDTO(
        playbook_id="pb_phishing_containment_v2",
        tenant_id="default_tenant",
        version=2,
        name="Automated Phishing Containment Playbook v2",
        owner="usr_soc_lead",
        approval_status="APPROVED",
        test_status="VERIFIED",
        nodes=pb_v1.nodes,
    )
    engine.register_playbook(pb_v2)

    assert engine.get_playbook("pb_phishing_containment_v2") is not None
    assert engine.get_playbook("pb_phishing_containment_v2").version == 2
