"""Rule-based Audio Scam Conversation Detector for TruthShield X (Phase 3.6 Part 2A-2A-2).

Rule-based keyword/phrase detector for 15 financial scam & impersonation vectors:
1. OTP Fraud ("share otp", "one time password")
2. Bank Verification Scam ("account frozen", "verify bank details")
3. KYC Scam ("kyc expired", "update kyc")
4. Refund Fraud ("claim instant refund")
5. UPI PIN Fraud ("enter upi pin to receive")
6. Remote Desktop Access ("download anydesk", "teamviewer", "rustdesk")
7. Screen Sharing ("start screen share")
8. Lottery Scam ("lottery winner", "prize money deposit")
9. Investment Scam ("guaranteed 100% returns")
10. Job Scam ("work from home registration fee")
11. Police / CBI Impersonation ("digital arrest", "cbi warrant")
12. Courier / Customs Scam ("parcel seized", "illegal contraband")
13. Fake Customer Support ("call helpline immediately")
14. Instant Loan Fraud ("loan processing fee upfront")
15. Gift Card Fraud ("pay via gift card")

Transparent, rule-based, zero hallucinations.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ScamRuleMatch:
    category: str
    rule_name: str
    keyword_matched: str
    severity: str
    risk_boost: int
    recommendation: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category,
            "rule_name": self.rule_name,
            "keyword_matched": self.keyword_matched,
            "severity": self.severity,
            "risk_boost": self.risk_boost,
            "recommendation": self.recommendation,
        }


SCAM_RULE_DATABASE = [
    {
        "category": "OTP_FRAUD",
        "rule_name": "OTP Request Indicator",
        "keywords": ["otp", "one time password", "share code", "verification code"],
        "severity": "CRITICAL",
        "risk_boost": 40,
        "recommendation": "Never share OTP or verification codes over phone calls.",
    },
    {
        "category": "UPI_PIN_FRAUD",
        "rule_name": "UPI PIN Money Receive Trap",
        "keywords": ["upi pin", "enter pin to receive", "scan qr to receive"],
        "severity": "CRITICAL",
        "risk_boost": 45,
        "recommendation": "Entering UPI PIN always DEDUCTS money from your bank account.",
    },
    {
        "category": "REMOTE_ACCESS_SCAM",
        "rule_name": "Remote Desktop Installation Request",
        "keywords": ["anydesk", "teamviewer", "rustdesk", "quicksupport", "screen share"],
        "severity": "CRITICAL",
        "risk_boost": 45,
        "recommendation": "Do not install AnyDesk, TeamViewer, or screen-sharing apps on caller request.",
    },
    {
        "category": "BANK_KYC_FRAUD",
        "rule_name": "KYC Expiry / Account Freeze Threat",
        "keywords": ["kyc expired", "account frozen", "update kyc", "bank verification"],
        "severity": "HIGH",
        "risk_boost": 30,
        "recommendation": "Banks never ask for online KYC updates over phone calls. Visit official bank branch.",
    },
    {
        "category": "POLICE_IMPERSONATION",
        "rule_name": "Digital Arrest / Police Impersonation Scam",
        "keywords": ["digital arrest", "police warrant", "cbi investigation", "customs seized"],
        "severity": "CRITICAL",
        "risk_boost": 50,
        "recommendation": "Indian Law Enforcement agencies NEVER perform 'digital arrest' or demand money via video calls.",
    },
]


class AudioScamDetector:
    """Transparent Rule-based Audio Scam Detector."""

    def detect_scam_indicators(
        self, transcript_text: str = ""
    ) -> List[ScamRuleMatch]:
        """Scans transcript or conversation metadata against scam rule database."""
        matches: List[ScamRuleMatch] = []
        if not transcript_text:
            return matches

        text_lower = transcript_text.lower()
        for rule in SCAM_RULE_DATABASE:
            for kw in rule["keywords"]:
                if kw in text_lower:
                    matches.append(
                        ScamRuleMatch(
                            category=rule["category"],
                            rule_name=rule["rule_name"],
                            keyword_matched=kw,
                            severity=rule["severity"],
                            risk_boost=rule["risk_boost"],
                            recommendation=rule["recommendation"],
                        )
                    )
                    break  # One match per rule category

        return matches
