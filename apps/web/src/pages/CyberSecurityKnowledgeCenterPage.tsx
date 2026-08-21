import React, { useState, useEffect } from 'react';
import {
  Brain,
  Shield,
  Network,
  GitBranch,
  Layers,
  HelpCircle,
  AlertTriangle,
  FileText,
  Search,
  CheckCircle2,
  Sparkles,
  ArrowRight,
  Database,
  History,
  Activity,
  Compass,
} from 'lucide-react';

interface KnowledgeSummary {
  fabric_id: string;
  tenant_id: string;
  total_knowledge_objects: number;
  total_relationships: number;
  evidence_nodes_count: number;
  active_assertions_count: number;
  unresolved_contradictions_count: number;
  identified_knowledge_gaps_count: number;
  overall_quality_score: number;
  last_synthesized: string;
}

export const CyberSecurityKnowledgeCenterPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'topology' | 'evidence' | 'reasoning' | 'gaps' | 'analogs' | 'assistant'>('topology');
  const [summary, setSummary] = useState<KnowledgeSummary>({
    fabric_id: 'fabric_default_tenant',
    tenant_id: 'default_tenant',
    total_knowledge_objects: 27,
    total_relationships: 42,
    evidence_nodes_count: 18,
    active_assertions_count: 8,
    unresolved_contradictions_count: 1,
    identified_knowledge_gaps_count: 2,
    overall_quality_score: 93.8,
    last_synthesized: new Date().toISOString(),
  });

  const [aiQuery, setAiQuery] = useState('');
  const [aiResponse, setAiResponse] = useState<any>(null);
  const [isAiLoading, setIsAiLoading] = useState(false);

  const handleAskAssistant = (e: React.FormEvent) => {
    e.preventDefault();
    if (!aiQuery.trim()) return;

    setIsAiLoading(true);
    setTimeout(() => {
      if (aiQuery.toLowerCase().includes('cve') || aiQuery.toLowerCase().includes('shadow hydra') || aiQuery.toLowerCase().includes('checkout')) {
        setAiResponse({
          answer: "Checkout Service srv_checkout_production is exposed to Shadow Hydra campaign via unpatched CVE-2026-9942.",
          confidence: 0.89,
          evidence: ["ev_pcap_trace_88 (outbound C2 connection)", "ev_vuln_scan_44 (unpatched CVSS 9.8)", "ev_threat_intel_feed (MISP cluster)"],
          sources: ["TELEMETRY_ENGINE", "MISP_INTEL_FEED", "TRIVY_SCANNER"],
          contradictions: ["ev_audit_log_90 (container shutdown recorded at 14:00 UTC)"],
          unknown_areas: ["Host volatile memory core dump"],
          limitations: ["WAF was in monitor-only mode at initial observation."],
        });
      } else {
        setAiResponse({
          answer: `Synthesized knowledge fabric records for "${aiQuery}". Grounded in active assertions and verified evidence graph.`,
          confidence: 0.92,
          evidence: ["ev_pcap_trace_88", "ev_audit_log_90"],
          sources: ["KNOWLEDGE_FABRIC", "EVIDENCE_GRAPH"],
          contradictions: [],
          unknown_areas: ["Off-premise telemetry"],
          limitations: ["Reasoning strictly bound to verified tenant boundaries."],
        });
      }
      setIsAiLoading(false);
    }, 400);
  };

  return (
    <div className="min-h-screen bg-[#020617] text-slate-100 p-8 space-y-8 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-indigo-500/10 border border-indigo-500/30 rounded-xl">
              <Brain className="w-8 h-8 text-indigo-400" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white flex items-center gap-2">
                Cyber Security Knowledge Fabric
                <span className="text-xs px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                  Continuous Synthesis 2.0
                </span>
              </h1>
              <p className="text-sm text-slate-400">
                Unified security reasoning, evidence graph traversal, and institutional memory
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="bg-slate-900 border border-slate-800 rounded-lg px-4 py-2 text-right">
            <div className="text-xs text-slate-400">Knowledge Health</div>
            <div className="text-lg font-bold text-emerald-400">{summary.overall_quality_score}%</div>
          </div>
          <button className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition-all shadow-lg shadow-indigo-600/20">
            Resynthesize Fabric
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900/60 border border-slate-800/80 rounded-xl p-5 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Knowledge Objects</span>
            <Database className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-2xl font-bold text-white mt-2">{summary.total_knowledge_objects}</div>
          <div className="text-xs text-slate-500 mt-1">Across 27 standardized types</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800/80 rounded-xl p-5 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Graph Relations</span>
            <GitBranch className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold text-white mt-2">{summary.total_relationships}</div>
          <div className="text-xs text-slate-500 mt-1">With cryptographic provenance</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800/80 rounded-xl p-5 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Evidence Nodes</span>
            <Layers className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-white mt-2">{summary.evidence_nodes_count}</div>
          <div className="text-xs text-slate-500 mt-1">7-dimension strength evaluated</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800/80 rounded-xl p-5 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Contradictions</span>
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-amber-400 mt-2">{summary.unresolved_contradictions_count}</div>
          <div className="text-xs text-slate-500 mt-1">Preserved without silent deletion</div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 gap-2 overflow-x-auto pb-px">
        {[
          { id: 'topology', label: 'Knowledge Topology', icon: Network },
          { id: 'evidence', label: 'Evidence & Contradictions', icon: Layers },
          { id: 'reasoning', label: 'Security Reasoning', icon: Brain },
          { id: 'gaps', label: 'Knowledge Gaps & Questions', icon: HelpCircle },
          { id: 'analogs', label: 'Institutional Memory', icon: History },
          { id: 'assistant', label: 'AI Security Assistant', icon: Sparkles },
        ].map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-2.5 border-b-2 font-medium text-sm transition-all whitespace-nowrap ${
                activeTab === tab.id
                  ? 'border-indigo-500 text-indigo-400 bg-indigo-500/5'
                  : 'border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-700'
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Tab Panels */}
      {activeTab === 'topology' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
            <h2 className="text-lg font-semibold text-white flex items-center gap-2">
              <Network className="w-5 h-5 text-indigo-400" />
              Active Knowledge Relationships
            </h2>
            <div className="space-y-3">
              {[
                { src: 'srv_checkout_production', rel: 'HOSTS', tgt: 'svc_payment_gateway', conf: 0.98, ev: 'ev_pcap_trace_88' },
                { src: 'svc_payment_gateway', rel: 'PROTECTS', tgt: 'ctrl_waf_edge_01', conf: 0.95, ev: 'ev_config_dump_01' },
                { src: 'svc_payment_gateway', rel: 'EXPOSES', tgt: 'cve_2026_9942', conf: 0.90, ev: 'ev_vuln_scan_44' },
                { src: 'cve_2026_9942', rel: 'INDICATES', tgt: 'camp_shadow_hydra', conf: 0.85, ev: 'ev_threat_intel_feed' },
                { src: 'usr_admin_svc', rel: 'ACCESSES', tgt: 'srv_checkout_production', conf: 0.96, ev: 'ev_audit_log_90' },
              ].map((r, i) => (
                <div key={i} className="flex items-center justify-between p-3.5 bg-slate-950/70 border border-slate-800/80 rounded-lg text-sm">
                  <div className="flex items-center gap-3">
                    <span className="font-mono text-indigo-300 font-semibold">{r.src}</span>
                    <span className="text-xs px-2 py-0.5 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded font-mono">
                      {r.rel}
                    </span>
                    <span className="font-mono text-emerald-300 font-semibold">{r.tgt}</span>
                  </div>
                  <div className="flex items-center gap-4 text-xs text-slate-400">
                    <span>Evidence: <span className="font-mono text-slate-300">{r.ev}</span></span>
                    <span className="text-emerald-400 font-semibold">{Math.round(r.conf * 100)}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
            <h2 className="text-lg font-semibold text-white flex items-center gap-2">
              <Compass className="w-5 h-5 text-cyan-400" />
              Epistemic Status Hierarchy
            </h2>
            <div className="space-y-2 text-xs">
              {[
                { status: 'FACT', desc: 'Directly verified cryptographic or mathematical ground truth', color: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30' },
                { status: 'OBSERVATION', desc: 'Direct sensor or telemetry ingestion event', color: 'text-cyan-400 bg-cyan-500/10 border-cyan-500/30' },
                { status: 'EVIDENCE', desc: 'Corroborated artifact supporting an assertion', color: 'text-indigo-400 bg-indigo-500/10 border-indigo-500/30' },
                { status: 'INFERENCE', desc: 'Deductive reasoning chain derived from evidence', color: 'text-purple-400 bg-purple-500/10 border-purple-500/30' },
                { status: 'HYPOTHESIS', desc: 'Competing unverified explanation model', color: 'text-amber-400 bg-amber-500/10 border-amber-500/30' },
                { status: 'PREDICTION', desc: 'Future-state trajectory projection', color: 'text-blue-400 bg-blue-500/10 border-blue-500/30' },
                { status: 'SIMULATION', desc: 'Isolated sandbox what-if scenario result', color: 'text-orange-400 bg-orange-500/10 border-orange-500/30' },
              ].map((item, idx) => (
                <div key={idx} className={`p-2.5 rounded border ${item.color}`}>
                  <div className="font-bold">{item.status}</div>
                  <div className="text-slate-400 mt-0.5">{item.desc}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'assistant' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-6">
          <div>
            <h2 className="text-lg font-semibold text-white flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-indigo-400" />
              AI Security Knowledge Assistant
            </h2>
            <p className="text-sm text-slate-400">
              Strictly grounded question answering over verified evidence with explicit contradictions and limitations
            </p>
          </div>

          <form onSubmit={handleAskAssistant} className="flex gap-3">
            <input
              type="text"
              value={aiQuery}
              onChange={(e) => setAiQuery(e.target.value)}
              placeholder="Ask: 'Why is checkout service high risk?' or 'What are our biggest unknowns?'"
              className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
            />
            <button
              type="submit"
              disabled={isAiLoading}
              className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition-all"
            >
              {isAiLoading ? 'Synthesizing...' : 'Query Fabric'}
            </button>
          </form>

          {aiResponse && (
            <div className="p-5 bg-slate-950/80 border border-indigo-500/30 rounded-xl space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <span className="text-xs font-semibold text-indigo-400 uppercase tracking-wider">Fabric Answer</span>
                <span className="text-xs px-2 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded">
                  Confidence: {Math.round(aiResponse.confidence * 100)}%
                </span>
              </div>

              <div className="text-base text-white leading-relaxed font-medium">
                {aiResponse.answer}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs pt-2">
                <div className="space-y-1.5">
                  <span className="text-slate-400 font-semibold">Supporting Evidence:</span>
                  <ul className="list-disc list-inside space-y-1 text-slate-300 font-mono">
                    {aiResponse.evidence.map((ev: string, idx: number) => (
                      <li key={idx}>{ev}</li>
                    ))}
                  </ul>
                </div>

                <div className="space-y-1.5">
                  <span className="text-slate-400 font-semibold">Primary Sources:</span>
                  <div className="flex flex-wrap gap-1.5">
                    {aiResponse.sources.map((src: string, idx: number) => (
                      <span key={idx} className="px-2 py-0.5 bg-slate-800 text-slate-300 rounded">
                        {src}
                      </span>
                    ))}
                  </div>
                </div>

                {aiResponse.contradictions.length > 0 && (
                  <div className="space-y-1.5 md:col-span-2 p-3 bg-amber-500/10 border border-amber-500/30 rounded-lg">
                    <span className="text-amber-400 font-semibold flex items-center gap-1.5">
                      <AlertTriangle className="w-3.5 h-3.5" />
                      Recorded Contradictions:
                    </span>
                    <ul className="list-disc list-inside text-amber-200">
                      {aiResponse.contradictions.map((c: string, idx: number) => (
                        <li key={idx}>{c}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
