import pytest
from app.services.soc.secure_playbook_engine import SecurePlaybookEngine


def test_secure_playbook_engine_retrieval():
    engine = SecurePlaybookEngine()
    pb = engine.get_playbook("pb_phishing_containment")

    assert pb is not None
    assert pb.name == "Automated Phishing Containment Playbook"
    assert pb.test_status == "VERIFIED"
    assert len(pb.nodes) >= 5
