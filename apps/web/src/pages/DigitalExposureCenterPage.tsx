import React, { useState } from 'react';
import { 
  ShieldAlert, 
  Globe, 
  Activity, 
  Layers, 
  Search, 
  AlertTriangle, 
  Radio, 
  CheckCircle2, 
  Eye,
  RefreshCw,
  TrendingUp,
  Cpu,
  Lock
} from 'lucide-react';

interface AssetRecord {
  asset_id: string;
  asset_type: string;
  canonical_identifier: string;
  display_identifier: string;
  ownership_status: string;
  criticality: string;
  exposure_score: number;
  risk_score: number;
  trust_score: number;
  monitoring_status: string;
}

interface ExposureFinding {
  finding_id: string;
  title: string;
  severity: string;
  exposure_score: number;
  risk_score: number;
  trust_score: number;
  recommended_action: string;
  asset_identifier: string;
}

export const DigitalExposureCenterPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'assets' | 'findings' | 'shadow' | 'impersonation' | 'monitoring'>('overview');
  const [searchTerm, setSearchTerm] = useState('');

  // Sample production state data for demonstration
  const [assets] = useState<AssetRecord[]>([
    {
      asset_id: 'ast_9a82bc1',
      asset_type: 'DOMAIN',
      canonical_identifier: 'auth.truthshield.io',
      display_identifier: 'auth.truthshield.io',
      ownership_status: 'VERIFIED_OWNER',
      criticality: 'CRITICAL',
      exposure_score: 45.0,
      risk_score: 12.0,
      trust_score: 96.0,
      monitoring_status: 'RUNNING'
    },
    {
      asset_id: 'ast_104f9b2',
      asset_type: 'API_ENDPOINT',
      canonical_identifier: 'api.truthshield.io/v1/scan',
      display_identifier: 'api.truthshield.io/v1/scan',
      ownership_status: 'VERIFIED_OWNER',
      criticality: 'HIGH',
      exposure_score: 60.0,
      risk_score: 18.0,
      trust_score: 92.0,
      monitoring_status: 'RUNNING'
    },
    {
      asset_id: 'ast_442e91a',
      asset_type: 'MOBILE_APPLICATION',
      canonical_identifier: 'io.truthshield.security.authenticator',
      display_identifier: 'TruthShield Security App (v4.2.0)',
      ownership_status: 'VERIFIED_OWNER',
      criticality: 'HIGH',
      exposure_score: 35.0,
      risk_score: 8.0,
      trust_score: 98.0,
      monitoring_status: 'RUNNING'
    },
    {
      asset_id: 'ast_77189c4',
      asset_type: 'CLOUD_ASSET',
      canonical_identifier: 'truthshield-backup-storage.s3.amazonaws.com',
      display_identifier: 'truthshield-backup-storage (AWS S3)',
      ownership_status: 'CLAIMED_OWNER',
      criticality: 'MEDIUM',
      exposure_score: 75.0,
      risk_score: 32.0,
      trust_score: 84.0,
      monitoring_status: 'SCHEDULED'
    }
  ]);

  const [findings] = useState<ExposureFinding[]>([
    {
      finding_id: 'fnd_01c448a',
      title: 'Newly Exposed Administrative Port (TCP 3389) on Staging Gateway',
      severity: 'CRITICAL',
      exposure_score: 88.0,
      risk_score: 82.0,
      trust_score: 55.0,
      recommended_action: 'Apply immediate security group restriction; verify origin change.',
      asset_identifier: 'staging-gw.truthshield.io'
    },
    {
      finding_id: 'fnd_02b991f',
      title: 'TLS Certificate Expiring within 48 Hours',
      severity: 'HIGH',
      exposure_score: 65.0,
      risk_score: 45.0,
      trust_score: 72.0,
      recommended_action: 'Trigger automated ACME certificate renewal sequence.',
      asset_identifier: 'partner-portal.truthshield.io'
    }
  ]);

  const filteredAssets = assets.filter(a => 
    a.canonical_identifier.toLowerCase().includes(searchTerm.toLowerCase()) ||
    a.asset_type.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 space-y-8 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-indigo-500/10 border border-indigo-500/30 rounded-xl text-indigo-400">
              <Globe className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
                Digital Exposure Center
                <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-medium">
                  Continuous Monitoring Active
                </span>
              </h1>
              <p className="text-sm text-slate-400">
                Continuous Attack Surface Intelligence, Asset Baselines & Real-time Exposure Management
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 rounded-lg text-sm transition-colors">
            <RefreshCw className="w-4 h-4" />
            Trigger Asset Discovery
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition-colors shadow-lg shadow-indigo-600/20">
            <Radio className="w-4 h-4" />
            Add Monitored Asset
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 backdrop-blur-sm">
          <div className="flex justify-between items-start text-slate-400 text-sm">
            <span>Total Digital Assets</span>
            <Layers className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-white">{assets.length}</span>
            <span className="text-xs text-emerald-400 font-medium">100% Verified Scope</span>
          </div>
          <div className="mt-2 text-xs text-slate-500">
            Domains, APIs, Cloud Storage, APKs
          </div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 backdrop-blur-sm">
          <div className="flex justify-between items-start text-slate-400 text-sm">
            <span>Mean Exposure Score</span>
            <Eye className="w-4 h-4 text-amber-400" />
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-amber-400">53.8</span>
            <span className="text-xs text-slate-400 font-medium">/ 100</span>
          </div>
          <div className="mt-2 text-xs text-slate-500">
            Public reachability & surface footprint
          </div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 backdrop-blur-sm">
          <div className="flex justify-between items-start text-slate-400 text-sm">
            <span>Average Trust Score</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-emerald-400">92.5</span>
            <span className="text-xs text-slate-400 font-medium">/ 100</span>
          </div>
          <div className="mt-2 text-xs text-slate-500">
            High cryptographic & identity integrity
          </div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 backdrop-blur-sm">
          <div className="flex justify-between items-start text-slate-400 text-sm">
            <span>Open Exposure Findings</span>
            <ShieldAlert className="w-4 h-4 text-rose-400" />
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-rose-400">{findings.length}</span>
            <span className="text-xs text-rose-400 font-medium">1 Critical</span>
          </div>
          <div className="mt-2 text-xs text-slate-500">
            Action required to prevent exposure escalation
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 space-x-8">
        {[
          { id: 'overview', label: 'Attack Surface Overview' },
          { id: 'assets', label: 'Asset Inventory' },
          { id: 'findings', label: 'Prioritized Findings' },
          { id: 'shadow', label: 'Shadow Asset Discovery' },
          { id: 'impersonation', label: 'Brand Impersonation' },
          { id: 'monitoring', label: 'Monitoring Schedulers' },
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
      {activeTab === 'overview' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 bg-slate-900/50 border border-slate-800 rounded-xl p-6">
              <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <Activity className="w-5 h-5 text-indigo-400" />
                Continuous Exposure & Trust Health Trend
              </h2>
              <div className="h-64 flex items-center justify-center border border-dashed border-slate-800 rounded-lg text-slate-500 text-sm">
                Real-Time Attack Surface Telemetry & Exposure Flux Curve
              </div>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
              <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <Lock className="w-5 h-5 text-emerald-400" />
                Asset Criticality Breakdown
              </h2>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-xs text-slate-400 mb-1">
                    <span>Critical Infrastructure</span>
                    <span className="font-semibold text-rose-400">1 Asset (25%)</span>
                  </div>
                  <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-rose-500 w-1/4 rounded-full" />
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-xs text-slate-400 mb-1">
                    <span>High Criticality (APIs / Apps)</span>
                    <span className="font-semibold text-amber-400">2 Assets (50%)</span>
                  </div>
                  <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-amber-500 w-2/4 rounded-full" />
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-xs text-slate-400 mb-1">
                    <span>Medium / Internal Storage</span>
                    <span className="font-semibold text-indigo-400">1 Asset (25%)</span>
                  </div>
                  <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-indigo-500 w-1/4 rounded-full" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'assets' && (
        <div className="space-y-4">
          <div className="flex justify-between items-center gap-4">
            <div className="relative flex-1 max-w-md">
              <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
              <input
                type="text"
                placeholder="Search by identifier, domain, or asset type..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-9 pr-4 py-2 bg-slate-900 border border-slate-800 rounded-lg text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-xl overflow-hidden">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="bg-slate-950/80 text-xs uppercase text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="px-6 py-4">Asset Identifier</th>
                  <th className="px-6 py-4">Type</th>
                  <th className="px-6 py-4">Criticality</th>
                  <th className="px-6 py-4">Exposure</th>
                  <th className="px-6 py-4">Trust Score</th>
                  <th className="px-6 py-4">Monitoring</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {filteredAssets.map((asset) => (
                  <tr key={asset.asset_id} className="hover:bg-slate-800/30 transition-colors">
                    <td className="px-6 py-4 font-mono font-medium text-white">
                      {asset.display_identifier}
                    </td>
                    <td className="px-6 py-4">
                      <span className="px-2.5 py-1 rounded bg-slate-800 text-xs text-slate-300 font-mono">
                        {asset.asset_type}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-0.5 rounded text-xs font-semibold ${
                        asset.criticality === 'CRITICAL' ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' :
                        asset.criticality === 'HIGH' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                        'bg-slate-800 text-slate-300'
                      }`}>
                        {asset.criticality}
                      </span>
                    </td>
                    <td className="px-6 py-4 font-mono text-amber-400 font-semibold">
                      {asset.exposure_score.toFixed(1)}
                    </td>
                    <td className="px-6 py-4 font-mono text-emerald-400 font-semibold">
                      {asset.trust_score.toFixed(1)}
                    </td>
                    <td className="px-6 py-4">
                      <span className="flex items-center gap-1.5 text-xs text-emerald-400">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                        {asset.monitoring_status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'findings' && (
        <div className="space-y-4">
          {findings.map((f) => (
            <div key={f.finding_id} className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 hover:border-slate-700 transition-colors">
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-3">
                  <div className={`p-2 rounded-lg ${
                    f.severity === 'CRITICAL' ? 'bg-rose-500/20 text-rose-400' : 'bg-amber-500/20 text-amber-400'
                  }`}>
                    <AlertTriangle className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold text-white">{f.title}</h3>
                      <span className={`px-2 py-0.5 text-xs font-bold rounded ${
                        f.severity === 'CRITICAL' ? 'bg-rose-500/20 text-rose-400' : 'bg-amber-500/20 text-amber-400'
                      }`}>
                        {f.severity}
                      </span>
                    </div>
                    <p className="text-xs font-mono text-slate-400 mt-1">Asset: {f.asset_identifier}</p>
                    <p className="text-sm text-slate-300 mt-2">{f.recommended_action}</p>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-xs text-slate-500">Exposure Score</div>
                  <div className="text-lg font-bold text-amber-400">{f.exposure_score.toFixed(1)}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DigitalExposureCenterPage;
