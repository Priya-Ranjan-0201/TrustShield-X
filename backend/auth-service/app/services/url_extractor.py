import urllib.parse
from typing import Dict, Any


HIGH_RISK_TLDS = {
    ".xyz", ".top", ".zip", ".work", ".click", ".gq", ".ml", ".cf", ".tk", ".ga",
    ".site", ".online", ".club", ".buzz", ".cam", ".icu", ".monster", ".sbs"
}

URL_SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "cutt.ly", "is.gd", "v.gd", "ow.ly",
    "buff.ly", "rb.gy", "shorturl.at", "tiny.cc"
}


class DomainIntelligence:
    def __init__(
        self,
        raw_url: str,
        hostname: str,
        domain: str,
        subdomain: str,
        tld: str,
        is_ip: bool,
        is_punycode: bool,
        is_shortener: bool,
        is_high_risk_tld: bool,
    ):
        self.raw_url = raw_url
        self.hostname = hostname
        self.domain = domain
        self.subdomain = subdomain
        self.tld = tld
        self.is_ip = is_ip
        self.is_punycode = is_punycode
        self.is_shortener = is_shortener
        self.is_high_risk_tld = is_high_risk_tld


def extract_domain_intelligence(parsed_url: urllib.parse.ParseResult) -> DomainIntelligence:
    hostname = (parsed_url.hostname or "").lower()
    raw_url = parsed_url.geturl()

    # Punycode check
    is_punycode = "xn--" in hostname

    # IP address check
    is_ip = False
    try:
        import ipaddress
        ipaddress.ip_address(hostname)
        is_ip = True
    except ValueError:
        is_ip = False

    # Extract TLD and domain
    parts = hostname.split(".")
    tld = f".{parts[-1]}" if len(parts) > 1 else ""
    is_high_risk_tld = tld in HIGH_RISK_TLDS

    if len(parts) >= 2:
        domain = ".".join(parts[-2:])
        subdomain = ".".join(parts[:-2])
    else:
        domain = hostname
        subdomain = ""

    is_shortener = hostname in URL_SHORTENERS or domain in URL_SHORTENERS

    return DomainIntelligence(
        raw_url=raw_url,
        hostname=hostname,
        domain=domain,
        subdomain=subdomain,
        tld=tld,
        is_ip=is_ip,
        is_punycode=is_punycode,
        is_shortener=is_shortener,
        is_high_risk_tld=is_high_risk_tld,
    )
