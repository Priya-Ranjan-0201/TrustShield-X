import React, { useState } from 'react';
import { 
  Cpu, Shield, AlertTriangle, CheckCircle2, Play, 
  RotateCcw, Sparkles, Sliders, Layers, ArrowRight, 
  Activity, Zap, Eye, Check, X, Compass, Database, BarChart3
} from 'lucide-react';

export const AutonomousDefenseCenterPage: React.FC = () => {
  const [autonomyLevel, setAutonomyLevel] = useState<string>('LEVEL_4');
  const [activeTab, setActiveTab] = useState<'overview' | 'decisions' | 'experiments' | 'learning' | 'models' | 'rollbacks'>('overview');
  
  const [approving, setApproving] = useState(false);
  const [approvedAction, setApprovedAction] = useState<string | null>(null);

  const handleApprove = async (decisionId: string) => {
    setApproving(true);
    try {
      await new Promise(r => setTimeout(r, 600));
      setApprovedAction(decisionId);
    } finally {
      setApproving(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <Cpu className="h-8 w-8 text-emerald-400" />
            <h1 className="text-3xl font-bold tracking-tight text-white">
              Autonomous Defense Center
            </h1>
          </div>
          <p className="text-slate-400 mt-1">
            Self-Optimizing Cyber Defense, Continuous Detection-to-Response Learning & Governed Closed-Loop Optimization
          </p>
        </div>
        
        {/* Autonomy Level Indicator */}
        <div className="flex items-center gap-3 bg-slate-900 border border-slate-800 rounded-xl px-4 py-2">
          <div className="text-xs text-slate-400">Current Autonomy:</div>
          <div className="flex items-center gap-2">
            <span className="text-sm font-bold text-emerald-400">{autonomyLevel}</span>
            <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded font-mono">
              APPROVAL-CONTROLLED
            </span>
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Active Decisions</span>
            <Sliders className="h-4 w-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">12</div>
          <div className="text-xs text-emerald-400 mt-1 font-medium">100% Grounded in System State</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Detection Quality</span>
            <BarChart3 className="h-4 w-4 text-cyan-400" />
          </div>
          <div className="text-3xl font-extrabold text-cyan-400">96.0%</div>
          <div className="text-xs text-cyan-400 mt-1 font-medium">Precision across 18 rules | 0 Drift</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Verified Lessons</span>
            <Database className="h-4 w-4 text-amber-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">5</div>
          <div className="text-xs text-amber-400 mt-1 font-medium">Strict Tenant-Bounded Memory</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Automatic Rollback</span>
            <RotateCcw className="h-4 w-4 text-rose-400" />
          </div>
          <div className="text-3xl font-extrabold text-rose-400">READY</div>
          <div className="text-xs text-rose-400 mt-1 font-medium">Transactional State Reversion</div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 gap-6">
        {(['overview', 'decisions', 'experiments', 'learning', 'models', 'rollbacks'] as const).map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`pb-3 text-sm font-semibold capitalize transition ${
              activeTab === tab 
                ? 'border-b-2 border-emerald-400 text-emerald-400' 
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            {tab.replace('_', ' ')}
          </button>
        ))}
      </div>

      {/* Tab Contents */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Pending Recommendation & Four-Eyes Approval */}
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-amber-400" />
                Pending Recommendation (Level 4 Gate)
              </h2>
              <span className="text-xs bg-amber-950 text-amber-300 border border-amber-800 px-2 py-0.5 rounded font-mono">
                APPROVAL_REQUIRED
              </span>
            </div>

            <div className="bg-slate-950/70 border border-slate-800/80 p-5 rounded-lg space-y-3">
              <div className="font-bold text-white">Apply Dynamic Ingress WAF Rate-Limiting on Edge Gateway</div>
              <p className="text-xs text-slate-400">
                Rationale: DarkStorm C2 burst detected with 94% confidence. Digital Twin simulation validated 85% containment with zero collateral impact on benign users.
              </p>
              
              <div className="text-xs font-mono text-cyan-400 bg-slate-900/80 p-3 rounded border border-slate-800 space-y-1">
                <div>• Evidence: Sigma alert C2 burst + Digital Twin sandbox simulation log</div>
                <div>• Rollback Plan: Transactional rule baseline restore within 500ms</div>
                <div>• Autonomy Level: Level 4 (Requires CISO Four-Eyes confirmation)</div>
              </div>

              <div className="flex items-center gap-3 pt-2">
                <button
                  onClick={() => handleApprove("dec_waf_containment_01")}
                  disabled={approving || approvedAction === "dec_waf_containment_01"}
                  className="flex items-center gap-1.5 bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-lg text-xs font-semibold transition"
                >
                  <Check className="h-4 w-4" />
                  {approvedAction === "dec_waf_containment_01" ? "Approved & Deployed" : "Authorize & Deploy"}
                </button>
                <button
                  className="flex items-center gap-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 px-4 py-2 rounded-lg text-xs font-semibold transition"
                >
                  <X className="h-4 w-4" />
                  Reject
                </button>
              </div>
            </div>
          </div>

          {/* Active Champion/Challenger Experiment */}
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Activity className="h-5 w-5 text-cyan-400" />
              Active Champion / Challenger Experiment
            </h2>
            <div className="bg-slate-950/70 border border-slate-800/80 p-5 rounded-lg space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-bold text-white">DNS Entropy Detection Threshold Tuning</span>
                <span className="text-xs bg-cyan-950 text-cyan-300 border border-cyan-800 px-2 py-0.5 rounded font-mono">
                  RUNNING
                </span>
              </div>
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="bg-slate-900 p-3 rounded border border-slate-800">
                  <div className="text-slate-400">Baseline (Champion)</div>
                  <div className="text-white font-bold mt-1">Entropy Threshold 4.2</div>
                  <div className="text-slate-500 text-[11px]">Precision: 94.2%</div>
                </div>
                <div className="bg-slate-900 p-3 rounded border border-slate-800 border-cyan-800/50">
                  <div className="text-cyan-400">Candidate (Challenger)</div>
                  <div className="text-white font-bold mt-1">Entropy Threshold 3.9</div>
                  <div className="text-emerald-400 text-[11px] font-semibold">Precision: 97.1% (+15% FP drop)</div>
                </div>
              </div>
              <div className="text-xs text-slate-400">
                Stop Condition: If false negatives exceed 0, candidate is immediately rejected and rolled back.
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'learning' && (
        <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Database className="h-5 w-5 text-amber-400" />
            Verified Defensive Institutional Memory
          </h2>
          <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-bold text-white">DarkStorm C2 DNS Tunneling Anomaly Lesson</span>
              <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded font-mono">
                [VERIFIED & LEARNED]
              </span>
            </div>
            <p className="text-xs text-slate-300">
              Observation: DarkStorm leverages high entropy subdomain queries to exfiltrate tokens.
            </p>
            <div className="text-xs text-slate-400">
              Recommended Action: Enable early DNS entropy inspection filter | Applicability: <span className="text-amber-400 font-bold">TENANT_SPECIFIC</span> (Cannot generalize across tenants)
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
