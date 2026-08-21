/**
 * TypeScript Definitions for Real-Time Trust Monitoring & Continuous Intelligence (Phase 4.0 Part 6).
 */

export interface ThreatFeedConfiguration {
  feed_id: string;
  provider_name: string;
  provider_type: string;
  endpoint: string;
  enabled: boolean;
  poll_interval: string;
  poll_interval_seconds: number;
  authentication_mode: string;
  timeout_seconds: number;
  trust_level: string;
  supported_types: string[];
  created_at: string;
  updated_at: string;
}

export interface ThreatFeedHealth {
  health_id: string;
  feed_id: string;
  status: "HEALTHY" | "DEGRADED" | "STALE" | "UNAVAILABLE" | "AUTH_FAILURE" | "RATE_LIMITED" | "INVALID_DATA" | "DISABLED" | "UNKNOWN";
  last_success?: string;
  last_failure?: string;
  last_attempt?: string;
  latency_ms: float;
  items_received: number;
  items_accepted: number;
  items_rejected: number;
  parse_errors: number;
  rate_limit_errors: number;
  staleness_days: number;
  provider_version: string;
}

export interface SecurityAlert {
  alert_id: string;
  case_id?: string;
  analysis_id?: string;
  event_id?: string;
  alert_type: string;
  title: string;
  description: string;
  priority: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFORMATIONAL";
  severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFORMATIONAL";
  confidence: string;
  status: "NEW" | "ACKNOWLEDGED" | "IN_PROGRESS" | "ESCALATED" | "SUPPRESSED" | "RESOLVED" | "CLOSED" | "REOPENED" | "EXPIRED";
  source: string;
  evidence_ids: string[];
  finding_ids: string[];
  entity_ids: string[];
  relationship_ids: string[];
  campaign_id?: string;
  attack_chain_id?: string;
  alert_fingerprint: string;
  created_at: string;
  updated_at: string;
  acknowledged_at?: string;
  resolved_at?: string;
  suppressed_until?: string;
}

export interface SecurityIncident {
  incident_id: string;
  case_id?: string;
  incident_type: string;
  title: string;
  status: "DETECTED" | "TRIAGED" | "INVESTIGATING" | "CONTAINED" | "ERADICATED" | "RECOVERED" | "CLOSED" | "REOPENED";
  priority: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFORMATIONAL";
  severity: string;
  confidence: string;
  first_seen: string;
  last_seen: string;
  alert_count: number;
  entity_count: number;
  finding_count: number;
  campaign_id?: string;
  attack_chain_id?: string;
  created_at: string;
  updated_at: string;
}

export interface IntelligenceEvent {
  event_id: string;
  event_type: string;
  producer: string;
  entity_id?: string;
  analysis_id?: string;
  case_id?: string;
  timestamp: string;
  correlation_id: string;
  payload: Record<string, any>;
  provenance: string;
}

export interface ThreatFeedSyncResponse {
  feed_id: string;
  status: string;
  items_received: number;
  items_accepted: number;
  items_rejected: number;
  changes_detected: number;
  events_published: number;
  alerts_generated: number;
  execution_time_ms: number;
}
