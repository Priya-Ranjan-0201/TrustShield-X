import pytest
from app.services.exposure.asset_canonicalization_service import AssetCanonicalizationService


def test_asset_canonicalization_formats():
    # Domain normalization
    c_dom, orig_dom = AssetCanonicalizationService.canonicalize_identifier("DOMAIN", "  HTTPS://Sub.Example.COM./ ")
    assert c_dom == "sub.example.com"
    assert orig_dom == "HTTPS://Sub.Example.COM./"

    # URL normalization
    c_url, _ = AssetCanonicalizationService.canonicalize_identifier("URL", "HTTP://API.EXAMPLE.COM:443/v1/auth?token=123")
    assert c_url.startswith("http://api.example.com")

    # Phone normalization
    c_phone, _ = AssetCanonicalizationService.canonicalize_identifier("PHONE_NUMBER", "+1 (555) 019-2834")
    assert c_phone == "+15550192834"

    # UPI normalization
    c_upi, _ = AssetCanonicalizationService.canonicalize_identifier("UPI_IDENTIFIER", "PAYMENT-DESK@HDFCBANK ")
    assert c_upi == "payment-desk@hdfcbank"
