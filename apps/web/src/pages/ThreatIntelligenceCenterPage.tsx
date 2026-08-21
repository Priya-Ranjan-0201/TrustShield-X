import React, { useState } from 'react';
import {
  Globe,
  Shield,
  Activity,
  AlertTriangle,
  Radio,
  Share2,
  TrendingUp,
  Cpu,
  RefreshCw,
  Search,
  Eye,
  CheckCircle2,
  XCircle,
  FileText,
  Lock,
  Layers,
  ArrowUpRight,
  Filter,
  Zap,
  Server,
  Database,
  ExternalLink,
} from 'lucide-react';
import { DashboardLayout } from '../layouts/DashboardLayout';
import { toast } from '../lib/sonner';

interface ThreatIndicator {
  id: string;
  type: string;
  value: string;
  source: string;
  confidence: number;
  status: string;
  classification: string;
  threatType: string;
}

const INITIAL_IOCS: ThreatIndicator[] = [
  {
    id: 'tio_ind_c2_shadow',
    type: 'DOMAIN',
    value: 'c2.shadowhydra.net',
    source: 'CrowdStrike Falcon',
    confidence: 0.96,
    status: 'ACTIVE',
    classification: 'COMMUNITY',
    threatType: 'C2 Command & Control',
  },
  {
    id: 'tio_ind_ip_shadow',
    type: 'IP',
    value: '198.51.100.42',
    source: 'MISP Threat Exchange',
    confidence: 0.92,
    status: 'ACTIVE',
    classification: 'PUBLIC',
    threatType: 'Credential Stuffing Node',
  },
  {
    id: 'tio_ind_phish_nios',
    type: 'DOMAIN',
    value: 'nios-ac.in',
    source: 'CERT-In / PhishTank Feed',
    confidence: 0.98,
    status: 'ACTIVE',
    classification: 'PUBLIC',
    threatType: 'Authority Typosquatting / Phishing',
  },
  {
    id: 'tio_ind_phish_sbi',
    type: 'DOMAIN',
    value: 'sbi-kyc-update.com',
    source: 'OpenPhish Global',
    confidence: 0.99,
    status: 'ACTIVE',
    classification: 'COMMUNITY',
    threatType: 'Banking Credential Harvester',
  },
  {
    id: 'tio_ind_upi_scam',
    type: 'URL',
    value: 'http://claim-reward-upi.top',
    source: 'Unified Threat Engine',
    confidence: 0.95,
    status: 'ACTIVE',
    classification: 'PUBLIC',
    threatType: 'UPI PIN Debit Exploit',
  },
];

export const ThreatIntelligenceCenterPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'landscape' | 'campaigns' | 'graph' | 'feeds' | 'early_warning' | 'forecast' | 'sharing'>('landscape');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCampaign, setSelectedCampaign] = useState<string>('Operation ShadowStrike');
  const [isSyncing, setIsSyncing] = useState(false);
  const [shareInput, setShareInput] = useState('');

  const handleSyncFeeds = () => {
    setIsSyncing(true);
    setTimeout(() => {
      setIsSyncing(false);
      toast.success('Successfully synchronized 6 global threat intelligence feeds.');
    }, 900);
  };

  const handleShareIntelligence = (e: React.FormEvent) => {
    e.preventDefault();
    if (!shareInput.trim()) return;
    toast.success('Intelligence contribution sanitized (PII redacted) and submitted to Collaborative Defense Fabric.');
    setShareInput('');
  };

  const filteredIOCs = INITIAL_IOCS.filter(
    (ioc) =>
      ioc.value.toLowerCase().includes(searchQuery.toLowerCase()) ||
      ioc.threatType.toLowerCase().includes(searchQuery.toLowerCase()) ||
      ioc.source.toLowerCase().includes(searchQuery.toLowerCase()) ||
      ioc.type.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
          <div>
            <div className="flex items-center gap-3">
              <div className="p-2.5 bg-cyan-950/60 border border-cyan-500/30 rounded-xl text-cyan-400">
                <Globe className="w-6 h-6 animate-pulse" />
              </div>
              <div>
                <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
                  Cyber Threat Intelligence Fabric
                  <span className="text-xs px-2.5 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-mono font-semibold">
                    ACTIVE FUSION
                  </span>
                </h1>
                <p className="text-sm text-slate-400">
                  Global Intelligence Ingestion, Campaign Correlation, Graph Traversal &amp; Collaborative Defense
                </p>
              </div>
            </div>
          </div>

          {/* Global Feeds & Health Indicator */}
          <div className="flex items-center gap-3">
            <div className="px-3 py-1.5 bg-slate-900 border border-slate-800 rounded-lg text-xs flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
              <span className="text-slate-300 font-medium">6 Active Feeds</span>
              <span className="text-slate-500">|</span>
              <span className="text-emerald-400 font-bold">99.8% Sync Health</span>
            </div>
            <button
              onClick={handleSyncFeeds}
              disabled={isSyncing}
              className="px-3 py-1.5 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors disabled:opacity-50"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isSyncing ? 'animate-spin' : ''}`} />
              {isSyncing ? 'Syncing...' : 'Sync Feeds'}
            </button>
          </div>
        </div>

        {/* Global Indicator Search Bar */}
        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl backdrop-blur-md">
          <div className="relative">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search threat indicators, malicious domains, C2 IPs, campaign tags (e.g. 'c2.shadowhydra.net', 'nios-ac.in', 'SBI', '198.51.100.42')..."
              className="w-full pl-10 pr-4 py-2.5 bg-slate-950/80 border border-slate-800 rounded-lg text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500"
            />
          </div>

          {searchQuery && (
            <div className="mt-3 pt-3 border-t border-slate-800 space-y-2">
              <div className="flex items-center justify-between text-xs text-slate-400">
                <span>Indicator Query Matches ({filteredIOCs.length})</span>
                <span className="font-mono text-cyan-400">Search grounded across Threat Intelligence Fabric</span>
              </div>
              <div className="space-y-1.5">
                {filteredIOCs.length === 0 ? (
                  <p className="text-xs text-slate-500 p-2">No matching indicators in active high-confidence threat cache.</p>
                ) : (
                  filteredIOCs.map((ioc) => (
                    <div key={ioc.id} className="flex items-center justify-between p-2.5 bg-slate-950 border border-slate-800 rounded-lg text-xs">
                      <div className="flex items-center gap-2.5">
                        <span className="px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 font-mono text-[10px] border border-cyan-500/20 font-bold">
                          {ioc.type}
                        </span>
                        <span className="text-white font-mono font-semibold">{ioc.value}</span>
                        <span className="text-slate-400">• {ioc.threatType}</span>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="text-slate-500 text-[11px]">Source: {ioc.source}</span>
                        <span className="px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 text-[10px] border border-rose-500/20 font-bold">
                          {(ioc.confidence * 100).toFixed(0)}% Confidence
                        </span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>

        {/* Navigation Tabs */}
        <div className="flex items-center gap-2 border-b border-slate-800/80 overflow-x-auto pb-2 text-sm">
          {[
            { id: 'landscape', label: 'Global Threat Landscape', icon: Globe },
            { id: 'campaigns', label: 'Campaign Explorer', icon: Layers },
            { id: 'graph', label: 'Threat Graph', icon: Cpu },
            { id: 'early_warning', label: 'Early Warnings', icon: AlertTriangle },
            { id: 'forecast', label: 'Trajectory Forecasts', icon: TrendingUp },
            { id: 'feeds', label: 'Sources & Feed Health', icon: Radio },
            { id: 'sharing', label: 'Collaborative Sharing', icon: Share2 },
          ].map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all whitespace-nowrap ${
                  isActive
                    ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 font-semibold'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
                }`}
              >
                <Icon className="w-4 h-4" />
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Main Tab Panels */}
        {activeTab === 'landscape' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Active Campaigns */}
            <div className="lg:col-span-2 space-y-4">
              <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-base font-semibold text-white flex items-center gap-2">
                    <Layers className="w-4 h-4 text-cyan-400" />
                    Active Global Campaigns
                  </h3>
                  <span className="text-xs text-slate-400">Grounded in 42.5k normalized IOCs</span>
                </div>

                <div className="space-y-3">
                  {[
                    {
                      name: 'Operation ShadowStrike',
                      status: 'ACTIVE',
                      attribution: 'APT-CHIMERA (UNCERTAIN_NEXUS_DEV_0442)',
                      confidence: '94%',
                      iocs: 18,
                      ttps: ['T1059.001', 'T1071.001', 'T1003.001'],
                      sectors: ['Financial', 'Government Portals', 'E-Commerce'],
                      relevance: 88.5,
                    },
                    {
                      name: 'SilentPulse Lateral Ingress',
                      status: 'EXPANDING',
                      attribution: 'AP_TEMPEST_CLUSTER',
                      confidence: '89%',
                      iocs: 12,
                      ttps: ['T1190', 'T1068', 'T1566'],
                      sectors: ['Cloud Infrastructure', 'SaaS', 'Telecom'],
                      relevance: 76.0,
                    },
                    {
                      name: 'Indian Public Sector Typosquatting Grid',
                      status: 'HIGH_ALERT',
                      attribution: 'FINANCIAL_FRAUD_SYNDICATE',
                      confidence: '98%',
                      iocs: 27,
                      ttps: ['T1566.002', 'T1584.004', 'T1587.001'],
                      sectors: ['Education (NIOS/CBSE)', 'Banking (SBI)', 'UIDAI'],
                      relevance: 95.0,
                    },
                  ].map((camp, idx) => (
                    <div
                      key={idx}
                      onClick={() => {
                        setSelectedCampaign(camp.name);
                        setActiveTab('campaigns');
                      }}
                      className="p-4 bg-slate-950/70 border border-slate-800/80 rounded-lg hover:border-cyan-500/40 transition-colors cursor-pointer space-y-2"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <span className="font-semibold text-white text-sm">{camp.name}</span>
                          <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold">
                            {camp.status}
                          </span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-slate-400">Relevance:</span>
                          <span className="text-xs font-bold text-amber-400 px-2 py-0.5 rounded bg-amber-500/10 border border-amber-500/20">
                            {camp.relevance}/100
                          </span>
                        </div>
                      </div>

                      <div className="text-xs text-slate-400 flex flex-wrap items-center gap-4">
                        <span>Attribution: <strong className="text-slate-300 font-mono">{camp.attribution}</strong></span>
                        <span>Confidence: <strong className="text-cyan-400">{camp.confidence}</strong></span>
                        <span>Sectors: <strong className="text-slate-300">{camp.sectors.join(', ')}</strong></span>
                      </div>

                      <div className="flex items-center gap-1.5 pt-1">
                        {camp.ttps.map((ttp, tIdx) => (
                          <span key={tIdx} className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-300">
                            {ttp}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Local Tenant Relevance & Exposure */}
            <div className="space-y-4">
              <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
                <h3 className="text-base font-semibold text-white flex items-center gap-2">
                  <Shield className="w-4 h-4 text-emerald-400" />
                  Local Threat Context &amp; Exposure
                </h3>

                <div className="space-y-3">
                  <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg space-y-1">
                    <div className="flex justify-between text-xs">
                      <span className="text-slate-400">Technical Stack Overlap</span>
                      <span className="text-cyan-400 font-semibold">90%</span>
                    </div>
                    <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                      <div className="bg-cyan-400 h-full w-[90%]"></div>
                    </div>
                  </div>

                  <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg space-y-1">
                    <div className="flex justify-between text-xs">
                      <span className="text-slate-400">Exposed Assets Overlap</span>
                      <span className="text-amber-400 font-semibold">75%</span>
                    </div>
                    <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                      <div className="bg-amber-400 h-full w-[75%]"></div>
                    </div>
                  </div>

                  <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg">
                    <span className="text-xs text-slate-400 block mb-1">Recommended Defensive Action:</span>
                    <span className="text-xs font-semibold text-emerald-400">
                      APPLY_VIRTUAL_PATCH_AND_SIMULATE_CONTAINMENT
                    </span>
                  </div>
                </div>
              </div>

              {/* Quality Summary */}
              <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-3">
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-cyan-400" />
                  Intelligence Quality Grade
                </h3>
                <div className="flex items-center justify-between">
                  <span className="text-2xl font-bold text-cyan-400 font-mono">GRADE_A</span>
                  <span className="text-xs text-slate-400">98.0% Freshness</span>
                </div>
                <p className="text-xs text-slate-400">
                  All active indicators cross-verified with immutable provenance hashes across 6 feeds.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Campaign Explorer Tab */}
        {activeTab === 'campaigns' && (
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <Layers className="w-5 h-5 text-cyan-400" />
                  Campaign Deep Explorer: {selectedCampaign}
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Kill-chain progression, mapped IOCs, and MITRE ATT&amp;CK TTP matrix
                </p>
              </div>
              <span className="px-3 py-1 bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 rounded-lg text-xs font-mono font-bold">
                CLUSTER_ID: CMP-2026-0442
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-1">
                <span className="text-[11px] text-slate-400 uppercase font-bold">Attribution Confidence</span>
                <p className="text-xl font-bold text-cyan-400">94.2%</p>
                <span className="text-xs text-slate-500">Corroborated by 4 global sensors</span>
              </div>
              <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-1">
                <span className="text-[11px] text-slate-400 uppercase font-bold">Associated Active IOCs</span>
                <p className="text-xl font-bold text-rose-400">18 Indicators</p>
                <span className="text-xs text-slate-500">7 Domains • 5 IPs • 6 Hashes</span>
              </div>
              <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-1">
                <span className="text-[11px] text-slate-400 uppercase font-bold">Targeted Industry Sectors</span>
                <p className="text-sm font-bold text-amber-400">Financial &amp; Indian Public Portals</p>
                <span className="text-xs text-slate-500">High Typosquatting Frequency</span>
              </div>
            </div>

            <div className="space-y-3">
              <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                MITRE ATT&amp;CK Technique Coverage
              </h4>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg space-y-1">
                  <span className="font-mono font-bold text-purple-400">T1566.002 — Spearphishing Link</span>
                  <p className="text-slate-400 text-[11px]">Deceptive URLs mimicking official government &amp; banking domains.</p>
                </div>
                <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg space-y-1">
                  <span className="font-mono font-bold text-cyan-400">T1071.001 — Web Protocols C2</span>
                  <p className="text-slate-400 text-[11px]">Encrypted HTTPS beaconing over port 443 with randomized intervals.</p>
                </div>
                <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg space-y-1">
                  <span className="font-mono font-bold text-amber-400">T1003.001 — Credential Ingress</span>
                  <p className="text-slate-400 text-[11px]">Deceptive login prompts harvesting OTPs and secondary auth tokens.</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Threat Graph Visualization Tab */}
        {activeTab === 'graph' && (
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-semibold text-white flex items-center gap-2">
                <Cpu className="w-4 h-4 text-cyan-400" />
                Cyber Threat Intelligence Graph Explorer
              </h3>
              <span className="text-xs text-slate-400 font-mono">Depth: 5 Bounded Hops • 12 Active Nodes</span>
            </div>

            <div className="p-8 bg-slate-950 border border-slate-800/80 rounded-xl flex flex-col items-center justify-center space-y-6">
              <div className="flex flex-wrap items-center justify-center gap-4">
                <div className="px-4 py-2.5 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-xs font-mono font-bold">
                  [CAMPAIGN] Operation ShadowStrike
                </div>
                <span className="text-slate-600 font-mono text-xs">──USES──►</span>
                <div className="px-4 py-2.5 bg-amber-500/10 border border-amber-500/30 rounded-lg text-amber-400 text-xs font-mono font-bold">
                  [MALWARE] HydraLoader.v2
                </div>
                <span className="text-slate-600 font-mono text-xs">──RESOLVES_TO──►</span>
                <div className="px-4 py-2.5 bg-cyan-500/10 border border-cyan-500/30 rounded-lg text-cyan-400 text-xs font-mono font-bold">
                  [INFRASTRUCTURE] 198.51.100.42
                </div>
                <span className="text-slate-600 font-mono text-xs">──CONTROLS──►</span>
                <div className="px-4 py-2.5 bg-purple-500/10 border border-purple-500/30 rounded-lg text-purple-400 text-xs font-mono font-bold">
                  [C2 DOMAIN] c2.shadowhydra.net
                </div>
              </div>

              <div className="text-xs text-slate-400 bg-slate-900 px-4 py-2 rounded border border-slate-800 text-center max-w-xl">
                Graph entities resolved via continuous entity resolution, transitive neighbor correlation, and deterministic provenance validation.
              </div>
            </div>
          </div>
        )}

        {/* Early Warning Center Tab */}
        {activeTab === 'early_warning' && (
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <h3 className="text-base font-semibold text-white flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-400" />
              Threat Early Warning Center
            </h3>
            <div className="space-y-3">
              <div className="p-4 bg-amber-500/5 border border-amber-500/20 rounded-lg space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-semibold text-amber-400">Emerging Exploit Surge on Enterprise Edge Gateways</span>
                  <span className="text-xs px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/30 font-bold">
                    ACTIVE EARLY WARNING
                  </span>
                </div>
                <p className="text-xs text-slate-300">
                  Global honeypots report a 400% scan increase on port 8443 targeting ingress edge instances.
                </p>
                <div className="text-xs text-slate-400">
                  Affected Local Assets: <code className="text-slate-300 font-mono">srv_vpn_gateway_01, srv_edge_ingress</code>
                </div>
              </div>

              <div className="p-4 bg-rose-500/5 border border-rose-500/20 rounded-lg space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-semibold text-rose-400">Spike in Hyphenated Government Domain Registrations</span>
                  <span className="text-xs px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/30 font-bold">
                    CRITICAL SEVERITY
                  </span>
                </div>
                <p className="text-xs text-slate-300">
                  Automated WHOIS sensors flagged 14 new domains registered in the last 48 hours mimicking `.ac.in` and `.gov.in` educational portals.
                </p>
                <div className="text-xs text-slate-400">
                  Defensive Action: <strong className="text-emerald-400">Autonomous Domain Blacklisting &amp; Edge Filter Sync</strong>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Trajectory Forecasts Tab */}
        {activeTab === 'forecast' && (
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <h3 className="text-base font-semibold text-white flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-cyan-400" />
              Predictive Threat Trajectory Forecasts (30-Day Window)
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2">
                <div className="flex items-center justify-between font-bold">
                  <span className="text-white">AI Deepfake Audio Voice Cloning Attacks</span>
                  <span className="text-rose-400">+145% Predicted</span>
                </div>
                <p className="text-slate-400">
                  Forecast models predict a surge in CEO/Executive voice cloning targeted at enterprise procurement and wire transfer approvals.
                </p>
                <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-rose-500 h-full w-[85%]"></div>
                </div>
              </div>

              <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2">
                <div className="flex items-center justify-between font-bold">
                  <span className="text-white">QR / UPI Reverse Payment Schemes</span>
                  <span className="text-amber-400">+68% Predicted</span>
                </div>
                <p className="text-slate-400">
                  Phishing vectors increasingly utilize QR code payloads embedded with fake refund parameters and disguised merchant requests.
                </p>
                <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-amber-400 h-full w-[68%]"></div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Sources & Feed Health Tab */}
        {activeTab === 'feeds' && (
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-semibold text-white flex items-center gap-2">
                <Radio className="w-4 h-4 text-cyan-400" />
                Integrated Threat Feeds &amp; Ingestion Pipeline
              </h3>
              <span className="text-xs text-emerald-400 font-semibold flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                All 6 Feeds Operational
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
              {[
                { name: 'CrowdStrike Falcon Fusion', status: 'ONLINE', latency: '42ms', records: '14,200 IOCs' },
                { name: 'MISP Threat Exchange', status: 'ONLINE', latency: '88ms', records: '9,840 IOCs' },
                { name: 'OpenPhish Global Feed', status: 'ONLINE', latency: '65ms', records: '6,400 IOCs' },
                { name: 'PhishTank Community Feed', status: 'ONLINE', latency: '110ms', records: '8,120 IOCs' },
                { name: 'VirusTotal Multi-Engine API', status: 'ONLINE', latency: '95ms', records: '18,500 IOCs' },
                { name: 'CERT-In Public Advisory Hub', status: 'ONLINE', latency: '120ms', records: '3,200 IOCs' },
              ].map((feed, idx) => (
                <div key={idx} className="p-3.5 bg-slate-950 border border-slate-800 rounded-lg flex items-center justify-between">
                  <div className="space-y-0.5">
                    <span className="font-semibold text-white">{feed.name}</span>
                    <span className="text-[11px] text-slate-500 block">Latency: {feed.latency} • {feed.records}</span>
                  </div>
                  <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-bold">
                    {feed.status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Collaborative Sharing Tab */}
        {activeTab === 'sharing' && (
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <h3 className="text-base font-semibold text-white flex items-center gap-2">
              <Share2 className="w-4 h-4 text-cyan-400" />
              Collaborative Intelligence Sharing &amp; Automated PII Redaction
            </h3>

            <form onSubmit={handleShareIntelligence} className="space-y-3">
              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">
                  Submit Anonymized Threat Observation / Malicious Indicator:
                </label>
                <textarea
                  value={shareInput}
                  onChange={(e) => setShareInput(e.target.value)}
                  placeholder="Paste raw log snippet, phishing headers, or suspicious IOCs (all PII, Authorization tokens, and credentials will be automatically redacted before ingestion)..."
                  rows={3}
                  className="w-full p-3 bg-slate-950 border border-slate-800 rounded-lg text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
                />
              </div>
              <button
                type="submit"
                className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg text-xs font-semibold flex items-center gap-2 transition-colors"
              >
                <Lock className="w-3.5 h-3.5" />
                Sanitize &amp; Contribute to Collective Defense
              </button>
            </form>

            <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2">
              <div className="flex items-center gap-2 text-xs text-slate-400">
                <Lock className="w-4 h-4 text-emerald-400" />
                <span>Deterministic Secret &amp; PII Scrubbing Preview:</span>
              </div>
              <div className="p-3 bg-slate-900 rounded font-mono text-xs text-slate-300">
                Sample Output: <span className="text-emerald-400">Authorization: Bearer [REDACTED_SECRET]</span> | Contributor: <span className="text-cyan-400">usr_soc_analyst</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};

export default ThreatIntelligenceCenterPage;
