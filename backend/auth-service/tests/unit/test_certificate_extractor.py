"""Unit tests for Certificate Intelligence Extractor (Phase 3.7 Part 1A Message 3A)."""

import os
import tempfile
import pytest
from app.services.certificate_extractor import APKCertificateExtractor, CertificateMetadata


def test_certificate_extractor_fallback_nonexistent():
    extractor = APKCertificateExtractor()
    meta = extractor.extract_certificates("nonexistent_path.apk")
    assert meta.certificate_unavailable is True


def test_certificate_extractor_empty_archive():
    extractor = APKCertificateExtractor()
    buf = tempfile.NamedTemporaryFile(delete=False, suffix=".apk")
    buf.write(b"PK\x03\x04 empty zip file")
    buf.close()

    try:
        meta = extractor.extract_certificates(buf.name)
        assert meta.certificate_unavailable is True
    finally:
        os.remove(buf.name)
