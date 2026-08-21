"""OCR Engine Abstraction Layer.

Engine priority: PaddleOCR primary → EasyOCR fallback → regex-based dev fallback.
If both ML engines fail or return confidence < 0.4, falls back to next engine.
If all fail, raises TSX-DOC-001 error.
30-second timeout enforced per document (TSX-DOC-002 on exceed).

NOTE: This phase uses heuristic/regex-based extraction as a development fallback
when PaddleOCR and EasyOCR are not installed. This is stated plainly — not a
fabricated "trained model" claim.
"""

import asyncio
import re
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


OCR_TIMEOUT_SECONDS = 30
MIN_CONFIDENCE_THRESHOLD = 0.4


@dataclass
class OCRResult:
    """Normalized OCR output — engine-agnostic."""
    text: str
    confidence: float  # 0.0–1.0, OCR engine's own reported confidence
    word_boxes: List[Dict[str, Any]] = field(default_factory=list)
    engine_used: str = "none"
    lines: List[str] = field(default_factory=list)


class BaseOCREngine(ABC):
    """Abstract OCR engine interface. All engines normalize to OCRResult."""

    @abstractmethod
    async def extract_text(self, image_bytes: bytes) -> OCRResult:
        pass


class PaddleOCREngine(BaseOCREngine):
    """Primary OCR engine using PaddleOCR."""

    async def extract_text(self, image_bytes: bytes) -> OCRResult:
        try:
            from paddleocr import PaddleOCR
            import numpy as np
        except ImportError:
            raise ImportError("PaddleOCR not installed")

        nparr = np.frombuffer(image_bytes, np.uint8)

        try:
            import cv2
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        except ImportError:
            raise ImportError("OpenCV not available for PaddleOCR image decoding")

        if img is None:
            raise ValueError("Failed to decode image for PaddleOCR")

        # Resize to max 2048px on longest edge before OCR
        h, w = img.shape[:2]
        if max(h, w) > 2048:
            scale = 2048 / max(h, w)
            img = cv2.resize(img, (int(w * scale), int(h * scale)))

        ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
        result = ocr.ocr(img, cls=True)

        lines = []
        confidences = []
        word_boxes = []

        if result and result[0]:
            for line_data in result[0]:
                box, (text, conf) = line_data
                lines.append(text)
                confidences.append(conf)
                word_boxes.append({"text": text, "confidence": conf, "box": box})

        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        full_text = "\n".join(lines)

        return OCRResult(
            text=full_text,
            confidence=avg_confidence,
            word_boxes=word_boxes,
            engine_used="PaddleOCR",
            lines=lines,
        )


class EasyOCREngine(BaseOCREngine):
    """Fallback OCR engine using EasyOCR."""

    async def extract_text(self, image_bytes: bytes) -> OCRResult:
        try:
            import easyocr
            import numpy as np
        except ImportError:
            raise ImportError("EasyOCR not installed")

        nparr = np.frombuffer(image_bytes, np.uint8)

        try:
            import cv2
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        except ImportError:
            raise ImportError("OpenCV not available for EasyOCR image decoding")

        if img is None:
            raise ValueError("Failed to decode image for EasyOCR")

        # Resize to max 2048px on longest edge before OCR
        h, w = img.shape[:2]
        if max(h, w) > 2048:
            scale = 2048 / max(h, w)
            img = cv2.resize(img, (int(w * scale), int(h * scale)))

        reader = easyocr.Reader(['en'], gpu=False)
        results = reader.readtext(img)

        lines = []
        confidences = []
        word_boxes = []

        for (box, text, conf) in results:
            lines.append(text)
            confidences.append(conf)
            word_boxes.append({"text": text, "confidence": conf})

        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        full_text = "\n".join(lines)

        return OCRResult(
            text=full_text,
            confidence=avg_confidence,
            word_boxes=word_boxes,
            engine_used="EasyOCR",
            lines=lines,
        )


class RegexFallbackEngine(BaseOCREngine):
    """Development fallback: extracts printable text from raw bytes.
    This is NOT an ML-based OCR engine — it extracts embedded text strings
    from PDF/image metadata and embedded text layers. Stated plainly per
    Rules.md honesty requirement.
    """

    async def extract_text(self, image_bytes: bytes) -> OCRResult:
        decoded = image_bytes.decode("latin-1", errors="ignore")

        # Extract text from PDF text streams
        pdf_text_chunks = re.findall(r'\(([^)]{2,})\)', decoded)

        # Extract readable ASCII runs (min 4 chars)
        ascii_runs = re.findall(r'[A-Za-z0-9\s@.,:;/\-]{4,}', decoded)

        all_chunks = pdf_text_chunks + ascii_runs

        # Deduplicate and filter noise
        seen = set()
        clean_lines = []
        for chunk in all_chunks:
            chunk = chunk.strip()
            if len(chunk) >= 3 and chunk not in seen:
                seen.add(chunk)
                clean_lines.append(chunk)

        full_text = "\n".join(clean_lines)

        return OCRResult(
            text=full_text,
            confidence=0.35,  # Below ML threshold — signals dev fallback was used
            word_boxes=[],
            engine_used="RegexFallback (development — not ML-based OCR)",
            lines=clean_lines,
        )


class OCROrchestrator:
    """Orchestrates OCR extraction with engine priority and timeout.

    Priority: PaddleOCR → EasyOCR → RegexFallback
    Timeout: 30 seconds per document (TSX-DOC-002)
    Min confidence: 0.4 (triggers fallback to next engine)
    """

    def __init__(self):
        self.engines: List[BaseOCREngine] = [
            PaddleOCREngine(),
            EasyOCREngine(),
            RegexFallbackEngine(),
        ]

    async def extract_text(self, image_bytes: bytes) -> OCRResult:
        """Tries each engine in priority order. Returns first successful result
        with confidence >= 0.4, or the last engine's result regardless."""

        last_error: Optional[Exception] = None

        for i, engine in enumerate(self.engines):
            is_last_engine = (i == len(self.engines) - 1)
            try:
                result = await asyncio.wait_for(
                    engine.extract_text(image_bytes),
                    timeout=OCR_TIMEOUT_SECONDS,
                )

                # Accept if confidence meets threshold or it's the last engine
                if result.confidence >= MIN_CONFIDENCE_THRESHOLD or is_last_engine:
                    return result

                # Confidence too low — try next engine
                continue

            except asyncio.TimeoutError:
                if is_last_engine:
                    raise RuntimeError(
                        "TSX-DOC-002: OCR processing exceeded 30-second timeout. "
                        "Document may be too complex or corrupted."
                    )
                continue

            except (ImportError, Exception) as e:
                last_error = e
                if is_last_engine:
                    raise RuntimeError(
                        f"TSX-DOC-001: Unable to read document text. "
                        f"All OCR engines failed. Last error: {str(e)}"
                    )
                continue

        # Should never reach here, but safety net
        raise RuntimeError("TSX-DOC-001: Unable to read document text — no OCR engine succeeded.")
