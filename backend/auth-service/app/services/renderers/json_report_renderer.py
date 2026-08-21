"""JSON Report Renderer (Phase 4.0 Part 3 — Sections 7-9).

Machine-readable canonical export with deterministic sorting, UTF-8 encoding,
and secret redaction.
"""

import json
from typing import Any, Optional, Dict
from app.schemas.digital_trust_report_models import ReportDocumentDTO
from app.schemas.trust_narrative_models import NarrativeDocumentDTO
from app.services.renderers.base_renderer import BaseReportRenderer


# Sensitive keys to redact from JSON output (Section 7)
SENSITIVE_KEYS = {
    "password", "passwd", "token", "access_token", "refresh_token",
    "private_key", "secret", "client_secret", "api_key", "credentials",
    "db_password", "database_password", "bearer", "authorization"
}


def _redact_dict(obj: Any) -> Any:
    """Recursively redact secrets and ensure stable ordering."""
    if isinstance(obj, dict):
        cleaned = {}
        for k, v in sorted(obj.items(), key=lambda x: str(x[0])):
            if any(s in k.lower() for s in SENSITIVE_KEYS):
                cleaned[k] = "[REDACTED_SECRET]"
            else:
                cleaned[k] = _redact_dict(v)
        return cleaned
    elif isinstance(obj, list):
        return [_redact_dict(item) for item in obj]
    return obj


class JSONReportRenderer(BaseReportRenderer):
    """Canonical JSON Report Renderer producing byte-for-byte deterministic JSON."""

    VERSION = "1.0.0"

    def validate_input(
        self,
        report_doc: ReportDocumentDTO,
        narrative_doc: Optional[NarrativeDocumentDTO] = None,
    ) -> bool:
        if not report_doc or not report_doc.report_id:
            return False
        return True

    def render(
        self,
        report_doc: ReportDocumentDTO,
        narrative_doc: Optional[NarrativeDocumentDTO] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> bytes:
        self.validate_input(report_doc, narrative_doc)

        raw_dict = report_doc.model_dump()

        # Sort major arrays for determinism (Section 8)
        if "major_findings" in raw_dict and isinstance(raw_dict["major_findings"], list):
            raw_dict["major_findings"] = sorted(
                raw_dict["major_findings"],
                key=lambda x: str(x.get("finding_id", ""))
            )

        if "evidence_cards" in raw_dict and isinstance(raw_dict["evidence_cards"], list):
            raw_dict["evidence_cards"] = sorted(
                raw_dict["evidence_cards"],
                key=lambda x: str(x.get("card_id", ""))
            )

        if "provenance" in raw_dict and isinstance(raw_dict["provenance"], list):
            raw_dict["provenance"] = sorted(
                raw_dict["provenance"],
                key=lambda x: str(x.get("statement_id", ""))
            )

        if "recommendations" in raw_dict and isinstance(raw_dict["recommendations"], list):
            raw_dict["recommendations"] = sorted(raw_dict["recommendations"])

        if "limitations" in raw_dict and isinstance(raw_dict["limitations"], list):
            raw_dict["limitations"] = sorted(raw_dict["limitations"])

        # Include narrative data if provided
        if narrative_doc:
            raw_dict["narratives"] = narrative_doc.model_dump()

        # Redact sensitive keys and sort dictionary keys
        cleaned_dict = _redact_dict(raw_dict)

        json_str = json.dumps(
            cleaned_dict,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
        )
        return json_str.encode("utf-8")

    def validate_output(self, rendered_bytes: bytes) -> bool:
        if not rendered_bytes or len(rendered_bytes) == 0:
            return False
        try:
            parsed = json.loads(rendered_bytes.decode("utf-8"))
            return isinstance(parsed, dict) and "report_id" in parsed
        except Exception:
            return False

    def get_content_type(self) -> str:
        return "application/json; charset=utf-8"

    def get_file_extension(self) -> str:
        return "json"

    def get_renderer_version(self) -> str:
        return self.VERSION
