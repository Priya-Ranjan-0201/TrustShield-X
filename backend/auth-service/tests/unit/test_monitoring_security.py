import pytest
from app.services.exposure.asset_canonicalization_service import AssetCanonicalizationService


def test_ssrf_and_private_network_rejection():
    # 1. Loopback addresses
    res_loop = AssetCanonicalizationService.validate_target_safety("127.0.0.1")
    assert res_loop["is_safe"] is False
    assert "local host" in res_loop["reason"] or "private or reserved subnet" in res_loop["reason"]

    # 2. Cloud metadata IP (169.254.169.254)
    res_meta = AssetCanonicalizationService.validate_target_safety("169.254.169.254")
    assert res_meta["is_safe"] is False

    # 3. Private 10.0.0.0/8 subnet
    res_priv = AssetCanonicalizationService.validate_target_safety("10.10.4.1")
    assert res_priv["is_safe"] is False
    assert "private or reserved subnet" in res_priv["reason"]

    # 4. Internal TLD
    res_tld = AssetCanonicalizationService.validate_target_safety("db-master.corp")
    assert res_tld["is_safe"] is False

    # 5. Legitimate public target
    res_pub = AssetCanonicalizationService.validate_target_safety("truthshield.io")
    assert res_pub["is_safe"] is True
