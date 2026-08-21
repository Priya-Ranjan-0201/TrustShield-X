"""
TruthShield X — Brand Impersonation & Lookalike Monitoring Engine
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.exposure_models import BrandImpersonationFindingDTO


class BrandImpersonationMonitoringEngine:
    """Detects brand impersonation across typo-squat domains, fraudulent UPI handles, and spoofed APKs."""

    def __init__(self):
        # tenant_id -> impersonation_id -> BrandImpersonationFindingDTO
        self._findings: Dict[str, Dict[str, BrandImpersonationFindingDTO]] = {}

    @staticmethod
    def _levenshtein_distance(s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return BrandImpersonationMonitoringEngine._levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        prev_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            curr_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = prev_row[j + 1] + 1
                deletions = curr_row[j] + 1
                substitutions = prev_row[j] + (c1 != c2)
                curr_row.append(min(insertions, deletions, substitutions))
            prev_row = curr_row
        return prev_row[-1]

    @staticmethod
    def _normalize_leetspeak(text: str) -> str:
        leet_map = {'1': 'l', '0': 'o', '3': 'e', '@': 'a', '5': 's', '8': 'b', '7': 't'}
        return "".join(leet_map.get(c, c) for c in text.lower())

    def evaluate_suspect_identifier(
        self,
        target_brand: str,
        suspect_identifier: str,
        identifier_type: str = "DOMAIN",  # DOMAIN, UPI, APK, PHONE
        tenant_id: str = "default_tenant",
    ) -> Optional[BrandImpersonationFindingDTO]:
        """Evaluates whether an identifier is a fraudulent brand lookalike or typosquat."""
        import re
        brand_clean = target_brand.lower().strip()
        suspect_clean = suspect_identifier.lower().strip()

        # Extract root or compare strings
        if identifier_type == "DOMAIN":
            root_suspect = suspect_clean.split(".")[0].replace("https://", "").replace("http://", "")
        else:
            root_suspect = suspect_clean

        dist = self._levenshtein_distance(brand_clean, root_suspect)
        max_len = max(len(brand_clean), len(root_suspect))
        similarity = 1.0 - (dist / max_len) if max_len > 0 else 0.0

        # Check leet-normalized and token-based similarity
        root_leet = self._normalize_leetspeak(root_suspect)
        tokens = [t for t in re.split(r'[-_.]+', root_suspect) if t]
        tokens_leet = [self._normalize_leetspeak(t) for t in tokens]

        token_match = any(
            t == brand_clean or self._levenshtein_distance(brand_clean, t) <= 1
            for t in tokens_leet
        )

        # Also check substring / brand containment with keywords like 'support', 'secure', 'portal', 'kyc', 'verify'
        phish_keywords = ["support", "secure", "portal", "kyc", "verify", "pay", "login", "bank", "security"]
        has_phish_kw = any(kw in suspect_clean for kw in phish_keywords)
        contains_brand = brand_clean in suspect_clean or brand_clean in root_leet

        is_impersonation = False
        impersonation_type = "UNKNOWN"
        risk_score = 20.0
        confidence = 0.50

        if (similarity >= 0.75 and dist > 0) or token_match or (contains_brand and has_phish_kw):
            is_impersonation = True
            impersonation_type = f"LOOKALIKE_{identifier_type}"
            risk_score = 85.0 if has_phish_kw else 65.0
            confidence = 0.92 if (contains_brand or token_match) else 0.82

        if not is_impersonation:
            return None

        finding_id = f"imp_{uuid.uuid4().hex[:12]}"
        finding = BrandImpersonationFindingDTO(
            impersonation_id=finding_id,
            target_brand=target_brand,
            suspect_identifier=suspect_identifier,
            impersonation_type=impersonation_type,
            similarity_score=round(similarity, 3),
            risk_score=risk_score,
            confidence=confidence,
            evidence={
                "levenshtein_distance": dist,
                "similarity": similarity,
                "contains_brand": contains_brand,
                "has_phish_keywords": has_phish_kw,
            },
            tenant_id=tenant_id,
            detected_at=datetime.now(timezone.utc).isoformat(),
        )

        if tenant_id not in self._findings:
            self._findings[tenant_id] = {}
        self._findings[tenant_id][finding_id] = finding

        return finding

    def list_impersonations(self, tenant_id: str = "default_tenant") -> List[BrandImpersonationFindingDTO]:
        """Lists all detected brand impersonations for a tenant."""
        return list(self._findings.get(tenant_id, {}).values())
