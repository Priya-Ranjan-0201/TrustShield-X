import React, { useState } from 'react';
import { 
  ShieldCheck, 
  CheckCircle2, 
  AlertTriangle, 
  XCircle, 
  Clock, 
  RotateCw, 
  Activity, 
  Lock, 
  Layers, 
  Cpu,
  TrendingUp,
  FileCheck2
} from 'lucide-react';

interface ControlItem {
  id: string;
  name: string;
  category: string;
  status: string;
  verification: string;
  freshness: string;
}

export const SecurityAssuranceCenterPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'controls' | 'invariants' | 'drift' | 'slo'>('overview');

  const [controls] = useState<ControlItem[]>([
    {
      id: 'ctrl_iso_01',
      name: 'Tenant Data Isolation Boundary',
      category: 'TENANT_ISOLATION',
      status: 'ACTIVE',
      verification: 'VERIFIED',
      freshness: 'CURRENT',
    },
    {
      id: 'ctrl_rbac_01',
      name: 'ABAC / RBAC Explicit Deny Precedence',
      category: 'ACCESS_CONTROL',
      status: 'ACTIVE',
      verification: 'VERIFIED',
      freshness: 'CURRENT',
    },
    {
      id: 'ctrl_audit_01',
      name: 'SHA-256 Immutability Audit Chain',
      category: 'AUDIT',
      status: 'ACTIVE',
      verification: 'VERIFIED',
      freshness: 'CURRENT',
    },
    {
      id: 'ctrl_waf_01',
      name: 'Edge Threat WAF & Rate Limiting',
      category: 'PREVENTIVE',
      status: 'ACTIVE',
      verification: 'VERIFIED',
      freshness: 'CURRENT',
    },
  ]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 space-y-8 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-emerald-400">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
              Continuous Security Assurance Center
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-medium">
                Certified & Verified
              </span>
            </h1>
            <p className="text-sm text-slate-400">
              Continuous Control Testing, Drift Detection, Invariant Validation & Digital Defense Certification
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 rounded-lg text-sm transition-colors">
            <RotateCw className="w-4 h-4" />
            Run Full Validation Suite
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-medium transition-colors shadow-lg shadow-emerald-600/20">
            <FileCheck2 className="w-4 h-4" />
            Export Audit Certificate
          </button>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Overall Assurance Score</div>
          <div className="text-3xl font-bold text-emerald-400 mt-2">100.0%</div>
          <div className="text-xs text-emerald-400/80 flex items-center gap-1 mt-1">
            <CheckCircle2 className="w-3.5 h-3.5" /> All critical controls verified
          </div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Security Invariants</div>
          <div className="text-3xl font-bold text-white mt-2">5 / 5</div>
          <div className="text-xs text-slate-400 mt-1">Zero invariant violations</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Configuration Drift</div>
          <div className="text-3xl font-bold text-white mt-2">0</div>
          <div className="text-xs text-emerald-400 mt-1">Baselines fully synchronized</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Detection SLO Availability</div>
          <div className="text-3xl font-bold text-emerald-400 mt-2">99.98%</div>
          <div className="text-xs text-slate-400 mt-1">Target: 99.90%</div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 space-x-8">
        {[
          { id: 'overview', label: 'Assurance Overview' },
          { id: 'controls', label: 'Control Registry' },
          { id: 'invariants', label: 'Security Invariants' },
          { id: 'drift', label: 'Drift Detection' },
          { id: 'slo', label: 'Security SLOs & Error Budgets' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`pb-4 text-sm font-medium transition-colors border-b-2 ${
              activeTab === tab.id
                ? 'border-emerald-500 text-emerald-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Controls Table */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-800/50 text-slate-400 text-xs font-semibold uppercase tracking-wider">
            <tr>
              <th className="py-3 px-4">Control Name</th>
              <th className="py-3 px-4">Category</th>
              <th className="py-3 px-4">Verification State</th>
              <th className="py-3 px-4">Test Freshness</th>
              <th className="py-3 px-4">Lifecycle</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800 text-slate-300">
            {controls.map((ctrl) => (
              <tr key={ctrl.id} className="hover:bg-slate-800/30 transition-colors">
                <td className="py-3.5 px-4 font-medium text-white flex items-center gap-2">
                  <Lock className="w-4 h-4 text-emerald-400" />
                  {ctrl.name}
                </td>
                <td className="py-3.5 px-4 text-xs font-mono text-slate-400">{ctrl.category}</td>
                <td className="py-3.5 px-4">
                  <span className="px-2 py-0.5 text-xs rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-semibold">
                    {ctrl.verification}
                  </span>
                </td>
                <td className="py-3.5 px-4">
                  <span className="text-xs text-slate-300 flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5 text-emerald-400" /> {ctrl.freshness}
                  </span>
                </td>
                <td className="py-3.5 px-4 text-xs font-semibold text-emerald-300">{ctrl.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default SecurityAssuranceCenterPage;
