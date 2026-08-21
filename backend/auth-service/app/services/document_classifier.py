"""Document Classification Engine.

Classifies OCR-extracted text into one of 12 document types using keyword/pattern
matching. Returns (document_type, classification_confidence).

Supported types:
  AADHAAR, PAN, PASSPORT, DRIVING_LICENCE, VOTER_ID, DEGREE_CERTIFICATE,
  MARKSHEET, BIRTH_CERTIFICATE, GOVERNMENT_CERTIFICATE, OFFER_LETTER,
  APPOINTMENT_LETTER, UNKNOWN

Unknown handling: skip document-specific extraction and government validation,
still run generic image tampering, cap verdict at MEDIUM RISK maximum.
"""

import re
from typing import Tuple, Dict, List


# Keyword patterns for each document type (case-insensitive matching)
# Ordered by specificity — more specific patterns checked first
DOCUMENT_PATTERNS: List[Tuple[str, List[str], float]] = [
    # (document_type, keyword_patterns, base_confidence)
    (
        "AADHAAR",
        [
            r"aadhaar",
            r"unique\s+identification",
            r"uidai",
            r"government\s+of\s+india.*aadhaar",
            r"\b\d{4}\s?\d{4}\s?\d{4}\b",  # 12-digit UID pattern
            r"enrol(?:l)?ment\s+no",
        ],
        0.88,
    ),
    (
        "PAN",
        [
            r"permanent\s+account\s+number",
            r"income\s+tax\s+department",
            r"\b[A-Z]{5}\d{4}[A-Z]\b",  # PAN format
            r"pan\s+card",
        ],
        0.90,
    ),
    (
        "PASSPORT",
        [
            r"passport",
            r"republic\s+of\s+india.*passport",
            r"nationality.*indian",
            r"place\s+of\s+(?:birth|issue)",
            r"date\s+of\s+expiry",
        ],
        0.85,
    ),
    (
        "DRIVING_LICENCE",
        [
            r"driving\s+licen[cs]e",
            r"motor\s+vehicle",
            r"transport\s+(?:department|authority)",
            r"vehicle\s+class",
            r"(?:non-?\s*)?transport",
            r"validity.*(?:from|to)",
        ],
        0.87,
    ),
    (
        "VOTER_ID",
        [
            r"election\s+commission",
            r"voter.*(?:id|card|identity)",
            r"electoral\s+(?:photo|roll)",
            r"epic\s+no",
        ],
        0.86,
    ),
    (
        "BIRTH_CERTIFICATE",
        [
            r"birth\s+certificate",
            r"registr(?:ar|ation)\s+(?:of\s+)?birth",
            r"date\s+of\s+birth.*place\s+of\s+birth",
            r"municipal\s+(?:corporation|council).*birth",
        ],
        0.84,
    ),
    (
        "MARKSHEET",
        [
            r"mark\s*sheet",
            r"statement\s+of\s+marks",
            r"grade\s+sheet",
            r"(?:total|aggregate)\s+(?:marks|percentage|score)",
            r"roll\s+no.*subject",
            r"examination\s+result",
        ],
        0.83,
    ),
    (
        "DEGREE_CERTIFICATE",
        [
            r"degree\s+(?:certificate|awarded)",
            r"bachelor\s+of|master\s+of|doctor\s+of",
            r"confer(?:red|ring).*degree",
            r"university.*hereby\s+certif",
            r"diploma\s+(?:in|certificate)",
        ],
        0.82,
    ),
    (
        "OFFER_LETTER",
        [
            r"offer\s+(?:letter|of\s+employment)",
            r"pleased\s+to\s+offer",
            r"compensation.*(?:package|salary|ctc)",
            r"joining\s+date",
            r"we\s+are\s+(?:pleased|happy)\s+to\s+(?:offer|inform)",
        ],
        0.80,
    ),
    (
        "APPOINTMENT_LETTER",
        [
            r"appointment\s+(?:letter|order)",
            r"appointed\s+(?:as|to\s+the\s+post)",
            r"terms\s+(?:and\s+conditions\s+)?of\s+(?:appointment|employment)",
            r"reporting\s+(?:date|to)",
        ],
        0.80,
    ),
    (
        "GOVERNMENT_CERTIFICATE",
        [
            r"government\s+of\s+(?:india|\w+)",
            r"certificate\s+(?:of|no)",
            r"hereby\s+certif(?:y|ied)",
            r"official\s+(?:seal|stamp)",
        ],
        0.70,
    ),
]


def classify_document(ocr_text: str) -> Tuple[str, float]:
    """Classifies document based on OCR text content.

    Returns:
        (document_type, classification_confidence)
        where document_type is one of the supported types or 'UNKNOWN'.
    """
    if not ocr_text or len(ocr_text.strip()) < 5:
        return "UNKNOWN", 0.0

    text_lower = ocr_text.lower()
    best_type = "UNKNOWN"
    best_score = 0.0
    best_base_confidence = 0.0

    for doc_type, patterns, base_confidence in DOCUMENT_PATTERNS:
        match_count = 0
        for pattern in patterns:
            if re.search(pattern, text_lower):
                match_count += 1

        if match_count > 0:
            # Score based on proportion of patterns matched
            match_ratio = match_count / len(patterns)
            score = match_ratio * base_confidence

            if score > best_score:
                best_score = score
                best_type = doc_type
                best_base_confidence = base_confidence

    if best_type == "UNKNOWN":
        return "UNKNOWN", 0.0

    # Final confidence: base_confidence adjusted by match strength
    # Clamp between 0.0 and 1.0
    final_confidence = min(1.0, max(0.0, best_score))
    return best_type, round(final_confidence, 3)
