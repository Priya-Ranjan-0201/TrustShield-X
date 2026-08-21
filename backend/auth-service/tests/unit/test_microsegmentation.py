import pytest
from app.services.zero_trust_exposure.microsegmentation_engine import MicrosegmentationEngine

def test_trust_zone_traffic_evaluation():
    engine = MicrosegmentationEngine()
    
    # Create zones
    engine.create_zone("Z-DMZ", "tenant-alpha", "DMZ Zone", "DMZ", 3)
    engine.create_zone("Z-DB", "tenant-alpha", "Database Zone", "DATABASE", 10)
    
    # Default without explicit rule -> BLOCKED
    res1 = engine.evaluate_traffic("tenant-alpha", "Z-DMZ", "Z-DB", "TCP", 5432)
    assert res1["action"] == "BLOCK"
    
    # Add rule
    engine.add_rule(
        rule_id="RULE-ALLOW-DB",
        tenant_id="tenant-alpha",
        source_zone_id="Z-DMZ",
        dest_zone_id="Z-DB",
        protocol="TCP",
        port_range="5432",
        action="ALLOW"
    )
    
    res2 = engine.evaluate_traffic("tenant-alpha", "Z-DMZ", "Z-DB", "TCP", 5432)
    assert res2["action"] == "ALLOW"
