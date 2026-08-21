import pytest
from app.core.url_security import validate_url_security
from app.services.url_extractor import extract_domain_intelligence
from app.services.website_heuristics import evaluate_website_heuristics
from app.services.website_detector import WebsitePhishingDetector


def test_url_security_valid():
    parsed = validate_url_security("https://google.com")
    assert parsed.scheme == "https"
    assert parsed.hostname == "google.com"


def test_url_security_ssrf_blocked():
    with pytest.raises(Exception) as exc_info:
        validate_url_security("http://127.0.0.1/admin")
    assert "SSRF Blocked" in str(exc_info.value.detail)


def test_domain_intelligence_extraction():
    parsed = validate_url_security("https://login.paypal.verify-account.xyz")
    dom_intel = extract_domain_intelligence(parsed)

    assert dom_intel.hostname == "login.paypal.verify-account.xyz"
    assert dom_intel.domain == "verify-account.xyz"
    assert dom_intel.subdomain == "login.paypal"
    assert dom_intel.tld == ".xyz"
    assert dom_intel.is_high_risk_tld is True
    assert dom_intel.is_ip is False


@pytest.mark.asyncio
async def test_website_phishing_detector_analysis():
    detector = WebsitePhishingDetector()
    result = await detector.analyze_url("http://login-verify-bank-security.xyz")

    assert result.module == "website-phishing"
    assert result.status == "completed"
    assert result.risk_score >= 50
    assert len(result.evidence) > 0
    assert len(result.recommendations) > 0
