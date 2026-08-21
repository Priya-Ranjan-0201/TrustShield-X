/**
 * API Client for Real-Time Trust Monitoring & Continuous Intelligence (Phase 4.0 Part 6).
 */

import {
  ThreatFeedConfiguration,
  ThreatFeedSyncResponse,
  SecurityAlert,
  SecurityIncident,
  IntelligenceEvent,
} from '../types';

const API_BASE = '/api/v1';

export const monitoringApi = {
  async listFeeds(): Promise<ThreatFeedConfiguration[]> {
    const res = await fetch(`${API_BASE}/intelligence/feeds`);
    const json = await res.json();
    return json.data;
  },

  async getFeed(feedId: string): Promise<ThreatFeedConfiguration> {
    const res = await fetch(`${API_BASE}/intelligence/feeds/${encodeURIComponent(feedId)}`);
    const json = await res.json();
    return json.data;
  },

  async syncFeed(feedId: string): Promise<ThreatFeedSyncResponse> {
    const res = await fetch(`${API_BASE}/intelligence/feeds/${encodeURIComponent(feedId)}/sync`, {
      method: 'POST',
    });
    const json = await res.json();
    return json.data;
  },

  async listAlerts(params?: { status?: string; priority?: string; caseId?: string }): Promise<SecurityAlert[]> {
    const q = new URLSearchParams();
    if (params?.status) q.append('status', params.status);
    if (params?.priority) q.append('priority', params.priority);
    if (params?.caseId) q.append('case_id', params.caseId);

    const res = await fetch(`${API_BASE}/security/alerts?${q.toString()}`);
    const json = await res.json();
    return json.data;
  },

  async getAlert(alertId: string): Promise<SecurityAlert> {
    const res = await fetch(`${API_BASE}/security/alerts/${encodeURIComponent(alertId)}`);
    const json = await res.json();
    return json.data;
  },

  async acknowledgeAlert(alertId: string, reason: string, comment?: string): Promise<any> {
    const res = await fetch(`${API_BASE}/security/alerts/${encodeURIComponent(alertId)}/acknowledge`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reason, comment }),
    });
    return (await res.json()).data;
  },

  async escalateAlert(alertId: string, priority: string, reason: string): Promise<any> {
    const res = await fetch(`${API_BASE}/security/alerts/${encodeURIComponent(alertId)}/escalate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ priority, reason }),
    });
    return (await res.json()).data;
  },

  async suppressAlert(alertId: string, reason: string, durationHours = 24): Promise<any> {
    const res = await fetch(`${API_BASE}/security/alerts/${encodeURIComponent(alertId)}/suppress`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reason, duration_hours: durationHours }),
    });
    return (await res.json()).data;
  },

  async resolveAlert(alertId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/security/alerts/${encodeURIComponent(alertId)}/resolve`, {
      method: 'POST',
    });
    return (await res.json()).data;
  },

  async listIncidents(): Promise<SecurityIncident[]> {
    const res = await fetch(`${API_BASE}/security/incidents`);
    const json = await res.json();
    return json.data;
  },

  async listRealtimeEvents(): Promise<IntelligenceEvent[]> {
    const res = await fetch(`${API_BASE}/realtime/events`);
    const json = await res.json();
    return json.data;
  },
};
