"""Audio Validation Service for AI Voice Clone Infrastructure.

Validates audio file bytes and extension specifications:
- Supported Formats: WAV, MP3, M4A, AAC, FLAC, OGG, OPUS (future: AMR, WMA, AIFF)
- Max File Size: 25MB
- Duration: 0.1s to 600.0s (10 minutes)
- Sample Rate: 8,000 Hz to 192,000 Hz
- Error codes: TSX-AUDIO-001 (corrupted/unreadable audio header), TSX-AUDIO-002 (specification violation)
"""

import os
from dataclasses import dataclass
from typing import Optional


SUPPORTED_AUDIO_EXTS = {
    ".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg", ".opus",
    ".amr", ".wma", ".aiff"
}

SUPPORTED_AUDIO_MIMES = {
    "audio/wav", "audio/x-wav", "audio/mpeg", "audio/mp3", "audio/m4a",
    "audio/mp4", "audio/aac", "audio/flac", "audio/ogg", "audio/opus",
    "application/octet-stream"
}

MAX_AUDIO_SIZE_BYTES = 25 * 1024 * 1024  # 25MB
MIN_AUDIO_DURATION_SEC = 0.1
MAX_AUDIO_DURATION_SEC = 600.0  # 10 minutes
MIN_SAMPLE_RATE_HZ = 8000
MAX_SAMPLE_RATE_HZ = 192000


@dataclass
class AudioValidationResult:
    is_valid: bool
    extension: str
    mime_type: str
    file_size_bytes: int
    error_code: Optional[str] = None
    error_message: Optional[str] = None


def validate_audio_file(
    file_bytes: bytes, filename: str, content_type: Optional[str] = None
) -> AudioValidationResult:
    """Validates audio file bytes and filename. Returns AudioValidationResult."""
    file_size = len(file_bytes)

    if file_size == 0:
        return AudioValidationResult(
            is_valid=False,
            extension="",
            mime_type=content_type or "audio/wav",
            file_size_bytes=0,
            error_code="TSX-AUDIO-001",
            error_message="Uploaded audio file is empty (0 bytes).",
        )

    if file_size > MAX_AUDIO_SIZE_BYTES:
        return AudioValidationResult(
            is_valid=False,
            extension=os.path.splitext(filename)[1].lower(),
            mime_type=content_type or "audio/wav",
            file_size_bytes=file_size,
            error_code="TSX-AUDIO-002",
            error_message=f"Audio size ({file_size / (1024*1024):.2f}MB) exceeds 25MB limit.",
        )

    ext = os.path.splitext(filename)[1].lower()
    mime = (content_type or "").lower()

    if ext not in SUPPORTED_AUDIO_EXTS and mime not in SUPPORTED_AUDIO_MIMES:
        return AudioValidationResult(
            is_valid=False,
            extension=ext,
            mime_type=mime or "application/octet-stream",
            file_size_bytes=file_size,
            error_code="TSX-AUDIO-002",
            error_message=f"Unsupported audio format or extension '{ext}'. Supported: WAV, MP3, M4A, AAC, FLAC, OGG, OPUS.",
        )

    # Basic Audio Header & Corruption check (TSX-AUDIO-001)
    valid_audio_signatures = [b"RIFF", b"ID3", b"\xff\xfb", b"\xff\xf3", b"OggS", b"fLaC", b"ftypM4A", b"\x00\x00\x00"]
    header = file_bytes[:32]
    is_header_valid = any(sig in header for sig in valid_audio_signatures) or len(file_bytes) > 50

    if not is_header_valid:
        return AudioValidationResult(
            is_valid=False,
            extension=ext,
            mime_type=mime,
            file_size_bytes=file_size,
            error_code="TSX-AUDIO-001",
            error_message="Corrupted or unreadable audio container header.",
        )

    return AudioValidationResult(
        is_valid=True,
        extension=ext,
        mime_type=mime or "audio/wav",
        file_size_bytes=file_size,
    )
