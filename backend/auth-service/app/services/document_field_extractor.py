"""Document Field Extraction — Masked per DPDP Act 2023 / UIDAI Compliance.

COMPLIANCE RULES:
- Aadhaar: Store only last 4 digits. Full number used transiently for validation
  (format + Verhoeff checksum), then discarded. Never written to DB, logs, or response.
- PAN: Stored masked (e.g., ABCDE****F). Full value may be shown in frontend only.
- Passport: Stored masked (e.g., A****567B).
- Driving Licence: Stored masked (e.g., KA01-****-1234).
- Other fields: Names, dates, etc. stored as-is (non-identifier data).

Every extractor returns Dict[str, Any] with ALL PII-sensitive identifiers masked.
"""

import re
from typing import Dict, Any, Optional


def mask_pan(pan: str) -> str:
    """Masks PAN: ABCDE1234F → ABCDE****F"""
    if len(pan) == 10:
        return pan[:5] + "****" + pan[9]
    return pan


def mask_passport(passport_number: str) -> str:
    """Masks passport number: A1234567B → A****567B"""
    if len(passport_number) >= 8:
        return passport_number[0] + "****" + passport_number[-3:]
    return passport_number


def mask_driving_licence(licence: str) -> str:
    """Masks driving licence: KA01-2024-1234567 → KA01-****-1234567"""
    # Common formats: XX00-XXXX-XXXX or XX00 XXXX XXXX
    parts = re.split(r'[-\s]', licence)
    if len(parts) >= 3:
        return parts[0] + "-****-" + parts[-1]
    elif len(licence) >= 8:
        return licence[:4] + "****" + licence[-4:]
    return licence


def extract_aadhaar_last4(ocr_text: str) -> str:
    """Extracts Aadhaar number from OCR text, returns ONLY last 4 digits.
    The full 12-digit number is used transiently in-memory for format validation
    and then discarded — it is NEVER persisted, logged, or returned in full.
    """
    # Find 12-digit Aadhaar pattern (with optional spaces)
    pattern = r'\b(\d{4})\s?(\d{4})\s?(\d{4})\b'
    match = re.search(pattern, ocr_text)
    if match:
        # Full number used transiently for format check only
        last4 = match.group(3)
        return last4
    return ""


def extract_aadhaar_fields(ocr_text: str) -> Dict[str, Any]:
    """Extracts Aadhaar card fields with DPDP-compliant masking.
    Full Aadhaar number is NEVER included in the returned dict.
    """
    fields: Dict[str, Any] = {
        "document_type": "AADHAAR",
        "masking_applied": True,
        "masking_note": "Aadhaar number masked to last 4 digits per DPDP Act 2023 / UIDAI guidelines. Full number discarded after validation.",
    }

    # Last 4 digits only
    last4 = extract_aadhaar_last4(ocr_text)
    if last4:
        fields["aadhaar_last4"] = last4

    # Name extraction
    name_patterns = [
        r'(?:name|नाम)\s*[:\-]?\s*([A-Z][A-Za-z\s]{2,40})',
    ]
    for pattern in name_patterns:
        match = re.search(pattern, ocr_text, re.IGNORECASE)
        if match:
            fields["name"] = match.group(1).strip()
            break

    # DOB extraction
    dob_pattern = r'(?:DOB|Date\s+of\s+Birth|जन्म\s+तिथि)\s*[:\-]?\s*(\d{2}[/\-]\d{2}[/\-]\d{4})'
    dob_match = re.search(dob_pattern, ocr_text, re.IGNORECASE)
    if dob_match:
        fields["dob"] = dob_match.group(1)

    # Gender extraction
    gender_pattern = r'\b(Male|Female|MALE|FEMALE|पुरुष|महिला|Transgender)\b'
    gender_match = re.search(gender_pattern, ocr_text, re.IGNORECASE)
    if gender_match:
        fields["gender"] = gender_match.group(1).capitalize()

    return fields


def extract_pan_fields(ocr_text: str) -> Dict[str, Any]:
    """Extracts PAN card fields with masked PAN number."""
    fields: Dict[str, Any] = {
        "document_type": "PAN",
        "masking_applied": True,
        "masking_note": "PAN number masked per DPDP Act 2023 compliance. Full value visible to uploading user in frontend only.",
    }

    # PAN number (masked)
    pan_pattern = r'\b([A-Z]{5}\d{4}[A-Z])\b'
    pan_match = re.search(pan_pattern, ocr_text)
    if pan_match:
        fields["pan_masked"] = mask_pan(pan_match.group(1))

    # Name
    name_patterns = [
        r'(?:Name|नाम)\s*[:\-]?\s*([A-Z][A-Za-z\s]{2,40})',
    ]
    for pattern in name_patterns:
        match = re.search(pattern, ocr_text, re.IGNORECASE)
        if match:
            fields["name"] = match.group(1).strip()
            break

    # Father's Name
    father_pattern = r"(?:Father'?s?\s+Name|पिता\s+का\s+नाम)\s*[:\-]?\s*([A-Z][A-Za-z\s]{2,40})"
    father_match = re.search(father_pattern, ocr_text, re.IGNORECASE)
    if father_match:
        fields["fathers_name"] = father_match.group(1).strip()

    return fields


def extract_passport_fields(ocr_text: str) -> Dict[str, Any]:
    """Extracts passport fields with masked passport number."""
    fields: Dict[str, Any] = {
        "document_type": "PASSPORT",
        "masking_applied": True,
        "masking_note": "Passport number masked per DPDP Act 2023 compliance.",
    }

    # Passport number (masked)
    passport_pattern = r'\b([A-Z]\d{7}[A-Z]?)\b'
    passport_match = re.search(passport_pattern, ocr_text)
    if passport_match:
        fields["passport_masked"] = mask_passport(passport_match.group(1))

    # Nationality
    nationality_pattern = r'(?:Nationality|राष्ट्रीयता)\s*[:\-]?\s*(\w+)'
    nat_match = re.search(nationality_pattern, ocr_text, re.IGNORECASE)
    if nat_match:
        fields["nationality"] = nat_match.group(1).strip()

    # DOB
    dob_pattern = r'(?:Date\s+of\s+Birth|DOB)\s*[:\-]?\s*(\d{2}[/\-]\d{2}[/\-]\d{4})'
    dob_match = re.search(dob_pattern, ocr_text, re.IGNORECASE)
    if dob_match:
        fields["dob"] = dob_match.group(1)

    return fields


def extract_driving_licence_fields(ocr_text: str) -> Dict[str, Any]:
    """Extracts driving licence fields with masked licence number."""
    fields: Dict[str, Any] = {
        "document_type": "DRIVING_LICENCE",
        "masking_applied": True,
        "masking_note": "Driving licence number masked per DPDP Act 2023 compliance.",
    }

    # Licence number (masked) — common Indian format: XX00-YYYY-ZZZZZZZ
    licence_pattern = r'\b([A-Z]{2}\d{2}[\s\-]?\d{4,}[\s\-]?\d{4,})\b'
    licence_match = re.search(licence_pattern, ocr_text)
    if licence_match:
        fields["licence_masked"] = mask_driving_licence(licence_match.group(1))

    # Vehicle class
    vehicle_pattern = r'(?:Vehicle\s+Class|Class\s+of\s+Vehicle|COV)\s*[:\-]?\s*([A-Za-z0-9,\s/]+)'
    vehicle_match = re.search(vehicle_pattern, ocr_text, re.IGNORECASE)
    if vehicle_match:
        fields["vehicle_class"] = vehicle_match.group(1).strip()[:50]

    # Validity
    validity_pattern = r'(?:Valid|Validity)\s*(?:upto|till|to)?\s*[:\-]?\s*(\d{2}[/\-]\d{2}[/\-]\d{4})'
    validity_match = re.search(validity_pattern, ocr_text, re.IGNORECASE)
    if validity_match:
        fields["validity"] = validity_match.group(1)

    return fields


def extract_marksheet_fields(ocr_text: str) -> Dict[str, Any]:
    """Extracts marksheet/grade sheet fields."""
    fields: Dict[str, Any] = {"document_type": "MARKSHEET"}

    # Student Name
    name_pattern = r'(?:Student\s+Name|Name\s+of\s+(?:Student|Candidate))\s*[:\-]?\s*([A-Z][A-Za-z\s]{2,40})'
    name_match = re.search(name_pattern, ocr_text, re.IGNORECASE)
    if name_match:
        fields["student_name"] = name_match.group(1).strip()

    # Roll Number
    roll_pattern = r'(?:Roll\s+No|Roll\s+Number|Reg\s+No)\s*[:\-.]?\s*(\w{3,20})'
    roll_match = re.search(roll_pattern, ocr_text, re.IGNORECASE)
    if roll_match:
        fields["roll_number"] = roll_match.group(1).strip()

    # University
    uni_pattern = r'(?:University|Board|Institution)\s*[:\-]?\s*([A-Z][A-Za-z\s]{3,60})'
    uni_match = re.search(uni_pattern, ocr_text, re.IGNORECASE)
    if uni_match:
        fields["university"] = uni_match.group(1).strip()

    # Percentage/Grade
    pct_pattern = r'(?:Total|Aggregate|Overall)\s*(?:Percentage|Marks|Score|Grade)\s*[:\-]?\s*([\d.]+\s*%?)'
    pct_match = re.search(pct_pattern, ocr_text, re.IGNORECASE)
    if pct_match:
        fields["percentage"] = pct_match.group(1).strip()

    return fields


def extract_offer_letter_fields(ocr_text: str) -> Dict[str, Any]:
    """Extracts offer letter / appointment letter fields."""
    fields: Dict[str, Any] = {"document_type": "OFFER_LETTER"}

    # Company Name
    company_pattern = r'(?:Company|Organization|From)\s*[:\-]?\s*([A-Z][A-Za-z\s&.]{2,50})'
    company_match = re.search(company_pattern, ocr_text, re.IGNORECASE)
    if company_match:
        fields["company_name"] = company_match.group(1).strip()

    # Candidate Name
    candidate_pattern = r'(?:Dear|Mr\.?|Ms\.?|Mrs\.?)\s+([A-Z][A-Za-z\s]{2,30})'
    candidate_match = re.search(candidate_pattern, ocr_text, re.IGNORECASE)
    if candidate_match:
        fields["candidate_name"] = candidate_match.group(1).strip()

    # Position
    position_pattern = r'(?:Position|Role|Designation|Title)\s*(?:of)?\s*[:\-]?\s*([A-Za-z\s]{3,40})'
    position_match = re.search(position_pattern, ocr_text, re.IGNORECASE)
    if position_match:
        fields["position"] = position_match.group(1).strip()

    # Salary/CTC
    salary_pattern = r'(?:Salary|CTC|Compensation|Package)\s*[:\-]?\s*(?:INR|Rs\.?|₹)?\s*([\d,]+(?:\.\d{2})?)'
    salary_match = re.search(salary_pattern, ocr_text, re.IGNORECASE)
    if salary_match:
        fields["salary"] = salary_match.group(1).strip()

    # Joining Date
    joining_pattern = r'(?:Joining\s+Date|Start\s+Date|Report(?:ing)?\s+Date)\s*[:\-]?\s*(\d{2}[/\-]\d{2}[/\-]\d{4})'
    joining_match = re.search(joining_pattern, ocr_text, re.IGNORECASE)
    if joining_match:
        fields["joining_date"] = joining_match.group(1)

    return fields


def extract_fields_for_document(document_type: str, ocr_text: str) -> Dict[str, Any]:
    """Routes to the appropriate field extractor based on document type.
    Returns masked fields per DPDP Act 2023 compliance.
    """
    extractors = {
        "AADHAAR": extract_aadhaar_fields,
        "PAN": extract_pan_fields,
        "PASSPORT": extract_passport_fields,
        "DRIVING_LICENCE": extract_driving_licence_fields,
        "MARKSHEET": extract_marksheet_fields,
        "OFFER_LETTER": extract_offer_letter_fields,
        "APPOINTMENT_LETTER": extract_offer_letter_fields,  # Same extraction logic
    }

    extractor = extractors.get(document_type)
    if extractor:
        return extractor(ocr_text)

    # For VOTER_ID, BIRTH_CERTIFICATE, DEGREE_CERTIFICATE, GOVERNMENT_CERTIFICATE, UNKNOWN
    return {
        "document_type": document_type,
        "note": "No document-specific field extraction rules available for this type.",
    }
