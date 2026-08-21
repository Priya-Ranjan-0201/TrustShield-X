import pytest
from app.services.assurance_fabric.continuous_assurance_scheduler import ContinuousAssuranceScheduler
from app.services.resilience.continuous_resilience_validation_engine import ContinuousResilienceValidationEngine

def test_phase24_continuous_validation():
    scheduler = ContinuousAssuranceScheduler()
    schedules = scheduler.list_schedules()
    assert len(schedules) >= 3
    res = scheduler.trigger_schedule("sched_hourly_authz")
    assert res["status"] == "PASS"

def test_resilience_continuous_validation():
    engine = ContinuousResilienceValidationEngine()
    schedules = engine.list_schedules()
    assert len(schedules) >= 3
