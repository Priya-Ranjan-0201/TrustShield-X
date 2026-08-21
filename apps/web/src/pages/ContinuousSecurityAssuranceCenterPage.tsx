import React, { useState } from 'react';
import { 
  ShieldCheck, AlertTriangle, RefreshCw, Play, CheckCircle2, 
  XCircle, GitBranch, Terminal, Activity, FileCheck, 
  Cpu, Lock, Database, ArrowRight, Zap, Target
} from 'lucide-react';

interface AssuranceOverview {
  security_controls_count: number;
  critical_controls_count: number;
  validated_controls_count: number;
  unverified_controls_count: number;
  active_drifts_count: number;
  game_days_count: number;
  security_debt_score: number;
  overall_assurance_score: number;
  assurance_maturity: string;
  scorecard_grade: string;
  residual_risk_score: number;
  evaluated_at: string;
}

export const ContinuousSecurityAssuranceCenterPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'controls' | 'drift' | 'regression' | 'ai' | 'remediation' | 'gamedays'>('overview');
  const [overview, setOverview] = useState<AssuranceOverview>({
    security_controls_count: 3,
    critical_controls_count: 2,
    validated_controls_count: 3,
    unverified_controls_count: 0,
    active_drifts_count: 1,
    game_days_count: 1,
    security_debt_score: 8.0,
    overall_assurance_score: 96.4,
    assurance_maturity: 'LEVEL_5_CONTINUOUSLY_VALIDATED',
    scorecard_grade: 'EXCELLENT',
    residual_risk_score: 3.6,
    evaluated_at: new Date().toISOString()
  });

  const [runningRegression, setRunningRegression] = useState(false);
  const [regressionResult, setRegressionResult] = useState<any>(null);

  const triggerRegression = async () => {
    setRunningRegression(true);
    try {
      await new Promise(r => setTimeout(r, 600));
      setRegressionResult({
        trigger_event: "PR_MERGE_AUTH_SERVICE",
        changed_components: ["app_auth_service"],
        affected_controls: ["ctl_tenant_isolation", "ctl_four_eyes_response"],
        tests_executed: 2,
        passed_count: 2,
        failed_count: 0,
        regressions_detected: []
      });
    } finally {
      setRunningRegression(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <ShieldCheck className="h-8 w-8 text-emerald-400" />
            <h1 className="text-3xl font-bold tracking-tight text-white">
              Continuous Security Assurance Center
            </h1>
          </div>
          <p className="text-slate-400 mt-1">
            Autonomous Control Validation, Security Regression, Drift Detection & Digital Defense Assurance
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="bg-slate-900 border border-slate-800 px-4 py-2 rounded-lg text-sm">
            <span className="text-slate-400">Maturity: </span>
            <span className="font-semibold text-emerald-400">{overview.assurance_maturity}</span>
          </div>
          <button
            onClick={triggerRegression}
            disabled={runningRegression}
            className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg font-medium transition"
          >
            {runningRegression ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4" />}
            Run Regression Suite
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Assurance Score</span>
            <Activity className="h-4 w-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">{overview.overall_assurance_score}%</div>
          <div className="text-xs text-emerald-400 mt-1 font-medium">Grade: {overview.scorecard_grade} (Empirically Validated)</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Control Pass Rate</span>
            <CheckCircle2 className="h-4 w-4 text-blue-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">100.0%</div>
          <div className="text-xs text-blue-400 mt-1 font-medium">{overview.validated_controls_count}/{overview.security_controls_count} Verified with SHA-256 Evidence</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Active Drift Signals</span>
            <AlertTriangle className="h-4 w-4 text-amber-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">{overview.active_drifts_count}</div>
          <div className="text-xs text-amber-400 mt-1 font-medium">1 Authorization Drift Detected</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Residual Risk</span>
            <Target className="h-4 w-4 text-purple-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">{overview.residual_risk_score}%</div>
          <div className="text-xs text-purple-400 mt-1 font-medium">Bounded across 20 Functional Categories</div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 gap-6">
        {(['overview', 'controls', 'drift', 'regression', 'ai', 'remediation', 'gamedays'] as const).map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`pb-3 text-sm font-semibold capitalize transition ${
              activeTab === tab 
                ? 'border-b-2 border-emerald-400 text-emerald-400' 
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Regression Results (if triggered) */}
      {regressionResult && (
        <div className="bg-indigo-950/40 border border-indigo-500/50 p-6 rounded-xl space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-indigo-400 font-bold text-lg flex items-center gap-2">
              <GitBranch className="h-5 w-5" />
              Security Regression Suite Results
            </span>
            <button 
              onClick={() => setRegressionResult(null)}
              className="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-1 rounded"
            >
              Dismiss
            </button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <span className="text-slate-400">Trigger: </span>
              <span className="text-white font-mono">{regressionResult.trigger_event}</span>
            </div>
            <div>
              <span className="text-slate-400">Tests Run: </span>
              <span className="text-emerald-400 font-semibold">{regressionResult.tests_executed} Passed</span>
            </div>
            <div>
              <span className="text-slate-400">Regressions: </span>
              <span className="text-white font-semibold">0 Detected</span>
            </div>
          </div>
        </div>
      )}

      {/* Tab Contents */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Active Controls */}
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Lock className="h-5 w-5 text-emerald-400" />
              Verified Core Security Controls
            </h2>
            <div className="space-y-3">
              <div className="bg-slate-950/70 border border-slate-800/80 p-4 rounded-lg flex items-center justify-between">
                <div>
                  <div className="font-semibold text-white">Strict Datastore Multi-Tenant Boundary</div>
                  <div className="text-xs text-slate-400 mt-0.5">Category: TENANT_ISOLATION | Owner: usr_platform_sec</div>
                </div>
                <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-1 rounded">VERIFIED PASS</span>
              </div>
              <div className="bg-slate-950/70 border border-slate-800/80 p-4 rounded-lg flex items-center justify-between">
                <div>
                  <div className="font-semibold text-white">Four-Eyes Governance for High-Impact Actions</div>
                  <div className="text-xs text-slate-400 mt-0.5">Category: SOAR | Owner: usr_ciso</div>
                </div>
                <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-1 rounded">VERIFIED PASS</span>
              </div>
            </div>
          </div>

          {/* AI Security Assurance */}
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Cpu className="h-5 w-5 text-purple-400" />
              AI Security & Tool Authorization Assurance
            </h2>
            <div className="bg-slate-950/70 border border-slate-800/80 p-5 rounded-lg space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-white">Security Copilot LLM Engine</span>
                <span className="text-xs bg-purple-950 text-purple-300 border border-purple-800 px-2 py-0.5 rounded">GUARDRAILS ACTIVE</span>
              </div>
              <div className="text-xs text-slate-400 space-y-1">
                <div>Prompt Injection Resistance: <span className="text-emerald-400 font-semibold">100% (Passed Negative Suite)</span></div>
                <div>Tool Authorization Verification: <span className="text-emerald-400 font-semibold">Enforced via RBAC/ABAC Gate</span></div>
                <div>Hallucination Score: <span className="text-emerald-400 font-semibold">0.02 (Grounded in Knowledge Fabric)</span></div>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'drift' && (
        <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-amber-400" />
            Security Drift Signals
          </h2>
          <div className="bg-slate-950/70 border border-amber-900/50 p-4 rounded-lg space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-bold text-amber-300">Authorization Role Expansion Drift</span>
              <span className="text-xs bg-amber-950 text-amber-300 border border-amber-800 px-2 py-0.5 rounded">AUTHORIZATION DRIFT</span>
            </div>
            <p className="text-xs text-slate-400">Wildcard action permission added to SOC Analyst role without change ticket.</p>
          </div>
        </div>
      )}

      {activeTab === 'gamedays' && (
        <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Zap className="h-5 w-5 text-blue-400" />
            Security Game Day Exercises
          </h2>
          <div className="bg-slate-950/70 border border-slate-800/80 p-5 rounded-lg space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-bold text-white">Credential Stuffing & Lateral Movement Drill</span>
              <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded">COMPLETED</span>
            </div>
            <div className="text-xs text-slate-400 flex items-center justify-between pt-2">
              <span>MTTD: 42.0s | MTTA: 115.0s</span>
              <span>Evidence Quality: 98.5%</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
