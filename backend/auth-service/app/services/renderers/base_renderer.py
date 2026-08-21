"""Base Report Renderer Interface (Phase 4.0 Part 3 — Section 2).

Defines universal contract for all format-specific report renderers:
JSON, HTML, PDF, Markdown, and CSV.
"""

from abc import ABC, abstractmethod
import hashlib
from typing import Any, Optional, Dict
from app.schemas.digital_trust_report_models import ReportDocumentDTO
from app.schemas.trust_narrative_models import NarrativeDocumentDTO


class BaseReportRenderer(ABC):
    """Universal interface for all Digital Trust Report renderers."""

    @abstractmethod
    def validate_input(
        self,
        report_doc: ReportDocumentDTO,
        narrative_doc: Optional[NarrativeDocumentDTO] = None,
    ) -> bool:
        """Validate that input report and narrative documents are structurally valid."""
        pass

    @abstractmethod
    def render(
        self,
        report_doc: ReportDocumentDTO,
        narrative_doc: Optional[NarrativeDocumentDTO] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> bytes:
        """Render format-specific output bytes from authoritative report models.

        MUST NEVER recalculate risk, modify findings, or alter analytical results.
        """
        pass

    @abstractmethod
    def validate_output(self, rendered_bytes: bytes) -> bool:
        """Validate that the rendered output is non-empty and well-formed."""
        pass

    def calculate_size(self, rendered_bytes: bytes) -> int:
        """Calculate byte size of rendered artifact."""
        return len(rendered_bytes) if rendered_bytes else 0

    def calculate_hash(self, rendered_bytes: bytes) -> str:
        """Calculate SHA-256 hash of exact artifact bytes."""
        if not rendered_bytes:
            return hashlib.sha256(b"").hexdigest()
        return hashlib.sha256(rendered_bytes).hexdigest()

    @abstractmethod
    def get_content_type(self) -> str:
        """Return MIME content type for HTTP responses."""
        pass

    @abstractmethod
    def get_file_extension(self) -> str:
        """Return canonical file extension."""
        pass

    @abstractmethod
    def get_renderer_version(self) -> str:
        """Return semantic version of the renderer."""
        pass
