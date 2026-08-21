import re
from typing import Dict, Any


def classify_qr_payload(payload: str) -> tuple[str, Dict[str, Any]]:
    """Classifies raw QR payload string and extracts structured parameters.
    Returns: (payload_category, parsed_metadata)
    """
    if not payload:
        return "UNKNOWN", {}

    p_clean = payload.strip()

    # 1. UPI Payment URI
    if p_clean.lower().startswith("upi://pay") or "pa=" in p_clean.lower():
        return "UPI_PAYMENT", {"raw_uri": p_clean}

    # 2. URL
    if p_clean.lower().startswith(("http://", "https://", "www.")):
        return "URL", {"url": p_clean}

    # 3. vCard Contact
    if p_clean.upper().startswith("BEGIN:VCARD"):
        return "VCARD_CONTACT", {"vcard": p_clean}

    # 4. WiFi Config
    if p_clean.upper().startswith("WIFI:"):
        return "WIFI_CONFIG", {"wifi_raw": p_clean}

    # 5. Email
    if p_clean.lower().startswith("mailto:") or re.match(r"^[^@]+@[^@]+\.[^@]+$", p_clean):
        return "EMAIL", {"email": p_clean.replace("mailto:", "")}

    # 6. Phone Number
    if p_clean.lower().startswith("tel:") or (p_clean.startswith("+") and p_clean[1:].isdigit()):
        return "PHONE_NUMBER", {"phone": p_clean.replace("tel:", "")}

    # 7. SMS
    if p_clean.lower().startswith(("smsto:", "sms:")):
        return "SMS", {"sms_raw": p_clean}

    # 8. Calendar Event
    if p_clean.upper().startswith("BEGIN:VEVENT"):
        return "CALENDAR_EVENT", {"event": p_clean}

    # 9. Plain Text
    return "PLAIN_TEXT", {"text": p_clean}
