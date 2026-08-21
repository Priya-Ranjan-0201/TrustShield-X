import React, { useState } from 'react';
import { 
  ShieldCheck, 
  ShieldAlert, 
  Activity, 
  Layers, 
  Zap, 
  Crosshair, 
  Radio, 
  AlertTriangle, 
  CheckCircle2, 
  TrendingDown, 
  TrendingUp, 
  Workflow, 
  FileText, 
  Terminal,
  Cpu,
  Server
} from 'lucide-react';

interface SecurityPostureState {
  overall_score: number;
  risk_score: number;
  trust_score: number;
  exposure_score: number;
  trend: string;
  trend_explanation: string;
}

interface ActiveThreatCluster {
  cluster_id: string;
  title: string;
  fusion_score: number;
  severity: string;
  modalities: string[];
  entity_count: number;
}

export const SecurityCommandCenterPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'posture' | 'threats' | 'campaigns' | 'incidents' | 'kpis' | 'health'>('posture');

  const [posture] = useState<SecurityPostureState>({
    overall_score: 82.5,
    risk_score: 18.0,
    trust_score: 91.5,
    exposure_score: 34.0,
    trend: 'stable',
    trend_explanation: 'Operational defense posture stable across all 10 monitoring dimensions.'
  });

  const [clusters] = useState<ActiveThreatCluster[]>([
    {
      cluster_id: 'tcl_88921a',
      title: 'Coordinated Banking Phishing & Dropper APK Convergence',
      fusion_score: 88.5,
      severity: 'CRITICAL',
      modalities: ['WEB', 'APK', 'UPI', 'INFRASTRUCTURE'],
      entity_count: 5
    },
    {
      cluster_id: 'tcl_44190c',
      title: 'Voice Clone Impersonation with Spoofed SMS Header',
      fusion_score: 72.0,
      severity: 'HIGH',
      modalities: ['VOICE', 'IDENTITY', 'PHONE'],
      entity_count: 3
    }
  ]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 space-y-8 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-indigo-500/10 border border-indigo-500/30 rounded-xl text-indigo-400">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
              Security Command Center
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-medium">
                Defense Fabric Operational
              </span>
            </h1>
            <p className="text-sm text-slate-400">
              Real-Time Threat Fusion, Security Operations Fabric & Autonomous Defense Telemetry
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 rounded-lg text-sm transition-colors">
            <FileText className="w-4 h-4" />
            Export Executive Brief
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white rounded-lg text-sm font-medium transition-colors shadow-lg shadow-rose-600/20">
            <ShieldAlert className="w-4 h-4" />
            Active Incident Command
          </button>
        </div>
      </div>

      {/* Global Posture Scorecard */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 backdrop-blur-sm">
          <div className="flex justify-between items-start text-slate-400 text-sm">
            <span>Overall Security Posture</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-emerald-400">{posture.overall_score.toFixed(1)}</span>
            <span className="text-xs text-slate-400 font-medium">/ 100</span>
          </div>
          <div className="mt-2 text-xs text-emerald-400 flex items-center gap-1">
            <TrendingUp className="w-3.5 h-3.5" />
            Healthy & Well Defended
          </div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 backdrop-blur-sm">
          <div className="flex justify-between items-start text-slate-400 text-sm">
            <span>Observed Threat Risk</span>
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-amber-400">{posture.risk_score.toFixed(1)}</span>
            <span className="text-xs text-slate-400 font-medium">/ 100</span>
          </div>
          <div className="mt-2 text-xs text-slate-500">
            Low active danger index
          </div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 backdrop-blur-sm">
          <div className="flex justify-between items-start text-slate-400 text-sm">
            <span>Digital Trust Health</span>
            <CheckCircle2 className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-indigo-400">{posture.trust_score.toFixed(1)}</span>
            <span className="text-xs text-slate-400 font-medium">/ 100</span>
          </div>
          <div className="mt-2 text-xs text-slate-500">
            High cryptographic provenance
          </div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 backdrop-blur-sm">
          <div className="flex justify-between items-start text-slate-400 text-sm">
            <span>Attack Surface Exposure</span>
            <Crosshair className="w-4 h-4 text-sky-400" />
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-sky-400">{posture.exposure_score.toFixed(1)}</span>
            <span className="text-xs text-slate-400 font-medium">/ 100</span>
          </div>
          <div className="mt-2 text-xs text-slate-500">
            Controlled external reachability
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 space-x-8">
        {[
          { id: 'posture', label: '10-Dimension Posture' },
          { id: 'threats', label: 'Multi-Modal Threat Fusion' },
          { id: 'campaigns', label: 'Active Campaigns' },
          { id: 'incidents', label: 'Incident Command' },
          { id: 'kpis', label: 'MTTx Operations KPIs' },
          { id: 'health', label: 'Subsystem Health' },
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

      {/* Main Tab Content */}
      {activeTab === 'posture' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <Activity className="w-5 h-5 text-indigo-400" />
              10-Dimension Security Posture Radar
            </h2>
            <div className="grid grid-cols-2 gap-4">
              {[
                { name: 'Threat Level Defense', score: 92.0 },
                { name: 'Asset Exposure Control', score: 86.0 },
                { name: 'Identity & Authentication', score: 95.0 },
                { name: 'Application Security', score: 88.0 },
                { name: 'Campaign Containment', score: 85.0 },
                { name: 'Incident Load Management', score: 90.0 },
                { name: 'Response Effectiveness', score: 98.5 },
                { name: 'Digital Trust Health', score: 91.5 },
                { name: 'Predictive Threat Horizon', score: 87.0 },
                { name: 'Governance & Compliance', score: 96.0 },
              ].map((dim) => (
                <div key={dim.name} className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-3">
                  <div className="flex justify-between text-xs text-slate-400 mb-1">
                    <span>{dim.name}</span>
                    <span className="font-semibold text-emerald-400">{dim.score.toFixed(1)}%</span>
                  </div>
                  <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-indigo-500 rounded-full" 
                      style={{ width: `${dim.score}%` }} 
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <Terminal className="w-5 h-5 text-emerald-400" />
              Operational Security Narrative
            </h2>
            <div className="space-y-3 text-xs text-slate-300 font-mono bg-slate-950 p-4 rounded-lg border border-slate-800">
              <p className="text-indigo-400 font-semibold">[WHAT HAPPENED]</p>
              <p>Platform evaluated active multi-modal telemetry across 13 modalities.</p>
              <p className="text-emerald-400 font-semibold mt-2">[VERIFIED EVIDENCE]</p>
              <p>All DNS sinkholes and WAF containment policies verified active with 0 bypasses.</p>
              <p className="text-amber-400 font-semibold mt-2">[REMAINING UNKNOWNS]</p>
              <p>Actor attribution remains UNCONFIRMED; monitoring continued.</p>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'threats' && (
        <div className="space-y-4">
          {clusters.map((c) => (
            <div key={c.cluster_id} className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 hover:border-slate-700 transition-colors">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-3">
                    <h3 className="text-lg font-semibold text-white">{c.title}</h3>
                    <span className={`px-2.5 py-0.5 text-xs font-bold rounded ${
                      c.severity === 'CRITICAL' ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                    }`}>
                      {c.severity}
                    </span>
                  </div>
                  <div className="flex items-center gap-2 mt-3">
                    <span className="text-xs text-slate-400">Converged Modalities:</span>
                    {c.modalities.map((m) => (
                      <span key={m} className="px-2 py-0.5 rounded bg-slate-800 text-xs font-mono text-indigo-300">
                        {m}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="text-right">
                  <div className="text-xs text-slate-400">Threat Fusion Score</div>
                  <div className="text-2xl font-bold text-amber-400">{c.fusion_score.toFixed(1)}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SecurityCommandCenterPage;
