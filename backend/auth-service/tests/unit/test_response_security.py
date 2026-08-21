import pytest
from app.services.protected_target_engine import (
    ProtectedTargetEngine,
    ProtectedTargetViolationError,
    TargetValidationError,
)


def test_protected_target_exact_matches():
    assert ProtectedTargetEngine.is_protected_target("127.0.0.1") is True
    assert ProtectedTargetEngine.is_protected_target("localhost") is True
    assert ProtectedTargetEngine.is_protected_target("10.0.0.1") is True
    assert ProtectedTargetEngine.is_protected_target("192.168.1.1") is True
    assert ProtectedTargetEngine.is_protected_target("auth-service") is True
    assert ProtectedTargetEngine.is_protected_target("root") is True
    assert ProtectedTargetEngine.is_protected_target("soc_lead") is True


def test_cloud_metadata_defense():
    # AWS / GCP / Azure Instance Metadata endpoint
    assert ProtectedTargetEngine.is_protected_target("169.254.169.254") is True
    assert ProtectedTargetEngine.is_protected_target("http://169.254.169.254/latest/meta-data") is True
    assert ProtectedTargetEngine.is_protected_target("metadata.google.internal") is True


def test_loopback_and_private_ip_ranges():
    # Loopback range (127.0.0.0/8)
    assert ProtectedTargetEngine.is_protected_target("127.0.0.2") is True
    assert ProtectedTargetEngine.is_protected_target("127.255.255.255") is True
    # IPv6 loopback
    assert ProtectedTargetEngine.is_protected_target("::1") is True
    assert ProtectedTargetEngine.is_protected_target("[::1]:8080") is True
    # Private subnets
    assert ProtectedTargetEngine.is_protected_target("10.50.1.20") is True
    assert ProtectedTargetEngine.is_protected_target("172.16.0.5") is True
    assert ProtectedTargetEngine.is_protected_target("192.168.0.100") is True


def test_internal_domain_suffixes():
    assert ProtectedTargetEngine.is_protected_target("db.trustshield.internal") is True
    assert ProtectedTargetEngine.is_protected_target("api.internal") is True
    assert ProtectedTargetEngine.is_protected_target("gateway.corp") is True
    assert ProtectedTargetEngine.is_protected_target("service.local") is True


def test_public_malicious_target_allowed():
    # Legitimate threat domains and public routable IPs are NOT blocked by protected target engine
    assert ProtectedTargetEngine.is_protected_target("evil-phishing-portal.com") is False
    assert ProtectedTargetEngine.is_protected_target("93.184.216.34") is False
    assert ProtectedTargetEngine.is_protected_target("104.244.42.1") is False


def test_validate_action_target_raises_violation():
    with pytest.raises(ProtectedTargetViolationError):
        ProtectedTargetEngine.validate_action_target("127.0.0.1", "IP", "org_default")

    with pytest.raises(ProtectedTargetViolationError):
        ProtectedTargetEngine.validate_action_target("http://localhost:8000", "URL", "org_default")

    with pytest.raises(ProtectedTargetViolationError):
        ProtectedTargetEngine.validate_action_target("169.254.169.254", "IP", "org_default")
