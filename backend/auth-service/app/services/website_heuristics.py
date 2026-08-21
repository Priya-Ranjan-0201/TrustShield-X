import re
from typing import Dict, Any, List
from app.services.url_extractor import DomainIntelligence
from app.services.dns_ssl_inspector import DNSAndSSLResult


PHISHING_KEYWORDS = {
    "login", "signin", "verify", "verification", "secure", "account",
    "banking", "update", "credential", "password", "security", "wallet",
    "support", "admin", "confirm", "billing", "token", "auth"
}


class EvidenceItem:
    def __init__(self, evidence_type: str, severity: str, title: str, description: str):
        self.evidence_type = evidence_type  # SSL, DNS, HEURISTIC, THREAT_INTEL
        self.severity = severity            # CRITICAL, HIGH, MEDIUM, LOW, INFO
        self.title = title
        self.description = description

    def to_dict(self) -> Dict[str, str]:
        return {
            "type": self.evidence_type,
            "severity": self.severity,
            "title": self.title,
            "description": self.description,
        }


def evaluate_website_heuristics(
    dom_intel: DomainIntelligence,
    dns_ssl: DNSAndSSLResult,
    scheme: str,
) -> tuple[List[EvidenceItem], List[str], int]:
    """Evaluates 10+ heuristics and returns:
    (evidence_list, recommendations, calculated_risk_score)
    """
    evidence: List[EvidenceItem] = []
    recommendations: List[str] = []
    risk_score = 0

    # 1. Scheme Check
    if scheme.lower() == "http":
        risk_score += 25
        evidence.append(
            EvidenceItem(
                evidence_type="SSL",
                severity="HIGH",
                title="Unencrypted HTTP Connection",
                description="The website uses unencrypted HTTP instead of HTTPS. Transmitted data can be intercepted.",
            )
        )
        recommendations.append("Do not submit passwords, PINs, or confidential banking data on unencrypted HTTP pages.")

    # 2. SSL Inspection Evidence
    if scheme.lower() == "https":
        if not dns_ssl.ssl_valid:
            risk_score += 35
            evidence.append(
                EvidenceItem(
                    evidence_type="SSL",
                    severity="CRITICAL" if dns_ssl.ssl_is_self_signed else "HIGH",
                    title="Invalid or Untrusted SSL Certificate",
                    description=dns_ssl.ssl_error or "Certificate verification failed for destination host.",
                )
            )
            recommendations.append("Leave this site immediately if your browser displays an SSL security warning.")
        else:
            evidence.append(
                EvidenceItem(
                    evidence_type="SSL",
                    severity="INFO",
                    title="Valid SSL Certificate",
                    description=f"Verified Certificate Authority: {dns_ssl.ssl_issuer}.",
                )
            )

    # 3. IP-based URL
    if dom_intel.is_ip:
        risk_score += 30
        evidence.append(
            EvidenceItem(
                evidence_type="HEURISTIC",
                severity="HIGH",
                title="Direct IP Address Hostname",
                description=f"The URL targets a raw IP address ('{dom_intel.hostname}') rather than a registered domain.",
            )
        )
        recommendations.append("Legitimate institutions use registered domain names rather than raw IP addresses.")

    # 4. Punycode IDN Homograph
    if dom_intel.is_punycode:
        risk_score += 40
        evidence.append(
            EvidenceItem(
                evidence_type="HEURISTIC",
                severity="CRITICAL",
                title="Punycode / IDN Homograph Attack Risk",
                description=f"Domain '{dom_intel.hostname}' uses internationalized characters to mimic a legitimate domain.",
            )
        )
        recommendations.append("Verify the exact character spelling in the address bar. IDN homographs spoof real brand names.")

    # 5. URL Shortener Service
    if dom_intel.is_shortener:
        risk_score += 20
        evidence.append(
            EvidenceItem(
                evidence_type="HEURISTIC",
                severity="MEDIUM",
                title="URL Shortening Service Detected",
                description=f"Domain '{dom_intel.hostname}' uses a link shortener that masks the real destination URL.",
            )
        )
        recommendations.append("Use a link expander tool before opening shortened URLs received via SMS or social media.")

    # 6. High-Risk TLD
    if dom_intel.is_high_risk_tld:
        risk_score += 20
        evidence.append(
            EvidenceItem(
                evidence_type="HEURISTIC",
                severity="MEDIUM",
                title="High-Risk Top-Level Domain (TLD)",
                description=f"TLD '{dom_intel.tld}' is frequently associated with disposable phishing infrastructure.",
            )
        )

    # 7. Phishing Target Keywords in Domain/Subdomain
    found_keywords = [kw for kw in PHISHING_KEYWORDS if kw in dom_intel.raw_url.lower()]
    if found_keywords:
        risk_score += 25
        evidence.append(
            EvidenceItem(
                evidence_type="HEURISTIC",
                severity="HIGH",
                title="Phishing Target Keywords Identified",
                description=f"URL contains sensitive authentication keywords: {', '.join(found_keywords)}.",
            )
        )
        recommendations.append("Ensure you navigated to this website from an official bookmark or verified app.")

    # 8. Excessive URL Length (>75 chars)
    if len(dom_intel.raw_url) > 75:
        risk_score += 15
        evidence.append(
            EvidenceItem(
                evidence_type="HEURISTIC",
                severity="LOW",
                title="Abnormally Long URL Length",
                description=f"URL length ({len(dom_intel.raw_url)} characters) exceeds typical domain standards.",
            )
        )

    # 9. Excessive Subdomains (>=3 parts)
    sub_parts = [p for p in dom_intel.subdomain.split(".") if p]
    if len(sub_parts) >= 2:
        risk_score += 20
        evidence.append(
            EvidenceItem(
                evidence_type="HEURISTIC",
                severity="MEDIUM",
                title="Deep Multi-Level Subdomain Structure",
                description=f"Hostname contains multiple subdomain layers: '{dom_intel.subdomain}'.",
            )
        )

    # 10. Government & Educational Authority Typosquatting / Impersonation
    GOV_ACADEMIC_TARGETS = {
        "nios": ("National Institute of Open Schooling", "nios.ac.in"),
        "cbse": ("Central Board of Secondary Education", "cbse.gov.in"),
        "upsc": ("Union Public Service Commission", "upsc.gov.in"),
        "uidai": ("Unique Identification Authority of India (Aadhaar)", "uidai.gov.in"),
        "aadhaar": ("Unique Identification Authority of India (Aadhaar)", "uidai.gov.in"),
        "incometax": ("Income Tax Department", "incometax.gov.in"),
        "epfo": ("Employees' Provident Fund Organisation", "epfindia.gov.in"),
        "sbi": ("State Bank of India", "onlinesbi.sbi"),
        "rbi": ("Reserve Bank of India", "rbi.org.in"),
        "digilocker": ("DigiLocker India", "digilocker.gov.in"),
    }

    host_lower = dom_intel.hostname.lower()
    for target_key, (target_name, legitimate_domain) in GOV_ACADEMIC_TARGETS.items():
        if target_key in host_lower and host_lower != legitimate_domain and not host_lower.endswith(f".{legitimate_domain}"):
            risk_score += 65
            evidence.append(
                EvidenceItem(
                    evidence_type="HEURISTIC",
                    severity="CRITICAL",
                    title=f"Critical Brand & Authority Impersonation ({target_name})",
                    description=(
                        f"Domain '{dom_intel.hostname}' appears to impersonate the official portal of {target_name}. "
                        f"The legitimate official domain is '{legitimate_domain}'. This is a known typosquatting/phishing technique."
                    ),
                )
            )
            recommendations.append(f"Do not interact with this portal. Always access {target_name} through its verified official domain: https://{legitimate_domain}")

    # 11. Hyphenated Subdomain Spoofing (e.g. nios-ac.in, sbi-bank.com)
    if "-" in dom_intel.domain and any(suffix in dom_intel.domain for suffix in ["-ac", "-gov", "-nic", "-edu", "-bank", "-login", "-kyc"]):
        risk_score += 45
        evidence.append(
            EvidenceItem(
                evidence_type="HEURISTIC",
                severity="HIGH",
                title="Hyphenated Domain Structure Spoofing",
                description=(
                    f"Domain '{dom_intel.hostname}' uses a deceptive hyphenated token (e.g. '{dom_intel.domain}') "
                    "designed to mimic legitimate secondary domain hierarchies."
                ),
            )
        )
        recommendations.append("Beware of domains using hyphens to simulate official domain hierarchies.")

    # Cap risk score between 0 and 100
    risk_score = min(100, max(0, risk_score))

    if not recommendations:
        recommendations.append("Website parameters match clean security baseline. Practice standard web safety.")

    return evidence, recommendations, risk_score

