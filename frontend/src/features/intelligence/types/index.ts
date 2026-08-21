/**
 * TypeScript Definitions for Unified Trust Intelligence Graph (Phase 4.0 Part 5).
 */

export interface CanonicalEntity {
  entity_id: string;
  entity_type: string;
  canonical_value: string;
  display_value: string;
  normalized_value: string;
  value_hash: string;
  source_count: number;
  first_seen: string;
  last_seen: string;
  confidence: "VERY_HIGH" | "HIGH" | "MEDIUM" | "LOW" | "VERY_LOW" | "UNKNOWN";
  resolution_status: string;
  privacy_classification: string;
  organization_id?: string;
  aliases: string[];
  metadata: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface GraphRelationship {
  relationship_id: string;
  source_entity_id: string;
  target_entity_id: string;
  relationship_type: string;
  confidence: "VERY_HIGH" | "HIGH" | "MEDIUM" | "LOW" | "VERY_LOW" | "UNKNOWN";
  evidence_strength: string;
  resolution_status: string;
  correlation_method: string;
  correlation_version: string;
  first_observed: string;
  last_observed: string;
  source_count: number;
  evidence_ids: string[];
  finding_ids: string[];
  analysis_ids: string[];
  provenance_ids: string[];
  status: "ACTIVE" | "WEAK" | "STALE" | "CONFLICTED" | "REVOKED" | "UNRESOLVED";
  is_manual: boolean;
  author_id?: string;
  staleness_reason?: string;
  conflicting_sources: string[];
  metadata: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface ThreatCampaign {
  campaign_id: string;
  name: string;
  campaign_type: string;
  status: string;
  confidence: string;
  first_seen: string;
  last_seen: string;
  entity_count: number;
  analysis_count: number;
  finding_count: number;
  evidence_count: number;
  relationship_count: number;
  threat_actor: string;
  threat_actor_confidence: string;
  entities: string[];
  attack_chain_ids: string[];
}

export interface AttackChainStep {
  step_id: string;
  chain_id: string;
  step_number: number;
  stage: "ENTRY_POINT" | "EXECUTION" | "COLLECTION" | "TRANSMISSION" | "IMPACT";
  title: string;
  description: string;
  step_state: "CONFIRMED_STEP" | "SUPPORTED_STEP" | "POSSIBLE_STEP" | "UNRESOLVED_STEP" | "MISSING_STEP" | "CONTRADICTED_STEP";
  confidence: string;
  entity_ids: string[];
  evidence_ids: string[];
  finding_ids: string[];
  missing_evidence_note?: string;
}

export interface AttackChain {
  chain_id: string;
  case_id?: string;
  campaign_id?: string;
  title: string;
  entry_point: string;
  confidence: string;
  status: string;
  steps: AttackChainStep[];
  evidence_ids: string[];
  finding_ids: string[];
  missing_steps_count: number;
  uncertainty_summary: string;
  created_at: string;
  updated_at: string;
}

export interface UnifiedGraphResponse {
  graph_version: number;
  total_nodes: number;
  total_edges: number;
  nodes: CanonicalEntity[];
  edges: GraphRelationship[];
  campaigns: ThreatCampaign[];
  attack_chains: AttackChain[];
  truncated: boolean;
  query_timestamp: string;
}

export interface CorrelationExplanation {
  relationship_id: string;
  source_entity: string;
  target_entity: string;
  relationship_type: string;
  confidence: string;
  why_connected: string;
  evidence_signals: string[];
  correlation_rule: string;
  rule_version: string;
  false_correlation_risk: string;
  unresolved_questions: string[];
}

export interface CorrelationReviewItem {
  review_id: string;
  relationship_id: string;
  source_entity_value: string;
  target_entity_value: string;
  relationship_type: string;
  confidence: string;
  flag_reason: string;
  priority: string;
  status: string;
  created_at: string;
}
