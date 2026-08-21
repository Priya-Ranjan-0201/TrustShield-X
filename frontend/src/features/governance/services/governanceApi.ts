/**
 * API Client for Enterprise Governance, RBAC, Compliance & Audit (Phase 4.0 Part 8).
 */

import {
  Organization,
  UserLifecycle,
  Role,
  GovernancePolicy,
  PolicySimulation,
  AuditEvent,
  ComplianceFramework,
  ComplianceAssessment,
  LegalHold,
  APIKeyMetadata,
} from '../types';

const API_BASE = '/api/v1/governance';

export const governanceApi = {
  async getOrganization(): Promise<Organization> {
    const res = await fetch(`${API_BASE}/organization`);
    return (await res.json()).data;
  },

  async listUsers(): Promise<UserLifecycle[]> {
    const res = await fetch(`${API_BASE}/users`);
    return (await res.json()).data;
  },

  async inviteUser(email: string, roles: string[], fullName = ''): Promise<UserLifecycle> {
    const res = await fetch(`${API_BASE}/users/invite`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, roles, full_name: fullName }),
    });
    return (await res.json()).data;
  },

  async listRoles(): Promise<Role[]> {
    const res = await fetch(`${API_BASE}/roles`);
    return (await res.json()).data;
  },

  async createRole(name: string, permissions: string[], description = ''): Promise<any> {
    const res = await fetch(`${API_BASE}/roles`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, permissions, description }),
    });
    return (await res.json()).data;
  },

  async listPolicies(): Promise<GovernancePolicy[]> {
    const res = await fetch(`${API_BASE}/policies`);
    return (await res.json()).data;
  },

  async createPolicy(name: string, rules: any[], policyType = 'ACCESS_CONTROL'): Promise<any> {
    const res = await fetch(`${API_BASE}/policies`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, rules, policy_type: policyType }),
    });
    return (await res.json()).data;
  },

  async simulatePolicy(policyId: string): Promise<PolicySimulation> {
    const res = await fetch(`${API_BASE}/policies/${encodeURIComponent(policyId)}/simulate`, {
      method: 'POST',
    });
    return (await res.json()).data;
  },

  async queryAudit(limit = 50): Promise<AuditEvent[]> {
    const res = await fetch(`${API_BASE}/audit?limit=${limit}`);
    return (await res.json()).data;
  },

  async verifyAuditIntegrity(): Promise<{ integrity_status: string }> {
    const res = await fetch(`${API_BASE}/audit/integrity`);
    return (await res.json()).data;
  },

  async listFrameworks(): Promise<ComplianceFramework[]> {
    const res = await fetch(`${API_BASE}/compliance/frameworks`);
    return (await res.json()).data;
  },

  async assessFramework(frameworkId: string): Promise<ComplianceAssessment> {
    const res = await fetch(`${API_BASE}/compliance/${encodeURIComponent(frameworkId)}/assess`, {
      method: 'POST',
    });
    return (await res.json()).data;
  },

  async listLegalHolds(): Promise<LegalHold[]> {
    const res = await fetch(`${API_BASE}/legal-holds`);
    return (await res.json()).data;
  },

  async createLegalHold(resourceType: string, resourceId: string, reason: string): Promise<LegalHold> {
    const res = await fetch(`${API_BASE}/legal-holds`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ resource_type: resourceType, resource_id: resourceId, reason }),
    });
    return (await res.json()).data;
  },

  async listApiKeys(): Promise<APIKeyMetadata[]> {
    const res = await fetch(`${API_BASE}/api-keys`);
    return (await res.json()).data;
  },

  async createApiKey(name: string, permissions: string[], validityDays = 90): Promise<any> {
    const res = await fetch(`${API_BASE}/api-keys`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, permissions, validity_days: validityDays }),
    });
    return (await res.json()).data;
  },
};
