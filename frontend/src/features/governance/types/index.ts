/**
 * TypeScript Definitions for Enterprise Governance, RBAC/ABAC & Compliance (Phase 4.0 Part 8).
 */

export interface Organization {
  organization_id: string;
  organization_name: string;
  slug: string;
  status: "ACTIVE" | "SUSPENDED" | "READ_ONLY" | "DECOMMISSION_PENDING" | "DECOMMISSIONED";
  plan: string;
  region: string;
  timezone: string;
  data_residency: string;
  created_at: string;
  updated_at: string;
}

export interface UserLifecycle {
  user_id: string;
  organization_id: string;
  email: string;
  full_name: string;
  status: "INVITED" | "ACTIVE" | "SUSPENDED" | "LOCKED" | "DEACTIVATED" | "DELETED" | "PENDING_DELETION";
  roles: string[];
  mfa_enforced: boolean;
  mfa_enabled: boolean;
  last_login_at?: string;
  created_at: string;
}

export interface Role {
  role_id: string;
  organization_id?: string;
  name: string;
  description: string;
  system_role: boolean;
  permissions: string[];
  scope: string;
  version: number;
  status: string;
  created_by: string;
}

export interface GovernancePolicy {
  policy_id: string;
  organization_id: string;
  name: string;
  description: string;
  policy_type: string;
  version: number;
  status: string;
  rules: Array<{
    resource?: string;
    action?: string;
    effect: "ALLOW" | "DENY" | "REQUIRE_APPROVAL" | "REQUIRE_MFA";
    reason?: string;
  }>;
  priority: number;
  created_by: string;
}

export interface PolicySimulation {
  simulation_id: string;
  policy_id: string;
  affected_users_count: number;
  affected_resources_count: number;
  new_denials_count: number;
  new_approvals_count: number;
  conflicts_detected: string[];
  simulation_verdict: string;
  simulated_at: string;
}

export interface AuditEvent {
  audit_id: string;
  organization_id: string;
  actor_type: string;
  actor_id: string;
  action: string;
  resource_type: string;
  resource_id: string;
  result: string;
  reason: string;
  previous_hash?: string;
  event_hash: string;
  timestamp: string;
}

export interface ComplianceFramework {
  framework_id: string;
  name: string;
  version: string;
  jurisdiction: string;
  description: string;
  control_count: number;
  status: string;
}

export interface ComplianceAssessment {
  assessment_id: string;
  framework_id: string;
  organization_id: string;
  status: string;
  score_percentage: number;
  control_count: number;
  implemented_count: number;
  partial_count: number;
  failed_count: number;
  exception_count: number;
  assessed_at: string;
}

export interface LegalHold {
  hold_id: string;
  organization_id: string;
  resource_type: string;
  resource_id: string;
  reason: string;
  created_by: string;
  status: string;
  created_at: string;
}

export interface APIKeyMetadata {
  key_id: string;
  organization_id: string;
  name: string;
  key_prefix: string;
  scope: string;
  permissions: string[];
  status: string;
  owner_id: string;
  expires_at?: string;
  created_at: string;
  last_used_at?: string;
}

export interface GovernancePosture {
  organization_id: string;
  overall_posture_score: number;
  authorization_maturity: number;
  policy_coverage: number;
  mfa_coverage: number;
  audit_coverage: number;
  retention_coverage: number;
  compliance_coverage: number;
}
