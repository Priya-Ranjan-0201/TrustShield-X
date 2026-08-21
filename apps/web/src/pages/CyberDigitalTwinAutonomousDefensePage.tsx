import React, { useState } from 'react';
import {
  Cpu, Layers, ShieldCheck, ShieldAlert, Zap,
  Activity, Play, CheckCircle2, XCircle, AlertTriangle,
  RotateCcw, Sliders, Server, Database, Network,
  Crosshair, Search, Eye, Lock, FileText, ArrowRight,
  Compass, BarChart3, RefreshCw, Radio, Check, KeyRound,
  Shield, Terminal, Users, UserCheck, Sparkles, AlertOctagon
} from 'lucide-react';

export const CyberDigitalTwinAutonomousDefensePage: React.FC = () => {
  type NavTab =
    | 'digital_twin'
    | 'environment_map'
    | 'attack_simulation'
    | 'defense_simulation'
    | 'what_if'
    | 'attack_paths'
    | 'control_gaps'
    | 'purple_team'
    | 'defense_optimization'
    | 'autonomous_defense'
    | 'action_approvals'
    | 'action_history'
    | 'verification'
    | 'simulation_history';

  const [activeTab, setActiveTab] = useState<NavTab>('digital_twin');
  const [runningSim, setRunningSim] = useState(false);
  const [whatIfTarget, setWhatIfTarget] = useState('API-GATEWAY-PROD');
  const [whatIfAction, setWhatIfAction] = useState('PATCH_VULNERABILITY');
  const [whatIfResult, setWhatIfResult] = useState<{
    riskBefore: number;
    riskAfter: number;
    pathsRemoved: number;
    impact: string;
    decision: string;
  } | null>({
    riskBefore: 8.5,
    riskAfter: 4.0,
    pathsRemoved: 3,
    impact: 'LOW (Zero downtime rolling patch)',
    decision: 'RECOMMENDED_DEFENSE'
  });

  const handleRunWhatIf = async () => {
    setRunningSim(true);
    try {
      await new Promise(r => setTimeout(r, 400));
      if (whatIfAction === 'PATCH_VULNERABILITY') {
        setWhatIfResult({
          riskBefore: 8.5,
          riskAfter: 4.0,
          pathsRemoved: 3,
          impact: 'LOW (Zero downtime rolling patch)',
          decision: 'RECOMMENDED_DEFENSE'
        });
      } else if (whatIfAction === 'ISOLATE_DEVICE') {
        setWhatIfResult({
          riskBefore: 8.5,
          riskAfter: 2.5,
          pathsRemoved: 4,
          impact: 'MEDIUM (Endpoint offline for triage)',
          decision: 'HIGH_CONTAINMENT_VERIFIED'
        });
      } else if (whatIfAction === 'SIMULATE_CONTROL_FAILURE') {
        setWhatIfResult({
          riskBefore: 8.5,
          riskAfter: 9.8,
          pathsRemoved: 0,
          impact: 'HIGH (Critical control failure, blast radius +3.5x)',
          decision: 'DISASTER_PREPAREDNESS_ALERT'
        });
      } else {
        setWhatIfResult({
          riskBefore: 8.5,
          riskAfter: 3.0,
          pathsRemoved: 4,
          impact: 'LOW (Zero-trust microsegmentation enforced)',
          decision: 'OPTIMAL_MINIMAL_ACTION'
        });
      }
    } finally {
      setRunningSim(false);
    }
  };

  const navItems: { id: NavTab; label: string; icon: React.ReactNode; badge?: string }[] = [
    { id: 'digital_twin', label: 'DIGITAL TWIN', icon: <Cpu className="h-4 w-4" /> },
    { id: 'environment_map', label: 'ENVIRONMENT MAP', icon: <Network className="h-4 w-4" /> },
    { id: 'attack_simulation', label: 'ATTACK SIMULATION', icon: <Crosshair className="h-4 w-4" /> },
    { id: 'defense_simulation', label: 'DEFENSE SIMULATION', icon: <Shield className="h-4 w-4" /> },
    { id: 'what_if', label: 'WHAT-IF', icon: <Sliders className="h-4 w-4" /> },
    { id: 'attack_paths', label: 'ATTACK PATHS', icon: <Compass className="h-4 w-4" />, badge: '5' },
    { id: 'control_gaps', label: 'CONTROL GAPS', icon: <AlertTriangle className="h-4 w-4" />, badge: '2' },
    { id: 'purple_team', label: 'PURPLE TEAM', icon: <Activity className="h-4 w-4" /> },
    { id: 'defense_optimization', label: 'DEFENSE OPTIMIZATION', icon: <Sparkles className="h-4 w-4" /> },
    { id: 'autonomous_defense', label: 'AUTONOMOUS DEFENSE', icon: <Zap className="h-4 w-4" /> },
    { id: 'action_approvals', label: 'ACTION APPROVALS', icon: <Users className="h-4 w-4" />, badge: '1' },
    { id: 'action_history', label: 'ACTION HISTORY', icon: <FileText className="h-4 w-4" /> },
    { id: 'verification', label: 'VERIFICATION', icon: <CheckCircle2 className="h-4 w-4" /> },
    { id: 'simulation_history', label: 'SIMULATION HISTORY', icon: <RotateCcw className="h-4 w-4" /> }
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 lg:p-8 space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 border border-indigo-500/30 rounded-xl">
            <Cpu className="h-8 w-8 text-indigo-400" />
          </div>
          <div>
            <h1 className="text-2xl lg:text-3xl font-extrabold tracking-tight text-white flex items-center gap-3">
              Cyber Digital Twin & Autonomous Defense Center
              <span className="text-xs bg-indigo-950 text-indigo-300 border border-indigo-700/50 px-2.5 py-0.5 rounded-full font-mono">
                PHASE 35 ACTIVE
              </span>
            </h1>
            <p className="text-sm text-slate-400 mt-0.5">
              High-Fidelity Virtual Replicas, Adversary Emulation, What-If Simulation, Pareto Strategy Optimization & Governed Closed-Loop Response
            </p>
          </div>
        </div>

        {/* Status Badge */}
        <div className="flex items-center gap-4 bg-slate-900/80 border border-slate-800 rounded-xl px-4 py-2.5 shadow-lg shadow-black/40">
          <div className="text-right">
            <div className="text-[11px] text-slate-400 font-medium">Autonomy Governance Level</div>
            <div className="text-sm font-bold text-indigo-400 flex items-center gap-1.5 justify-end">
              <Zap className="h-4 w-4" /> LEVEL 2 (HUMAN-GOVERNED)
            </div>
          </div>
          <div className="h-8 w-[1px] bg-slate-800" />
          <span className="text-xs bg-indigo-950 text-indigo-300 border border-indigo-800 px-2.5 py-1 rounded font-mono font-bold">
            ZERO MUTATION ON PROD
          </span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-5">
        <div className="bg-slate-900/70 border border-slate-800 p-5 rounded-xl backdrop-blur-sm">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Digital Twin Fidelity</span>
            <Layers className="h-4 w-4 text-cyan-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">94.8% <span className="text-xs text-slate-400 font-normal">Score</span></div>
          <div className="text-xs text-cyan-400 mt-2 flex items-center gap-1 font-medium">
            <CheckCircle2 className="h-3.5 w-3.5" /> 6 Dimensions Synchronized
          </div>
        </div>

        <div className="bg-slate-900/70 border border-slate-800 p-5 rounded-xl backdrop-blur-sm">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Active Simulations</span>
            <Play className="h-4 w-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">12 <span className="text-xs text-slate-400 font-normal">Runs</span></div>
          <div className="text-xs text-emerald-400 mt-2 flex items-center gap-1 font-medium">
            <Radio className="h-3.5 w-3.5" /> 100% Non-Destructive Isolation
          </div>
        </div>

        <div className="bg-slate-900/70 border border-slate-800 p-5 rounded-xl backdrop-blur-sm">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Predicted Attack Paths</span>
            <Compass className="h-4 w-4 text-amber-400" />
          </div>
          <div className="text-3xl font-extrabold text-amber-400">5 <span className="text-xs text-slate-400 font-normal">Ranked</span></div>
          <div className="text-xs text-amber-300/80 mt-2 flex items-center gap-1 font-medium">
            0 Infiltration to Crown Jewels
          </div>
        </div>

        <div className="bg-slate-900/70 border border-slate-800 p-5 rounded-xl backdrop-blur-sm">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Four-Eyes Approvals</span>
            <Users className="h-4 w-4 text-indigo-400" />
          </div>
          <div className="text-3xl font-extrabold text-indigo-400">1 <span className="text-xs text-slate-400 font-normal">Pending</span></div>
          <div className="text-xs text-slate-400 mt-2 flex items-center gap-1 font-medium">
            100% Dual Auth Enforced
          </div>
        </div>
      </div>

      {/* Navigation Tabs (14 views) */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-2 border-b border-slate-800 scrollbar-thin scrollbar-thumb-slate-800">
        {navItems.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-3.5 py-2 font-medium text-xs rounded-lg transition-all flex items-center gap-2 whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/50 shadow-sm'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/80 border border-transparent'
            }`}
          >
            {tab.icon}
            {tab.label}
            {tab.badge && (
              <span className="text-[10px] bg-slate-800 text-slate-300 px-1.5 py-0.2 rounded-full font-mono">
                {tab.badge}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Tab 1: DIGITAL TWIN */}
      {activeTab === 'digital_twin' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-base font-bold text-white flex items-center gap-2">
                  <Cpu className="h-5 w-5 text-indigo-400" /> Active Digital Twin Environments
                </h2>
                <button className="text-xs bg-indigo-950 hover:bg-indigo-900 text-indigo-300 border border-indigo-800 px-3 py-1.5 rounded font-medium transition-colors">
                  + Create Simulation Replica
                </button>
              </div>
              <div className="space-y-3">
                {[
                  { id: 'TWIN-ENV-PROD-01', type: 'PRODUCTION_REPLICA', assets: 384, ver: '1.0.0', fid: '94.8%', status: 'SYNCHRONIZED', hash: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855' },
                  { id: 'TWIN-ENV-WHATIF-02', type: 'WHAT_IF', assets: 384, ver: '1.0.1', fid: '95.2%', status: 'SIMULATING', hash: '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8' },
                  { id: 'TWIN-ENV-CHAOS-03', type: 'TEST', assets: 120, ver: '0.9.0', fid: '91.0%', status: 'ISOLATED', hash: '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a' }
                ].map((env, idx) => (
                  <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3">
                    <div>
                      <div className="font-semibold text-slate-100 text-sm flex items-center gap-2">
                        <span className="font-mono text-cyan-400">{env.id}</span>
                        <span className="text-xs bg-slate-800 text-slate-300 px-2 py-0.5 rounded font-sans">{env.type}</span>
                      </div>
                      <div className="text-xs text-slate-400 font-mono mt-1">
                        Assets: {env.assets} &bull; Fidelity: <span className="text-emerald-400 font-bold">{env.fid}</span> &bull; State Hash: {env.hash.substring(0, 16)}...
                      </div>
                    </div>
                    <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 px-2.5 py-1 rounded font-mono font-bold self-start md:self-auto">
                      {env.status}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Fidelity Dimensions */}
            <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <BarChart3 className="h-5 w-5 text-cyan-400" /> Digital Twin Fidelity Dimensions (No False Certainty)
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {[
                  { name: 'Asset Fidelity', score: '98%', status: 'VERIFIED' },
                  { name: 'Network Fidelity', score: '95%', status: 'VERIFIED' },
                  { name: 'Identity Fidelity', score: '96%', status: 'VERIFIED' },
                  { name: 'Vulnerability Fidelity', score: '94%', status: 'GROUNDED' },
                  { name: 'Control Fidelity', score: '92%', status: 'GROUNDED' },
                  { name: 'Dependency Fidelity', score: '90%', status: 'GROUNDED' }
                ].map((dim, idx) => (
                  <div key={idx} className="bg-slate-950 border border-slate-800 p-3.5 rounded-lg">
                    <div className="text-[11px] text-slate-400 font-medium">{dim.name}</div>
                    <div className="text-xl font-extrabold text-cyan-300 mt-1">{dim.score}</div>
                    <div className="text-[10px] text-slate-500 font-mono mt-0.5">{dim.status}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <RotateCcw className="h-5 w-5 text-indigo-400" /> Snapshot Checkpoints &amp; Diff
              </h2>
              <p className="text-xs text-slate-400 leading-relaxed">
                Immutable, hash-chained environment snapshots enable point-in-time state comparisons and disaster replays.
              </p>
              <div className="space-y-3 pt-2">
                {[
                  { id: 'SNAP-20260821-01', src: 'AUTO_SCHEDULE', assets: 384, time: '10 mins ago' },
                  { id: 'SNAP-20260820-23', src: 'PRE_PATCH_CHECKPOINT', assets: 382, time: '1 hour ago' }
                ].map((s, idx) => (
                  <div key={idx} className="bg-slate-950 border border-slate-800 p-3 rounded-lg flex items-center justify-between text-xs font-mono">
                    <div>
                      <div className="text-indigo-300 font-bold">{s.id}</div>
                      <div className="text-slate-400 text-[11px]">{s.src} &bull; {s.time}</div>
                    </div>
                    <button className="bg-slate-800 hover:bg-slate-700 text-slate-200 px-2 py-1 rounded text-[11px]">
                      Compare Diff
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 5: WHAT-IF ENGINE */}
      {activeTab === 'what_if' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-6">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            <div>
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <Sliders className="h-5 w-5 text-indigo-400" /> What-If Security Simulation Engine
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Safely simulate proposed defensive changes or control failures before taking operational actions.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 bg-slate-950 border border-slate-800 p-4 rounded-xl">
            <div>
              <label className="text-xs text-slate-400 font-medium block mb-1.5">Target Component / Asset</label>
              <select
                value={whatIfTarget}
                onChange={(e) => setWhatIfTarget(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 text-slate-200 rounded-lg px-3 py-2 text-xs font-mono focus:outline-none focus:border-indigo-500"
              >
                <option value="API-GATEWAY-PROD">API-GATEWAY-PROD (External Ingress)</option>
                <option value="DEV-WORKSTATION-09">DEV-WORKSTATION-09 (Endpoint Host)</option>
                <option value="AUTH-SERVICE-OIDC">AUTH-SERVICE-OIDC (Identity Provider)</option>
                <option value="CORE-DB-VAULT">CORE-DB-VAULT (Protected Target)</option>
              </select>
            </div>

            <div>
              <label className="text-xs text-slate-400 font-medium block mb-1.5">Simulated What-If Action</label>
              <select
                value={whatIfAction}
                onChange={(e) => setWhatIfAction(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 text-slate-200 rounded-lg px-3 py-2 text-xs font-mono focus:outline-none focus:border-indigo-500"
              >
                <option value="PATCH_VULNERABILITY">What if we patch CVE-2024-3094?</option>
                <option value="ISOLATE_DEVICE">What if we isolate this device?</option>
                <option value="ADD_MICROSEGMENTATION">What if we enforce microsegmentation?</option>
                <option value="SIMULATE_CONTROL_FAILURE">What if MFA / Firewall control fails?</option>
              </select>
            </div>

            <div className="flex items-end">
              <button
                disabled={runningSim}
                onClick={handleRunWhatIf}
                className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-2 px-4 rounded-lg text-xs flex items-center justify-center gap-2 transition-colors disabled:opacity-50"
              >
                <Play className="h-4 w-4" /> {runningSim ? 'Simulating...' : 'Run What-If Simulation'}
              </button>
            </div>
          </div>

          {whatIfResult && (
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 pt-2">
              <div className="bg-slate-950 border border-slate-800 p-4 rounded-lg">
                <div className="text-[11px] text-slate-400 font-medium">Baseline Composite Risk</div>
                <div className="text-2xl font-bold text-rose-400 mt-1">{whatIfResult.riskBefore} / 10</div>
                <div className="text-[10px] text-slate-500 font-mono mt-0.5">CURRENT_STATE</div>
              </div>

              <div className="bg-slate-950 border border-slate-800 p-4 rounded-lg">
                <div className="text-[11px] text-slate-400 font-medium">Simulated Residual Risk</div>
                <div className={`text-2xl font-bold mt-1 ${whatIfResult.riskAfter < whatIfResult.riskBefore ? 'text-emerald-400' : 'text-rose-400'}`}>
                  {whatIfResult.riskAfter} / 10
                </div>
                <div className="text-[10px] text-slate-500 font-mono mt-0.5">SIMULATED_STATE</div>
              </div>

              <div className="bg-slate-950 border border-slate-800 p-4 rounded-lg">
                <div className="text-[11px] text-slate-400 font-medium">Attack Paths Disrupted</div>
                <div className="text-2xl font-bold text-cyan-400 mt-1">-{whatIfResult.pathsRemoved} Paths</div>
                <div className="text-[10px] text-slate-500 font-mono mt-0.5">PATH_DIFF</div>
              </div>

              <div className="bg-slate-950 border border-slate-800 p-4 rounded-lg">
                <div className="text-[11px] text-slate-400 font-medium">Projected Business Impact</div>
                <div className="text-xs font-semibold text-slate-200 mt-2 leading-tight">{whatIfResult.impact}</div>
                <div className="text-[10px] text-indigo-400 font-mono mt-1.5">{whatIfResult.decision}</div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Tab 9: DEFENSE OPTIMIZATION */}
      {activeTab === 'defense_optimization' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-indigo-400" /> Multi-Objective Pareto Defense Optimization
            </h2>
            <span className="text-xs bg-indigo-950 text-indigo-300 border border-indigo-800 px-2.5 py-1 rounded font-mono">
              MINIMAL EFFECTIVE ACTION
            </span>
          </div>
          <div className="space-y-3">
            {[
              { rank: 1, name: 'Strategy A: Microsegment Rule + FIDO2 Step-up', drop: '-6.2 Risk', cost: 'LOW', impact: 'ZERO DOWNTIME', status: 'RECOMMENDED (Pareto Optimal)', color: 'border-emerald-700/60 bg-emerald-950/20 text-emerald-300' },
              { rank: 2, name: 'Strategy B: Full Host Quarantine & Re-image', drop: '-7.0 Risk', cost: 'HIGH', impact: 'SERVICE OFFLINE', status: 'OVERKILL (High Blast Radius)', color: 'border-slate-800 bg-slate-950 text-slate-400' },
              { rank: 3, name: 'Strategy C: Increase Log Verbosity Only', drop: '-1.8 Risk', cost: 'MINIMAL', impact: 'NONE', status: 'INSUFFICIENT (Leaves Exposure Open)', color: 'border-slate-800 bg-slate-950 text-slate-400' }
            ].map((strat, idx) => (
              <div key={idx} className={`border p-4 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3 ${strat.color}`}>
                <div>
                  <div className="text-sm font-semibold flex items-center gap-2">
                    <span className="font-mono text-xs">#{strat.rank}</span>
                    <span>{strat.name}</span>
                  </div>
                  <div className="text-xs mt-1 opacity-80 font-mono">
                    Risk Reduction: <span className="font-bold">{strat.drop}</span> &bull; Cost: {strat.cost} &bull; Impact: {strat.impact}
                  </div>
                </div>
                <span className="text-xs font-mono font-bold px-2.5 py-1 rounded border self-start md:self-auto">
                  {strat.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 10: AUTONOMOUS DEFENSE */}
      {activeTab === 'autonomous_defense' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <Zap className="h-5 w-5 text-indigo-400" /> Governed Autonomous Defense Control Plane
            </h2>
            <div className="text-xs text-slate-400 font-mono">
              Allowlist: <span className="text-emerald-400">ACTIVE</span> &bull; Protected Targets: <span className="text-rose-400">ENFORCED</span>
            </div>
          </div>
          <div className="space-y-3">
            {[
              { id: 'ACT-AUTO-101', target: 'WAF-INGRESS-01', action: 'BLOCK_SUSPICIOUS_IP_ON_WAF', cat: 'REVERSIBLE', auth: 'AUTONOMOUS_EXECUTION_PERMITTED', status: 'EXECUTED_AND_VERIFIED' },
              { id: 'ACT-AUTO-102', target: 'DB-MAIN-CORE-VAULT', action: 'REVOKE_ALL_DB_CONNECTIONS', cat: 'DESTRUCTIVE', auth: 'FOUR_EYES_DUAL_APPROVAL_REQUIRED', status: 'BLOCKED_PROTECTED_TARGET' },
              { id: 'ACT-AUTO-103', target: 'DEV-WORKSTATION-44', action: 'QUARANTINE_NON_CRITICAL_ENDPOINT', cat: 'REVERSIBLE', auth: 'HUMAN_APPROVAL_REQUIRED', status: 'PENDING_APPROVAL' }
            ].map((act, idx) => (
              <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div>
                  <div className="text-sm font-semibold text-slate-100 font-mono flex items-center gap-2">
                    <span className="text-cyan-400">{act.id}</span>
                    <span>&bull; {act.action}</span>
                  </div>
                  <div className="text-xs text-slate-400 font-mono mt-1">
                    Target: <span className="text-slate-200">{act.target}</span> &bull; Category: {act.cat} &bull; Policy: {act.auth}
                  </div>
                </div>
                <span className={`text-xs px-2.5 py-1 rounded font-mono font-bold self-start md:self-auto ${
                  act.status.includes('EXECUTED') ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' :
                  act.status.includes('BLOCKED') ? 'bg-rose-950 text-rose-300 border border-rose-800' :
                  'bg-amber-950 text-amber-300 border border-amber-800'
                }`}>
                  {act.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 11: ACTION APPROVALS */}
      {activeTab === 'action_approvals' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <Users className="h-5 w-5 text-indigo-400" /> Four-Eyes Dual Approval Request Queue
            </h2>
            <span className="text-xs text-amber-300 bg-amber-950/60 border border-amber-800 px-2.5 py-1 rounded font-mono">
              1 PENDING REVIEW
            </span>
          </div>
          <div className="bg-slate-950 border border-slate-800 p-5 rounded-lg space-y-3">
            <div className="flex items-center justify-between">
              <div className="text-sm font-semibold text-slate-200">
                Action ID: <span className="font-mono text-cyan-300">ACT-FOUR-EYES-09</span> &bull; <span className="text-amber-400">ISOLATE_APP_CLUSTER_NODE_03</span>
              </div>
              <span className="text-xs bg-amber-950 text-amber-300 border border-amber-800 px-2 py-0.5 rounded font-mono">
                1/2 APPROVALS SATISFIED
              </span>
            </div>
            <div className="text-xs text-slate-400 space-y-1 font-mono">
              <div>Target: <span className="text-slate-200">K8S-APP-NODE-03</span> (Production Worker)</div>
              <div>Reason: Lateral reconnaissance attempt flagged by EDR &amp; digital twin what-if simulation</div>
              <div>First Approver: <span className="text-indigo-300">analyst-tier2@truthshield.io</span> (10:52:19 UTC)</div>
              <div>Second Approver Required: <span className="text-amber-400 font-bold">Awaiting SecOps Commander Signature</span></div>
            </div>
            <div className="flex items-center gap-3 pt-2">
              <button className="text-xs bg-emerald-600 hover:bg-emerald-500 text-white px-3.5 py-1.5 rounded font-medium transition-colors flex items-center gap-1.5">
                <Check className="h-3.5 w-3.5" /> Sign &amp; Concur (Second Approval)
              </button>
              <button className="text-xs bg-rose-950 hover:bg-rose-900 text-rose-300 border border-rose-800 px-3.5 py-1.5 rounded font-medium transition-colors">
                Reject Action
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Tab 8: PURPLE TEAM */}
      {activeTab === 'purple_team' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <Activity className="h-5 w-5 text-cyan-400" /> Collaborative Purple-Team Exercises
            </h2>
            <button className="text-xs bg-cyan-950 hover:bg-cyan-900 text-cyan-300 border border-cyan-800 px-3 py-1.5 rounded font-medium transition-colors">
              + Launch Purple-Team Exercise
            </button>
          </div>
          <div className="space-y-3">
            {[
              { id: 'PURPLE-EX-01', name: 'Q3 Enterprise Ransomware Defense Validation', red: 'LockBit Emulation (T1190, T1486)', blue: 'EDR + Microsegmentation + SOAR', det: '94%', prev: '96%', status: 'COMPLETED' },
              { id: 'PURPLE-EX-02', name: 'Identity Hijacking & Lateral Pass-the-Hash', red: 'Mimikatz + Kerberoasting (T1558)', blue: 'FIDO2 MFA + Zero-Trust Engine', det: '98%', prev: '99%', status: 'COMPLETED' }
            ].map((p, idx) => (
              <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div>
                  <div className="font-semibold text-slate-100 text-sm flex items-center gap-2">
                    <span className="font-mono text-cyan-300">{p.id}</span>
                    <span>&bull; {p.name}</span>
                  </div>
                  <div className="text-xs text-slate-400 font-mono mt-1">
                    Red Team: <span className="text-rose-300">{p.red}</span> &bull; Blue Team: <span className="text-indigo-300">{p.blue}</span>
                  </div>
                  <div className="text-xs text-slate-500 font-mono mt-0.5">
                    Detection Rate: <span className="text-emerald-400 font-bold">{p.det}</span> &bull; Prevention Rate: <span className="text-emerald-400 font-bold">{p.prev}</span>
                  </div>
                </div>
                <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 px-2.5 py-1 rounded font-mono font-bold self-start md:self-auto">
                  {p.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default CyberDigitalTwinAutonomousDefensePage;
