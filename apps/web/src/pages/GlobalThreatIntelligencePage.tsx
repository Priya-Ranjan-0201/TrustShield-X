import React, { useState } from 'react';
import {
  ShieldAlert,
  Globe2,
  Cpu,
  Radio,
  FileCheck,
  AlertTriangle,
  Flame,
  Binary,
  Layers,
  Search,
  Eye,
  CheckCircle2,
  Lock,
  Compass,
  Zap,
  Sparkles,
  Database,
  ArrowRight,
  TrendingUp,
  Fingerprint,
  RefreshCw,
} from 'lucide-react';

interface IntelligenceSource {
  source_id: string;
  source_name: string;
  source_type: string;
  reliability: string;
  freshness: string;
  approval_status: string;
}

interface ThreatCampaign {
  campaign_id: string;
  name: string;
  indicators_count: number;
  techniques: string[];
  affected_sectors: string[];
  confidence: number;
  status: string;
}

interface ThreatForecast {
  forecast_id: string;
  predicted_threat: string;
  forecast_horizon: string;
  predicted_probability: number;
  state: string;
}

interface ThreatEarlyWarning {
  warning_id: string;
  reason: string;
  urgency: string;
  confidence: number;
}

export const GlobalThreatIntelligencePage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'landscape' | 'campaigns' | 'indicators' | 'forecasts' | 'dissemination'>('landscape');
  const [searchQuery, setSearchQuery] = useState('');
  const [simulatedSigma, setSimulatedSigma] = useState<string | null>(null);

  const sources: IntelligenceSource[] = [
    { source_id: 'src_cert_in_advisory', source_name: 'CERT-In National Advisory', source_type: 'GOVERNMENT', reliability: 'A (High)', freshness: 'FRESH (<1h)', approval_status: 'APPROVED' },
    { source_id: 'src_fs_isac_feed', source_name: 'Financial Services ISAC Stream', source_type: 'ISAC', reliability: 'A (High)', freshness: 'FRESH (<2h)', approval_status: 'APPROVED' },
    { source_id: 'src_commercial_feed', source_name: 'Commercial High-Fidelity Feed', source_type: 'COMMERCIAL', reliability: 'B (Good)', freshness: 'FRESH (<6h)', approval_status: 'APPROVED' },
  ];

  const campaigns: ThreatCampaign[] = [
    { campaign_id: 'cmp_darkstorm_apac', name: 'Operation DarkStorm APAC', indicators_count: 14, techniques: ['T1071.001', 'T1059.001', 'T1110.003'], affected_sectors: ['FINANCIAL_SERVICES', 'CRITICAL_INFRASTRUCTURE'], confidence: 0.88, status: 'ACTIVE' },
    { campaign_id: 'cmp_ghostviper_cloud', name: 'GhostViper Cloud Infiltration', indicators_count: 9, techniques: ['T1552.005', 'T1078.004'], affected_sectors: ['TECHNOLOGY', 'TELECOM'], confidence: 0.82, status: 'ACTIVE' },
  ];

  const forecasts: ThreatForecast[] = [
    { forecast_id: 'fc_darkstorm_7d', predicted_threat: 'Ember Bear DarkStorm Campaign expansion into APAC SWIFT banking networks.', forecast_horizon: '7_DAYS', predicted_probability: 0.82, state: 'HIGH_CONFIDENCE_FORECAST' },
    { forecast_id: 'fc_ddos_24h', predicted_threat: 'High-volume UDP amplification targeting regional telecom DNS infra.', forecast_horizon: '24_HOURS', predicted_probability: 0.74, state: 'SIGNAL' },
  ];

  const earlyWarnings: ThreatEarlyWarning[] = [
    { warning_id: 'ew_darkstorm_01', reason: 'Rapid C2 beacon frequency surge detected targeting APAC payment gateways.', urgency: 'CRITICAL', confidence: 0.94 },
  ];

  const handleGenerateSigma = (indicator: string) => {
    setSimulatedSigma(`title: Detect DarkStorm C2 Traffic
id: 9a781c-4b10-sigma-rule
status: experimental
logsource:
  category: network_traffic
detection:
  selection:
    destination_url|contains: '${indicator}'
  condition: selection
level: high`);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between border-b border-slate-800 pb-6 mb-8 gap-4">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-cyan-500/10 border border-cyan-500/30 rounded-xl text-cyan-400">
              <Globe2 className="w-8 h-8" />
            </div>
            <div>
              <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-white flex items-center gap-3">
                Global Cyber Threat Intelligence Fusion
                <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800">
                  PHASE 33 CONTROL PLANE
                </span>
              </h1>
              <p className="text-slate-400 text-sm mt-1">
                Multi-source correlation, threat actor profiling, predictive early-warning, and governed dissemination.
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <div className="px-4 py-2 bg-emerald-950/60 border border-emerald-800 rounded-lg text-emerald-400 text-xs font-mono flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            FEED HEALTH: OPTIMAL (100%)
          </div>
          <button className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg text-sm font-medium transition flex items-center gap-2">
            <RefreshCw className="w-4 h-4" /> Re-Sync Global Feeds
          </button>
        </div>
      </div>

      {/* KPI Overview Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div className="p-5 bg-slate-900/60 border border-slate-800 rounded-xl">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-slate-400">Validated Sources</span>
            <Database className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold text-white">3</div>
          <div className="text-xs text-emerald-400 mt-1 flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5" /> 100% Provenance Verified
          </div>
        </div>

        <div className="p-5 bg-slate-900/60 border border-slate-800 rounded-xl">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-slate-400">Active Threat Campaigns</span>
            <Flame className="w-4 h-4 text-rose-400" />
          </div>
          <div className="text-2xl font-bold text-white">2</div>
          <div className="text-xs text-rose-400 mt-1 flex items-center gap-1">
            <AlertTriangle className="w-3.5 h-3.5" /> Multi-factor clustered
          </div>
        </div>

        <div className="p-5 bg-slate-900/60 border border-slate-800 rounded-xl">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-slate-400">Predictive Forecasts</span>
            <TrendingUp className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-white">2</div>
          <div className="text-xs text-amber-400 mt-1 flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5" /> Brier calibrated (0.08)
          </div>
        </div>

        <div className="p-5 bg-slate-900/60 border border-slate-800 rounded-xl">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-slate-400">Early Warning Signals</span>
            <Radio className="w-4 h-4 text-violet-400" />
          </div>
          <div className="text-2xl font-bold text-white">1</div>
          <div className="text-xs text-violet-400 mt-1 flex items-center gap-1">
            <Zap className="w-3.5 h-3.5" /> Critical Urgency Active
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 mb-6 gap-2">
        {(['landscape', 'campaigns', 'indicators', 'forecasts', 'dissemination'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2.5 text-sm font-medium transition border-b-2 capitalize ${
              activeTab === tab
                ? 'border-cyan-500 text-cyan-400 bg-cyan-950/20'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Tab Contents */}
      {activeTab === 'landscape' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            {/* Early Warning Banner */}
            {earlyWarnings.map((w) => (
              <div key={w.warning_id} className="p-5 bg-rose-950/30 border border-rose-800/60 rounded-xl flex items-start gap-4">
                <div className="p-2 bg-rose-900/40 rounded-lg text-rose-400 mt-1">
                  <ShieldAlert className="w-6 h-6" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold px-2 py-0.5 rounded bg-rose-900 text-rose-200 uppercase">
                      {w.urgency} EARLY WARNING
                    </span>
                    <span className="text-xs font-mono text-slate-400">Confidence: {(w.confidence * 100).toFixed(0)}%</span>
                  </div>
                  <p className="text-sm font-medium text-rose-100 mt-2">{w.reason}</p>
                </div>
              </div>
            ))}

            {/* Ingested Feeds & Source Reliability */}
            <div className="p-6 bg-slate-900/50 border border-slate-800 rounded-xl">
              <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <Database className="w-5 h-5 text-cyan-400" />
                Intelligence Feed Registry & Source Integrity
              </h2>
              <div className="space-y-3">
                {sources.map((s) => (
                  <div key={s.source_id} className="p-4 bg-slate-950/60 border border-slate-800 rounded-lg flex items-center justify-between">
                    <div>
                      <div className="font-medium text-slate-200 text-sm">{s.source_name}</div>
                      <div className="text-xs text-slate-500 font-mono mt-0.5">{s.source_id} • Type: {s.source_type}</div>
                    </div>
                    <div className="flex items-center gap-3 text-xs">
                      <span className="px-2 py-1 bg-slate-800 text-cyan-400 rounded">Reliability: {s.reliability}</span>
                      <span className="px-2 py-1 bg-emerald-950 text-emerald-400 border border-emerald-800 rounded">{s.approval_status}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="space-y-6">
            {/* 6-Dimensional Quality Scorecard */}
            <div className="p-6 bg-slate-900/50 border border-slate-800 rounded-xl">
              <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <FileCheck className="w-5 h-5 text-emerald-400" />
                Intelligence Quality Scorecard
              </h2>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between py-1.5 border-b border-slate-800 text-slate-400">
                  <span>Source Reliability:</span>
                  <span className="text-slate-200 font-mono font-medium">A (Admiralty Scale)</span>
                </div>
                <div className="flex justify-between py-1.5 border-b border-slate-800 text-slate-400">
                  <span>Information Credibility:</span>
                  <span className="text-slate-200 font-mono font-medium">1 (Confirmed)</span>
                </div>
                <div className="flex justify-between py-1.5 border-b border-slate-800 text-slate-400">
                  <span>Freshness Score:</span>
                  <span className="text-emerald-400 font-mono font-medium">0.95 (Fresh)</span>
                </div>
                <div className="flex justify-between py-1.5 border-b border-slate-800 text-slate-400">
                  <span>Independent Corroboration:</span>
                  <span className="text-cyan-400 font-mono font-medium">3 Independent Sources</span>
                </div>
                <div className="flex justify-between py-1.5 border-b border-slate-800 text-slate-400">
                  <span>Context Completeness:</span>
                  <span className="text-slate-200 font-mono font-medium">1.0 (Full TTP & Asset Linkage)</span>
                </div>
                <div className="flex justify-between py-1.5 text-slate-400">
                  <span>Provenance Cryptography:</span>
                  <span className="text-emerald-400 font-mono font-medium flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> SHA-256 Verified
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'campaigns' && (
        <div className="space-y-4">
          {campaigns.map((c) => (
            <div key={c.campaign_id} className="p-6 bg-slate-900/50 border border-slate-800 rounded-xl">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <Flame className="w-5 h-5 text-rose-400" />
                  {c.name}
                </h3>
                <span className="text-xs font-mono px-3 py-1 bg-rose-950 text-rose-400 border border-rose-800 rounded-full w-fit">
                  Confidence: {(c.confidence * 100).toFixed(0)}%
                </span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-slate-400">
                <div>
                  <span className="block text-slate-500 mb-1">MITRE ATT&CK Techniques:</span>
                  <div className="flex flex-wrap gap-1.5">
                    {c.techniques.map((t) => (
                      <span key={t} className="px-2 py-0.5 bg-slate-800 text-cyan-300 font-mono rounded">{t}</span>
                    ))}
                  </div>
                </div>
                <div>
                  <span className="block text-slate-500 mb-1">Affected Industry Sectors:</span>
                  <div className="flex flex-wrap gap-1.5">
                    {c.affected_sectors.map((s) => (
                      <span key={s} className="px-2 py-0.5 bg-slate-800 text-amber-300 font-mono rounded">{s}</span>
                    ))}
                  </div>
                </div>
                <div>
                  <span className="block text-slate-500 mb-1">Multi-Factor Clustering Guard:</span>
                  <span className="text-emerald-400">Multi-Factor Validated (No Single-IOC Merges)</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'indicators' && (
        <div className="p-6 bg-slate-900/50 border border-slate-800 rounded-xl">
          <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Fingerprint className="w-5 h-5 text-cyan-400" />
            Indicator Intelligence (IOC / IOA / IOB)
          </h2>
          <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="text-xs font-mono text-cyan-400">URL / C2 BEACON</div>
              <div className="text-sm font-medium text-slate-200 mt-1 font-mono">
                http://malicious-c2.darkstorm-threat.com/beacon
              </div>
              <div className="text-xs text-slate-500 mt-1">Lifecycle: ACTIVE • Canonical Hash: 9a781c4b10...</div>
            </div>
            <button
              onClick={() => handleGenerateSigma('http://malicious-c2.darkstorm-threat.com/beacon')}
              className="px-3 py-1.5 bg-cyan-900/50 hover:bg-cyan-900 text-cyan-300 border border-cyan-700 rounded text-xs transition flex items-center gap-1.5"
            >
              <Zap className="w-3.5 h-3.5" /> Generate Sigma Rule
            </button>
          </div>

          {simulatedSigma && (
            <div className="mt-4 p-4 bg-slate-950/80 border border-cyan-800/60 rounded-lg">
              <div className="text-xs font-bold text-cyan-400 mb-2">Candidate Sigma Rule (Requires Approval):</div>
              <pre className="text-xs font-mono text-slate-300 overflow-x-auto whitespace-pre-wrap">{simulatedSigma}</pre>
            </div>
          )}
        </div>
      )}

      {activeTab === 'forecasts' && (
        <div className="space-y-4">
          {forecasts.map((f) => (
            <div key={f.forecast_id} className="p-5 bg-slate-900/50 border border-slate-800 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold px-2 py-0.5 bg-amber-950 text-amber-400 border border-amber-800 rounded">
                    HORIZON: {f.forecast_horizon}
                  </span>
                  <span className="text-xs font-mono text-slate-400">State: {f.state}</span>
                </div>
                <p className="text-sm text-slate-200 font-medium mt-2">{f.predicted_threat}</p>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-amber-400 font-mono">{(f.predicted_probability * 100).toFixed(0)}%</div>
                <div className="text-xs text-slate-500">Predicted Probability</div>
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'dissemination' && (
        <div className="p-6 bg-slate-900/50 border border-slate-800 rounded-xl">
          <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Lock className="w-5 h-5 text-violet-400" />
            Governed Intelligence Dissemination & ABAC
          </h2>
          <p className="text-sm text-slate-400 mb-4">
            Dissemination policies enforce strict tenant isolation, classification clearance checks, and explicit DENY precedence.
          </p>
          <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg flex items-center justify-between">
            <div>
              <div className="text-sm font-medium text-slate-200">Candidate Detection Dissemination — DarkStorm Sigma</div>
              <div className="text-xs text-slate-500 mt-0.5">Recipient: SOC_DETECTION_ENGINEERING • Classification: INTERNAL</div>
            </div>
            <span className="px-2.5 py-1 bg-emerald-950 text-emerald-400 border border-emerald-800 text-xs rounded font-medium">
              PERMITTED (ABAC Passed)
            </span>
          </div>
        </div>
      )}
    </div>
  );
};
