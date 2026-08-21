import pytest
from app.services.digital_twin_lab.scenario_library_manager import ScenarioLibraryManager

def test_scenario_library_templates():
    mgr = ScenarioLibraryManager()
    templates = mgr.list_templates()
    assert len(templates) >= 3
    tmpl = mgr.get_template("tmpl_ransomware_disruption")
    assert tmpl["category"] == "ATTACK"
