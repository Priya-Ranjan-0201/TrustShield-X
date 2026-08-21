"""
TruthShield X — Release Guardian Unit & Adversarial Gate Tests
==============================================================
Validates:
- ReleaseCandidate creation, 17-vector classification, impact graph, targeted test selection
- 13 Release Guardian Gates evaluation
- Human Four-Eyes Approval Enforcement (AI agents strictly forbidden from self-approval)
- Adversarial Release Defense (detects fake results, skipped tests, forged build hashes)
- Deployment with post-deployment sanity verification
- Safe Automated Rollback
"""

import pytest
from app.services.release_guardian import (
    release_guardian_engine,
    ReleaseCandidateStatus,
    ChangeCategory,
)


def test_create_release_candidate_and_classification():
    cand = release_guardian_engine.create_release_candidate(
        version="4.1.0-rc1",
        commit_hash="git:a1b2c3d4e5",
        author="Lead_Security_Architect",
        changed_components=["auth_service", "tenancy", "rbac"],
        change_types=["AUTHORIZATION", "TENANT_ISOLATION"],
        description="Strengthening tenant boundary enforcement."
    )
    assert cand["release_id"].startswith("REL-4.1.0-rc1")
    assert cand["risk_level"] == "CRITICAL"
    assert ChangeCategory.TENANT.value in cand["categories"]
    assert ChangeCategory.AUTHORIZATION.value in cand["categories"]
    assert "tests/unit/test_tenant_isolation.py" in cand["tests_selected"]
    assert cand["impact_graph"]["critical_path_affected"] is True


def test_release_evaluation_and_human_approval_lifecycle():
    cand = release_guardian_engine.create_release_candidate(
        version="4.1.0-rc2",
        commit_hash="git:e5f6g7h8",
        author="DevOps_Engineer",
        changed_components=["ai_governance", "web_dashboard"],
        change_types=["AI", "FRONTEND"],
        description="Updating AI safety guardrails."
    )
    rel_id = cand["release_id"]

    # 1. Evaluate release
    eval_res = release_guardian_engine.evaluate_release_candidate(
        release_id=rel_id,
        test_execution_results={"test_integrity_valid": True}
    )
    assert eval_res["decision"] in [ReleaseCandidateStatus.APPROVED.value, ReleaseCandidateStatus.CONDITIONAL_APPROVAL.value]
    assert "CRITICAL_SECURITY_GATE" in eval_res["gates"]

    # 2. Adversarial rejection: AI agent attempts to approve itself
    ai_approval = release_guardian_engine.record_human_approval(
        release_id=rel_id,
        approver="AI_Agent_Copilot_Autonomous",
        role="AI_ASSISTANT",
        justification="Self-approving this release."
    )
    assert ai_approval["success"] is False
    assert "SECURITY VIOLATION" in ai_approval["error"]

    # 3. Valid Human Approval
    human_approval = release_guardian_engine.record_human_approval(
        release_id=rel_id,
        approver="usr_chief_security_officer",
        role="CISO",
        justification="All security tests verified and approved."
    )
    assert human_approval["success"] is True
    assert human_approval["status"] == ReleaseCandidateStatus.APPROVED.value

    # 4. Deploy release
    deploy_res = release_guardian_engine.deploy_release(release_id=rel_id, deployed_by="usr_ciso")
    assert deploy_res["success"] is True
    assert deploy_res["post_deployment_sanity"]["health_probes"] == "HEALTHY"

    # 5. Rollback release
    rollback_res = release_guardian_engine.rollback_release(
        release_id=rel_id,
        reason="Post-release synthetic latency deviation",
        authorized_by="usr_ciso"
    )
    assert rollback_res["success"] is True
    assert rollback_res["active_version"] == "4.0.0-PROD-CERTIFIED"


def test_adversarial_release_manipulation_defense():
    cand = release_guardian_engine.create_release_candidate(
        version="4.1.0-malicious-rc",
        commit_hash="git:evil_hash",
        author="Adversary",
        changed_components=["crypto", "auth"],
        change_types=["SECURITY"],
    )
    rel_id = cand["release_id"]

    # Adversarial probe: fake test results / manipulated coverage
    eval_res = release_guardian_engine.evaluate_release_candidate(
        release_id=rel_id,
        test_execution_results={"test_integrity_valid": False},
        adversarial_probe_results={"fake_results_detected": True}
    )
    assert eval_res["decision"] == ReleaseCandidateStatus.BLOCKED.value
    assert eval_res["gates"]["TEST_AND_ARTIFACT_INTEGRITY_GATE"] == "FAIL"
    assert any(b["gate"] == "TEST_AND_ARTIFACT_INTEGRITY_GATE" for b in eval_res["blockers"])
