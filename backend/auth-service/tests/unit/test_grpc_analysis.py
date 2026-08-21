"""Unit tests for gRPC Protocol Detection (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkGrpcDTO


def test_grpc_dto():
    grpc = NetworkGrpcDTO(
        caller_method="com.bank.GrpcClient.call",
        service_name="BankService",
        method_name="GetBalance",
        host="grpc.bank.com",
        port=443,
    )

    assert grpc.service_name == "BankService"
    assert grpc.method_name == "GetBalance"
    assert grpc.port == 443
