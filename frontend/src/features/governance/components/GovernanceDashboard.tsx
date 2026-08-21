/**
 * Enterprise Governance & Security Posture Dashboard (Phase 4.0 Part 8 — Section 64).
 */

import React from 'react';
import { Organization, UserLifecycle, Role, GovernancePolicy, ComplianceFramework } from '../types';

export const GovernanceDashboard: React.FC<{
  org: Organization | null;
  users: UserLifecycle[];
  roles: Role[];
  policies: GovernancePolicy[];
  frameworks: ComplianceFramework[];
}> = ({ org, users, roles, policies, frameworks }) => {
  const mfaEnabledCount = users.filter((u) => u.mfa_enabled || u.mfa_enforced).length;
  const mfaPercentage = users.length > 0 ? Math.round((mfaEnabledCount / users.length) * 100) : 100;

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      {/* Organization Posture */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between shadow-lg">
        <div className="flex items-center justify-between">
          <span className="text-xs text-slate-400 font-medium">Tenant Context</span>
          <span className="text-xs px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 font-mono">
            {org?.status || 'ACTIVE'}
          </span>
        </div>
        <div className="mt-2">
          <div className="text-base font-bold text-slate-100 truncate">{org?.organization_name || 'Enterprise'}</div>
          <span className="text-xs text-slate-500 font-mono">{org?.slug || 'tenant-root'}</span>
        </div>
      </div>

      {/* Access & MFA Coverage */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between shadow-lg">
        <div className="flex items-center justify-between">
          <span className="text-xs text-cyan-400 font-medium">MFA Policy Coverage</span>
          <span className="text-xs px-1.5 py-0.5 rounded bg-cyan-950 text-cyan-300 font-mono">Auth Strength</span>
        </div>
        <div className="mt-2 flex items-baseline gap-2">
          <span className="text-2xl font-bold text-cyan-300">{mfaPercentage}%</span>
          <span className="text-xs text-slate-500">({mfaEnabledCount}/{users.length} users)</span>
        </div>
      </div>

      {/* Active Policies & Roles */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between shadow-lg">
        <div className="flex items-center justify-between">
          <span className="text-xs text-indigo-400 font-medium">Active Policies & Roles</span>
          <span className="text-xs px-1.5 py-0.5 rounded bg-indigo-950 text-indigo-300 font-mono">RBAC/ABAC</span>
        </div>
        <div className="mt-2 flex items-baseline gap-2">
          <span className="text-2xl font-bold text-indigo-300">{policies.length} Policies</span>
          <span className="text-xs text-slate-500">({roles.length} roles)</span>
        </div>
      </div>

      {/* Compliance Frameworks */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between shadow-lg">
        <div className="flex items-center justify-between">
          <span className="text-xs text-amber-400 font-medium">Mapped Frameworks</span>
          <span className="text-xs px-1.5 py-0.5 rounded bg-amber-950 text-amber-300 font-mono">Evidence-Backed</span>
        </div>
        <div className="mt-2 flex items-baseline gap-2">
          <span className="text-2xl font-bold text-amber-300">{frameworks.length} Frameworks</span>
          <span className="text-xs text-slate-500">ISO / SOC2 / DPDP</span>
        </div>
      </div>
    </div>
  );
};
