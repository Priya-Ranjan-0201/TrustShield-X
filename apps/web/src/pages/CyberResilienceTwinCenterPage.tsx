import React, { useState } from 'react';
import {
  Layers,
  Activity,
  Cpu,
  ShieldCheck,
  AlertTriangle,
  GitBranch,
  Play,
  RotateCcw,
  Sliders,
  TrendingUp,
  Clock,
  Compass,
  CheckCircle2,
  XCircle,
  Eye,
  Target,
  Zap,
  BarChart3,
} from 'lucide-react';

export const CyberResilienceTwinCenterPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'completeness' | 'dependencies' | 'scenarios' | 'whatif' | 'recovery' | 'accuracy' | 'roadmap'>('completeness');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 space-y-8 font-sans">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-cyan-500/10 border border-cyan-500/30 rounded-xl text-cyan-400">
            <Layers className="w-7 h-7" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-3">
              Cyber Resilience Digital Twin 2.0
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 font-semibold uppercase">
                SYNCHRONIZED (v15)
              </span>
            </h1>
            <p className="text-sm text-slate-400">
              Predictive Cyber Resilience • Multi-Step Attack Propagation • Pareto Defense Optimization
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-semibold transition-all shadow-lg shadow-indigo-600/30">
            <Play className="w-4 h-4" /> Run Sandbox What-If
          </button>
        </div>
      </div>

      {/* KPI Scorecard Matrix */}
      <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Cyber Resilience Score</div>
          <div className="text-3xl font-bold text-emerald-400 mt-2">87.3%</div>
          <div className="text-xs text-emerald-400 mt-1">7-dimension score</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Twin Completeness</div>
          <div className="text-3xl font-bold text-cyan-400 mt-2">88.0%</div>
          <div className="text-xs text-slate-400 mt-1">8 visibility dimensions</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Twin Confidence</div>
          <div className="text-3xl font-bold text-indigo-400 mt-2">91.0%</div>
          <div className="text-xs text-indigo-300/80 mt-1">Empirical telemetry</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Telemetry Freshness</div>
          <div className="text-3xl font-bold text-emerald-400 mt-2">96.0%</div>
          <div className="text-xs text-slate-400 mt-1">&lt; 30s latency</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Active SPOFs</div>
          <div className="text-3xl font-bold text-amber-400 mt-2">1</div>
          <div className="text-xs text-amber-300/80 mt-1">Mitigation in roadmap</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Prediction Precision</div>
          <div className="text-3xl font-bold text-emerald-400 mt-2">92.0%</div>
          <div className="text-xs text-emerald-300/80 mt-1">Calibrated on 240 runs</div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 space-x-8 overflow-x-auto">
        {[
          { id: 'completeness', label: 'Twin State & Completeness' },
          { id: 'dependencies', label: 'Dependency Graph & SPOF' },
          { id: 'scenarios', label: 'Attack Propagation & Scenarios' },
          { id: 'whatif', label: 'What-If & Pareto Optimizer' },
          { id: 'recovery', label: 'Disaster Recovery & RTO/RPO' },
          { id: 'accuracy', label: 'Simulation vs Reality & Calibration' },
          { id: 'roadmap', label: 'Resilience Roadmap' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`pb-4 text-sm font-medium transition-colors border-b-2 whitespace-nowrap ${
              activeTab === tab.id
                ? 'border-cyan-500 text-cyan-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab: Twin State & Completeness */}
      {activeTab === 'completeness' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Eye className="w-5 h-5 text-cyan-400" />
              8-Dimension Completeness Scorecard
            </h3>
            <div className="space-y-3 text-xs">
              {[
                { label: 'Asset Visibility', val: 95 },
                { label: 'Identity Visibility', val: 90 },
                { label: 'Service Visibility', val: 92 },
                { label: 'Dependency Visibility', val: 84 },
                { label: 'Control Visibility', val: 96 },
                { label: 'Threat Visibility', val: 88 },
                { label: 'Business Service Mapping', val: 78 },
                { label: 'Recovery Mapping', val: 82 },
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
              <ShieldCheck className="w-5 h-5 text-emerald-400" />
              7-Dimension Cyber Resilience Scorecard
            </h3>
            <div className="space-y-3 text-xs">
              {[
                { label: 'Prevention Strength', val: 88 },
                { label: 'Detection Fidelity', val: 92 },
                { label: 'Containment Speed', val: 85 },
                { label: 'Recovery Capability', val: 80 },
                { label: 'Adaptive Agility', val: 90 },
                { label: 'Dependency Resilience', val: 82 },
                { label: 'Governance Readiness', val: 94 },
              ].map((dim) => (
                <div key={dim.label} className="space-y-1">
                  <div className="flex justify-between text-slate-300">
                    <span>{dim.label}</span>
                    <span className="font-bold text-emerald-400">{dim.val}%</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-1.5">
                    <div className="bg-emerald-500 h-1.5 rounded-full" style={{ width: `${dim.val}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Tab: Dependency Graph & SPOF */}
      {activeTab === 'dependencies' && (
        <div className="space-y-6">
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-amber-400" />
              Single Points of Failure (SPOF) & Cascading Outage Models
            </h3>
            <div className="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2 text-xs">
              <div className="flex justify-between font-bold text-white">
                <span>Critical SPOF: service_auth_jwt</span>
                <span className="text-red-400">CRITICAL IMPACT</span>
              </div>
              <p className="text-slate-400">
                Failure causes cascading outages on: <span className="text-slate-200">service_api_gateway, service_billing, admin_portal</span>.
              </p>
              <div className="text-indigo-400 font-medium">
                Mitigation: Deploy redundant multi-zone replica to achieve high availability.
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab: Scenarios & Attack Propagation */}
      {activeTab === 'scenarios' && (
        <div className="space-y-4">
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <GitBranch className="w-5 h-5 text-cyan-400" />
              4-Step Future Attack Propagation Projections
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
              {[
                { step: 'CURRENT', title: 'Initial Access on Workstation', label: 'SIMULATED', conf: '95%' },
                { step: '+1 STEP', title: 'Privilege Escalation via Shadow Copy', label: 'PREDICTED', conf: '88%' },
                { step: '+2 STEPS', title: 'Lateral Movement to Auth Service', label: 'PREDICTED', conf: '78%' },
                { step: '+3 STEPS', title: 'Target Database Exfiltration', label: 'PREDICTED', conf: '65%' },
              ].map((s) => (
                <div key={s.step} className="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-cyan-400">{s.step}</span>
                    <span className="px-2 py-0.5 bg-slate-800 text-slate-300 rounded font-mono text-[10px]">
                      {s.label}
                    </span>
                  </div>
                  <div className="font-medium text-white">{s.title}</div>
                  <div className="text-slate-400">Confidence: <span className="text-emerald-400">{s.conf}</span></div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Tab: What-If & Pareto */}
      {activeTab === 'whatif' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Sliders className="w-5 h-5 text-indigo-400" />
            Pareto-Optimal Defense Strategy Candidates
          </h3>
          <div className="divide-y divide-slate-800 text-xs">
            {[
              { id: 'strat_c', name: 'Micro-Segmentation + Automated Step-Up MFA', riskRed: '91%', cost: 'LOW', disrup: 'NEGLIGIBLE', pareto: true },
              { id: 'strat_a', name: 'Global Service Hard Isolation', riskRed: '95%', cost: 'HIGH', disrup: 'SEVERE', pareto: false },
              { id: 'strat_b', name: 'Increased Telemetry Logging Only', riskRed: '45%', cost: 'LOW', disrup: 'NONE', pareto: false },
            ].map((strat) => (
              <div key={strat.id} className="py-3 flex justify-between items-center">
                <div>
                  <div className="font-bold text-white text-sm flex items-center gap-2">
                    {strat.name}
                    {strat.pareto && (
                      <span className="px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-semibold text-[10px]">
                        PARETO OPTIMAL
                      </span>
                    )}
                  </div>
                  <div className="text-slate-400 mt-1">
                    Risk Reduction: <span className="text-emerald-400 font-semibold">{strat.riskRed}</span> • Disruption: <span className="text-slate-200">{strat.disrup}</span> • Cost: <span className="text-slate-200">{strat.cost}</span>
                  </div>
                </div>
                <button className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold">
                  Select Strategy
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab: Recovery */}
      {activeTab === 'recovery' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Clock className="w-5 h-5 text-emerald-400" />
            Disaster Recovery & RTO / RPO Simulation
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <span className="text-slate-400">Target RTO:</span>
              <div className="text-2xl font-bold text-white mt-1">60 min</div>
            </div>
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <span className="text-slate-400">Simulated RTO:</span>
              <div className="text-2xl font-bold text-cyan-400 mt-1">68 min</div>
            </div>
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <span className="text-slate-400">Empirical Validated RTO:</span>
              <div className="text-2xl font-bold text-indigo-400 mt-1">75 min</div>
            </div>
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <span className="text-slate-400">Target RPO:</span>
              <div className="text-2xl font-bold text-emerald-400 mt-1">15 min</div>
            </div>
          </div>
        </div>
      )}

      {/* Tab: Accuracy & Calibration */}
      {activeTab === 'accuracy' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-cyan-400" />
            Statistical Prediction Accuracy & Continuous Model Calibration
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <span className="text-slate-400">Prediction Precision:</span>
              <div className="text-2xl font-bold text-emerald-400 mt-1">92.0%</div>
            </div>
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <span className="text-slate-400">Prediction Recall:</span>
              <div className="text-2xl font-bold text-cyan-400 mt-1">89.0%</div>
            </div>
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <span className="text-slate-400">Calibration Score:</span>
              <div className="text-2xl font-bold text-indigo-400 mt-1">94.0%</div>
            </div>
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <span className="text-slate-400">Evaluated Sample Size:</span>
              <div className="text-2xl font-bold text-white mt-1">240 runs</div>
            </div>
          </div>
        </div>
      )}

      {/* Tab: Roadmap */}
      {activeTab === 'roadmap' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-indigo-400" />
            Prioritized Resilience Improvement Roadmap
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div className="space-y-3">
              <div className="font-bold text-emerald-400 text-sm border-b border-slate-800 pb-2">STAGE 1: NOW</div>
              <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 space-y-1">
                <div className="font-semibold text-white">Deploy Redundant Auth Replica</div>
                <div className="text-slate-400">Risk Reduction: +85% • Effort: LOW</div>
              </div>
            </div>
            <div className="space-y-3">
              <div className="font-bold text-cyan-400 text-sm border-b border-slate-800 pb-2">STAGE 2: NEXT</div>
              <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 space-y-1">
                <div className="font-semibold text-white">Enforce DMZ Micro-Segmentation</div>
                <div className="text-slate-400">Risk Reduction: +70% • Effort: MEDIUM</div>
              </div>
            </div>
            <div className="space-y-3">
              <div className="font-bold text-indigo-400 text-sm border-b border-slate-800 pb-2">STAGE 3: LATER</div>
              <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 space-y-1">
                <div className="font-semibold text-white">Automate DR DNS Failover Checks</div>
                <div className="text-slate-400">Risk Reduction: +60% • Effort: HIGH</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CyberResilienceTwinCenterPage;
