"""Unit tests for Core Behavioral Correlation Service (Phase 3.9 Part 1A.22)."""

import pytest
from app.services.behavioral_correlation_service import BehavioralCorrelationService
from app.schemas.permission_intelligence_models import PermissionIntelligenceResultDTO, EnrichedPermissionDTO
from app.schemas.api_intelligence_models import APIIntelligenceResultDTO, APIUsageDTO
from app.schemas.dataflow_models import DataflowResultDTO, DataflowPathDTO


def test_behavioral_correlation_sms_flow():
    service = BehavioralCorrelationService()
    perm_dto = PermissionIntelligenceResultDTO(
        permissions=[EnrichedPermissionDTO(permission_name="android.permission.READ_SMS", category="SMS", protection_level="DANGEROUS")]
    )
    api_dto = APIIntelligenceResultDTO(
        api_usage=[APIUsageDTO(caller_method="com.bank.SMS.read", api_canonical_id="android.telephony.SmsManager.receive")]
    )
    df_dto = DataflowResultDTO(
        paths=[DataflowPathDTO(path_id="p1", source_id="s1", sink_id="snk1", path_nodes=["s1", "snk1"])]
    )

    res = service.correlate_behavior(
        permission_intelligence_dto=perm_dto,
        api_intelligence_dto=api_dto,
        dataflow_intelligence_dto=df_dto,
    )

    assert any(f.finding_type == "SMS_DATA_NETWORK_FLOW" for f in res.findings)
    assert res.analysis_time_ms >= 0
