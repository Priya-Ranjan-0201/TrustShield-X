/**
 * TypeScript Definitions for SOC Operations & Incident Response (Phase 4.0 Part 7).
 */

export interface SOCAlert {
  alert_id: string;
  source_alert_id?: string;
  source_system: string;
  alert_type: string;
  category: string;
  subcategory?: string;
  title: string;
  description: string;
  severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFORMATIONAL";
  priority: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFORMATIONAL";
  confidence: string;
  status: string;
  entity_ids: string[];
  finding_ids: string[];
  evidence_ids: string[];
  relationship_ids: string[];
  campaign_id?: string;
  attack_chain_id?: string;
  case_id?: string;
  incident_id?: string;
  first_seen: string;
  last_seen: string;
  created_at: string;
  updated_at: string;
}

export interface SecurityIncident {
  incident_id: string;
  incident_number: string;
  title: string;
  description: string;
  incident_type: string;
  severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFORMATIONAL";
  priority: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFORMATIONAL";
  confidence: string;
  status: "NEW" | "TRIAGE" | "ASSIGNED" | "INVESTIGATING" | "CONTAINMENT_PENDING" | "CONTAINED" | "ERADICATION" | "RECOVERY" | "RESOLVED" | "CLOSED" | "REOPENED" | "CANCELLED";
  owner_id?: string;
  team_id?: string;
  source_alert_count: number;
  entity_count: number;
  finding_count: number;
  evidence_count: number;
  campaign_id?: string;
  attack_chain_id?: string;
  case_id?: string;
  incident_fingerprint: string;
  first_seen: string;
  last_seen: string;
  detected_at: string;
  acknowledged_at?: string;
  contained_at?: string;
  resolved_at?: string;
  closed_at?: string;
  created_at: string;
  updated_at: string;
}

export interface TriageResult {
  triage_id: string;
  incident_id: string;
  classification: string;
  severity: string;
  priority: string;
  confidence: string;
  summary: string;
  affected_entities: string[];
  evidence_ids: string[];
  finding_ids: string[];
  recommended_actions: Array<{
    action_type: string;
    target: string;
    risk: string;
    reason: string;
    requires_approval: boolean;
  }>;
  uncertainties: string[];
  limitations: string[];
  created_at: string;
}

export interface PlaybookStep {
  step_id: string;
  playbook_id: string;
  step_number: number;
  name: string;
  description: string;
  action_type: string;
  risk_level: string;
  approval_required: boolean;
  dry_run_supported: boolean;
  rollback_supported: boolean;
  timeout: number;
}

export interface ResponsePlaybook {
  playbook_id: string;
  name: string;
  current_version: number;
  description: string;
  incident_types: string[];
  required_permissions: string[];
  steps: PlaybookStep[];
  enabled: boolean;
}

export interface ResponseAction {
  action_id: string;
  incident_id: string;
  playbook_id?: string;
  playbook_version: number;
  step_id?: string;
  action_type: string;
  target: string;
  target_type: string;
  requested_by: string;
  approved_by?: string;
  approval_status: "NOT_REQUIRED" | "PENDING" | "APPROVED" | "REJECTED" | "EXPIRED" | "CANCELLED";
  dry_run: boolean;
  status: "QUEUED" | "VALIDATING" | "WAITING_APPROVAL" | "DRY_RUN" | "EXECUTING" | "VERIFYING" | "COMPLETED" | "FAILED" | "ROLLBACK_PENDING" | "ROLLING_BACK" | "ROLLED_BACK" | "CANCELLED" | "TIMED_OUT" | "UNKNOWN_EXECUTION_STATE";
  reason: string;
  started_at?: string;
  completed_at?: string;
  result_reference?: string;
  created_at: string;
}

export interface ApprovalRequest {
  approval_id: string;
  action_id: string;
  incident_id: string;
  requested_by: string;
  approver_scope: string;
  reason: string;
  risk: string;
  evidence: string[];
  expires_at: string;
  status: string;
}

export interface ResponseSimulation {
  simulation_id: string;
  action_id: string;
  target: string;
  provider: string;
  expected_effect: string;
  risk_assessment: string;
  required_permissions: string[];
  rollback_supported: boolean;
  side_effects: string[];
}
