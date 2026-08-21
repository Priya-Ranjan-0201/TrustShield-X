import pytest
from app.services.security_engineering.improvement_generation_engine import ImprovementGenerationEngine

def test_improvement_generation():
    engine = ImprovementGenerationEngine()
    imp = engine.generate_improvement(
        category="POLICY",
        title="Prune Wildcard Permissions on Backup Role",
        description="Limit backup service account strictly to backup bucket",
        problem="Overprivileged IAM role",
        proposed_change="Remove s3:* permission",
        expected_benefit="Zero least-privilege violations",
        expected_risk="None",
    )
    assert imp.category == "POLICY"
    assert imp.confidence == 0.95
