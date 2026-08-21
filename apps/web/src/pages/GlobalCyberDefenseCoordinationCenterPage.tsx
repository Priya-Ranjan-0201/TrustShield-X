import React, { useState } from 'react';
import { 
  ShieldCheck, Users, Share2, Lock, FileCheck2, 
  CheckCircle2, AlertTriangle, Play, RefreshCw, Layers, 
  EyeOff, Globe, BookOpen, Clock, Activity, ShieldAlert, Cpu
} from 'lucide-react';

interface CoordinationCase {
  coordination_id: string;
  objective: string;
  severity: string;
  participating_entities: string[];
  execution_status: string;
  verification_status: string;
  classification: string;
}

export const GlobalCyberDefenseCoordinationCenterPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'cases' | 'networks' | 'sanitization' | 'approvals' | 'knowledge' | 'scorecard'>('overview');
  const [cases, setCases] = useState<any[]>([
    {
      coordination_id: "coord_darkstorm_finance_defense",
      objective: "Coordinated API Gateway Rate-Limiting & C2 Ingress Quarantine across Finance Peers",
      severity: "HIGH",
      participating_entities: ["tenant_finance_alpha", "tenant_cloud_beta"],
      execution_status: "ACTIVE",
      verification_status: "VERIFIED",
      classification: "CONFIDENTIAL",
      outcome: "DarkStorm C2 lateral propagation intercepted across 100% of participating peers."
    }
  ]);

  const [executing, setExecuting] = useState(false);
  const [executionResult, setExecutionResult] = useState<any>(null);

  const triggerFourEyesExecution = async () => {
    setExecuting(true);
    try {
      await new Promise(r => setTimeout(r, 600));
      setExecutionResult({
        action_id: "act_darkstorm_c2_block",
        status: "EXECUTED",
        approvers: ["CISO_ALPHA", "SOC_LEAD_BETA"],
        outcome: "Coordinated mitigation deployed across authorized peers. Containment verified in Digital Twin."
      });
    } finally {
      setExecuting(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <ShieldCheck className="h-8 w-8 text-indigo-400" />
            <h1 className="text-3xl font-bold tracking-tight text-white">
              Global Cyber Defense Coordination Center
            </h1>
          </div>
          <p className="text-slate-400 mt-1">
            Privacy-Preserving Threat-to-Response Orchestration, Four-Eyes Approvals & Coordinated Defense
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="bg-slate-900 border border-slate-800 px-4 py-2 rounded-lg text-sm">
            <span className="text-slate-400">Defense Networks: </span>
            <span className="font-semibold text-emerald-400">1 ACTIVE</span>
          </div>
          <button
            onClick={triggerFourEyesExecution}
            disabled={executing}
            className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg font-medium transition"
          >
            {executing ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4" />}
            Execute Coordinated Mitigation
          </button>
        </div>
      </div>

      {/* KPI Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Active Coordination Cases</span>
            <Users className="h-4 w-4 text-indigo-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">1</div>
          <div className="text-xs text-indigo-400 mt-1 font-medium">DarkStorm Joint Defense Active</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Four-Eyes Approval Gate</span>
            <Lock className="h-4 w-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-extrabold text-emerald-400">SATISFIED</div>
          <div className="text-xs text-emerald-400 mt-1 font-medium">2 Independent Approvals Recorded</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Privacy Sanitization</span>
            <EyeOff className="h-4 w-4 text-cyan-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">100%</div>
          <div className="text-xs text-cyan-400 mt-1 font-medium">Secrets & PII Auto-Redacted</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Coordination SLA</span>
            <Clock className="h-4 w-4 text-amber-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">&lt; 15m</div>
          <div className="text-xs text-amber-400 mt-1 font-medium">Response SLA 100% Compliant</div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 gap-6">
        {(['overview', 'cases', 'networks', 'sanitization', 'approvals', 'knowledge', 'scorecard'] as const).map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`pb-3 text-sm font-semibold capitalize transition ${
              activeTab === tab 
                ? 'border-b-2 border-indigo-400 text-indigo-400' 
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            {tab.replace('_', ' ')}
          </button>
        ))}
      </div>

      {/* Execution Result Banner */}
      {executionResult && (
        <div className="bg-indigo-950/40 border border-indigo-500/50 p-6 rounded-xl space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-indigo-300 font-bold text-lg flex items-center gap-2">
              <CheckCircle2 className="h-5 w-5 text-emerald-400" />
              Coordinated Defense Plan Executed
            </span>
            <span className="text-xs bg-indigo-950 text-indigo-300 border border-indigo-800 px-2 py-0.5 rounded font-mono">
              [FOUR-EYES VERIFIED]
            </span>
          </div>
          <p className="text-sm text-slate-200">{executionResult.outcome}</p>
        </div>
      )}

      {/* Tab Contents */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Active Coordination Cases */}
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Users className="h-5 w-5 text-indigo-400" />
              Active Coordination Cases
            </h2>
            {cases.map((c, idx) => (
              <div key={idx} className="bg-slate-950/70 border border-slate-800/80 p-5 rounded-lg space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-white">{c.objective}</span>
                  <span className="text-xs bg-indigo-950 text-indigo-300 border border-indigo-800 px-2 py-0.5 rounded font-mono">
                    {c.execution_status}
                  </span>
                </div>
                <div className="text-xs text-slate-400">
                  <span>Participants: {c.participating_entities.join(', ')}</span>
                </div>
                <div className="text-xs text-emerald-400 bg-slate-900/80 p-2.5 rounded border border-slate-800">
                  {c.outcome}
                </div>
              </div>
            ))}
          </div>

          {/* Defensive Knowledge & Playbooks */}
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <BookOpen className="h-5 w-5 text-cyan-400" />
              Shared Defensive Knowledge & Playbooks
            </h2>
            <div className="bg-slate-950/70 border border-slate-800/80 p-5 rounded-lg space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-white">DarkStorm C2 DNS Entropy Sigma Rule</span>
                <span className="text-xs bg-cyan-950 text-cyan-300 border border-cyan-800 px-2 py-0.5 rounded font-mono">
                  [VALIDATED]
                </span>
              </div>
              <p className="text-xs text-slate-300">
                Deploy DNS Entropy Detection Sigma Rule & Dynamic Rate-Limiter to stop C2 bursts.
              </p>
              <div className="text-xs text-cyan-400">
                Validation: Verified 85% Containment in Phase 26 Digital Twin Lab
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'sanitization' && (
        <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <EyeOff className="h-5 w-5 text-cyan-400" />
            Automatic Privacy & Secret Sanitization Queue
          </h2>
          <div className="bg-slate-950/70 border border-slate-800/80 p-5 rounded-lg space-y-3 font-mono text-xs">
            <div className="text-emerald-400 font-bold">100% Sanitization Verified</div>
            <div className="text-slate-400">
              Raw: &#123; "target_ip": "10.0.4.15", "admin_email": "ciso@alpha.org", "api_token": "sk_live_991823" &#125;
            </div>
            <div className="text-cyan-300">
              Sanitized: &#123; "target_ip": "[REDACTED_PRIVATE_IP]", "admin_email": "[REDACTED_PII]", "api_token": "[REDACTED_SECRET]" &#125;
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
