import React, { useState } from 'react';
import {
  Sparkles,
  Shield,
  Send,
  Terminal,
  Activity,
  AlertTriangle,
  CheckCircle2,
  Lock,
  Layers,
  Search,
  Compass,
  FileCheck,
  Zap,
  Play,
  RotateCcw,
  Eye,
  Sliders,
  History,
  TrendingUp,
} from 'lucide-react';

interface Citation {
  evidence_id: string;
  source_id: string;
  object_id: string;
  snippet: string;
  confidence: number;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
  confidence?: number;
  epistemic_status?: string;
  contradictions?: string[];
  unknowns?: string[];
  limitations?: string[];
}

export const SecurityCopilotCenterPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'copilot' | 'command_center' | 'actions' | 'hunting' | 'briefings'>('copilot');
  const [inputPrompt, setInputPrompt] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'msg_0',
      role: 'assistant',
      content: 'TruthShield X Autonomous Security Copilot active. How may I assist your security operations today?',
      citations: [
        {
          evidence_id: 'ev_init_01',
          source_id: 'FABRIC_ORCHESTRATOR',
          object_id: 'tenant_default',
          snippet: 'Security Knowledge Fabric synchronized (93.8% quality health).',
          confidence: 0.98,
        },
      ],
      confidence: 0.98,
      epistemic_status: 'VERIFIED',
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);

  // Action plan state
  const [pendingPlan, setPendingPlan] = useState<any>({
    plan_id: 'act_plan_991',
    action_type: 'ISOLATE_NETWORK_EGRESS',
    target_resource: 'srv_checkout_production',
    reason: 'Contain active Shadow Hydra lateral propagation probing.',
    expected_benefit: 'Zero lateral SMB/RPC traversal to user database.',
    possible_impact: 'Temporary disconnection of background analytics ETL jobs.',
    approval_status: 'APPROVAL_REQUIRED',
    required_approval_tier: 'TIER_2_FOUR_EYES',
  });
  const [executionResult, setExecutionResult] = useState<any>(null);

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputPrompt.trim() || isLoading) return;

    const userText = inputPrompt;
    const userMsg: Message = {
      id: `usr_${Date.now()}`,
      role: 'user',
      content: userText,
    };
    setMessages((prev) => [...prev, userMsg]);
    setInputPrompt('');
    setIsLoading(true);

    setTimeout(() => {
      let assistantMsg: Message;
      const lower = userText.toLowerCase();

      if (lower.includes('ignore') || lower.includes('override') || lower.includes('secret')) {
        assistantMsg = {
          id: `ast_${Date.now()}`,
          role: 'assistant',
          content: 'Request rejected: Prompt violated safety boundaries (Prompt injection / unauthorized disclosure blocked).',
          confidence: 0.0,
          epistemic_status: 'UNKNOWN',
          limitations: ['Prompt rejected by safety guard.'],
        };
      } else if (lower.includes('cve') || lower.includes('shadow hydra') || lower.includes('checkout')) {
        assistantMsg = {
          id: `ast_${Date.now()}`,
          role: 'assistant',
          content: 'Checkout Service srv_checkout_production is exposed to Shadow Hydra campaign via unpatched CVE-2026-9942.',
          confidence: 0.91,
          epistemic_status: 'INFERRED',
          citations: [
            {
              evidence_id: 'ev_pcap_trace_88',
              source_id: 'TELEMETRY_ENGINE',
              object_id: 'srv_checkout_production',
              snippet: 'TCP Outbound flow to C2 198.51.100.42 detected on port 8443',
              confidence: 0.96,
            },
            {
              evidence_id: 'ev_vuln_scan_44',
              source_id: 'TRIVY_SCANNER',
              object_id: 'cve_2026_9942',
              snippet: 'Unpatched CVSS 9.8 remote code execution in payment gateway binary',
              confidence: 0.94,
            },
          ],
          contradictions: ['ev_audit_log_90 (container shutdown recorded 2m earlier)'],
          unknowns: ['Host memory core dump at time of process injection'],
          limitations: ['WAF was operating in monitor-only mode at initial observation.'],
        };
      } else if (lower.includes('posture') || lower.includes('ciso') || lower.includes('executive')) {
        assistantMsg = {
          id: `ast_${Date.now()}`,
          role: 'assistant',
          content: 'Executive Posture Summary: Customer checkout transactions running normally at 99.98% availability. 1 active high-priority investigation on payment gateway perimeter. WAF edge rules tightened.',
          confidence: 0.94,
          epistemic_status: 'OBSERVED',
          citations: [
            {
              evidence_id: 'ciso_brief_01',
              source_id: 'CISO_COMMAND_CENTER',
              object_id: 'tenant_default',
              snippet: 'Security posture score 87.5/100 (IMPROVING trend).',
              confidence: 0.95,
            },
          ],
          limitations: ['Financial estimates require manual finance ledger synchronization.'],
        };
      } else {
        assistantMsg = {
          id: `ast_${Date.now()}`,
          role: 'assistant',
          content: `Security Copilot analyzed query: "${userText}". Grounded telemetry confirms system operation within nominal parameters.`,
          confidence: 0.88,
          epistemic_status: 'INFERRED',
          citations: [
            {
              evidence_id: 'ev_telemetry_flow',
              source_id: 'TELEMETRY',
              object_id: 'system_fabric',
              snippet: 'Active telemetry stream confirmed.',
              confidence: 0.90,
            },
          ],
        };
      }

      setMessages((prev) => [...prev, assistantMsg]);
      setIsLoading(false);
    }, 450);
  };

  const handleApprovePlan = () => {
    setPendingPlan((prev: any) => ({ ...prev, approval_status: 'APPROVED' }));
  };

  const handleExecutePlan = () => {
    setExecutionResult({
      action_state: 'VERIFIED',
      verification_result: 'Verification confirmed expected security group egress isolation applied.',
      actual_state: 'ISOLATED_SECURITY_GROUP_APPLIED',
      expected_state: 'ISOLATED_SECURITY_GROUP_APPLIED',
      has_divergence: false,
      rollback_status: 'READY',
      verified_at: new Date().toISOString(),
    });
    setPendingPlan((prev: any) => ({ ...prev, approval_status: 'EXECUTED' }));
  };

  return (
    <div className="min-h-screen bg-[#020617] text-slate-100 p-8 space-y-8 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-indigo-500/10 border border-indigo-500/30 rounded-xl">
              <Sparkles className="w-8 h-8 text-indigo-400" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white flex items-center gap-2">
                Cyber Command Center & Security Copilot
                <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                  Production 2.0
                </span>
              </h1>
              <p className="text-sm text-slate-400">
                Evidence-grounded conversational AI operations, executive intelligence, and safe action execution
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="bg-slate-900 border border-slate-800 rounded-lg px-4 py-2 text-right">
            <div className="text-xs text-slate-400">Security Posture</div>
            <div className="text-lg font-bold text-emerald-400">87.5 / 100</div>
          </div>
          <button className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition-all shadow-lg shadow-indigo-600/20">
            Export Brief
          </button>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 gap-2 overflow-x-auto pb-px">
        {[
          { id: 'copilot', label: 'Security Copilot Chat', icon: Sparkles },
          { id: 'command_center', label: 'CISO Command Center', icon: Activity },
          { id: 'actions', label: 'Action & Approval Gates', icon: Lock },
          { id: 'hunting', label: 'Threat Hunting Studio', icon: Terminal },
          { id: 'briefings', label: 'Executive Briefings', icon: TrendingUp },
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

      {/* Tab Content */}
      {activeTab === 'copilot' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 flex flex-col h-[650px] bg-slate-900/60 border border-slate-800 rounded-xl overflow-hidden">
            {/* Chat Messages */}
            <div className="flex-1 p-6 overflow-y-auto space-y-6">
              {messages.map((m) => (
                <div
                  key={m.id}
                  className={`flex flex-col ${
                    m.role === 'user' ? 'items-end' : 'items-start'
                  }`}
                >
                  <div
                    className={`max-w-[85%] rounded-2xl p-4 space-y-3 ${
                      m.role === 'user'
                        ? 'bg-indigo-600 text-white rounded-br-none'
                        : 'bg-slate-950/80 border border-slate-800 text-slate-200 rounded-bl-none'
                    }`}
                  >
                    <div className="text-sm leading-relaxed">{m.content}</div>

                    {m.role === 'assistant' && m.citations && m.citations.length > 0 && (
                      <div className="border-t border-slate-800/80 pt-3 space-y-2 text-xs">
                        <div className="flex items-center justify-between text-indigo-400 font-semibold">
                          <span className="flex items-center gap-1.5">
                            <Layers className="w-3.5 h-3.5" />
                            Authoritative Evidence Citations:
                          </span>
                          <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
                            {m.epistemic_status || 'VERIFIED'} ({(m.confidence! * 100).toFixed(0)}%)
                          </span>
                        </div>
                        {m.citations.map((c, i) => (
                          <div key={i} className="p-2 bg-slate-900/80 border border-slate-800 rounded font-mono text-slate-300">
                            <div className="text-[11px] text-slate-500 flex justify-between">
                              <span>[{c.evidence_id}] via {c.source_id}</span>
                              <span className="text-emerald-400">{(c.confidence * 100).toFixed(0)}%</span>
                            </div>
                            <div className="text-xs text-slate-200 mt-0.5">{c.snippet}</div>
                          </div>
                        ))}
                      </div>
                    )}

                    {m.contradictions && m.contradictions.length > 0 && (
                      <div className="p-2.5 bg-amber-500/10 border border-amber-500/30 rounded text-xs text-amber-200 space-y-1">
                        <div className="font-semibold text-amber-400 flex items-center gap-1">
                          <AlertTriangle className="w-3.5 h-3.5" />
                          Preserved Contradiction:
                        </div>
                        {m.contradictions.map((c, idx) => (
                          <div key={idx}>{c}</div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex items-center gap-2 text-sm text-indigo-400 animate-pulse">
                  <Sparkles className="w-4 h-4" />
                  Synthesizing evidence-grounded response...
                </div>
              )}
            </div>

            {/* Input Bar */}
            <form onSubmit={handleSendMessage} className="p-4 border-t border-slate-800 bg-slate-950/80 flex gap-3">
              <input
                type="text"
                value={inputPrompt}
                onChange={(e) => setInputPrompt(e.target.value)}
                placeholder="Ask Copilot: 'Why is checkout service high risk?' or 'What are our top risks?'"
                className="flex-1 bg-slate-900 border border-slate-800 rounded-lg px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
              />
              <button
                type="submit"
                disabled={isLoading}
                className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition-all flex items-center gap-2 shadow-lg shadow-indigo-600/20"
              >
                <Send className="w-4 h-4" />
                Send
              </button>
            </form>
          </div>

          {/* Quick Context & Actions Sidebar */}
          <div className="space-y-4">
            <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
              <h2 className="text-sm font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-2">
                <Compass className="w-4 h-4 text-cyan-400" />
                Role & Persona Controls
              </h2>
              <div className="grid grid-cols-2 gap-2 text-xs">
                {['ANALYST', 'HUNTER', 'INCIDENT_RESPONDER', 'CISO'].map((role) => (
                  <button
                    key={role}
                    className="p-2 rounded bg-slate-950 border border-slate-800 text-left hover:border-indigo-500 text-slate-300 font-mono transition-all"
                  >
                    {role}
                  </button>
                ))}
              </div>
            </div>

            <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-3">
              <h2 className="text-sm font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-2">
                <Zap className="w-4 h-4 text-amber-400" />
                One-Click Quick Actions
              </h2>
              <div className="space-y-2 text-xs">
                <button
                  onClick={() => setInputPrompt('Investigate srv_checkout_production')}
                  className="w-full text-left p-2.5 rounded bg-slate-950 border border-slate-800 hover:border-indigo-500 text-slate-300 flex items-center justify-between"
                >
                  <span>Investigate Active Incident</span>
                  <Eye className="w-3.5 h-3.5 text-indigo-400" />
                </button>
                <button
                  onClick={() => setInputPrompt('What are our top risks and blind spots?')}
                  className="w-full text-left p-2.5 rounded bg-slate-950 border border-slate-800 hover:border-indigo-500 text-slate-300 flex items-center justify-between"
                >
                  <span>Explain Top Risks & Gaps</span>
                  <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
                </button>
                <button
                  onClick={() => setInputPrompt('Simulate isolating network egress on srv_checkout_production')}
                  className="w-full text-left p-2.5 rounded bg-slate-950 border border-slate-800 hover:border-indigo-500 text-slate-300 flex items-center justify-between"
                >
                  <span>Simulate Containment Defense</span>
                  <Play className="w-3.5 h-3.5 text-emerald-400" />
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'command_center' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-2">
            <span className="text-xs font-semibold uppercase text-slate-400">Security Posture</span>
            <div className="text-3xl font-bold text-emerald-400">87.5 / 100</div>
            <div className="text-xs text-slate-500">Trend: IMPROVING</div>
          </div>
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-2">
            <span className="text-xs font-semibold uppercase text-slate-400">Control Health</span>
            <div className="text-3xl font-bold text-indigo-400">94.0%</div>
            <div className="text-xs text-slate-500">Across 42 enforced policies</div>
          </div>
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-2">
            <span className="text-xs font-semibold uppercase text-slate-400">Exposure Index</span>
            <div className="text-3xl font-bold text-amber-400">14.2%</div>
            <div className="text-xs text-slate-500">1 active high-risk vulnerability</div>
          </div>
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-2">
            <span className="text-xs font-semibold uppercase text-slate-400">Open Decisions</span>
            <div className="text-3xl font-bold text-cyan-400">1</div>
            <div className="text-xs text-slate-500">Patch approval pending</div>
          </div>
        </div>
      )}

      {activeTab === 'actions' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold text-white flex items-center gap-2">
                <Lock className="w-5 h-5 text-indigo-400" />
                Action & Approval Gates (Tier-2 Four-Eyes)
              </h2>
              <p className="text-sm text-slate-400">
                Mandatory human authorization required before executing any containment or remediation mutation
              </p>
            </div>
            <span className={`text-xs px-3 py-1 rounded-full font-mono font-bold ${
              pendingPlan.approval_status === 'APPROVED' ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' :
              pendingPlan.approval_status === 'EXECUTED' ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/30' :
              'bg-amber-500/20 text-amber-300 border border-amber-500/30'
            }`}>
              {pendingPlan.approval_status}
            </span>
          </div>

          <div className="p-5 bg-slate-950/80 border border-slate-800 rounded-xl space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-xs text-slate-500 uppercase font-semibold">Action Type:</span>
                <div className="font-mono text-indigo-300 font-bold">{pendingPlan.action_type}</div>
              </div>
              <div>
                <span className="text-xs text-slate-500 uppercase font-semibold">Target Resource:</span>
                <div className="font-mono text-white font-bold">{pendingPlan.target_resource}</div>
              </div>
              <div>
                <span className="text-xs text-slate-500 uppercase font-semibold">Reason:</span>
                <div className="text-slate-300">{pendingPlan.reason}</div>
              </div>
              <div>
                <span className="text-xs text-slate-500 uppercase font-semibold">Possible Impact:</span>
                <div className="text-amber-300">{pendingPlan.possible_impact}</div>
              </div>
            </div>

            <div className="flex gap-3 pt-4 border-t border-slate-800">
              {pendingPlan.approval_status === 'APPROVAL_REQUIRED' && (
                <button
                  onClick={handleApprovePlan}
                  className="px-5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-medium transition-all flex items-center gap-2"
                >
                  <CheckCircle2 className="w-4 h-4" />
                  Authorize & Approve Plan (Tier-2)
                </button>
              )}
              {pendingPlan.approval_status === 'APPROVED' && (
                <button
                  onClick={handleExecutePlan}
                  className="px-5 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition-all flex items-center gap-2 shadow-lg shadow-indigo-600/20"
                >
                  <Play className="w-4 h-4" />
                  Execute & Verify Action
                </button>
              )}
            </div>

            {executionResult && (
              <div className="p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-lg space-y-2 mt-4">
                <div className="text-sm font-bold text-emerald-400 flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4" />
                  Execution Verified: {executionResult.actual_state}
                </div>
                <div className="text-xs text-slate-300">{executionResult.verification_result}</div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
