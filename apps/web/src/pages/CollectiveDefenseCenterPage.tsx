import React, { useState } from 'react';
import {
  Globe,
  Shield,
  Radio,
  AlertTriangle,
  Network,
  Share2,
  Lock,
  Eye,
  CheckCircle2,
  Search,
  Filter,
  RefreshCw,
  TrendingUp,
  Activity,
  Layers,
  HelpCircle,
  FileCheck,
  Ban,
} from 'lucide-react';

export const CollectiveDefenseCenterPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'feed' | 'campaigns' | 'warnings' | 'graph' | 'quality' | 'partners' | 'disputes'>('feed');
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 space-y-8 font-sans">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-cyan-500/10 border border-cyan-500/30 rounded-xl text-cyan-400">
            <Globe className="w-7 h-7" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
              Collective Defense Network
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 font-medium">
                Federation Online
              </span>
            </h1>
            <p className="text-sm text-slate-400">
              Cross-Organization Early Warning • Privacy-Preserving Threat Intelligence • Global Campaign Graph
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 rounded-lg text-sm transition-colors">
            <RefreshCw className="w-4 h-4" />
            Sync Federation
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg text-sm font-medium transition-colors shadow-lg shadow-cyan-600/20">
            <Share2 className="w-4 h-4" />
            Share Intelligence
          </button>
        </div>
      </div>

      {/* Global Metrics Bar */}
      <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Total Indicators</div>
          <div className="text-3xl font-bold text-white mt-2">1,420</div>
          <div className="text-xs text-cyan-400 mt-1">Cross-tenant verified</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Global Campaigns</div>
          <div className="text-3xl font-bold text-amber-400 mt-2">18</div>
          <div className="text-xs text-amber-300/80 mt-1">Multi-modal clustered</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Early Warnings</div>
          <div className="text-3xl font-bold text-red-400 mt-2">4</div>
          <div className="text-xs text-red-300/80 mt-1">Active broadcast waves</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Federation Nodes</div>
          <div className="text-3xl font-bold text-emerald-400 mt-2">24</div>
          <div className="text-xs text-emerald-400 mt-1">Authenticated partners</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Quality Index</div>
          <div className="text-3xl font-bold text-indigo-400 mt-2">94.6%</div>
          <div className="text-xs text-indigo-300/80 mt-1">Multi-source corroborated</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Privacy Status</div>
          <div className="text-xl font-bold text-emerald-400 mt-2">ZERO LEAK</div>
          <div className="text-xs text-emerald-300/80 mt-1">100% PII Redacted</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 space-x-8 overflow-x-auto">
        {[
          { id: 'feed', label: 'Collective Threat Feed' },
          { id: 'campaigns', label: 'Global Campaigns' },
          { id: 'warnings', label: 'Early Warnings & Forecasts' },
          { id: 'graph', label: 'Threat Graph Explorer' },
          { id: 'quality', label: 'Quality & Disputes' },
          { id: 'partners', label: 'Federation Partners' },
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

      {/* Main Content Area */}
      {activeTab === 'feed' && (
        <div className="space-y-4">
          <div className="flex justify-between items-center gap-4 bg-slate-900/40 p-4 rounded-xl border border-slate-800">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-2.5 w-4 h-4 text-slate-500" />
              <input
                type="text"
                placeholder="Search domain, IP, hash, certificate, or phone..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-4 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-cyan-500"
              />
            </div>
            <div className="flex items-center gap-2">
              <button className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-300">
                <Filter className="w-3.5 h-3.5" /> Filter by Type
              </button>
              <button className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-300">
                <Lock className="w-3.5 h-3.5" /> Privacy Filter
              </button>
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800 rounded-xl overflow-hidden">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="bg-slate-900/80 text-xs uppercase text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="px-6 py-4">Indicator</th>
                  <th className="px-6 py-4">Type</th>
                  <th className="px-6 py-4">Classification</th>
                  <th className="px-6 py-4">Confidence</th>
                  <th className="px-6 py-4">Source Reliability</th>
                  <th className="px-6 py-4">Anonymized Cohort</th>
                  <th className="px-6 py-4">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-mono text-xs">
                {[
                  {
                    ind: 'cdn-secure-verify-update.com',
                    type: 'DOMAIN',
                    cls: 'SHARED_THREAT_INTELLIGENCE',
                    conf: '92%',
                    rel: '88%',
                    cohort: 'COHORT_FINANCIAL_a7c1',
                    status: 'VALIDATED',
                  },
                  {
                    ind: '198.51.100.42',
                    type: 'IP',
                    cls: 'SHARED_THREAT_INTELLIGENCE',
                    conf: '85%',
                    rel: '90%',
                    cohort: 'COHORT_HEALTHCARE_3f2b',
                    status: 'CORRELATED',
                  },
                  {
                    ind: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
                    type: 'FILE_HASH',
                    cls: 'SHARED_THREAT_INTELLIGENCE',
                    conf: '96%',
                    rel: '95%',
                    cohort: 'COHORT_ECOMMERCE_89de',
                    status: 'VALIDATED',
                  },
                  {
                    ind: 'voice_sig_clone_wave_78912',
                    type: 'VOICE_SIGNATURE',
                    cls: 'SHARED_THREAT_INTELLIGENCE',
                    conf: '88%',
                    rel: '85%',
                    cohort: 'COHORT_FINANCIAL_a7c1',
                    status: 'VALIDATED',
                  },
                ].map((row, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/30 transition-colors">
                    <td className="px-6 py-4 font-semibold text-slate-100">{row.ind}</td>
                    <td className="px-6 py-4">
                      <span className="px-2 py-0.5 bg-slate-800 border border-slate-700 rounded text-slate-300">
                        {row.type}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="px-2 py-0.5 bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 rounded">
                        {row.cls}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-emerald-400">{row.conf}</td>
                    <td className="px-6 py-4 text-cyan-400">{row.rel}</td>
                    <td className="px-6 py-4 text-slate-400">{row.cohort}</td>
                    <td className="px-6 py-4">
                      <span className="px-2 py-0.5 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 rounded">
                        {row.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Global Campaigns Tab */}
      {activeTab === 'campaigns' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {[
            {
              id: 'gcmp_99a8',
              name: 'Operation Spectral Voice',
              conf: 0.88,
              attr: 'ATTRIBUTION_UNCONFIRMED',
              modalities: ['VOICE_CLONE', 'FINANCIAL_FRAUD', 'QR_PHISHING'],
              cohorts: ['COHORT_FINANCIAL_a7c1', 'COHORT_FINANCIAL_b8d2'],
              indicatorsCount: 14,
              expansion: true,
            },
            {
              id: 'gcmp_42f1',
              name: 'Shadow APK Banking Impersonation',
              conf: 0.94,
              attr: 'ATTRIBUTION_UNCONFIRMED',
              modalities: ['MALICIOUS_APK', 'NETWORK_INFRASTRUCTURE', 'SMS_PHISHING'],
              cohorts: ['COHORT_FINANCIAL_a7c1', 'COHORT_RETAIL_11e4'],
              indicatorsCount: 22,
              expansion: false,
            },
          ].map((camp) => (
            <div key={camp.id} className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-lg font-bold text-white">{camp.name}</h3>
                  <div className="text-xs text-slate-500 font-mono mt-0.5">{camp.id}</div>
                </div>
                <span className="px-2.5 py-1 bg-amber-500/10 border border-amber-500/30 text-amber-400 rounded-lg text-xs font-semibold">
                  {camp.attr}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="bg-slate-950 p-3 rounded-lg border border-slate-800/80">
                  <span className="text-slate-400">Confidence Score:</span>
                  <div className="text-base font-bold text-cyan-400 mt-1">{(camp.conf * 100).toFixed(0)}%</div>
                </div>
                <div className="bg-slate-950 p-3 rounded-lg border border-slate-800/80">
                  <span className="text-slate-400">Tracked Indicators:</span>
                  <div className="text-base font-bold text-white mt-1">{camp.indicatorsCount}</div>
                </div>
              </div>

              <div className="space-y-2">
                <div className="text-xs text-slate-400 font-medium">Correlated Modalities:</div>
                <div className="flex flex-wrap gap-1.5">
                  {camp.modalities.map((m) => (
                    <span key={m} className="px-2 py-0.5 bg-slate-800 border border-slate-700 text-slate-300 rounded text-xs">
                      {m}
                    </span>
                  ))}
                </div>
              </div>

              <div className="pt-2 border-t border-slate-800 flex justify-between items-center text-xs text-slate-400">
                <span>Affected Cohorts: {camp.cohorts.length}</span>
                {camp.expansion && (
                  <span className="text-red-400 font-medium flex items-center gap-1">
                    <TrendingUp className="w-3.5 h-3.5" /> Rapid Expansion Warning
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Early Warnings Tab */}
      {activeTab === 'warnings' && (
        <div className="space-y-4">
          {[
            {
              title: 'Global Early Warning: Coordinated Multi-Modal Voice Clone & QR Payment Surge',
              scope: 'GLOBAL_CROSS_TENANT',
              trigger: 'MULTI_MODAL_EXPANSION',
              conf: '88%',
              sectors: ['FINANCIAL_SERVICES', 'TELECOM', 'PAYMENT_GATEWAYS'],
              limitations: 'Attribution unconfirmed; multi-source telemetry correlation.',
            },
            {
              title: 'Global Early Warning: Reused C2 Infrastructure Across Regional Banking Applications',
              scope: 'GLOBAL_CROSS_TENANT',
              trigger: 'INFRASTRUCTURE_REUSE',
              conf: '92%',
              sectors: ['FINANCIAL_SERVICES', 'DIGITAL_BANKING'],
              limitations: 'Based on shared TLS certificate hashes and DNS patterns.',
            },
          ].map((w, idx) => (
            <div key={idx} className="bg-slate-900/60 border border-red-500/30 rounded-xl p-6 space-y-3">
              <div className="flex justify-between items-start">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-red-500/10 rounded-lg text-red-400 border border-red-500/20">
                    <AlertTriangle className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-base font-bold text-white">{w.title}</h3>
                    <div className="text-xs text-slate-400 mt-0.5">Scope: {w.scope} • Trigger: {w.trigger}</div>
                  </div>
                </div>
                <span className="px-3 py-1 bg-red-500/20 border border-red-500/40 text-red-300 rounded-lg text-xs font-bold">
                  {w.conf} Confidence
                </span>
              </div>

              <div className="flex flex-wrap gap-2 pt-2">
                <span className="text-xs text-slate-400">Targeted Sectors:</span>
                {w.sectors.map((s) => (
                  <span key={s} className="px-2 py-0.5 bg-slate-800 text-slate-300 rounded text-xs border border-slate-700">
                    {s}
                  </span>
                ))}
              </div>

              <div className="text-xs text-slate-500 italic bg-slate-950/60 p-2.5 rounded-lg border border-slate-800">
                Guardrail Notice: {w.limitations}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Threat Graph Explorer Tab */}
      {activeTab === 'graph' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Network className="w-5 h-5 text-cyan-400" />
              Global Threat Knowledge Graph
            </h3>
            <span className="text-xs text-slate-400 font-mono">
              Nodes: 124 • Edges: 382 • Anonymized Cohorts: 12
            </span>
          </div>

          <div className="h-96 bg-slate-950 border border-slate-800 rounded-xl flex items-center justify-center relative overflow-hidden">
            <div className="text-center space-y-3">
              <Network className="w-12 h-12 text-cyan-500/40 mx-auto animate-pulse" />
              <div className="text-sm text-slate-400">
                Interactive Graph Explorer Rendered (Privacy Safe • Node-Link Topology)
              </div>
              <div className="flex justify-center gap-3 text-xs">
                <span className="flex items-center gap-1 text-cyan-400">
                  <span className="w-2 h-2 rounded-full bg-cyan-400" /> Indicator Nodes
                </span>
                <span className="flex items-center gap-1 text-amber-400">
                  <span className="w-2 h-2 rounded-full bg-amber-400" /> Campaign Clusters
                </span>
                <span className="flex items-center gap-1 text-purple-400">
                  <span className="w-2 h-2 rounded-full bg-purple-400" /> Anonymized Cohorts
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Quality & Disputes Tab */}
      {activeTab === 'quality' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <FileCheck className="w-5 h-5 text-emerald-400" />
              Quality Score Dimensions
            </h3>
            <div className="space-y-3 text-xs">
              {[
                { label: 'Freshness Index', val: 96 },
                { label: 'Provenance Lineage', val: 92 },
                { label: 'Multi-Source Corroboration', val: 89 },
                { label: 'Source Reliability Average', val: 94 },
                { label: 'Validation Completeness', val: 95 },
              ].map((d) => (
                <div key={d.label} className="space-y-1">
                  <div className="flex justify-between text-slate-300">
                    <span>{d.label}</span>
                    <span className="font-bold text-emerald-400">{d.val}%</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-1.5">
                    <div className="bg-emerald-500 h-1.5 rounded-full" style={{ width: `${d.val}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <HelpCircle className="w-5 h-5 text-amber-400" />
              Intelligence Dispute Management
            </h3>
            <div className="text-xs text-slate-400">
              Tenants may submit formal disputes against false positive, outdated, or misclassified indicators.
            </div>
            <div className="p-4 bg-slate-950 rounded-lg border border-slate-800 text-xs space-y-2">
              <div className="flex justify-between items-center">
                <span className="font-semibold text-slate-200">Dispute #dsp_49a2 - api-checkout-gateway.net</span>
                <span className="px-2 py-0.5 bg-emerald-500/20 text-emerald-400 rounded">RESOLVED</span>
              </div>
              <p className="text-slate-400">
                Reason: False positive on legitimate payment partner subdomain.
              </p>
              <div className="text-slate-500 text-[10px]">
                Resolution: Indicator downgraded to BENIGN_SERVICE and removed from active defense feed.
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Federation Partners Tab */}
      {activeTab === 'partners' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl overflow-hidden">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-900/80 text-xs uppercase text-slate-400 border-b border-slate-800">
              <tr>
                <th className="px-6 py-4">Partner Network</th>
                <th className="px-6 py-4">Trust Level</th>
                <th className="px-6 py-4">Supported Formats</th>
                <th className="px-6 py-4">Rate Limit</th>
                <th className="px-6 py-4">Total Received</th>
                <th className="px-6 py-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-xs">
              {[
                { name: 'Global Cyber Alliance Node A', trust: '92%', fmt: 'STIX 2.1, JSON', rate: '200 / min', recv: '12,490', status: 'ACTIVE' },
                { name: 'Financial Sector ISAC Federation', trust: '96%', fmt: 'TAXII 2.1, JSON', rate: '500 / min', recv: '48,120', status: 'ACTIVE' },
                { name: 'Community Security Collective', trust: '78%', fmt: 'JSON Bundle', rate: '100 / min', recv: '3,210', status: 'ACTIVE' },
              ].map((p, idx) => (
                <tr key={idx} className="hover:bg-slate-800/30 transition-colors">
                  <td className="px-6 py-4 font-semibold text-slate-100">{p.name}</td>
                  <td className="px-6 py-4 text-cyan-400 font-bold">{p.trust}</td>
                  <td className="px-6 py-4 text-slate-400">{p.fmt}</td>
                  <td className="px-6 py-4 text-slate-400">{p.rate}</td>
                  <td className="px-6 py-4 text-emerald-400">{p.recv}</td>
                  <td className="px-6 py-4">
                    <span className="px-2 py-0.5 bg-emerald-500/20 text-emerald-400 rounded text-xs">
                      {p.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default CollectiveDefenseCenterPage;
