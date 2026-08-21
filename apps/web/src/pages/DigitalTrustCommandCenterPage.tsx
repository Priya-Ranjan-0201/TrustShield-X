import React, { useState } from 'react';
import {
  Brain,
  ShieldCheck,
  Search,
  Network,
  History,
  Bot,
  Layers,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  RefreshCw,
  FileText,
  Clock,
  ExternalLink,
  Target,
  Activity,
  GitBranch,
} from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Card } from '../components/ui/Card';
import { toast } from '../lib/sonner';

interface TrustDimension {
  name: string;
  score: number;
  description: string;
}

export const DigitalTrustCommandCenterPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'profiles' | 'investigations' | 'copilot' | 'snapshots'>('overview');
  const [searchQuery, setSearchQuery] = useState('');
  const [copilotQuery, setCopilotQuery] = useState('');
  const [copilotMessages, setCopilotMessages] = useState<Array<{
    role: 'user' | 'assistant';
    text: string;
    citations?: Array<{ type: string; id: string; snippet: string }>;
    uncertainty?: string;
    recommendation?: string;
  }>>([
    {
      role: 'assistant',
      text: 'Investigator Copilot initialized. I reason strictly over authorized TruthShield X knowledge fabric evidence and ground all answers in verifiable forensic telemetry.',
      citations: [
        { type: 'CAMPAIGN', id: 'CAMP-2026-0891', snippet: 'Coordinated Trojanized APK & Phishing C2 Campaign' },
      ],
      recommendation: 'Try asking: "Why is this domain suspicious?" or "Show me the attack chain."',
    },
  ]);

  const trustDimensions: TrustDimension[] = [
    { name: 'Identity Trust', score: 88, description: 'PKI certificate validation & publisher authenticity' },
    { name: 'Content Trust', score: 74, description: 'DEX bytecode integrity & document forgery analysis' },
    { name: 'Source Trust', score: 92, description: 'Canonical scanner reliability & threat feed credibility' },
    { name: 'Infrastructure Trust', score: 42, description: 'ASN reputation & DNS sinkhole correlation' },
    { name: 'Behavior Trust', score: 68, description: 'Runtime API abuse & network exfiltration telemetry' },
    { name: 'Evidence Trust', score: 96, description: 'Cryptographic SHA-256 evidence chain of custody' },
  ];

  const handleCopilotSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!copilotQuery.trim()) return;

    const q = copilotQuery.trim();
    const userMsg = { role: 'user' as const, text: q };
    let replyText = 'Knowledge fabric retrieved 3 correlated evidence records matching your inquiry.';
    let citations: Array<{ type: string; id: string; snippet: string }> = [];
    let uncertainty: string | undefined = undefined;
    let rec: string | undefined = undefined;

    if (q.toLowerCase().includes('why') || q.toLowerCase().includes('suspicious')) {
      replyText = 'Domain secure-verification-hdfc-portal.net was classified as HIGH RISK (92.4/100) due to verified SMS OTP stealer DEX payload linkage and spoofed UPI merchant gateway.';
      citations = [
        { type: 'EVIDENCE', id: 'EVID_APK_DEX_01', snippet: 'Trojanized APK DEX bytecode matches SMS sniffer' },
        { type: 'CAMPAIGN', id: 'CAMP-2026-0891', snippet: 'Active multi-vector credential harvesting campaign' },
      ];
      rec = 'Execute dry-run simulation and request Four-Eyes DNS sinkhole authorization.';
    } else if (q.toLowerCase().includes('attack') || q.toLowerCase().includes('chain')) {
      replyText = 'Reconstructed attack chain: Initial WhatsApp APK drop → SMS interception background service → C2 Domain resolution → UPI Payment diversion.';
      citations = [
        { type: 'INCIDENT', id: 'INC-2026-0891', snippet: 'Multi-modal banking scam incident' },
      ];
      rec = 'Review attack story stages in the Investigation Workspace.';
    } else if (q.toLowerCase().includes('unknown') || q.toLowerCase().includes('actor')) {
      replyText = 'Threat actor attribution cannot be established from current cryptographic evidence. Operator identity remains unverified.';
      uncertainty = 'Attribution cannot be established without additional ISP-level routing telemetry.';
      rec = 'Pivot on ASN sibling domain infrastructure to identify staging servers.';
    }

    setCopilotMessages((prev) => [
      ...prev,
      userMsg,
      { role: 'assistant', text: replyText, citations, uncertainty, recommendation: rec },
    ]);
    setCopilotQuery('');
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold tracking-tight text-slate-100 flex items-center gap-2">
              <Brain className="h-8 w-8 text-cyan-400" />
              Digital Trust Command Center
            </h1>
            <Badge variant="info" className="bg-cyan-950/60 text-cyan-400 border border-cyan-800">
              PHASE 7 REASONING FABRIC ACTIVE
            </Badge>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Grounded security reasoning, evidence provenance graph, multi-dimensional digital trust scoring &amp; investigator copilot.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="secondary" className="border-slate-700 bg-slate-900">
            <History className="h-4 w-4 mr-2" />
            Snapshot History
          </Button>
          <Button variant="primary" className="bg-cyan-600 hover:bg-cyan-500 text-white shadow-lg shadow-cyan-950/50">
            <Sparkles className="h-4 w-4 mr-2" />
            New Investigation
          </Button>
        </div>
      </div>

      {/* Top Metric Tiles */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-5 bg-slate-900/60 border-slate-800 backdrop-blur-md">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Overall Trust Score</span>
            <ShieldCheck className="h-5 w-5 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold text-cyan-400 mt-2">76.8 / 100</div>
          <div className="text-xs text-slate-400 mt-1">Status: MODERATELY_TRUSTED</div>
        </Card>

        <Card className="p-5 bg-slate-900/60 border-slate-800 backdrop-blur-md">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Knowledge Objects</span>
            <Layers className="h-5 w-5 text-indigo-400" />
          </div>
          <div className="text-2xl font-bold text-slate-100 mt-2">1,482 Objects</div>
          <div className="text-xs text-indigo-400 mt-1">Across 3,120 Relationships</div>
        </Card>

        <Card className="p-5 bg-slate-900/60 border-slate-800 backdrop-blur-md">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Active Investigations</span>
            <Target className="h-5 w-5 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-amber-400 mt-2">3 In Progress</div>
          <div className="text-xs text-slate-400 mt-1">1 Campaign Link Identified</div>
        </Card>

        <Card className="p-5 bg-slate-900/60 border-slate-800 backdrop-blur-md">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Reasoning Precision</span>
            <CheckCircle2 className="h-5 w-5 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-emerald-400 mt-2">99.4%</div>
          <div className="text-xs text-slate-400 mt-1">Zero Hallucination Verified</div>
        </Card>
      </div>

      {/* Tabs Navigation */}
      <div className="flex gap-2 border-b border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab('overview')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
            activeTab === 'overview' ? 'bg-cyan-950/60 text-cyan-400 border border-cyan-800/80' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Knowledge Fabric &amp; Search
        </button>
        <button
          onClick={() => setActiveTab('profiles')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
            activeTab === 'profiles' ? 'bg-cyan-950/60 text-cyan-400 border border-cyan-800/80' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Digital Trust Profiles
        </button>
        <button
          onClick={() => setActiveTab('investigations')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
            activeTab === 'investigations' ? 'bg-cyan-950/60 text-cyan-400 border border-cyan-800/80' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Investigation Workspaces
        </button>
        <button
          onClick={() => setActiveTab('copilot')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors flex items-center gap-1.5 ${
            activeTab === 'copilot' ? 'bg-cyan-950/60 text-cyan-400 border border-cyan-800/80' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Bot className="h-4 w-4" />
          Investigator Copilot
        </button>
        <button
          onClick={() => setActiveTab('snapshots')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
            activeTab === 'snapshots' ? 'bg-cyan-950/60 text-cyan-400 border border-cyan-800/80' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Snapshots &amp; Diffs
        </button>
      </div>

      {/* Tab Content: Knowledge Fabric & Search */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          <Card className="p-6 bg-slate-900/50 border-slate-800 space-y-4">
            <div className="flex items-center gap-3">
              <Search className="h-5 w-5 text-cyan-400" />
              <input
                type="text"
                placeholder="Search across entities, evidence, incidents, campaigns, predictions, and reports..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-100 focus:outline-none focus:border-cyan-500"
              />
              <Button variant="primary" className="bg-cyan-600 hover:bg-cyan-500 text-white">
                Query Fabric
              </Button>
            </div>
          </Card>

          {/* Sample Knowledge Objects */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card className="p-5 bg-slate-900/40 border-slate-800 space-y-3">
              <div className="flex items-center justify-between">
                <Badge variant="info">ENTITY: DOMAIN</Badge>
                <span className="text-xs text-slate-400 font-mono">Confidence: 94%</span>
              </div>
              <div className="text-base font-semibold text-slate-200 font-mono">secure-verification-hdfc-portal.net</div>
              <p className="text-xs text-slate-400">
                Correlated with Campaign <span className="text-cyan-400 font-mono">CAMP-2026-0891</span> and DEX SMS Payload.
              </p>
              <div className="flex items-center justify-between pt-2 border-t border-slate-800/60 text-xs text-slate-400">
                <span>Provenance: DEX Static Analyzer</span>
                <span className="text-cyan-400 hover:underline cursor-pointer flex items-center gap-1">
                  View Lineage <ArrowRight className="h-3 w-3" />
                </span>
              </div>
            </Card>

            <Card className="p-5 bg-slate-900/40 border-slate-800 space-y-3">
              <div className="flex items-center justify-between">
                <Badge variant="warning">EVIDENCE: CODE_SIGNATURE</Badge>
                <span className="text-xs text-slate-400 font-mono">Confidence: 98%</span>
              </div>
              <div className="text-base font-semibold text-slate-200 font-mono">APK Certificate SHA256: 8a4b...f012</div>
              <p className="text-xs text-slate-400">
                Self-signed debug certificate reused across 3 malicious APK dropper packages.
              </p>
              <div className="flex items-center justify-between pt-2 border-t border-slate-800/60 text-xs text-slate-400">
                <span>Provenance: APK Crypto Verifier</span>
                <span className="text-cyan-400 hover:underline cursor-pointer flex items-center gap-1">
                  View Lineage <ArrowRight className="h-3 w-3" />
                </span>
              </div>
            </Card>
          </div>
        </div>
      )}

      {/* Tab Content: Trust Profiles */}
      {activeTab === 'profiles' && (
        <div className="space-y-6">
          <Card className="p-6 bg-slate-900/50 border-slate-800 space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
              <div>
                <h3 className="text-lg font-semibold text-slate-100">Digital Trust Profile — Domain: secure-verification-hdfc-portal.net</h3>
                <p className="text-xs text-slate-400 mt-1">Multi-dimensional empirical trustworthiness assessment.</p>
              </div>
              <Badge variant="danger" className="bg-rose-950/60 text-rose-400 border border-rose-800">
                OVERALL TRUST: 32.5 / 100 (LOW)
              </Badge>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {trustDimensions.map((dim) => (
                <div key={dim.name} className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-semibold text-slate-200">{dim.name}</span>
                    <span className={`text-sm font-bold font-mono ${dim.score >= 70 ? 'text-emerald-400' : dim.score >= 50 ? 'text-amber-400' : 'text-rose-400'}`}>
                      {dim.score} / 100
                    </span>
                  </div>
                  <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                    <div
                      className={`h-full ${dim.score >= 70 ? 'bg-emerald-500' : dim.score >= 50 ? 'bg-amber-500' : 'bg-rose-500'}`}
                      style={{ width: `${dim.score}%` }}
                    />
                  </div>
                  <p className="text-xs text-slate-400">{dim.description}</p>
                </div>
              ))}
            </div>

            {/* Trust History Transition Log */}
            <div className="space-y-3 pt-4 border-t border-slate-800">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400">Trust Score Transition History</h4>
              <div className="space-y-2">
                <div className="p-3 bg-slate-950/40 border border-slate-800/80 rounded-lg flex items-center justify-between text-xs">
                  <div className="flex items-center gap-3">
                    <Clock className="h-4 w-4 text-slate-400" />
                    <span className="text-rose-400 font-bold font-mono">82.0 → 32.5</span>
                    <span className="text-slate-300">Reason: New verified phishing evidence and DEX Trojan linkage</span>
                  </div>
                  <span className="text-slate-400">2026-08-14 10:15:00 UTC</span>
                </div>
              </div>
            </div>
          </Card>
        </div>
      )}

      {/* Tab Content: Investigator Copilot */}
      {activeTab === 'copilot' && (
        <Card className="p-6 bg-slate-900/50 border-slate-800 space-y-4">
          <div className="flex items-center gap-3 border-b border-slate-800 pb-4">
            <Bot className="h-6 w-6 text-cyan-400" />
            <div>
              <h3 className="text-base font-semibold text-slate-100">Investigator Copilot</h3>
              <p className="text-xs text-slate-400">Evidence-grounded natural language security reasoning &amp; citation engine.</p>
            </div>
          </div>

          {/* Conversation history */}
          <div className="space-y-4 max-h-96 overflow-y-auto pr-2">
            {copilotMessages.map((msg, idx) => (
              <div
                key={idx}
                className={`p-4 rounded-xl text-sm space-y-3 ${
                  msg.role === 'assistant'
                    ? 'bg-slate-950/80 border border-slate-800 text-slate-200'
                    : 'bg-cyan-950/40 border border-cyan-800/60 text-cyan-100 ml-8'
                }`}
              >
                <div className="font-semibold text-xs text-slate-400 uppercase tracking-wider">
                  {msg.role === 'assistant' ? '🤖 Investigator Copilot' : '👤 Security Analyst'}
                </div>
                <div>{msg.text}</div>

                {/* Citations */}
                {msg.citations && msg.citations.length > 0 && (
                  <div className="space-y-1.5 pt-2 border-t border-slate-800/80">
                    <div className="text-xs font-semibold text-cyan-400 uppercase tracking-wider">Evidence Citations:</div>
                    <div className="flex flex-wrap gap-2">
                      {msg.citations.map((c, i) => (
                        <div
                          key={i}
                          onClick={() => toast.info(`Viewing citation ${c.id}: ${c.snippet}`)}
                          className="px-2.5 py-1 bg-cyan-950/60 border border-cyan-800 rounded text-xs font-mono text-cyan-300 hover:bg-cyan-900/60 cursor-pointer flex items-center gap-1"
                        >
                          <ExternalLink className="h-3 w-3" />
                          [{c.type}: {c.id}]
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Uncertainty */}
                {msg.uncertainty && (
                  <div className="text-xs text-amber-400 bg-amber-950/40 p-2.5 rounded border border-amber-900/60 flex items-center gap-2">
                    <AlertTriangle className="h-4 w-4 flex-shrink-0" />
                    <span><strong>Uncertainty:</strong> {msg.uncertainty}</span>
                  </div>
                )}

                {/* Recommendation */}
                {msg.recommendation && (
                  <div className="text-xs text-emerald-400 bg-emerald-950/40 p-2.5 rounded border border-emerald-900/60">
                    💡 <strong>Recommended Next Step:</strong> {msg.recommendation}
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Form */}
          <form onSubmit={handleCopilotSubmit} className="flex gap-2 pt-2 border-t border-slate-800">
            <input
              type="text"
              value={copilotQuery}
              onChange={(e) => setCopilotQuery(e.target.value)}
              placeholder="Ask Copilot (e.g. 'Why is this domain suspicious?' or 'Show me the attack chain')..."
              className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-100 focus:outline-none focus:border-cyan-500"
            />
            <Button type="submit" variant="primary" className="bg-cyan-600 hover:bg-cyan-500 text-white">
              <ArrowRight className="h-4 w-4" />
            </Button>
          </form>
        </Card>
      )}

      {/* Tab Content: Investigations & Attack Stories */}
      {activeTab === 'investigations' && (
        <Card className="p-6 bg-slate-900/50 border-slate-800 space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <h3 className="text-base font-semibold text-slate-100">Attack Narrative &amp; Reconstructed Timeline</h3>
              <p className="text-xs text-slate-400">Zero-hallucination attack story: explicit gap declarations on missing intervals.</p>
            </div>
            <Button size="sm" variant="secondary" className="bg-slate-800 text-slate-200">
              <FileText className="h-3.5 w-3.5 mr-1" />
              Generate Case Brief
            </Button>
          </div>

          <div className="relative pl-6 border-l border-slate-800 space-y-6">
            <div className="relative">
              <div className="absolute -left-[31px] top-1.5 h-3 w-3 rounded-full bg-cyan-400 ring-4 ring-slate-900" />
              <div className="text-xs font-semibold text-cyan-400 uppercase">Stage 1: Initial Observation (2026-08-14 09:00 UTC)</div>
              <p className="text-sm text-slate-200 mt-1">Suspicious APK package uploaded containing unmapped SMS background receivers.</p>
              <span className="text-xs text-slate-400 font-mono">[Evidence: EVID_APK_DEX_01]</span>
            </div>

            <div className="relative">
              <div className="absolute -left-[31px] top-1.5 h-3 w-3 rounded-full bg-indigo-400 ring-4 ring-slate-900" />
              <div className="text-xs font-semibold text-indigo-400 uppercase">Stage 2: Correlation &amp; Campaign Discovery</div>
              <p className="text-sm text-slate-200 mt-1">Unified Intelligence Graph linked APK C2 endpoint to active campaign CAMP-2026-0891.</p>
              <span className="text-xs text-slate-400 font-mono">[Campaign: CAMP-2026-0891]</span>
            </div>

            <div className="relative">
              <div className="absolute -left-[31px] top-1.5 h-3 w-3 rounded-full bg-emerald-400 ring-4 ring-slate-900" />
              <div className="text-xs font-semibold text-emerald-400 uppercase">Stage 3: Response &amp; Empirical Verification</div>
              <p className="text-sm text-slate-200 mt-1">Four-Eyes approved DNS sinkhole applied and verified within 4.2s.</p>
              <span className="text-xs text-slate-400 font-mono">[Action: PACT_01 • State: VERIFIED]</span>
            </div>
          </div>
        </Card>
      )}

      {/* Tab Content: Snapshots & Diffs */}
      {activeTab === 'snapshots' && (
        <Card className="p-6 bg-slate-900/50 border-slate-800 space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <h3 className="text-base font-semibold text-slate-100">Knowledge Snapshots &amp; Diff Engine</h3>
              <p className="text-xs text-slate-400">Point-in-time historical reconstruction: "What did TruthShield know then vs now?"</p>
            </div>
            <Button size="sm" variant="primary" className="bg-cyan-600 hover:bg-cyan-500 text-white">
              <GitBranch className="h-3.5 w-3.5 mr-1" />
              Capture Snapshot
            </Button>
          </div>

          <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl space-y-3">
            <div className="text-sm font-semibold text-slate-200">Knowledge Diff: Snapshot Aug 10 vs Snapshot Aug 14</div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs text-slate-300">
              <div className="p-3 bg-slate-900/60 rounded border border-slate-800">
                <span className="text-emerald-400 font-bold">+2 New Evidence Artifacts</span>
                <p className="text-slate-400 mt-1">DEX Trojan Payload &amp; Spoofed VPA</p>
              </div>
              <div className="p-3 bg-slate-900/60 rounded border border-slate-800">
                <span className="text-amber-400 font-bold">1 Campaign Escalation</span>
                <p className="text-slate-400 mt-1">Risk escalated from 65.0 to 92.4</p>
              </div>
              <div className="p-3 bg-slate-900/60 rounded border border-slate-800">
                <span className="text-cyan-400 font-bold">4 New Relationships</span>
                <p className="text-slate-400 mt-1">Linked C2 server to UPI handle</p>
              </div>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
};
