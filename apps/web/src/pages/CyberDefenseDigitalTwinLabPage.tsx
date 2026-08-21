import React, { useState } from 'react';
import { 
  Boxes, Activity, GitBranch, Play, RefreshCw, 
  AlertTriangle, Shield, CheckCircle2, Sliders, Target, 
  Layers, Database, Cpu, Compass, Lock, Zap, FileText
} from 'lucide-react';

interface TwinOverview {
  digital_twin_states_count: number;
  twin_freshness_status: string;
  twin_confidence_score: number;
  active_drift_count: number;
  scenarios_count: number;
  simulation_accuracy_score: number;
  simulation_isolation_status: string;
  production_mutation_protection: string;
}

export const CyberDefenseDigitalTwinLabPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'scenarios' | 'attack_paths' | 'what_if' | 'business_impact' | 'calibration' | 'drift'>('overview');
  const [overview, setOverview] = useState<TwinOverview>({
    digital_twin_states_count: 1,
    twin_freshness_status: 'FRESH',
    twin_confidence_score: 0.98,
    active_drift_count: 1,
    scenarios_count: 1,
    simulation_accuracy_score: 0.96,
    simulation_isolation_status: 'ENFORCED',
    production_mutation_protection: 'ACTIVE',
  });

  const [simulating, setSimulating] = useState(false);
  const [simulationOutput, setSimulationOutput] = useState<any>(null);

  const triggerAttackPathSimulation = async () => {
    setSimulating(true);
    try {
      await new Promise(r => setTimeout(r, 600));
      setSimulationOutput({
        scenario_name: "Phishing Credential Stuffing & Lateral Movement Drill",
        stages: [
          { stage: "INITIAL_ACCESS", node: "ast_api_gw", technique: "T1078 Valid Accounts" },
          { stage: "EXECUTION", node: "ast_auth_cluster", technique: "T1055 Process Injection" },
          { stage: "LATERAL_MOVEMENT", node: "ast_postgres_primary", technique: "T1021 Remote Services" },
        ],
        containment: "INTERCEPTED",
        containment_control: "ctl_tenant_isolation",
        claim_status: "SIMULATED",
        containment_time_seconds: 42.0
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
            <Boxes className="h-8 w-8 text-cyan-400" />
            <h1 className="text-3xl font-bold tracking-tight text-white">
              Cyber Defense Digital Twin Lab
            </h1>
          </div>
          <p className="text-slate-400 mt-1">
            Autonomous Simulation Studio, Attack-Scenario Modeling, Defense What-If Lab & Empirical Calibration
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="bg-slate-900 border border-slate-800 px-4 py-2 rounded-lg text-sm">
            <span className="text-slate-400">Freshness: </span>
            <span className="font-semibold text-emerald-400">{overview.twin_freshness_status} (98% Conf)</span>
          </div>
          <button
            onClick={triggerAttackPathSimulation}
            disabled={simulating}
            className="flex items-center gap-2 bg-cyan-600 hover:bg-cyan-500 text-white px-4 py-2 rounded-lg font-medium transition"
          >
            {simulating ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4" />}
            Simulate Attack Scenario
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Twin Topology</span>
            <Activity className="h-4 w-4 text-cyan-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">150 Nodes</div>
          <div className="text-xs text-cyan-400 mt-1 font-medium">Production Mirror Synchronized</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Model Accuracy</span>
            <CheckCircle2 className="h-4 w-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">96.0%</div>
          <div className="text-xs text-emerald-400 mt-1 font-medium">Calibrated against Real Incident Replays</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Simulation Isolation</span>
            <Lock className="h-4 w-4 text-blue-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">ENFORCED</div>
          <div className="text-xs text-blue-400 mt-1 font-medium">0 Production Mutation Risk</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Twin Drift Signals</span>
            <AlertTriangle className="h-4 w-4 text-amber-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">{overview.active_drift_count}</div>
          <div className="text-xs text-amber-400 mt-1 font-medium">1 Configuration Drift Detected</div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 gap-6">
        {(['overview', 'scenarios', 'attack_paths', 'what_if', 'business_impact', 'calibration', 'drift'] as const).map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`pb-3 text-sm font-semibold capitalize transition ${
              activeTab === tab 
                ? 'border-b-2 border-cyan-400 text-cyan-400' 
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            {tab.replace('_', ' ')}
          </button>
        ))}
      </div>

      {/* Simulation Result Output */}
      {simulationOutput && (
        <div className="bg-cyan-950/40 border border-cyan-500/50 p-6 rounded-xl space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-cyan-400 font-bold text-lg flex items-center gap-2">
              <Compass className="h-5 w-5" />
              Attack Trajectory Simulation Outcome
            </span>
            <span className="text-xs bg-cyan-950 text-cyan-300 border border-cyan-800 px-2 py-0.5 rounded font-mono">
              [SIMULATED]
            </span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <span className="text-slate-400">Containment Status: </span>
              <span className="text-emerald-400 font-semibold">{simulationOutput.containment}</span>
            </div>
            <div>
              <span className="text-slate-400">Interception Point: </span>
              <span className="text-white font-mono">{simulationOutput.containment_control}</span>
            </div>
            <div>
              <span className="text-slate-400">Modeled Time: </span>
              <span className="text-white font-semibold">{simulationOutput.containment_time_seconds}s</span>
            </div>
          </div>
        </div>
      )}

      {/* Tab Contents */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Active Scenarios */}
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Target className="h-5 w-5 text-cyan-400" />
              Validated Simulation Scenarios
            </h2>
            <div className="bg-slate-950/70 border border-slate-800/80 p-4 rounded-lg space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-white">Phishing Credential Stuffing & Lateral Movement Drill</span>
                <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded">READY</span>
              </div>
              <p className="text-xs text-slate-400">Model blast radius and detection efficacy during compromised credential propagation.</p>
              <div className="text-xs text-slate-400 pt-1 flex items-center justify-between">
                <span>Category: ATTACK</span>
                <span className="text-cyan-400 font-mono">State: v1.0.0-PROD-SYNC</span>
              </div>
            </div>
          </div>

          {/* Defense What-If Matrix */}
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Sliders className="h-5 w-5 text-purple-400" />
              Pareto Defense Strategy Comparison
            </h2>
            <div className="bg-slate-950/70 border border-slate-800/80 p-5 rounded-lg space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-white">Recommended: STRATEGY_A_AUTOMATED_ISOLATION</span>
                <span className="text-xs bg-purple-950 text-purple-300 border border-purple-800 px-2 py-0.5 rounded font-mono">[MODELED]</span>
              </div>
              <div className="text-xs text-slate-400 space-y-1">
                <div>Security Benefit: <span className="text-emerald-400 font-semibold">95.0% Risk Reduction</span></div>
                <div>Availability Impact: <span className="text-emerald-400 font-semibold">5.0% Minimal Disruption</span></div>
                <div>Reversibility: <span className="text-cyan-400 font-semibold">FULLY_REVERSIBLE</span></div>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'drift' && (
        <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-amber-400" />
            Digital Twin Drift Signals
          </h2>
          <div className="bg-slate-950/70 border border-amber-900/50 p-4 rounded-lg space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-bold text-amber-300">API Gateway Rate Limit Drift</span>
              <span className="text-xs bg-amber-950 text-amber-300 border border-amber-800 px-2 py-0.5 rounded">CONFIGURATION DRIFT</span>
            </div>
            <p className="text-xs text-slate-400">Live API gateway rate-limit threshold differs from Digital Twin model.</p>
          </div>
        </div>
      )}

      {activeTab === 'calibration' && (
        <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <CheckCircle2 className="h-5 w-5 text-emerald-400" />
            Empirical Model Calibration Records
          </h2>
          <div className="bg-slate-950/70 border border-slate-800/80 p-5 rounded-lg space-y-3 text-sm">
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Scenario:</span>
              <span className="text-white font-semibold">Phishing Credential Stuffing Drill</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Predicted Containment:</span>
              <span className="text-cyan-400 font-mono">45.0 seconds</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Actual Containment:</span>
              <span className="text-emerald-400 font-mono">42.0 seconds</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Error & Calibration:</span>
              <span className="text-emerald-400 font-semibold">CORRECT (Calibration Score: 0.96)</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
