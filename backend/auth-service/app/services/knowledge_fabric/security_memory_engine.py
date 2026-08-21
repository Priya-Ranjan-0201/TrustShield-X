"""
TruthShield X — Security Memory Engine (Phase 19).

Provides persistent organizational security memory isolated by tenant boundary.
"""

from typing import Dict, List, Optional, Any
from app.schemas.cyber_knowledge_fabric_models import SecurityMemoryRecordDTO


class SecurityMemoryEngine:
    """Manages tenant-isolated persistent organizational security memory."""

    def __init__(self):
        self._memory_store: Dict[str, List[SecurityMemoryRecordDTO]] = {}
        self._initialize_default_memory()

    def _initialize_default_memory(self):
        rec = SecurityMemoryRecordDTO(
            memory_id="mem_init_01",
            tenant_id="default_tenant",
            category="PATTERN",
            title="Periodic Weekend Credential Spraying Pattern",
            details={
                "source_asn": "AS13335",
                "targeted_endpoints": ["/api/v1/auth/login", "/api/v1/auth/token"],
                "mitigation_rule": "Enable adaptive captcha during off-peak hours",
            },
        )
        self._memory_store["default_tenant"] = [rec]

    def store_memory(
        self,
        tenant_id: str,
        category: str,
        title: str,
        details: Dict[str, Any],
    ) -> SecurityMemoryRecordDTO:
        rec = SecurityMemoryRecordDTO(
            tenant_id=tenant_id,
            category=category,  # type: ignore
            title=title,
            details=details,
        )
        if tenant_id not in self._memory_store:
            self._memory_store[tenant_id] = []
        self._memory_store[tenant_id].append(rec)
        return rec

    def list_memories(self, tenant_id: str = "default_tenant") -> List[SecurityMemoryRecordDTO]:
        """Lists memories strictly filtered by tenant boundary."""
        return self._memory_store.get(tenant_id, [])
