"""Government Document Format Validation.

Validates structural format and internal consistency of Indian government document
identifiers. Each validation failure generates one evidence entry (never silent skip).

CRITICAL DISCLAIMER (included in every response):
  "This validates structure and internal consistency only — it does NOT confirm
   authenticity against any government database."

Supported validations:
  - Aadhaar: 12-digit format + Verhoeff checksum (transient, never persisted)
  - PAN: [A-Z]{5}[0-9]{4}[A-Z] + 4th character type classification
  - Passport: [A-Z][0-9]{7}[A-Z]? format
  - Driving Licence: State prefix XX00 format check
"""

import re
from typing import Dict, Any, List, Tuple


# Verhoeff checksum tables for Aadhaar validation
# Reference: https://en.wikipedia.org/wiki/Verhoeff_algorithm
_VERHOEFF_D = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
]

_VERHOEFF_P = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8],
]

_VERHOEFF_INV = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]


def _verhoeff_checksum(number_str: str) -> bool:
    """Validates Verhoeff checksum. Returns True if checksum is valid.
    Used transiently — the full number is NEVER persisted or returned.
    """
    c = 0
    for i, digit in enumerate(reversed(number_str)):
        c = _VERHOEFF_D[c][_VERHOEFF_P[i % 8][int(digit)]]
    return c == 0


def validate_aadhaar_format(ocr_text: str) -> List[Dict[str, str]]:
    """Validates Aadhaar UID format and Verhoeff checksum.
    The full 12-digit number is used transiently in-memory and discarded.
    Only the validation RESULT (pass/fail) is returned — never the number itself.
    """
    evidence: List[Dict[str, str]] = []

    # Find 12-digit Aadhaar number
    pattern = r'\b(\d{4})\s?(\d{4})\s?(\d{4})\b'
    match = re.search(pattern, ocr_text)

    if not match:
        evidence.append({
            "type": "DOCUMENT_VALIDATION",
            "severity": "HIGH",
            "title": "Aadhaar UID Number Not Found",
            "description": "No valid 12-digit Aadhaar UID number detected in the document.",
        })
        return evidence

    # Full number used transiently for checksum — never stored
    full_uid = match.group(1) + match.group(2) + match.group(3)

    # Format check: must not start with 0 or 1
    if full_uid[0] in ('0', '1'):
        evidence.append({
            "type": "DOCUMENT_VALIDATION",
            "severity": "CRITICAL",
            "title": "Invalid Aadhaar UID Starting Digit",
            "description": "Aadhaar UIDs never start with 0 or 1. This is a likely forged number.",
        })

    # Verhoeff checksum validation
    if not _verhoeff_checksum(full_uid):
        evidence.append({
            "type": "DOCUMENT_VALIDATION",
            "severity": "CRITICAL",
            "title": "Aadhaar Verhoeff Checksum Failed",
            "description": "The Aadhaar UID fails the Verhoeff checksum algorithm. This indicates a fabricated or incorrectly entered number.",
        })

    # full_uid is NOT returned, stored, or logged — discarded after this scope
    return evidence


def validate_pan_format(ocr_text: str) -> List[Dict[str, str]]:
    """Validates PAN format: [A-Z]{5}[0-9]{4}[A-Z].
    4th character encodes entity type (P=Individual, C=Company, H=HUF, etc.).
    """
    evidence: List[Dict[str, str]] = []

    pan_pattern = r'\b([A-Z]{5}\d{4}[A-Z])\b'
    match = re.search(pan_pattern, ocr_text)

    if not match:
        evidence.append({
            "type": "DOCUMENT_VALIDATION",
            "severity": "HIGH",
            "title": "PAN Number Not Found",
            "description": "No valid PAN number (format: XXXXX0000X) detected in the document.",
        })
        return evidence

    pan = match.group(1)

    # 4th character entity type validation
    valid_entity_codes = {'A', 'B', 'C', 'F', 'G', 'H', 'J', 'L', 'P', 'T'}
    if pan[3] not in valid_entity_codes:
        evidence.append({
            "type": "DOCUMENT_VALIDATION",
            "severity": "HIGH",
            "title": "Invalid PAN Entity Type Code",
            "description": f"PAN 4th character '{pan[3]}' is not a recognized entity type code. Valid codes: {', '.join(sorted(valid_entity_codes))}.",
        })

    # 5th character should match first letter of surname
    # (cannot validate without name, so skip)

    return evidence


def validate_passport_format(ocr_text: str) -> List[Dict[str, str]]:
    """Validates Indian passport number format: [A-Z][0-9]{7}[A-Z]?"""
    evidence: List[Dict[str, str]] = []

    passport_pattern = r'\b([A-Z]\d{7}[A-Z]?)\b'
    match = re.search(passport_pattern, ocr_text)

    if not match:
        evidence.append({
            "type": "DOCUMENT_VALIDATION",
            "severity": "HIGH",
            "title": "Passport Number Not Found",
            "description": "No valid Indian passport number format detected.",
        })
        return evidence

    passport = match.group(1)

    # First character should be a valid series letter
    valid_series = {'A', 'B', 'C', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Z'}
    if passport[0] not in valid_series:
        evidence.append({
            "type": "DOCUMENT_VALIDATION",
            "severity": "MEDIUM",
            "title": "Unusual Passport Series Letter",
            "description": f"Passport series letter '{passport[0]}' is not commonly used in Indian passports.",
        })

    return evidence


def validate_driving_licence_format(ocr_text: str) -> List[Dict[str, str]]:
    """Validates Indian driving licence format: state code prefix XX00."""
    evidence: List[Dict[str, str]] = []

    # Indian DL format: 2-letter state code + 2-digit RTO code + year + number
    dl_pattern = r'\b([A-Z]{2}\d{2}[\s\-]?\d{4,}[\s\-]?\d{4,})\b'
    match = re.search(dl_pattern, ocr_text)

    if not match:
        evidence.append({
            "type": "DOCUMENT_VALIDATION",
            "severity": "HIGH",
            "title": "Driving Licence Number Not Found",
            "description": "No valid Indian driving licence number format detected.",
        })
        return evidence

    dl_number = match.group(1)
    state_code = dl_number[:2]

    valid_states = {
        'AN', 'AP', 'AR', 'AS', 'BR', 'CG', 'CH', 'DD', 'DL', 'GA',
        'GJ', 'HP', 'HR', 'JH', 'JK', 'KA', 'KL', 'LA', 'LD', 'MH',
        'ML', 'MN', 'MP', 'MZ', 'NL', 'OD', 'PB', 'PY', 'RJ', 'SK',
        'TN', 'TR', 'TS', 'UK', 'UP', 'WB',
    }

    if state_code not in valid_states:
        evidence.append({
            "type": "DOCUMENT_VALIDATION",
            "severity": "HIGH",
            "title": "Invalid Driving Licence State Code",
            "description": f"State code '{state_code}' is not a recognized Indian state/UT code.",
        })

    return evidence


def validate_document_format(document_type: str, ocr_text: str) -> Tuple[List[Dict[str, str]], str]:
    """Routes to appropriate format validator. Returns (evidence_list, disclaimer).

    The disclaimer MUST be included in every response:
    "This validates structure and internal consistency only — it does NOT confirm
     authenticity against any government database."
    """
    disclaimer = (
        "This validates structure and internal consistency only — it does NOT "
        "confirm authenticity against any government database. Do not rely on "
        "this result as legal proof of document authenticity."
    )

    validators = {
        "AADHAAR": validate_aadhaar_format,
        "PAN": validate_pan_format,
        "PASSPORT": validate_passport_format,
        "DRIVING_LICENCE": validate_driving_licence_format,
    }

    validator = validators.get(document_type)
    if validator:
        return validator(ocr_text), disclaimer

    # No format validator for this document type
    return [], disclaimer
