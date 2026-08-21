/**
 * API Client for Unified Trust Intelligence Graph (Phase 4.0 Part 5).
 */

import {
  CanonicalEntity,
  GraphRelationship,
  ThreatCampaign,
  AttackChain,
  UnifiedGraphResponse,
  CorrelationExplanation,
  CorrelationReviewItem,
} from '../types';

const API_BASE = '/api/v1/intelligence';

export const intelligenceApi = {
  async getUnifiedGraph(params?: { caseId?: string; depth?: number; minConfidence?: string }): Promise<UnifiedGraphResponse> {
    const q = new URLSearchParams();
    if (params?.caseId) q.append('case_id', params.caseId);
    if (params?.depth) q.append('depth', params.depth.toString());
    if (params?.minConfidence) q.append('min_confidence', params.minConfidence);

    const res = await fetch(`${API_BASE}/graph?${q.toString()}`);
    const json = await res.json();
    return json.data;
  },

  async getEntity(entityId: string): Promise<CanonicalEntity> {
    const res = await fetch(`${API_BASE}/entities/${encodeURIComponent(entityId)}`);
    const json = await res.json();
    return json.data;
  },

  async getEntityNeighbors(entityId: string, depth = 1): Promise<GraphRelationship[]> {
    const res = await fetch(`${API_BASE}/entities/${encodeURIComponent(entityId)}/neighbors?depth=${depth}`);
    const json = await res.json();
    return json.data;
  },

  async listCampaigns(limit = 50): Promise<ThreatCampaign[]> {
    const res = await fetch(`${API_BASE}/campaigns?limit=${limit}`);
    const json = await res.json();
    return json.data;
  },

  async getCampaign(campaignId: string): Promise<ThreatCampaign> {
    const res = await fetch(`${API_BASE}/campaigns/${encodeURIComponent(campaignId)}`);
    const json = await res.json();
    return json.data;
  },

  async getAttackChain(chainId: string): Promise<AttackChain> {
    const res = await fetch(`${API_BASE}/attack-chains/${encodeURIComponent(chainId)}`);
    const json = await res.json();
    return json.data;
  },

  async searchIntelligence(query: string, entityTypes?: string[]): Promise<any> {
    const q = new URLSearchParams({ q: query });
    if (entityTypes) entityTypes.forEach((t) => q.append('entity_types', t));
    const res = await fetch(`${API_BASE}/search?${q.toString()}`);
    const json = await res.json();
    return json.data;
  },

  async listReviewQueue(limit = 50): Promise<CorrelationReviewItem[]> {
    const res = await fetch(`${API_BASE}/review-queue?limit=${limit}`);
    const json = await res.json();
    return json.data;
  },
};
