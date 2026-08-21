import re
import time
from typing import Dict, Any, List


URGENCY_PATTERNS = [
    r"\b(urgent|immediately|action required|suspended|blocked|deactivated|disconnected|freeze|penalty|legal action|police|court|arrest|warrant|customs)\b",
    r"\b(within 24 hours|today only|last chance|account will be closed|electricity will be disconnected)\b",
]

CREDENTIAL_THEFT_PATTERNS = [
    r"\b(otp|pin|password|cvv|card number|expiry date|netbanking|banking password|aadhaar|pan card|secret code|login details)\b",
    r"\b(share otp|enter pin|verify password|update kyc|submit credentials)\b",
]

FINANCIAL_LURE_PATTERNS = [
    r"\b(lottery|winner|won|cashback|reward|prize|kisan|bonus|crypto|free recharge|earning|earn \d+|work from home|telegram job|like youtube)\b",
    r"\b(claim now|congratulations you have won|refund credited|approved for loan)\b",
]

ACTION_LURE_PATTERNS = [
    r"\b(click here|visit link|download apk|install app|call immediately|send screenshot|open link|verify here)\b",
    r"https?://[^\s]+|bit\.ly/[^\s]+|tinyurl\.com/[^\s]+|t\.me/[^\s]+",
]

IMPERSONATED_ENTITIES = {
    "sbi": "State Bank of India (SBI)",
    "hdfc": "HDFC Bank",
    "icici": "ICICI Bank",
    "paytm": "Paytm Payment Services",
    "phonepe": "PhonePe",
    "gpay": "Google Pay",
    "google pay": "Google Pay",
    "rbi": "Reserve Bank of India (RBI)",
    "income tax": "Income Tax Department",
    "electricity": "State Electricity Department",
    "bill": "Utility Billing Desk",
    "india post": "India Post / Postal Department",
    "fedex": "FedEx Courier Services",
    "customs": "Indian Customs Enforcement",
    "police": "Cyber Police / Law Enforcement",
    "cbi": "Central Bureau of Investigation (CBI)",
    "trai": "Telecom Regulatory Authority (TRAI)",
}


class NLPDetectorResult:
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
        detected_intents: List[str],
    ):
        self.module = module
        self.status = status
        self.risk_score = risk_score
        self.confidence_score = confidence_score
        self.severity = severity
        self.evidence = evidence
        self.recommendations = recommendations
        self.execution_time_ms = execution_time_ms
        self.detected_intents = detected_intents

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
            "detected_intents": self.detected_intents,
        }


class NLPPhishingDetector:
    """Neural & Rule-based NLP Phishing, Social Engineering & Scam Inspection Engine."""

    def analyze_text(self, text: str) -> NLPDetectorResult:
        start_time = time.time()
        text_lower = text.lower()
        evidence: List[Dict[str, str]] = []
        recommendations: List[str] = []
        detected_intents: List[str] = []
        risk_score = 0

        # 1. Check Urgency / Coercion
        urgency_matches = []
        for pattern in URGENCY_PATTERNS:
            matches = re.findall(pattern, text_lower)
            if matches:
                urgency_matches.extend(matches)
        if urgency_matches:
            risk_score += 30
            detected_intents.append("URGENCY_COERCION")
            evidence.append(
                {
                    "type": "NLP_URGENCY",
                    "severity": "HIGH",
                    "title": "Artificial Urgency & Coercion Tactics",
                    "description": f"Message employs psychological pressure tactics ({', '.join(set(urgency_matches[:4]))}) to force hurried compliance.",
                }
            )
            recommendations.append("Do not act under panic or artificial urgency. Real government and banking institutions never threaten instant disconnection or arrest via SMS/messaging.")

        # 2. Check Credential & PIN Theft Lures
        credential_matches = []
        for pattern in CREDENTIAL_THEFT_PATTERNS:
            matches = re.findall(pattern, text_lower)
            if matches:
                credential_matches.extend(matches)
        if credential_matches:
            risk_score += 45
            detected_intents.append("CREDENTIAL_HARVESTING")
            evidence.append(
                {
                    "type": "NLP_CREDENTIALS",
                    "severity": "CRITICAL",
                    "title": "Confidential Credential / OTP Solicitation",
                    "description": f"Message requests sensitive authentication tokens ({', '.join(set(credential_matches[:4]))}).",
                }
            )
            recommendations.append("NEVER share OTP, UPI PIN, ATM PIN, or passwords with anyone over phone, SMS, WhatsApp, or unverified web links.")

        # 3. Check Financial / Lottery / Prize Scams
        lure_matches = []
        for pattern in FINANCIAL_LURE_PATTERNS:
            matches = re.findall(pattern, text_lower)
            if matches:
                lure_matches.extend(matches)
        if lure_matches:
            risk_score += 35
            detected_intents.append("FINANCIAL_FRAUD_LURE")
            evidence.append(
                {
                    "type": "NLP_FINANCIAL_LURE",
                    "severity": "HIGH",
                    "title": "Unsolicited Financial Prize / Lottery Scam",
                    "description": f"Message contains high-risk bait terms ({', '.join(set(lure_matches[:4]))}) typical of advance-fee and lottery fraud schemes.",
                }
            )
            recommendations.append("If an offer sounds too good to be true, it is almost certainly a scam. Legitimate lotteries never require prior deposits or personal KYC verification via chat.")

        # 4. Check Suspicious Link & Action Directives
        action_matches = []
        for pattern in ACTION_LURE_PATTERNS:
            matches = re.findall(pattern, text_lower)
            if matches:
                action_matches.extend(matches)
        if action_matches:
            risk_score += 25
            detected_intents.append("MALICIOUS_LINK_DOWNLOAD")
            evidence.append(
                {
                    "type": "NLP_CALL_TO_ACTION",
                    "severity": "HIGH",
                    "title": "Suspicious External Action / Download Link",
                    "description": "Message instructs recipient to click external links, download unknown APKs, or contact unofficial numbers.",
                }
            )
            recommendations.append("Do not click links received in unsolicited messages. Type official website URLs directly into your browser.")

        # 5. Check Authority / Brand Impersonation
        impersonated = []
        for brand_key, brand_full in IMPERSONATED_ENTITIES.items():
            if re.search(rf"\b{re.escape(brand_key)}\b", text_lower):
                impersonated.append(brand_full)
        if impersonated and (urgency_matches or credential_matches or lure_matches or action_matches):
            risk_score += 40
            detected_intents.append("BRAND_IMPERSONATION")
            evidence.append(
                {
                    "type": "NLP_IMPERSONATION",
                    "severity": "CRITICAL",
                    "title": f"Targeted Brand & Authority Impersonation ({', '.join(impersonated[:2])})",
                    "description": f"The communication impersonates {', '.join(impersonated)} alongside deceptive action lures.",
                }
            )
            recommendations.append(f"Contact {impersonated[0]} directly through their verified customer support hotline or official mobile application.")

        # Compute Final Scores & Severity
        risk_score = min(100, max(0, risk_score))
        if risk_score >= 80:
            severity = "CRITICAL"
        elif risk_score >= 50:
            severity = "HIGH"
        elif risk_score >= 25:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        confidence_score = 0.96 if len(evidence) > 1 else (0.90 if len(evidence) == 1 else 0.85)
        execution_time_ms = int((time.time() - start_time) * 1000)

        if not recommendations:
            recommendations.append("Text content does not match known phishing or social engineering patterns. Practice standard digital hygiene.")

        return NLPDetectorResult(
            module="nlp-phishing",
            status="completed",
            risk_score=risk_score,
            confidence_score=confidence_score,
            severity=severity,
            evidence=evidence,
            recommendations=recommendations,
            execution_time_ms=execution_time_ms,
            detected_intents=detected_intents,
        )
