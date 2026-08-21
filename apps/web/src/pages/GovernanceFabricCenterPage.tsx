import React, { useState } from 'react';
import { 
  FileCheck, 
  CheckCircle2, 
  AlertCircle, 
  ShieldAlert, 
  Layers, 
  Download, 
  Scale, 
  Clock, 
  Lock, 
  KeyRound, 
  Sparkles,
  Award
} from 'lucide-react';

interface RequirementItem {
  id: string;
  framework: string;
  ref: string;
  title: string;
  status: string;
  owner: string;
}

export const GovernanceFabricCenterPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'frameworks' | 'requirements' | 'evidence' | 'exceptions' | 'audit'>('overview');

  const [requirements] = useState<RequirementItem[]>([
    {
      id: 'req_dpdp_sec8',
      framework: 'DPDP Act 2023',
      ref: 'Sec. 8(5)',
      title: 'Reasonable Security Safeguards & Data Protection',
      status: 'SATISFIED',
      owner: 'Data Protection Officer',
    },
    {
      id: 'req_iso_a9_4',
      framework: 'ISO 27001:2022',
      ref: 'A.9.4.2',
      title: 'Secure Log-on Procedures & Access Control',
      status: 'SATISFIED',
      owner: 'Access Governance Lead',
    },
    {
      id: 'req_soc2_cc6_1',
      framework: 'SOC 2 Type II',
      ref: 'CC6.1',
      title: 'Logical Boundary & Multi-Tenant Isolation',
      status: 'SATISFIED',
      owner: 'Infrastructure Lead',
    },
    {
      id: 'req_nist_pr_ac',
      framework: 'NIST CSF 2.0',
      ref: 'PR.AC-4',
      title: 'Access Permissions & Principle of Least Privilege',
      status: 'SATISFIED',
      owner: 'Security Lead',
    },
  ]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 space-y-8 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-indigo-500/10 border border-indigo-500/30 rounded-xl text-indigo-400">
            <Scale className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
              Continuous Governance & Audit Fabric
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-medium">
                Audit-Ready Control Evidence
              </span>
            </h1>
            <p className="text-sm text-slate-400">
              Traceable Compliance Mapping, Zero-Trust Access Reviews, Evidence Automation & Manifest Generation
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 rounded-lg text-sm transition-colors">
            <Clock className="w-4 h-4" />
            Recalculate Posture
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition-colors shadow-lg shadow-indigo-600/20">
            <Download className="w-4 h-4" />
            Compile Audit Package
          </button>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Governance Posture Score</div>
          <div className="text-3xl font-bold text-indigo-400 mt-2">100.0%</div>
          <div className="text-xs text-indigo-400/80 flex items-center gap-1 mt-1">
            <CheckCircle2 className="w-3.5 h-3.5" /> All requirements verified
          </div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Compliance Confidence</div>
          <div className="text-3xl font-bold text-white mt-2">95%</div>
          <div className="text-xs text-emerald-400 mt-1">High evidence freshness</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Active Frameworks</div>
          <div className="text-3xl font-bold text-white mt-2">4</div>
          <div className="text-xs text-slate-400 mt-1">DPDP, ISO 27001, SOC 2, NIST</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Governance Gaps</div>
          <div className="text-3xl font-bold text-emerald-400 mt-2">0</div>
          <div className="text-xs text-emerald-400 mt-1">Zero unmapped controls</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 space-x-8">
        {[
          { id: 'overview', label: 'Governance Overview' },
          { id: 'frameworks', label: 'Framework Registry' },
          { id: 'requirements', label: 'Verifiable Requirements' },
          { id: 'evidence', label: 'Evidence Chains' },
          { id: 'exceptions', label: 'Exceptions & Risk Acceptance' },
          { id: 'audit', label: 'Audit Packages & Manifests' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`pb-4 text-sm font-medium transition-colors border-b-2 ${
              activeTab === tab.id
                ? 'border-indigo-500 text-indigo-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Requirements Table */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-800/50 text-slate-400 text-xs font-semibold uppercase tracking-wider">
            <tr>
              <th className="py-3 px-4">Requirement Title</th>
              <th className="py-3 px-4">Framework & Ref</th>
              <th className="py-3 px-4">Compliance Status</th>
              <th className="py-3 px-4">Owner</th>
              <th className="py-3 px-4">Evidence Link</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800 text-slate-300">
            {requirements.map((req) => (
              <tr key={req.id} className="hover:bg-slate-800/30 transition-colors">
                <td className="py-3.5 px-4 font-medium text-white flex items-center gap-2">
                  <FileCheck className="w-4 h-4 text-indigo-400" />
                  {req.title}
                </td>
                <td className="py-3.5 px-4 text-xs font-mono text-slate-400">
                  {req.framework} ({req.ref})
                </td>
                <td className="py-3.5 px-4">
                  <span className="px-2 py-0.5 text-xs rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-semibold">
                    {req.status}
                  </span>
                </td>
                <td className="py-3.5 px-4 text-slate-300">{req.owner}</td>
                <td className="py-3.5 px-4 text-xs font-mono text-indigo-400">SHA-256 Verified</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default GovernanceFabricCenterPage;
