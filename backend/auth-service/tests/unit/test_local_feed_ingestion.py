"""Unit tests for Local/Offline Feed Ingestion (Phase 3.9 Part 1A.23)."""

import pytest
from app.services.threat_feed_ingestion_service import ThreatFeedIngestionService


def test_local_feed_ingestion_service():
    service = ThreatFeedIngestionService()
    records = [
        {"indicator": "phish.example.com", "reputation": "PHISHING"},
        {"malformed_field": "no_indicator_key"},
    ]

    feed_dto = service.ingest_feed("Test Phish Feed", records)

    assert feed_dto.feed_name == "Test Phish Feed"
    assert feed_dto.record_count == 1  # Malformed record isolated
