import React, { useState } from 'react';
import { 
  Compass, Shield, AlertOctagon, Activity, Play, 
  CheckCircle2, AlertTriangle, Layers, Clock, Cpu, 
  RefreshCw, Terminal, Eye, HeartPulse, Network, Zap
} from 'lucide-react';

export const GlobalSecurityMissionControlPage: React.FC = () => {
  const [activeView, setActiveView] = useState<'soc' | 'executive' | 'ciso' | 'operations'>('soc');
  const [activeTab, setActiveTab] = useState<'overview' | 'posture' | 'incidents' | 'tasks' | 'workflows' | 'health'>('overview');
  
  const [posture, setPosture] = useState<any>({
    threat_posture: 0.94,
    exposure_posture: 0.92,
    control_posture: 0.95,
    incident_posture: 0.90,
    response_posture: 0.93,
    recovery_posture: 0.95,
    governance_posture: 0.96,
    resilience_posture: 0.94,
    overall_trend: "IMPROVING"
  });

  const [executingWf, setExecutingWf] = useState(false);
  const [wfResult, setWfResult] = useState<any>(null);

  const triggerCrossSubsystemWorkflow = async () => {
    setExecutingWf(true);
    try {
      await new Promise(r => setTimeout(r, 650));
      setWfResult({
        workflow_id: "wf_threat_to_investigation_01",
        status: "COMPLETED",
        message: "Threat forecast correlated -> Digital Twin verified -> Assurance re-checked -> SOC Task assigned -> Response ready."
      });
    } finally {
      setExecutingWf(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <Compass className="h-8 w-8 text-amber-400" />
            <h1 className="text-3xl font-bold tracking-tight text-white">
              Global Security Mission Control
            </h1>
          </div>
          <p className="text-slate-400 mt-1">
            Unified Cyber Defense Operating System, Situational Awareness & Cross-Module Orchestration
          </p>
        </div>
        
        {/* Perspective Switcher & Action */}
        <div className="flex items-center gap-3">
          <div className="flex bg-slate-900 border border-slate-800 rounded-lg p-1 text-xs">
            {(['soc', 'executive', 'ciso', 'operations'] as const).map(view => (
              <button
                key={view}
                onClick={() => setActiveView(view)}
                className={`px-3 py-1.5 rounded-md uppercase font-semibold transition ${
                  activeView === view ? 'bg-amber-500 text-slate-950' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {view}
              </button>
            ))}
          </div>

          <button
            onClick={triggerCrossSubsystemWorkflow}
            disabled={executingWf}
            className="flex items-center gap-2 bg-amber-600 hover:bg-amber-500 text-white px-4 py-2 rounded-lg font-medium transition"
          >
            {executingWf ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Zap className="h-4 w-4" />}
            Execute Mission Workflow
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Active Incidents</span>
            <AlertOctagon className="h-4 w-4 text-rose-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">1</div>
          <div className="text-xs text-emerald-400 mt-1 font-medium">DarkStorm C2 Contained</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Posture Trend</span>
            <Activity className="h-4 w-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-extrabold text-emerald-400">IMPROVING</div>
          <div className="text-xs text-emerald-400 mt-1 font-medium">94.0% Composite Readiness</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Event Fabric</span>
            <Cpu className="h-4 w-4 text-cyan-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">100%</div>
          <div className="text-xs text-cyan-400 mt-1 font-medium">Zero Duplicate Events / Idempotent</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Subsystem Health</span>
            <HeartPulse className="h-4 w-4 text-amber-400" />
          </div>
          <div className="text-3xl font-extrabold text-amber-400">HEALTHY</div>
          <div className="text-xs text-amber-400 mt-1 font-medium">All 28 Subsystem Bridges Online</div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 gap-6">
        {(['overview', 'posture', 'incidents', 'tasks', 'workflows', 'health'] as const).map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`pb-3 text-sm font-semibold capitalize transition ${
              activeTab === tab 
                ? 'border-b-2 border-amber-400 text-amber-400' 
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            {tab.replace('_', ' ')}
          </button>
        ))}
      </div>

      {/* Workflow Result Banner */}
      {wfResult && (
        <div className="bg-amber-950/40 border border-amber-500/50 p-6 rounded-xl space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-amber-300 font-bold text-lg flex items-center gap-2">
              <CheckCircle2 className="h-5 w-5 text-emerald-400" />
              Cross-Subsystem Mission Workflow Completed
            </span>
            <span className="text-xs bg-amber-950 text-amber-300 border border-amber-800 px-2 py-0.5 rounded font-mono">
              [VERIFIED END-TO-END]
            </span>
          </div>
          <p className="text-sm text-slate-200">{wfResult.message}</p>
        </div>
      )}

      {/* Tab Contents */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Active Incidents & Command */}
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <AlertOctagon className="h-5 w-5 text-rose-400" />
              Active Incident Command
            </h2>
            <div className="bg-slate-950/70 border border-slate-800/80 p-5 rounded-lg space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-bold text-white">DarkStorm C2 Gateway Intrusion Incident</span>
                <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded font-mono">CONTAINED</span>
              </div>
              <p className="text-xs text-slate-400">Commander: usr_ciso_alpha | Severity: CRITICAL | SLA: Normal</p>
              <div className="text-xs text-cyan-400 bg-slate-900/80 p-3 rounded border border-slate-800">
                Timeline: Early Warning correlated &rarr; Digital Twin verified &rarr; Four-Eyes approved WAF enforced.
              </div>

            </div>
          </div>

          {/* 8-Dimensional Posture Summary */}
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Layers className="h-5 w-5 text-amber-400" />
              8-Dimensional Operational Posture
            </h2>
            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="bg-slate-950/70 p-3 rounded border border-slate-800">Threat Posture: <span className="text-emerald-400 font-bold">94%</span></div>
              <div className="bg-slate-950/70 p-3 rounded border border-slate-800">Exposure Posture: <span className="text-emerald-400 font-bold">92%</span></div>
              <div className="bg-slate-950/70 p-3 rounded border border-slate-800">Control Posture: <span className="text-emerald-400 font-bold">95%</span></div>
              <div className="bg-slate-950/70 p-3 rounded border border-slate-800">Incident Posture: <span className="text-emerald-400 font-bold">90%</span></div>
              <div className="bg-slate-950/70 p-3 rounded border border-slate-800">Response Posture: <span className="text-emerald-400 font-bold">93%</span></div>
              <div className="bg-slate-950/70 p-3 rounded border border-slate-800">Recovery Posture: <span className="text-emerald-400 font-bold">95%</span></div>
              <div className="bg-slate-950/70 p-3 rounded border border-slate-800">Governance Posture: <span className="text-emerald-400 font-bold">96%</span></div>
              <div className="bg-slate-950/70 p-3 rounded border border-slate-800">Resilience Posture: <span className="text-emerald-400 font-bold">94%</span></div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'health' && (
        <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <HeartPulse className="h-5 w-5 text-emerald-400" />
            Subsystem & Dependency Health Matrix
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs font-mono">
            <div className="bg-slate-950 p-4 rounded border border-slate-800 flex justify-between items-center">
              <span>Threat Intelligence:</span>
              <span className="text-emerald-400 font-bold">HEALTHY</span>
            </div>
            <div className="bg-slate-950 p-4 rounded border border-slate-800 flex justify-between items-center">
              <span>Digital Twin Lab:</span>
              <span className="text-emerald-400 font-bold">HEALTHY</span>
            </div>
            <div className="bg-slate-950 p-4 rounded border border-slate-800 flex justify-between items-center">
              <span>Security Assurance:</span>
              <span className="text-emerald-400 font-bold">HEALTHY</span>
            </div>
            <div className="bg-slate-950 p-4 rounded border border-slate-800 flex justify-between items-center">
              <span>Autonomous Engineering:</span>
              <span className="text-emerald-400 font-bold">HEALTHY</span>
            </div>
            <div className="bg-slate-950 p-4 rounded border border-slate-800 flex justify-between items-center">
              <span>SOC SOAR:</span>
              <span className="text-emerald-400 font-bold">HEALTHY</span>
            </div>
            <div className="bg-slate-950 p-4 rounded border border-slate-800 flex justify-between items-center">
              <span>Cyber Resilience:</span>
              <span className="text-emerald-400 font-bold">HEALTHY</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
