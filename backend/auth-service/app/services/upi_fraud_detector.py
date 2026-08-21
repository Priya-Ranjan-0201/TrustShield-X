import urllib.parse
from typing import Dict, Any, List


SUSPICIOUS_UPI_HANDLES = {
    "fakebank", "claim", "refund", "cashback", "lottery", "reward", "winner",
    "customer-care", "support-help", "verify-pin", "paytm-refund", "gpay-reward"
}

GENERIC_PAYEE_NAMES = {
    "customer", "refund", "verification", "support", "admin", "cashback", "winner", "helpdesk"
}


class UPIPaymentDetails:
    def __init__(
        self,
        raw_uri: str,
        vpa_handle: str,
        payee_name: str,
        amount: float | None,
        currency: str,
        note: str,
        merchant_code: str | None,
    ):
        self.raw_uri = raw_uri
        self.vpa_handle = vpa_handle
        self.payee_name = payee_name
        self.amount = amount
        self.currency = currency
        self.note = note
        self.merchant_code = merchant_code


def parse_upi_uri(upi_uri: str) -> UPIPaymentDetails:
    """Parses upi://pay?pa=...&pn=...&am=... URI query string into structured fields."""
    parsed = urllib.parse.urlparse(upi_uri)
    query_params = urllib.parse.parse_qs(parsed.query)

    vpa = query_params.get("pa", [""])[0]
    pn = query_params.get("pn", [""])[0]
    am_str = query_params.get("am", [None])[0]
    cu = query_params.get("cu", ["INR"])[0]
    tn = query_params.get("tn", [""])[0]
    mc = query_params.get("mc", [None])[0]

    amount = float(am_str) if am_str and am_str.replace(".", "", 1).isdigit() else None

    return UPIPaymentDetails(
        raw_uri=upi_uri,
        vpa_handle=vpa,
        payee_name=pn,
        amount=amount,
        currency=cu,
        note=tn,
        merchant_code=mc,
    )


def evaluate_upi_fraud_heuristics(upi: UPIPaymentDetails) -> tuple[List[Dict[str, str]], List[str], int]:
    """Evaluates UPI scam heuristics and returns:
    (evidence_list, recommendations, calculated_risk_score)
    """
    evidence: List[Dict[str, str]] = []
    recommendations: List[str] = []
    risk_score = 0

    vpa_lower = upi.vpa_handle.lower()
    pn_lower = upi.payee_name.lower()
    note_lower = upi.note.lower()

    # 1. Suspicious VPA Handle
    if any(word in vpa_lower for word in SUSPICIOUS_UPI_HANDLES):
        risk_score += 45
        evidence.append(
            {
                "type": "UPI",
                "severity": "CRITICAL",
                "title": "Malicious UPI VPA Handle Flagged",
                "description": f"UPI Address '{upi.vpa_handle}' contains known scam keywords ('refund', 'cashback', 'reward').",
            }
        )
        recommendations.append("Never enter your 4-digit or 6-digit UPI PIN to receive money. UPI PIN is required ONLY to DEDUCT money from your account.")

    # 2. PIN Refund Fraud Scheme in Transaction Note
    if any(word in note_lower for word in ["pin", "claim", "lottery", "cashback", "refund", "receive"]):
        risk_score += 40
        evidence.append(
            {
                "type": "UPI",
                "severity": "CRITICAL",
                "title": "PIN Refund Fraud Exploit in Note",
                "description": f"Transaction note '{upi.note}' contains fraudulent instructions prompting PIN entry for receiving funds.",
            }
        )
        recommendations.append("Scammers use pre-filled debit payment requests disguised as refunds. Reject payment requests from unknown callers.")

    # 3. Generic or Missing Payee Name
    if not upi.payee_name or any(w == pn_lower for w in GENERIC_PAYEE_NAMES):
        risk_score += 25
        evidence.append(
            {
                "type": "UPI",
                "severity": "HIGH",
                "title": "Generic or Suspicious Payee Name",
                "description": f"Payee name is set to generic name '{upi.payee_name or 'Unspecified'}', concealing the true recipient identity.",
            }
        )
        recommendations.append("Verify the recipient's verified legal name in your UPI app before confirming any transaction.")

    # 4. Pre-filled High Transaction Amount (> INR 2,000)
    if upi.amount and upi.amount >= 2000:
        risk_score += 20
        evidence.append(
            {
                "type": "UPI",
                "severity": "MEDIUM",
                "title": "High Pre-filled Payment Request Amount",
                "description": f"QR code requests an automatic debit of {upi.currency} {upi.amount:,.2f}.",
            }
        )

    # 5. Non-Standard UPI Domain / Handle Format
    if "@" not in upi.vpa_handle:
        risk_score += 30
        evidence.append(
            {
                "type": "UPI",
                "severity": "HIGH",
                "title": "Malformed UPI VPA Address",
                "description": f"The VPA string '{upi.vpa_handle}' is missing a valid bank domain suffix.",
            }
        )

    # Cap risk score between 0 and 100
    risk_score = min(100, max(0, risk_score))

    if not recommendations:
        recommendations.append("Verify the recipient VPA handle and amount in your banking app before authorizing payment.")

    return evidence, recommendations, risk_score
