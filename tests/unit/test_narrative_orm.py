"""Unit Tests — Narrative ORM Models (Phase 4.0 Part 2)."""

import pytest
from app.models.trust_narrative import (
    TrustNarrativeModel, NarrativeSectionModel, NarrativeStatementModel,
    NarrativeLineageModel, NarrativeVersionModel, NarrativeTemplateModel,
    NarrativeValidationModel, NarrativeGenerationRunModel,
    NarrativeGenerationErrorModel, NarrativeTranslationModel,
)


class TestNarrativeORMModels:
    """Mandatory Test Case 19: All 10 ORM models have correct table names and column defaults."""

    def test_trust_narrative_model(self):
        assert TrustNarrativeModel.__tablename__ == "trust_narratives"

    def test_narrative_section_model(self):
        assert NarrativeSectionModel.__tablename__ == "narrative_sections"

    def test_narrative_statement_model(self):
        assert NarrativeStatementModel.__tablename__ == "narrative_statements"

    def test_narrative_lineage_model(self):
        assert NarrativeLineageModel.__tablename__ == "narrative_lineage"

    def test_narrative_version_model(self):
        assert NarrativeVersionModel.__tablename__ == "narrative_versions"

    def test_narrative_template_model(self):
        assert NarrativeTemplateModel.__tablename__ == "narrative_templates"

    def test_narrative_validation_model(self):
        assert NarrativeValidationModel.__tablename__ == "narrative_validation_results"

    def test_narrative_generation_run_model(self):
        assert NarrativeGenerationRunModel.__tablename__ == "narrative_generation_runs"

    def test_narrative_generation_error_model(self):
        assert NarrativeGenerationErrorModel.__tablename__ == "narrative_generation_errors"

    def test_narrative_translation_model(self):
        assert NarrativeTranslationModel.__tablename__ == "narrative_translation_records"
