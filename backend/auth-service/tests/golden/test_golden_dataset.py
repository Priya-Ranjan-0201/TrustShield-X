"""Golden Dataset Execution Tests (Phase 3.9 Part 1C)."""

import json
import pytest
from app.schemas.risk_validation_models import GoldenCaseDTO
from app.services.risk_validation_service import RiskValidationService


def test_golden_dataset_validation():
    with open("tests/golden/golden_cases.json", "r", encoding="utf-8") as f:
        cases_raw = json.load(f)

    validator = RiskValidationService()
    for raw in cases_raw:
        case = GoldenCaseDTO(**raw)
        res = validator.validate_golden_case(case, [])
        assert res is not None
        assert res.case_id == case.case_id
