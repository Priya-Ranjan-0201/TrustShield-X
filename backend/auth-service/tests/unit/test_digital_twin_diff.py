import pytest
from app.services.cyber_digital_twin.cyber_digital_twin_engine import CyberDigitalTwinEngine

def test_digital_twin_snapshot_diff():
    engine = CyberDigitalTwinEngine()
    engine.create_environment("ENV-DIFF", "t1", initial_state={"assets": [{"id": "A1", "name": "API"}]})
    engine.create_snapshot("SNAP-A", "ENV-DIFF", "t1")
    
    # Mutate environment state
    env = engine.get_environment("ENV-DIFF", "t1")
    env["state"]["assets"].append({"id": "A2", "name": "DB"})
    engine.create_snapshot("SNAP-B", "ENV-DIFF", "t1")
    
    diff = engine.diff_snapshots("SNAP-A", "SNAP-B", "t1")
    assert len(diff["new_assets"]) == 1
    assert diff["new_assets"][0]["id"] == "A2"
    assert diff["total_delta_count"] == 1
