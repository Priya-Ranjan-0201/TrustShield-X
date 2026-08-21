import time
from typing import Dict, Any, List
from app.core.url_security import validate_url_security
from app.services.url_extractor import extract_domain_intelligence
from app.services.dns_ssl_inspector import inspect_dns_and_ssl
from app.services.website_heuristics import evaluate_website_heuristics
from app.services.threat_intelligence import ThreatIntelligenceAggregator


class WebsiteDetectorResult:
    def __init__(
        self,
        module: str,
        status: str,
        risk_score: int,
        confidence_score: float,
        severity: str,
        evidence: List[Dict[str, str]],
        recommendations: List[str],
        execution_time_ms: int,
    ):
        self.module = module
        self.status = status
        self.risk_score = risk_score
        self.confidence_score = confidence_score
        self.severity = severity
        self.evidence = evidence
        self.recommendations = recommendations
        self.execution_time_ms = execution_time_ms

    def to_dict(self) -> Dict[str, Any]:
        return {
            "module": self.module,
            "status": self.status,
            "risk_score": self.risk_score,
            "confidence_score": self.confidence_score,
            "severity": self.severity,
            "evidence": self.evidence,
            "recommendations": self.recommendations,
            "execution_time_ms": self.execution_time_ms,
        }


class WebsitePhishingDetector:
    def __init__(self):
        self.threat_intel = ThreatIntelligenceAggregator()

    async def analyze_url(self, raw_url: str) -> WebsiteDetectorResult:
        start_time = time.time()

        # 1. SSRF & URL Security Validation
        parsed_url = validate_url_security(raw_url)

        # 2. URL Normalization & Domain Extraction
        dom_intel = extract_domain_intelligence(parsed_url)

        # 3. Async DNS & SSL Inspection
        port = parsed_url.port or (443 if parsed_url.scheme == "https" else 80)
        dns_ssl = await inspect_dns_and_ssl(dom_intel.hostname, parsed_url.scheme, port)

        # 4. Evaluate Heuristic Rules
        evidence_items, recommendations, risk_score = evaluate_website_heuristics(
            dom_intel, dns_ssl, parsed_url.scheme
        )

        # 5. Threat Intelligence Integration
        threat_matches = await self.threat_intel.evaluate_url(raw_url)
        for match in threat_matches:
            if match.is_malicious:
                risk_score = max(risk_score, 90)
                evidence_items.append(
                    {
                        "type": "THREAT_INTEL",
                        "severity": "CRITICAL",
                        "title": f"Threat Feed Flagged ({match.provider})",
                        "description": match.details or f"Flagged as malicious by {match.provider}.",
                    }
                )

        # 6. Severity & Confidence Computation
        confidence_score = 0.95 if dns_ssl.dns_records["A"] else 0.85
        if risk_score >= 80:
            severity = "CRITICAL"
        elif risk_score >= 50:
            severity = "HIGH"
        elif risk_score >= 25:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        execution_time_ms = int((time.time() - start_time) * 1000)
        evidence_dicts = [e.to_dict() if hasattr(e, "to_dict") else e for e in evidence_items]

        return WebsiteDetectorResult(
            module="website-phishing",
            status="completed",
            risk_score=risk_score,
            confidence_score=confidence_score,
            severity=severity,
            evidence=evidence_dicts,
            recommendations=recommendations,
            execution_time_ms=execution_time_ms,
        )
