/**
 * API Client for SOC Operations & Incident Response (Phase 4.0 Part 7).
 */

import {
  SOCAlert,
  SecurityIncident,
  TriageResult,
  ResponsePlaybook,
  ResponseAction,
  ResponseSimulation,
} from '../types';

const API_BASE = '/api/v1/soc';

export const socApi = {
  async listAlerts(): Promise<SOCAlert[]> {
    const res = await fetch(`${API_BASE}/alerts`);
    const json = await res.json();
    return json.data;
  },

  async listIncidents(): Promise<SecurityIncident[]> {
    const res = await fetch(`${API_BASE}/incidents`);
    const json = await res.json();
    return json.data;
  },

  async getIncident(incidentId: string): Promise<SecurityIncident> {
    const res = await fetch(`${API_BASE}/incidents/${encodeURIComponent(incidentId)}`);
    const json = await res.json();
    return json.data;
  },

  async assignIncident(incidentId: string, analystId: string): Promise<SecurityIncident> {
    const res = await fetch(`${API_BASE}/incidents/${encodeURIComponent(incidentId)}/assign`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ analyst_id: analystId }),
    });
    return (await res.json()).data;
  },

  async triageIncident(incidentId: string): Promise<TriageResult> {
    const res = await fetch(`${API_BASE}/incidents/${encodeURIComponent(incidentId)}/triage`, {
      method: 'POST',
    });
    return (await res.json()).data;
  },

  async listPlaybooks(): Promise<ResponsePlaybook[]> {
    const res = await fetch(`${API_BASE}/playbooks`);
    const json = await res.json();
    return json.data;
  },

  async createAction(incidentId: string, payload: { action_type: string; target: string; reason: string; requires_approval: boolean }): Promise<any> {
    const res = await fetch(`${API_BASE}/incidents/${encodeURIComponent(incidentId)}/actions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return (await res.json()).data;
  },

  async simulateAction(actionId: string): Promise<ResponseSimulation> {
    const res = await fetch(`${API_BASE}/actions/${encodeURIComponent(actionId)}/simulate`, {
      method: 'POST',
    });
    return (await res.json()).data;
  },

  async approveAction(approvalId: string, reason = 'Approved'): Promise<ResponseAction> {
    const res = await fetch(`${API_BASE}/approvals/${encodeURIComponent(approvalId)}/approve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reason }),
    });
    return (await res.json()).data;
  },

  async rejectAction(approvalId: string, reason = 'Rejected'): Promise<ResponseAction> {
    const res = await fetch(`${API_BASE}/approvals/${encodeURIComponent(approvalId)}/reject`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reason }),
    });
    return (await res.json()).data;
  },

  async executeAction(actionId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/actions/${encodeURIComponent(actionId)}/execute`, {
      method: 'POST',
    });
    return (await res.json()).data;
  },

  async rollbackAction(actionId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/actions/${encodeURIComponent(actionId)}/rollback`, {
      method: 'POST',
    });
    return (await res.json()).data;
  },
};
