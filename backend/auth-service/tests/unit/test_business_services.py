import pytest
from app.services.resilience.resilience_asset_manager import ResilienceAssetManager
from app.schemas.cyber_resilience_models import BusinessServiceDTO

def test_business_services():
    mgr = ResilienceAssetManager()
    services = mgr.list_business_services()
    assert len(services) >= 1
    svc = mgr.get_business_service("svc_checkout_api")
    assert svc is not None
    assert svc.target_RTO_minutes == 30
    assert svc.target_RPO_minutes == 15
