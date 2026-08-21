import React, { useState } from 'react';
import {
  ShieldAlert,
  ShieldCheck,
  Zap,
  Activity,
  Lock,
  Cpu,
  Layers,
  AlertOctagon,
  RefreshCw,
  Play,
  RotateCcw,
  CheckCircle2,
  XCircle,
  Clock,
  Eye,
  Sliders,
  TrendingDown,
  Power,
} from 'lucide-react';

export const AdaptiveDefenseCenterPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'closed-loop' | 'surface' | 'automation' | 'detection' | 'graph' | 'effectiveness'>('closed-loop');
  const [killSwitchActive, setKillSwitchActive] = useState(false);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 space-y-8 font-sans">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-indigo-500/10 border border-indigo-500/30 rounded-xl text-indigo-400">
            <Zap className="w-7 h-7" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-3">
              Adaptive Cyber Defense Center
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-semibold uppercase">
                POSTURE: NORMAL
              </span>
            </h1>
            <p className="text-sm text-slate-400">
              Closed-Loop Autonomous Defense • Real-Time Exposure Control • Adaptive Security Mesh
            </p>
          </div>
        </div>

        {/* Emergency Kill Switch */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => setKillSwitchActive(!killSwitchActive)}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-bold transition-all shadow-lg ${
              killSwitchActive
                ? 'bg-red-600 text-white animate-pulse shadow-red-600/50'
                : 'bg-red-500/10 border border-red-500/30 text-red-400 hover:bg-red-500/20'
            }`}
          >
            <Power className="w-4 h-4" />
            {killSwitchActive ? 'KILL SWITCH ACTIVE (HALTED)' : 'EMERGENCY KILL SWITCH'}
          </button>
        </div>
      </div>

      {/* Real-Time KPI Matrix */}
      <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Attack Surface Score</div>
          <div className="text-3xl font-bold text-cyan-400 mt-2">24.5</div>
          <div className="text-xs text-slate-400 mt-1">Low Exposure (0-100)</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Control Health</div>
          <div className="text-3xl font-bold text-emerald-400 mt-2">95.0%</div>
          <div className="text-xs text-emerald-400 mt-1">Controls enforcing</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Pending Approvals</div>
          <div className="text-3xl font-bold text-amber-400 mt-2">1</div>
          <div className="text-xs text-amber-300/80 mt-1">Four-Eyes required</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Active Adaptations</div>
          <div className="text-3xl font-bold text-indigo-400 mt-2">8</div>
          <div className="text-xs text-indigo-300/80 mt-1">Time-bounded controls</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Circuit Breaker</div>
          <div className="text-xl font-bold text-emerald-400 mt-2">CLOSED</div>
          <div className="text-xs text-slate-400 mt-1">0 consecutive faults</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Residual Risk</div>
          <div className="text-3xl font-bold text-emerald-400 mt-2">11.5%</div>
          <div className="text-xs text-emerald-300/80 mt-1">Risk mitigated by 88.5%</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 space-x-8 overflow-x-auto">
        {[
          { id: 'closed-loop', label: 'Closed-Loop Adaptations' },
          { id: 'surface', label: 'Attack Surface & Drift' },
          { id: 'automation', label: 'Automation & Circuit Breaker' },
          { id: 'detection', label: 'Adaptive Detection & Rollback' },
          { id: 'graph', label: 'Adaptive Defense Graph' },
          { id: 'effectiveness', label: 'Effectiveness Analytics' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`pb-4 text-sm font-medium transition-colors border-b-2 whitespace-nowrap ${
              activeTab === tab.id
                ? 'border-indigo-500 text-indigo-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab: Closed-Loop Adaptations */}
      {activeTab === 'closed-loop' && (
        <div className="space-y-4">
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Activity className="w-5 h-5 text-indigo-400" />
              Active Recommendations & Closed-Loop Actions
            </h3>

            <div className="space-y-3">
              {[
                {
                  id: 'rec_48a1',
                  title: 'Enforce Step-Up MFA on Suspicious Service Account Session',
                  target: 'svc_account_runner',
                  type: 'ACCESS_CHANGE',
                  level: 'LEVEL_3_PREAUTHORIZED',
                  status: 'READY_TO_EXECUTE',
                  simulatedReduction: '75%',
                },
                {
                  id: 'rec_99c2',
                  title: 'Isolate Host ep-finance-workstation-04 Following Malicious APK Beaconing',
                  target: 'ep-finance-workstation-04',
                  type: 'ASSET_ISOLATION',
                  level: 'LEVEL_2_HUMAN_APPROVAL',
                  status: 'APPROVAL_REQUIRED',
                  simulatedReduction: '92%',
                },
              ].map((rec) => (
                <div key={rec.id} className="p-4 bg-slate-950 rounded-xl border border-slate-800 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-white text-sm">{rec.title}</span>
                      <span className="text-xs px-2 py-0.5 bg-slate-800 text-slate-300 rounded font-mono">
                        {rec.target}
                      </span>
                    </div>
                    <div className="text-xs text-slate-400">
                      Type: <span className="text-slate-300 font-semibold">{rec.type}</span> • Level: <span className="text-indigo-400 font-semibold">{rec.level}</span> • Expected Risk Reduction: <span className="text-emerald-400 font-semibold">{rec.simulatedReduction}</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <button className="px-3 py-1.5 bg-slate-900 border border-slate-700 text-slate-300 rounded-lg text-xs hover:border-slate-600 transition-colors">
                      View Digital Twin Simulation
                    </button>
                    {rec.status === 'APPROVAL_REQUIRED' ? (
                      <button className="px-4 py-1.5 bg-amber-600 hover:bg-amber-500 text-white rounded-lg text-xs font-semibold transition-colors">
                        Four-Eyes Approve & Execute
                      </button>
                    ) : (
                      <button className="px-4 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold transition-colors">
                        Execute Preauthorized
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Tab: Attack Surface & Drift */}
      {activeTab === 'surface' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Sliders className="w-5 h-5 text-cyan-400" />
              Attack Surface Dimensions
            </h3>
            <div className="space-y-3 text-xs">
              {[
                { label: 'Exposed Internet Assets', val: 20 },
                { label: 'Public Services & APIs', val: 15 },
                { label: 'Unpatched Vulnerabilities', val: 25 },
                { label: 'Identity & Privilege Risks', val: 10 },
                { label: 'Third-Party Dependency Exposure', val: 12 },
                { label: 'Cloud Resource Exposure', val: 18 },
              ].map((dim) => (
                <div key={dim.label} className="space-y-1">
                  <div className="flex justify-between text-slate-300">
                    <span>{dim.label}</span>
                    <span className="font-bold text-cyan-400">{dim.val}%</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-1.5">
                    <div className="bg-cyan-500 h-1.5 rounded-full" style={{ width: `${dim.val}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <AlertOctagon className="w-5 h-5 text-amber-400" />
              Observed Security Drift Events
            </h3>
            <div className="space-y-2 text-xs">
              <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                <div className="flex justify-between text-slate-200 font-semibold">
                  <span>CONFIGURATION_DRIFT: WAF Ingress Port 8443</span>
                  <span className="text-amber-400">MEDIUM</span>
                </div>
                <div className="text-slate-400 mt-1">
                  Previous: Closed • Current: Open to public CIDR • Exploitability: 0.50
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab: Automation & Circuit Breaker */}
      {activeTab === 'automation' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Cpu className="w-5 h-5 text-emerald-400" />
              Defense Circuit Breaker Health
            </h3>
            <div className="p-4 bg-slate-950 rounded-xl border border-slate-800 text-xs space-y-3">
              <div className="flex justify-between">
                <span className="text-slate-400">Circuit State:</span>
                <span className="font-bold text-emerald-400">CLOSED (HEALTHY)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Consecutive Failures:</span>
                <span className="text-slate-200 font-mono">0 / 3 (Threshold)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Runaway Loop Protection:</span>
                <span className="text-emerald-400">ACTIVE (Deduplication Enforced)</span>
              </div>
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Lock className="w-5 h-5 text-indigo-400" />
              Protected Target Safeguards
            </h3>
            <div className="text-xs text-slate-400">
              The following critical resources are blacklisted from automated high-impact destruction:
            </div>
            <div className="flex flex-wrap gap-2 text-xs font-mono">
              {['localhost', '127.0.0.1', 'production-db-primary', 'trustshield.internal', 'aws-root-account'].map((t) => (
                <span key={t} className="px-2 py-1 bg-red-500/10 border border-red-500/20 text-red-300 rounded">
                  {t}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Tab: Detection & Rollback */}
      {activeTab === 'detection' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <RotateCcw className="w-5 h-5 text-cyan-400" />
            Adaptive Detection Rule Management & Instant Rollback
          </h3>
          <div className="divide-y divide-slate-800 text-xs">
            {[
              { id: 'rule_9912', name: 'Malicious Voice Clone Traffic Anomaly', ver: 3, prev: 2, status: 'ACTIVE' },
              { id: 'rule_4421', name: 'Quishing QR Code HTTP Redirection Surge', ver: 2, prev: 1, status: 'ACTIVE' },
            ].map((r) => (
              <div key={r.id} className="py-3 flex justify-between items-center">
                <div>
                  <div className="font-bold text-white text-sm">{r.name}</div>
                  <div className="text-slate-400 font-mono mt-0.5">
                    ID: {r.id} • Version: v{r.ver} (Previous: v{r.prev})
                  </div>
                </div>
                <button className="flex items-center gap-1 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs transition-colors">
                  <RotateCcw className="w-3.5 h-3.5" /> Rollback to v{r.prev}
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab: Defense Graph */}
      {activeTab === 'graph' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Layers className="w-5 h-5 text-indigo-400" />
            Adaptive Defense Knowledge Graph
          </h3>
          <div className="h-96 bg-slate-950 border border-slate-800 rounded-xl flex items-center justify-center text-center space-y-3">
            <div>
              <Layers className="w-12 h-12 text-indigo-500/40 mx-auto animate-pulse" />
              <div className="text-sm text-slate-400 mt-2">
                Defense Topology: Threat Nodes ↔ Protected Assets ↔ Mitigating Controls
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab: Effectiveness */}
      {activeTab === 'effectiveness' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <TrendingDown className="w-5 h-5 text-emerald-400" />
            Empirical Post-Adaptation Effectiveness
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <span className="text-slate-400">Threat Reduction:</span>
              <div className="text-2xl font-bold text-emerald-400 mt-1">85.0%</div>
            </div>
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <span className="text-slate-400">Exposure Mitigation:</span>
              <div className="text-2xl font-bold text-cyan-400 mt-1">70.0%</div>
            </div>
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <span className="text-slate-400">Control Improvement:</span>
              <div className="text-2xl font-bold text-indigo-400 mt-1">90.0%</div>
            </div>
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <span className="text-slate-400">Service Stability:</span>
              <div className="text-2xl font-bold text-emerald-400 mt-1">98.0%</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdaptiveDefenseCenterPage;
