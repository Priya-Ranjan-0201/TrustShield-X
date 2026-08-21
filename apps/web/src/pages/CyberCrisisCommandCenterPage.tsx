import React, { useState } from 'react';
import {
  ShieldAlert, AlertOctagon, Activity, Clock, Layers,
  Compass, Radio, Zap, Users, CheckCircle2, XCircle,
  FileText, Send, Sparkles, Sliders, Eye, RefreshCw,
  Terminal, ShieldCheck, ChevronRight, Check, MessageSquare,
  AlertTriangle, Lock, Shield, Cpu, Play
} from 'lucide-react';

export const CyberCrisisCommandCenterPage: React.FC = () => {
  type CrisisTab =
    | 'status_severity'
    | 'situational_awareness'
    | 'incident_timeline'
    | 'evidence_graph'
    | 'affected_assets'
    | 'blast_radius'
    | 'threat_intelligence'
    | 'decision_board'
    | 'what_if_preview'
    | 'autonomous_defense'
    | 'recovery_board'
    | 'communications'
    | 'escalation_sla'
    | 'copilot_chat'
    | 'executive_briefing';

  const [activeTab, setActiveTab] = useState<CrisisTab>('status_severity');
  const [copilotQuery, setCopilotQuery] = useState('');
  const [copilotMode, setCopilotMode] = useState('SOC_ANALYST');
  const [copilotResponses, setCopilotResponses] = useState<Array<{
    query: string;
    answer: string;
    confidence: string;
    sources: string[];
    timestamp: string;
  }>>([
    {
      query: 'What is the current containment status on API-GATEWAY-PROD?',
      answer: 'Analysis: Microsegmentation boundary active. Zero unencrypted egress packets detected. APT29 lateral attempt blocked at step 2.',
      confidence: 'HIGH_CONFIDENCE',
      sources: ['EDR Real-time Probe', 'Cyber Digital Twin State Diff'],
      timestamp: '11:42:08 UTC'
    }
  ]);

  const [queryingCopilot, setQueryingCopilot] = useState(false);

  const handleSendCopilotQuery = async () => {
    if (!copilotQuery.trim()) return;
    setQueryingCopilot(true);
    const q = copilotQuery;
    setCopilotQuery('');
    try {
      await new Promise(r => setTimeout(r, 450));
      let answer = `Analysis for ${copilotMode}:\n- Verified: Ingress boundary quarantined.\n- Evidence: 12 correlated telemetry events.\n- Recommendation: Proceed with Option A response.`;
      let confidence = 'HIGH_CONFIDENCE';
      let sources = ['TruthShield Evidence Graph', 'Digital Twin Replica'];

      if (q.toLowerCase().includes('root cause')) {
        answer = 'Root cause analysis has not established a definitive origin. Forensics investigation is ongoing (ROOT_CAUSE_NOT_ESTABLISHED).';
        confidence = 'NOT_VERIFIED';
        sources = ['Forensics Memory Analysis'];
      }

      setCopilotResponses(prev => [
        ...prev,
        {
          query: q,
          answer,
          confidence,
          sources,
          timestamp: new Date().toISOString().substring(11, 19) + ' UTC'
        }
      ]);
    } finally {
      setQueryingCopilot(false);
    }
  };

  const navItems: { id: CrisisTab; label: string; icon: React.ReactNode; badge?: string }[] = [
    { id: 'status_severity', label: 'CRISIS STATUS & SEVERITY', icon: <ShieldAlert className="h-4 w-4" /> },
    { id: 'situational_awareness', label: 'SITUATIONAL AWARENESS', icon: <Activity className="h-4 w-4" /> },
    { id: 'incident_timeline', label: 'INCIDENT TIMELINE', icon: <Clock className="h-4 w-4" /> },
    { id: 'evidence_graph', label: 'EVIDENCE GRAPH', icon: <Layers className="h-4 w-4" /> },
    { id: 'affected_assets', label: 'AFFECTED ASSETS', icon: <Cpu className="h-4 w-4" />, badge: '3' },
    { id: 'blast_radius', label: 'BLAST RADIUS & IMPACT', icon: <AlertOctagon className="h-4 w-4" /> },
    { id: 'threat_intelligence', label: 'THREAT INTEL & PATHS', icon: <Compass className="h-4 w-4" /> },
    { id: 'decision_board', label: 'DECISION BOARD', icon: <Sliders className="h-4 w-4" />, badge: '1' },
    { id: 'what_if_preview', label: 'WHAT-IF PREVIEW', icon: <Play className="h-4 w-4" /> },
    { id: 'autonomous_defense', label: 'AUTONOMOUS DEFENSE', icon: <Zap className="h-4 w-4" /> },
    { id: 'recovery_board', label: 'RECOVERY & VERIFICATION', icon: <CheckCircle2 className="h-4 w-4" /> },
    { id: 'communications', label: 'COMMUNICATIONS & FACTS', icon: <FileText className="h-4 w-4" /> },
    { id: 'escalation_sla', label: 'ESCALATION & SLA', icon: <Radio className="h-4 w-4" /> },
    { id: 'copilot_chat', label: 'AI SECURITY COPILOT', icon: <Sparkles className="h-4 w-4" />, badge: '9 Modes' },
    { id: 'executive_briefing', label: 'EXECUTIVE BRIEFING', icon: <Users className="h-4 w-4" /> }
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 lg:p-8 space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-rose-500/10 border border-rose-500/30 rounded-xl">
            <ShieldAlert className="h-8 w-8 text-rose-500 animate-pulse" />
          </div>
          <div>
            <h1 className="text-2xl lg:text-3xl font-extrabold tracking-tight text-white flex items-center gap-3">
              Cyber Crisis Command Center
              <span className="text-xs bg-rose-950 text-rose-300 border border-rose-700/60 px-2.5 py-0.5 rounded-full font-mono font-bold">
                SEV_1 ACTIVE CRISIS
              </span>
            </h1>
            <p className="text-sm text-slate-400 mt-0.5">
              Unified Incident Command, Evidence-Grounded Decision Intelligence, Digital Twin What-If & Governed AI Security Copilot
            </p>
          </div>
        </div>

        <div className="flex items-center gap-4 bg-slate-900/90 border border-slate-800 rounded-xl px-4 py-2.5 shadow-xl shadow-black/50">
          <div className="text-right">
            <div className="text-[11px] text-slate-400 font-medium">Incident Commander</div>
            <div className="text-sm font-bold text-rose-400 font-mono">SECOPS-COMMANDER-01</div>
          </div>
          <div className="h-8 w-[1px] bg-slate-800" />
          <span className="text-xs bg-rose-950 text-rose-300 border border-rose-800 px-2.5 py-1 rounded font-mono font-bold">
            CONTAINMENT PHASE
          </span>
        </div>
      </div>

      {/* KPI Banner */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-5">
        <div className="bg-slate-900/70 border border-slate-800 p-5 rounded-xl backdrop-blur-sm">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Active Crisis Severity</span>
            <AlertOctagon className="h-4 w-4 text-rose-400" />
          </div>
          <div className="text-3xl font-extrabold text-rose-400">SEV_1 <span className="text-xs text-slate-400 font-normal">Critical</span></div>
          <div className="text-xs text-rose-300 mt-2 font-medium">Multi-vector lateral intrusion attempt</div>
        </div>

        <div className="bg-slate-900/70 border border-slate-800 p-5 rounded-xl backdrop-blur-sm">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Containment SLA Remaining</span>
            <Clock className="h-4 w-4 text-amber-400" />
          </div>
          <div className="text-3xl font-extrabold text-amber-400">38m <span className="text-xs text-slate-400 font-normal">/ 60m</span></div>
          <div className="text-xs text-emerald-400 mt-2 font-medium flex items-center gap-1">
            <CheckCircle2 className="h-3.5 w-3.5" /> Healthy SLA Horizon
          </div>
        </div>

        <div className="bg-slate-900/70 border border-slate-800 p-5 rounded-xl backdrop-blur-sm">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Evidence Graph Nodes</span>
            <Layers className="h-4 w-4 text-cyan-400" />
          </div>
          <div className="text-3xl font-extrabold text-cyan-400">48 <span className="text-xs text-slate-400 font-normal">Correlated</span></div>
          <div className="text-xs text-cyan-300 mt-2 font-medium">100% Chain-of-Custody Verified</div>
        </div>

        <div className="bg-slate-900/70 border border-slate-800 p-5 rounded-xl backdrop-blur-sm">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Four-Eyes Response Decision</span>
            <Sliders className="h-4 w-4 text-indigo-400" />
          </div>
          <div className="text-3xl font-extrabold text-indigo-400">Option A <span className="text-xs text-slate-400 font-normal">Recommended</span></div>
          <div className="text-xs text-indigo-300 mt-2 font-medium">Pareto Optimal (-6.2 Risk)</div>
        </div>
      </div>

      {/* Navigation (15 Tabs) */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-2 border-b border-slate-800 scrollbar-thin scrollbar-thumb-slate-800">
        {navItems.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-3.5 py-2 font-medium text-xs rounded-lg transition-all flex items-center gap-2 whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-rose-600/20 text-rose-300 border border-rose-500/50 shadow-sm'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/80 border border-transparent'
            }`}
          >
            {tab.icon}
            {tab.label}
            {tab.badge && (
              <span className="text-[10px] bg-slate-800 text-slate-300 px-1.5 py-0.2 rounded-full font-mono">
                {tab.badge}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Tab 1: CRISIS STATUS & SEVERITY */}
      {activeTab === 'status_severity' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <ShieldAlert className="h-5 w-5 text-rose-500" /> Active Cyber Crisis Declaration Record
              </h2>
              <div className="bg-slate-950 border border-slate-800 p-4 rounded-lg space-y-2 text-xs font-mono">
                <div className="flex justify-between">
                  <span className="text-slate-400">Crisis Identifier:</span>
                  <span className="text-rose-400 font-bold">CRISIS-20260821-01</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Associated Incidents:</span>
                  <span className="text-slate-200">INC-1042, INC-1043, INC-1044</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Declared By:</span>
                  <span className="text-indigo-300">SECOPS-COMMANDER-01 (CISO Delegation)</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Declaration Reason:</span>
                  <span className="text-slate-200">Multi-vector lateral intrusion attempt on API Gateway & Auth Service</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Lifecycle State:</span>
                  <span className="text-amber-400 font-bold">CONTAINMENT</span>
                </div>
              </div>
            </div>

            {/* Command Structure Hierarchy */}
            <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <Users className="h-5 w-5 text-indigo-400" /> Incident Command Structure (12 Standard Roles)
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {[
                  { role: 'INCIDENT_COMMANDER', user: 'SECOPS-COMMANDER-01', status: 'ACTIVE' },
                  { role: 'SECURITY_LEAD', user: 'lead-secops@truthshield.io', status: 'ACTIVE' },
                  { role: 'SOC_LEAD', user: 'soc-manager@truthshield.io', status: 'ACTIVE' },
                  { role: 'FORENSICS_LEAD', user: 'forensics-lead@truthshield.io', status: 'ACTIVE' },
                  { role: 'IT_OPERATIONS', user: 'devops-lead@truthshield.io', status: 'ACTIVE' },
                  { role: 'COMMUNICATIONS', user: 'comms-head@truthshield.io', status: 'ACTIVE' }
                ].map((r, idx) => (
                  <div key={idx} className="bg-slate-950 border border-slate-800 p-3 rounded-lg flex items-center justify-between text-xs">
                    <div>
                      <div className="font-bold text-slate-200">{r.role}</div>
                      <div className="text-slate-400 font-mono mt-0.5">{r.user}</div>
                    </div>
                    <span className="bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded font-mono font-bold text-[10px]">
                      {r.status}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <Activity className="h-5 w-5 text-amber-400" /> 7D Crisis Risk Quantification
              </h2>
              <div className="space-y-2.5 text-xs font-mono">
                {[
                  { dim: 'Threat Score', val: '8.5 / 10', color: 'text-rose-400' },
                  { dim: 'Exposure Score', val: '7.0 / 10', color: 'text-amber-400' },
                  { dim: 'Asset Criticality', val: '9.0 / 10', color: 'text-rose-400' },
                  { dim: 'Business Impact', val: '6.5 / 10', color: 'text-amber-400' },
                  { dim: 'Control Failure Score', val: '3.0 / 10', color: 'text-emerald-400' },
                  { dim: 'Confidence Score', val: '92%', color: 'text-cyan-400' },
                  { dim: 'Uncertainty Score', val: '8%', color: 'text-slate-400' }
                ].map((k, idx) => (
                  <div key={idx} className="flex justify-between border-b border-slate-800/80 pb-1.5">
                    <span className="text-slate-400">{k.dim}:</span>
                    <span className={`font-bold ${k.color}`}>{k.val}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 8: DECISION BOARD */}
      {activeTab === 'decision_board' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <Sliders className="h-5 w-5 text-indigo-400" /> Crisis Response Option Analysis &amp; Decision Board
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Multi-objective comparative evaluation grounded in Digital Twin what-if simulations.
              </p>
            </div>
            <span className="text-xs bg-indigo-950 text-indigo-300 border border-indigo-800 px-3 py-1 rounded font-mono">
              IMMUTABLE DECISION LOG
            </span>
          </div>

          <div className="space-y-4">
            {[
              {
                id: 'OPT-A',
                title: 'Option A: Granular Microsegmentation Rule + Step-Up MFA',
                drop: '-6.2 / 10 Risk',
                paths: '4 Eliminated',
                impact: 'LOW (Zero Service Outage)',
                cost: 'LOW',
                rev: 'HIGH (Immediate Revert)',
                auth: 'SECOPS_COMMANDER',
                status: 'RECOMMENDED (Pareto Optimal)',
                border: 'border-emerald-700/60 bg-emerald-950/20'
              },
              {
                id: 'OPT-B',
                title: 'Option B: Complete Target Subnet Isolation & Node Re-Image',
                drop: '-7.5 / 10 Risk',
                paths: '5 Eliminated',
                impact: 'HIGH (30m Subnet Downtime)',
                cost: 'HIGH',
                rev: 'LOW (Destructive Rebuild)',
                auth: 'EXECUTIVE_CRISIS_BOARD',
                status: 'HIGH BLAST RADIUS',
                border: 'border-slate-800 bg-slate-950'
              },
              {
                id: 'OPT-C',
                title: 'Option C: Passive EDR Ingress Triage & Monitoring Only',
                drop: '-1.5 / 10 Risk',
                paths: '0 Eliminated',
                impact: 'NONE',
                cost: 'MINIMAL',
                rev: 'HIGH',
                auth: 'TIER_2_ANALYST',
                status: 'INSUFFICIENT CONTAINMENT',
                border: 'border-slate-800 bg-slate-950'
              }
            ].map((opt, idx) => (
              <div key={idx} className={`border p-5 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-4 ${opt.border}`}>
                <div>
                  <div className="text-sm font-bold text-white flex items-center gap-2 font-mono">
                    <span className="text-indigo-400">{opt.id}:</span> {opt.title}
                  </div>
                  <div className="text-xs text-slate-300 mt-2 grid grid-cols-2 md:grid-cols-4 gap-2 font-mono">
                    <div>Risk: <span className="text-emerald-400 font-bold">{opt.drop}</span></div>
                    <div>Attack Paths: <span className="text-cyan-400 font-bold">{opt.paths}</span></div>
                    <div>Impact: <span className="text-slate-300">{opt.impact}</span></div>
                    <div>Approval: <span className="text-indigo-300">{opt.auth}</span></div>
                  </div>
                </div>
                <div className="flex items-center gap-3 self-start md:self-auto">
                  <span className="text-xs font-mono font-bold px-2.5 py-1 rounded border border-emerald-800 bg-emerald-950 text-emerald-300">
                    {opt.status}
                  </span>
                  {opt.id === 'OPT-A' && (
                    <button className="text-xs bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded font-semibold transition-colors flex items-center gap-1">
                      <Check className="h-3.5 w-3.5" /> Execute Option A
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 14: AI SECURITY COPILOT CHAT */}
      {activeTab === 'copilot_chat' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-6">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            <div>
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-indigo-400" /> Evidence-Grounded AI Security Copilot
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Permission-aware security intelligence assistant operating with strict anti-hallucination guardrails.
              </p>
            </div>
            <div className="flex items-center gap-2">
              <label className="text-xs text-slate-400 font-medium">Copilot Mode:</label>
              <select
                value={copilotMode}
                onChange={(e) => setCopilotMode(e.target.value)}
                className="bg-slate-950 border border-slate-700 text-indigo-300 rounded-lg px-3 py-1.5 text-xs font-mono focus:outline-none focus:border-indigo-500"
              >
                <option value="SOC_ANALYST">SOC Analyst Mode</option>
                <option value="INCIDENT_RESPONDER">Incident Responder Mode</option>
                <option value="THREAT_HUNTER">Threat Hunter Mode</option>
                <option value="FORENSICS_ANALYST">Forensics Analyst Mode</option>
                <option value="SECURITY_ENGINEER">Security Engineer Mode</option>
                <option value="RISK_ANALYST">Risk Analyst Mode</option>
                <option value="COMPLIANCE_ANALYST">Compliance Analyst Mode</option>
                <option value="EXECUTIVE">Executive Mode</option>
                <option value="CRISIS_COMMANDER">Crisis Commander Mode</option>
              </select>
            </div>
          </div>

          {/* Chat Messages */}
          <div className="space-y-4 max-h-96 overflow-y-auto pr-2 scrollbar-thin scrollbar-thumb-slate-800">
            {copilotResponses.map((item, idx) => (
              <div key={idx} className="space-y-2">
                <div className="bg-slate-800/60 border border-slate-700/60 p-3 rounded-lg text-xs font-mono text-slate-200">
                  <span className="text-indigo-400 font-bold">User ({copilotMode}):</span> {item.query}
                </div>
                <div className="bg-slate-950 border border-slate-800 p-4 rounded-lg space-y-2 text-xs">
                  <div className="flex items-center justify-between text-[11px] font-mono">
                    <span className="text-indigo-400 font-bold flex items-center gap-1.5">
                      <Sparkles className="h-3.5 w-3.5" /> TruthShield Copilot Response
                    </span>
                    <span className="text-emerald-400 font-bold">{item.confidence} &bull; {item.timestamp}</span>
                  </div>
                  <div className="text-slate-200 font-sans whitespace-pre-line leading-relaxed">
                    {item.answer}
                  </div>
                  <div className="pt-2 border-t border-slate-800/80 text-[11px] text-slate-400 font-mono flex items-center gap-2">
                    <span className="font-bold text-slate-300">Sources:</span>
                    {item.sources.map((s, sidx) => (
                      <span key={sidx} className="bg-slate-900 border border-slate-700 px-2 py-0.5 rounded text-indigo-300">
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Query Input */}
          <div className="flex items-center gap-3">
            <input
              type="text"
              value={copilotQuery}
              onChange={(e) => setCopilotQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSendCopilotQuery()}
              placeholder="Ask the Security Copilot (e.g., 'What is confirmed?', 'Show evidence', 'Response options?')..."
              className="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 font-mono"
            />
            <button
              disabled={queryingCopilot}
              onClick={handleSendCopilotQuery}
              className="bg-indigo-600 hover:bg-indigo-500 text-white px-5 py-2.5 rounded-lg text-xs font-semibold flex items-center gap-2 transition-colors disabled:opacity-50"
            >
              <Send className="h-3.5 w-3.5" /> {queryingCopilot ? 'Thinking...' : 'Query Copilot'}
            </button>
          </div>
        </div>
      )}

      {/* Tab 15: EXECUTIVE BRIEFING */}
      {activeTab === 'executive_briefing' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <Users className="h-5 w-5 text-indigo-400" /> Executive Cyber Situational Awareness &amp; Briefing
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Concise, evidence-grounded briefings formatted for Board and Executive Leadership.
              </p>
            </div>
            <button className="text-xs bg-indigo-950 hover:bg-indigo-900 text-indigo-300 border border-indigo-800 px-3 py-1.5 rounded font-medium transition-colors">
              Export PDF Briefing
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-slate-950 border border-slate-800 p-5 rounded-xl space-y-3">
              <h3 className="text-xs font-bold text-indigo-300 uppercase tracking-wider font-mono">
                30-Second Executive Summary
              </h3>
              <p className="text-xs text-slate-300 leading-relaxed">
                TruthShield X SOC contained an external adversary probe targeting the API Gateway at 11:15 UTC.
                Microsegmentation prevented any access to customer databases or credentials.
                Current business operations remain 100% online with zero financial or data leakage.
              </p>
            </div>

            <div className="bg-slate-950 border border-slate-800 p-5 rounded-xl space-y-3">
              <h3 className="text-xs font-bold text-indigo-300 uppercase tracking-wider font-mono">
                Key Decision Points
              </h3>
              <ul className="text-xs text-slate-300 space-y-1.5 list-disc list-inside">
                <li>Option A (Microsegmentation + MFA) executed under SecOps Commander authorization.</li>
                <li>DPDP Act 2023 notification threshold not met (No personal data accessed).</li>
                <li>Full post-recovery verification scheduled for 13:00 UTC.</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CyberCrisisCommandCenterPage;
