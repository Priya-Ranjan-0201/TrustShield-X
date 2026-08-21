/**
 * Enterprise Governance, Authorization & Compliance Console Main Page (Phase 4.0 Part 8).
 */

import React, { useState, useEffect } from 'react';
import { GovernanceDashboard } from '../components/GovernanceDashboard';
import { OrganizationUsers } from '../components/OrganizationUsers';
import { PolicyManagement } from '../components/PolicyManagement';
import { AuditDashboard } from '../components/AuditDashboard';
import { governanceApi } from '../services/governanceApi';
import {
  Organization,
  UserLifecycle,
  Role,
  GovernancePolicy,
  AuditEvent,
  ComplianceFramework,
  LegalHold,
} from '../types';

export const GovernanceConsolePage: React.FC = () => {
  const [org, setOrg] = useState<Organization | null>(null);
  const [users, setUsers] = useState<UserLifecycle[]>([]);
  const [roles, setRoles] = useState<Role[]>([]);
  const [policies, setPolicies] = useState<GovernancePolicy[]>([]);
  const [auditEvents, setAuditEvents] = useState<AuditEvent[]>([]);
  const [frameworks, setFrameworks] = useState<ComplianceFramework[]>([]);
  const [legalHolds, setLegalHolds] = useState<LegalHold[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const loadData = async () => {
    try {
      const [o, u, r, p, a, f, lh] = await Promise.all([
        governanceApi.getOrganization(),
        governanceApi.listUsers(),
        governanceApi.listRoles(),
        governanceApi.listPolicies(),
        governanceApi.queryAudit(50),
        governanceApi.listFrameworks(),
        governanceApi.listLegalHolds(),
      ]);
      setOrg(o);
      setUsers(u);
      setRoles(r);
      setPolicies(p);
      setAuditEvents(a);
      setFrameworks(f);
      setLegalHolds(lh);
      setLoading(false);
    } catch {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleInviteUser = async (email: string, userRoles: string[], fullName: string) => {
    await governanceApi.inviteUser(email, userRoles, fullName);
    loadData();
  };

  const handleSimulatePolicy = async (policyId: string) => {
    return await governanceApi.simulatePolicy(policyId);
  };

  const handleVerifyIntegrity = async () => {
    return await governanceApi.verifyAuditIntegrity();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-slate-950 text-slate-400">
        Loading Enterprise Governance Control Plane...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col p-6 gap-6">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-xl font-bold text-slate-100">Enterprise Governance Control Plane</h1>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-indigo-950 text-indigo-400 border border-indigo-800 font-mono font-semibold">
              RBAC / ABAC / POLICY CONTROL
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Server-side authorization, immutable policy versioning, data classification, legal hold preservation, and append-only audit intelligence.
          </p>
        </div>

        <button
          onClick={loadData}
          className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700 shadow"
        >
          Refresh Control Plane
        </button>
      </div>

      {/* Metrics Row */}
      <GovernanceDashboard
        org={org}
        users={users}
        roles={roles}
        policies={policies}
        frameworks={frameworks}
      />

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <OrganizationUsers
          users={users}
          roles={roles}
          onInviteUser={handleInviteUser}
        />

        <PolicyManagement
          policies={policies}
          onSimulatePolicy={handleSimulatePolicy}
          onCreatePolicy={async (name, rules) => {
            await governanceApi.createPolicy(name, rules);
            loadData();
          }}
        />
      </div>

      {/* Audit Stream */}
      <AuditDashboard
        events={auditEvents}
        onVerifyIntegrity={handleVerifyIntegrity}
      />
    </div>
  );
};
