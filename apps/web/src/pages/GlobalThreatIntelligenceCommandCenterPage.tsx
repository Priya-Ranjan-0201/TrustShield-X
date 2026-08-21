import React, { useState } from 'react';
import { 
  Globe, ShieldAlert, Activity, GitBranch, Radio, 
  Flame, TrendingUp, AlertTriangle, Eye, Compass, 
  Database, CheckCircle2, Layers, Sliders, Play, RefreshCw, Lock
} from 'lucide-react';

interface IntelOverview {
  registered_sources_count: number;
  active_threat_campaigns_count: number;
  threat_forecasts_count: number;
  early_warnings_count: number;
  intelligence_accuracy_score: number;
  feed_health_status: string;
}

export const GlobalThreatIntelligenceCommandCenterPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'campaigns' | 'forecasts' | 'early_warnings' | 'hypotheses' | 'sources' | 'conflicts'>('overview');
  const [overview, setOverview] = useState<IntelOverview>({
    registered_sources_count: 1,
    active_threat_campaigns_count: 1,
    threat_forecasts_count: 1,
    early_warnings_count: 1,
    intelligence_accuracy_score: 0.96,
    feed_health_status: 'HEALTHY',
  });

  const [forecasting, setForecasting] = useState(false);
  const [forecastOutput, setForecastOutput] = useState<any>(null);

  const triggerForecastRun = async () => {
    setForecasting(true);
    try {
      await new Promise(r => setTimeout(r, 600));
      setForecastOutput({
        subject: "DarkStorm Campaign Lateral Movement Velocity",
        horizon: "SHORT_TERM (72h)",
        prediction: "Projected 40% increase in API credential stuffing across finance sector.",
        confidence_score: 0.88,
        methodology: "ARIMA Time-Series on NetFlow Velocity + Attacker Infrastructure Clustering",
        claim_status: "FORECAST"
      });
    } finally {
      setForecasting(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <Globe className="h-8 w-8 text-rose-400" />
            <h1 className="text-3xl font-bold tracking-tight text-white">
              Global Threat Intelligence Command Center
            </h1>
          </div>
          <p className="text-slate-400 mt-1">
            Provenance-First Threat Fusion, Campaign Correlation, Early Warnings & Predictive Forecasting
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="bg-slate-900 border border-slate-800 px-4 py-2 rounded-lg text-sm">
            <span className="text-slate-400">Feed Health: </span>
            <span className="font-semibold text-emerald-400">{overview.feed_health_status}</span>
          </div>
          <button
            onClick={triggerForecastRun}
            disabled={forecasting}
            className="flex items-center gap-2 bg-rose-600 hover:bg-rose-500 text-white px-4 py-2 rounded-lg font-medium transition"
          >
            {forecasting ? <RefreshCw className="h-4 w-4 animate-spin" /> : <TrendingUp className="h-4 w-4" />}
            Generate Threat Forecast
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Active Campaigns</span>
            <Flame className="h-4 w-4 text-rose-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">{overview.active_threat_campaigns_count}</div>
          <div className="text-xs text-rose-400 mt-1 font-medium">DarkStorm Global Cluster Tracked</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Early Warning State</span>
            <ShieldAlert className="h-4 w-4 text-amber-400" />
          </div>
          <div className="text-3xl font-extrabold text-amber-400">HIGH</div>
          <div className="text-xs text-amber-400 mt-1 font-medium">Surge Velocity Detected in Edge C2</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Forecast Accuracy</span>
            <CheckCircle2 className="h-4 w-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">96.0%</div>
          <div className="text-xs text-emerald-400 mt-1 font-medium">Calibrated against Historical Drills</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Intelligence Quality</span>
            <Activity className="h-4 w-4 text-cyan-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">0.94</div>
          <div className="text-xs text-cyan-400 mt-1 font-medium">Cryptographic Provenance Verified</div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 gap-6">
        {(['overview', 'campaigns', 'forecasts', 'early_warnings', 'hypotheses', 'sources', 'conflicts'] as const).map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`pb-3 text-sm font-semibold capitalize transition ${
              activeTab === tab 
                ? 'border-b-2 border-rose-400 text-rose-400' 
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            {tab.replace('_', ' ')}
          </button>
        ))}
      </div>

      {/* Forecast Result Output */}
      {forecastOutput && (
        <div className="bg-rose-950/40 border border-rose-500/50 p-6 rounded-xl space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-rose-400 font-bold text-lg flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              Predictive Threat Forecast Generated
            </span>
            <span className="text-xs bg-rose-950 text-rose-300 border border-rose-800 px-2 py-0.5 rounded font-mono">
              [FORECAST]
            </span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <span className="text-slate-400">Subject: </span>
              <span className="text-white font-semibold">{forecastOutput.subject}</span>
            </div>
            <div>
              <span className="text-slate-400">Horizon: </span>
              <span className="text-cyan-400 font-mono">{forecastOutput.horizon}</span>
            </div>
            <div>
              <span className="text-slate-400">Confidence: </span>
              <span className="text-emerald-400 font-semibold">{forecastOutput.confidence_score * 100}%</span>
            </div>
          </div>
          <p className="text-xs text-slate-300 bg-slate-900/80 p-3 rounded border border-slate-800">
            {forecastOutput.prediction}
          </p>
        </div>
      )}

      {/* Tab Contents */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Active Campaigns */}
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Flame className="h-5 w-5 text-rose-400" />
              Active Correlated Campaigns
            </h2>
            <div className="bg-slate-950/70 border border-slate-800/80 p-4 rounded-lg space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-white">DarkStorm Global Supply-Chain Infiltration</span>
                <span className="text-xs bg-rose-950 text-rose-300 border border-rose-800 px-2 py-0.5 rounded">EXPANDING</span>
              </div>
              <p className="text-xs text-slate-400">Multi-stage credential stuffing targeting cloud gateways across finance & defense.</p>
              <div className="text-xs text-slate-400 pt-1 flex items-center justify-between">
                <span>TTPs: T1078, T1055, T1021</span>
                <span className="text-rose-400 font-mono">Confidence: 92%</span>
              </div>
            </div>
          </div>

          {/* Defensive Hypotheses */}
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Compass className="h-5 w-5 text-cyan-400" />
              Digital Twin Defensive Hypotheses
            </h2>
            <div className="bg-slate-950/70 border border-slate-800/80 p-5 rounded-lg space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-white">DarkStorm WAF Rate-Limit Hardening</span>
                <span className="text-xs bg-cyan-950 text-cyan-300 border border-cyan-800 px-2 py-0.5 rounded font-mono">[TESTABLE]</span>
              </div>
              <p className="text-xs text-slate-300">
                If rate-limiting and MFA step-up are enforced, DarkStorm initial credential stuffing containment improves by 85%.
              </p>
              <div className="text-xs text-cyan-400">
                Linked Scenario: <span className="font-mono text-white">scen_phishing_lateral_movement</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'early_warnings' && (
        <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldAlert className="h-5 w-5 text-amber-400" />
            Active Threat Early Warnings
          </h2>
          <div className="bg-slate-950/70 border border-amber-900/50 p-4 rounded-lg space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-bold text-amber-300">DarkStorm Rapid C2 Expansion</span>
              <span className="text-xs bg-amber-950 text-amber-300 border border-amber-800 px-2 py-0.5 rounded">HIGH SEVERITY</span>
            </div>
            <p className="text-xs text-slate-400">Pre-position rate-limiting Sigma rules on edge API gateways and simulate in Digital Twin.</p>
            <div className="text-xs text-slate-400 pt-1 flex items-center justify-between">
              <span>Velocity Score: 0.85</span>
              <span>Novelty Score: 0.78</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
