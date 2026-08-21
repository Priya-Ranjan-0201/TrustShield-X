"""Production Permission Intelligence Normalization Engine (Phase 3.7 Part 1A.8).

Normalizes, enriches, categorizes, and classifies Android permissions requested by an APK
using the Android Permission Catalog.
Zero malware scoring, threat verdicts, or uninstall recommendations.
"""

import time
from typing import List, Dict, Any, Optional, Set
from app.services.permission_catalog import lookup_permission
from app.schemas.permission_intelligence_models import (
    EnrichedPermissionDTO,
    PermissionStatisticsDTO,
    PermissionIntelligenceResultDTO,
    ProtectionLevel,
)


class PermissionIntelligenceService:
    """Master Permission Intelligence Normalization & Catalog Enrichment Engine."""

    def enrich_permissions(
        self,
        raw_permissions: List[Any],
        target_sdk: Optional[int] = 33,
    ) -> PermissionIntelligenceResultDTO:
        start_time = time.time()
        if not raw_permissions:
            return PermissionIntelligenceResultDTO()

        # Deduplicate & normalize permission strings
        seen_names: Set[str] = set()
        enriched_list: List[EnrichedPermissionDTO] = []
        kb_hits = 0

        stat_normal = 0
        stat_dangerous = 0
        stat_signature = 0
        stat_special = 0
        stat_custom = 0
        stat_vendor = 0
        stat_unknown = 0
        stat_runtime = 0

        for raw_p in raw_permissions:
            p_name = raw_p.name if hasattr(raw_p, "name") else str(raw_p)
            norm_name = p_name.strip()
            if not norm_name or norm_name in seen_names:
                continue
            seen_names.add(norm_name)

            meta = lookup_permission(norm_name)
            if meta.get("is_known", False):
                kb_hits += 1

            prot_level = meta.get("protection_level", "UNKNOWN")
            is_dangerous = prot_level == ProtectionLevel.DANGEROUS.value
            is_runtime = meta.get("is_runtime", False)
            is_custom = prot_level == ProtectionLevel.CUSTOM.value
            is_vendor = prot_level == ProtectionLevel.VENDOR.value
            is_unknown = prot_level == ProtectionLevel.UNKNOWN.value

            # Counters
            if prot_level == ProtectionLevel.NORMAL.value:
                stat_normal += 1
            elif is_dangerous:
                stat_dangerous += 1
            elif prot_level == ProtectionLevel.SIGNATURE.value:
                stat_signature += 1
            elif prot_level == ProtectionLevel.SPECIAL.value:
                stat_special += 1

            if is_custom:
                stat_custom += 1
            if is_vendor:
                stat_vendor += 1
            if is_unknown:
                stat_unknown += 1
            if is_runtime:
                stat_runtime += 1

            enriched_list.append(
                EnrichedPermissionDTO(
                    permission_name=norm_name,
                    category=meta.get("category", "Unknown"),
                    protection_level=prot_level,
                    permission_group=meta.get("group"),
                    is_runtime=is_runtime,
                    is_dangerous=is_dangerous,
                    is_custom=is_custom,
                    is_vendor=is_vendor,
                    is_unknown=is_unknown,
                    target_sdk_supported=True,
                    description=meta.get("description"),
                    doc_url=meta.get("doc_url"),
                )
            )

        stats = PermissionStatisticsDTO(
            total_permissions=len(enriched_list),
            normal_count=stat_normal,
            dangerous_count=stat_dangerous,
            signature_count=stat_signature,
            special_count=stat_special,
            custom_count=stat_custom,
            vendor_count=stat_vendor,
            unknown_count=stat_unknown,
            runtime_count=stat_runtime,
        )

        norm_time_ms = int((time.time() - start_time) * 1000)

        return PermissionIntelligenceResultDTO(
            permissions=enriched_list,
            statistics=stats,
            knowledge_base_hits=kb_hits,
            normalization_time_ms=norm_time_ms,
        )
