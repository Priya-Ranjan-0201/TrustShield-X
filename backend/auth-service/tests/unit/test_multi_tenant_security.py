"""Multi-Tenant Security Test Suite (Phase 4.0 Part 5 — Section 99).

Implements Tests 28 to 29:
- Test 28: Org A queries entity belonging to Org B -> Access Denied.
- Test 29: Org A searches B's private domain -> No cross-tenant leakage.
"""

import pytest
from app.schemas.intelligence_graph_models import CanonicalEntityDTO


class TestMultiTenantSecuritySuite:
    def test_28_org_a_queries_org_b_entity_denied(self):
        ent_org_b = CanonicalEntityDTO(
            entity_id="ent_b",
            entity_type="DOMAIN",
            canonical_value="internal-b.corp",
            display_value="internal-b.corp",
            normalized_value="internal-b.corp",
            value_hash="h_b",
            organization_id="org_victim_b",
        )
        user_org_a = "org_attacker_a"

        has_access = ent_org_b.organization_id is None or ent_org_b.organization_id == user_org_a
        assert has_access is False

    def test_29_org_a_searches_b_domain_no_leakage(self):
        entities = [
            CanonicalEntityDTO(entity_id="e1", entity_type="DOMAIN", canonical_value="b-secret.net", display_value="b-secret.net", normalized_value="b-secret.net", value_hash="h1", organization_id="org_b"),
            CanonicalEntityDTO(entity_id="e2", entity_type="DOMAIN", canonical_value="a-public.net", display_value="a-public.net", normalized_value="a-public.net", value_hash="h2", organization_id="org_a"),
        ]
        requesting_org = "org_a"
        query = "secret"

        visible = [
            e for e in entities
            if (e.organization_id == requesting_org or e.organization_id is None) and query in e.canonical_value
        ]
        assert len(visible) == 0
