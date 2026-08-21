import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, AlertTriangle, RefreshCw, Play, CheckCircle2, 
  XCircle, Database, Server, GitPullRequest, Activity, 
  Clock, FileText, ArrowRight, Eye, ShieldAlert, Cpu, 
  CheckSquare, StopCircle, Lock
} from 'lucide-react';

interface ResilienceOverview {
  critical_assets_count: number;
  critical_services_count: number;
  single_points_of_failure_count: number;
  unresolved_gaps_count: number;
  active_plans_count: number;
  drills_count: number;
  unreconciled_drift_count: number;
  overall_resilience_score: number;
  resilience_maturity: string;
  scorecard_grade: string;
  evaluated_at: string;
}

export const CyberResilienceCommandCenterPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'services' | 'plans' | 'drills' | 'gaps' | 'backups' | 'drift'>('overview');
  const [loading, setLoading] = useState(false);
  const [overview, setOverview] = useState<ResilienceOverview>({
    critical_assets_count: 3,
    critical_services_count: 1,
    single_points_of_failure_count: 2,
    unresolved_gaps_count: 1,
    active_plans_count: 1,
    drills_count: 1,
    unreconciled_drift_count: 1,
    overall_resilience_score: 93.8,
    resilience_maturity: 'LEVEL_5_CONTINUOUSLY_VALIDATED',
    scorecard_grade: 'EXCELLENT',
    evaluated_at: new Date().toISOString()
  });

  const [simulating, setSimulating] = useState(false);
  const [simulationResult, setSimulationResult] = useState<any>(null);

  const triggerSimulation = async () => {
    setSimulating(true);
    try {
      // Synthetic simulation delay
      await new Promise(r => setTimeout(r, 600));
      setSimulationResult({
        mode: "SIMULATED",
        initial_target: "ast_pg_primary",
        attack_type: "RANSOMWARE_ENCRYPTION",
        simulated_blast_radius: 2,
        cascading_failures: [
          { component: "ast_api_gateway", status: "DEGRADED", reason: "Database connection pool exhausted" },
          { component: "svc_checkout_api", status: "OFFLINE", reason: "Unable to persist transaction ledger" }
        ],
        estimated_simulated_rto_minutes: 18.0,
        estimated_simulated_data_loss_minutes: 2.0,
        recommended_recovery_strategy: "RESTORE_FROM_BACKUP"
      });
    } finally {
      setSimulating(false);
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
              Cyber Resilience & Autonomous Recovery Center
            </h1>
          </div>
          <p className="text-slate-400 mt-1">
            Continuous Empirical Validation, Autonomous Recovery & Verified Business Continuity
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="bg-slate-900 border border-slate-800 px-4 py-2 rounded-lg text-sm">
            <span className="text-slate-400">Maturity: </span>
            <span className="font-semibold text-emerald-400">{overview.resilience_maturity}</span>
          </div>
          <button
            onClick={triggerSimulation}
            disabled={simulating}
            className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg font-medium transition"
          >
            {simulating ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4" />}
            Simulate Attack & Disruption
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Resilience Score</span>
            <Activity className="h-4 w-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">{overview.overall_resilience_score}%</div>
          <div className="text-xs text-emerald-400 mt-1 font-medium">Grade: {overview.scorecard_grade} (Empirically Measured)</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Empirical RTO</span>
            <Clock className="h-4 w-4 text-blue-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">14.5 min</div>
          <div className="text-xs text-blue-400 mt-1 font-medium">Target: ≤ 30.0 min (Verified in Drill)</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Empirical RPO</span>
            <Database className="h-4 w-4 text-purple-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">4.2 min</div>
          <div className="text-xs text-purple-400 mt-1 font-medium">Target: ≤ 15.0 min (WAL Tested)</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Single Points of Failure</span>
            <AlertTriangle className="h-4 w-4 text-amber-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">{overview.single_points_of_failure_count}</div>
          <div className="text-xs text-amber-400 mt-1 font-medium">Shared Database & Cache Cluster</div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 gap-6">
        {(['overview', 'services', 'plans', 'drills', 'gaps', 'backups', 'drift'] as const).map(tab => (
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

      {/* Simulation Result Drawer (if simulated) */}
      {simulationResult && (
        <div className="bg-indigo-950/40 border border-indigo-500/50 p-6 rounded-xl space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-indigo-400 font-bold text-lg">
              <Cpu className="h-5 w-5" />
              <span>Digital Twin Disruption Simulation (LABEL: SIMULATED)</span>
            </div>
            <button 
              onClick={() => setSimulationResult(null)}
              className="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-1 rounded"
            >
              Dismiss
            </button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <span className="text-slate-400">Target: </span>
              <span className="text-white font-mono">{simulationResult.initial_target}</span>
            </div>
            <div>
              <span className="text-slate-400">Attack Type: </span>
              <span className="text-white">{simulationResult.attack_type}</span>
            </div>
            <div>
              <span className="text-slate-400">Estimated Simulated RTO: </span>
              <span className="text-emerald-400 font-semibold">{simulationResult.estimated_simulated_rto_minutes} min</span>
            </div>
          </div>
          <div className="space-y-2">
            <span className="text-xs uppercase tracking-wider text-slate-400 font-semibold">Cascading Disruption:</span>
            <div className="space-y-1">
              {simulationResult.cascading_failures.map((f: any, idx: number) => (
                <div key={idx} className="flex items-center justify-between bg-slate-900/80 p-2.5 rounded border border-slate-800 text-xs">
                  <span className="font-mono text-amber-300">{f.component}</span>
                  <span className="text-slate-400">{f.reason}</span>
                  <span className="bg-rose-950/80 text-rose-300 px-2 py-0.5 rounded font-semibold">{f.status}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Tab Contents */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Critical Business Services */}
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Server className="h-5 w-5 text-emerald-400" />
              Critical Business Services
            </h2>
            <div className="space-y-3">
              <div className="bg-slate-950/70 border border-slate-800/80 p-4 rounded-lg flex items-center justify-between">
                <div>
                  <div className="font-semibold text-white">Enterprise Checkout & Payments</div>
                  <div className="text-xs text-slate-400 mt-0.5">Target RTO: 30 min | Target RPO: 15 min</div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-1 rounded">OPERATIONAL</span>
                  <span className="text-xs bg-rose-950 text-rose-300 border border-rose-800 px-2 py-1 rounded">CRITICAL</span>
                </div>
              </div>
            </div>
          </div>

          {/* DR Drills & Safety */}
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <CheckSquare className="h-5 w-5 text-blue-400" />
              Disaster Recovery Exercises
            </h2>
            <div className="space-y-3">
              <div className="bg-slate-950/70 border border-slate-800/80 p-4 rounded-lg space-y-2">
                <div className="flex items-center justify-between">
                  <div className="font-semibold text-white">PostgreSQL Sandbox Restore Drill</div>
                  <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded">COMPLETED</span>
                </div>
                <div className="text-xs text-slate-400 flex items-center justify-between">
                  <span>Scope: Isolated Sandbox</span>
                  <span>Measured RTO: 14.5 min | Measured RPO: 4.2 min</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'plans' && (
        <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <FileText className="h-5 w-5 text-purple-400" />
            Dependency-Aware Recovery Plans
          </h2>
          <div className="bg-slate-950/70 border border-slate-800/80 p-5 rounded-lg space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-bold text-white">Checkout & Payment Service Automated Disaster Recovery</h3>
                <p className="text-xs text-slate-400">Sequential multi-tier failover and restore</p>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs bg-purple-950 text-purple-300 border border-purple-800 px-2 py-1 rounded">FOUR-EYES APPROVED</span>
                <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-1 rounded">CURRENT</span>
              </div>
            </div>
            <div className="border-t border-slate-800/80 pt-3">
              <span className="text-xs text-slate-400 uppercase font-semibold">Recovery Sequence:</span>
              <div className="flex items-center gap-2 mt-2 text-xs">
                <span className="bg-slate-800 px-3 py-1 rounded font-mono">1. Network VPC</span>
                <ArrowRight className="h-3 w-3 text-slate-500" />
                <span className="bg-slate-800 px-3 py-1 rounded font-mono">2. PostgreSQL Standby</span>
                <ArrowRight className="h-3 w-3 text-slate-500" />
                <span className="bg-slate-800 px-3 py-1 rounded font-mono">3. Redis Replica</span>
                <ArrowRight className="h-3 w-3 text-slate-500" />
                <span className="bg-slate-800 px-3 py-1 rounded font-mono">4. API Gateway Pods</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'gaps' && (
        <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-amber-400" />
            Resilience Gaps
          </h2>
          <div className="bg-slate-950/70 border border-amber-900/50 p-4 rounded-lg space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-bold text-amber-300">Unverified Redis Failover</span>
              <span className="text-xs bg-amber-950 text-amber-300 border border-amber-800 px-2 py-0.5 rounded">HIGH SEVERITY</span>
            </div>
            <p className="text-xs text-slate-400">Redis Multi-AZ failover has not been tested in sandbox during the last 90 days.</p>
          </div>
        </div>
      )}

      {activeTab === 'backups' && (
        <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Database className="h-5 w-5 text-emerald-400" />
            Backup Integrity & Sandbox Restore Validation
          </h2>
          <div className="bg-slate-950/70 border border-slate-800/80 p-4 rounded-lg flex items-center justify-between">
            <div>
              <div className="font-semibold text-white">Primary PostgreSQL Cluster Snapshot</div>
              <div className="text-xs text-slate-400">Age: 2.5h | Checksum: SHA-256 Verified | Records: 152,400</div>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-1 rounded">INTEGRITY VERIFIED</span>
              <span className="text-xs bg-blue-950 text-blue-300 border border-blue-800 px-2 py-1 rounded">SANDBOX TESTED</span>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'drift' && (
        <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <GitPullRequest className="h-5 w-5 text-indigo-400" />
            Recovery Drift Detection
          </h2>
          <div className="bg-slate-950/70 border border-slate-800/80 p-4 rounded-lg space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-semibold text-white">Unregistered PostgreSQL Replica</span>
              <span className="text-xs bg-rose-950 text-rose-300 border border-rose-800 px-2 py-0.5 rounded">UNRECONCILED</span>
            </div>
            <p className="text-xs text-slate-400">Unregistered read-replica added in us-east-2 without updating failover DNS recovery plan.</p>
          </div>
        </div>
      )}
    </div>
  );
};
