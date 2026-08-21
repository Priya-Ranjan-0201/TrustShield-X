import pytest
from app.services.soc.false_positive_learning_engine import FalsePositiveLearningEngine


def test_false_positive_learning_verification():
    fp_engine = FalsePositiveLearningEngine()

    rec = fp_engine.record_outcome(
        rule_id="rule_waf_99",
        tenant_id="tenant_1",
        status="FALSE_POSITIVE",
        evidence_ids=["ev_1"],
        patterns=["GET /healthz scanner payload"],
        human_validated=True,
    )

    assert rec.status == "FALSE_POSITIVE"
    assert fp_engine.is_suppressible("rule_waf_99", "tenant_1") is True
