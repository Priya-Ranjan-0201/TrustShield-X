/**
 * TypeScript Interfaces for TruthShield X Investigation Workspace (Phase 4.0 Part 4).
 */

export type InvestigationRole = 'EXECUTIVE' | 'ANALYST' | 'TECHNICAL' | 'AUDITOR' | 'ADMIN';

export type CaseStatus = 'OPEN' | 'IN_PROGRESS' | 'REVIEW' | 'CONTAINED' | 'RESOLVED' | 'CLOSED' | 'ARCHIVED';

export type CasePriority = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'INFORMATIONAL';

export interface WorkspaceContext {
  workspace_id: string;
  case_id?: string;
  analysis_id: string;
  report_id: string;
  report_version: string;
  user_id: string;
  organization_id: string;
  role: InvestigationRole;
  created_at: string;
  last_accessed_at: string;
}

export interface InvestigationCase {
  case_id: string;
  organization_id: string;
  title: string;
  description: string;
  status: CaseStatus;
  priority: CasePriority;
  owner_id: string;
  created_by: string;
  classification: string;
  retention_policy: string;
  created_at: string;
  updated_at: string;
  closed_at?: string;
  analysis_count: number;
  note_count: number;
  task_count: number;
}

export interface CaseAnalysis {
  link_id: string;
  case_id: string;
  analysis_id: string;
  module_type: string;
  target_identifier: string;
  status: string;
  risk_score: number;
  risk_band: string;
  attached_at: string;
}

export interface CaseNote {
  note_id: string;
  case_id: string;
  author_id: string;
  note_type: 'OBSERVATION' | 'HYPOTHESIS' | 'FOLLOW_UP' | 'INVESTIGATION' | 'FALSE_POSITIVE_REVIEW' | 'ESCALATION' | 'GENERAL';
  content: string;
  visibility: string;
  created_at: string;
}

export interface CaseBookmark {
  bookmark_id: string;
  case_id: string;
  user_id: string;
  item_type: string;
  item_id: string;
  label: string;
}

export interface CaseTask {
  task_id: string;
  case_id: string;
  title: string;
  description: string;
  assigned_to: string;
  priority: string;
  status: 'TODO' | 'IN_PROGRESS' | 'BLOCKED' | 'COMPLETED' | 'CANCELLED';
  due_at?: string;
}

export interface GraphNode {
  id: string;
  label: string;
  type: string;
  category: string;
  confidence: string;
  risk_contribution: number;
  properties: Record<string, any>;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  relationship: string;
  resolution_status: string;
  confidence: string;
  metadata: Record<string, any>;
}

export interface InvestigationGraph {
  analysis_id: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
  total_nodes: number;
  total_edges: number;
  truncated: boolean;
}

export interface TimelineEvent {
  event_id: string;
  analysis_id: string;
  timestamp: string;
  event_type: string;
  title: string;
  description: string;
  severity: string;
  source_module: string;
  related_entity_id?: string;
}

export interface SearchResultItem {
  object_type: string;
  object_id: string;
  title: string;
  summary: string;
  risk_reference?: string;
  timestamp: string;
  source_module: string;
  case_id?: string;
}
