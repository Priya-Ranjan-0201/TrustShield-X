import React, { useState } from 'react';
import {
  ShieldAlert,
  ShieldCheck,
  Zap,
  Play,
  CheckCircle2,
  AlertTriangle,
  RotateCcw,
  Bot,
  Activity,
  Check,
  X,
  Lock,
  Layers,
  Search,
  ArrowRight,
  RefreshCw,
  Terminal,
} from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Card } from '../components/ui/Card';
import { toast } from '../lib/sonner';

interface ResponseAction {
  id: string;
  type: string;
  target: string;
  safety: string;
  status: string;
  approvalRequired: boolean;
  approvalStatus: string;
}

interface ResponsePlan {
  id: string;
  title: string;
  incidentId: string;
  riskScore: number;
  confidence: number;
  state: string;
  actions: ResponseAction[];
}

export const DefenseControlCenterPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'plans' | 'approvals' | 'simulation' | 'copilot' | 'effectiveness'>('plans');
  const [copilotQuery, setCopilotQuery] = useState('');
  const [copilotMessages, setCopilotMessages] = useState<Array<{ role: 'user' | 'assistant'; text: string; next?: string }>>([
    {
      role: 'assistant',
      text: 'Security Copilot initialized. I can explain campaign risks, simulate containment impacts, or analyze action refusal reasons.',
      next: 'Try asking: "Why was this campaign classified as high risk?" or "Simulate containment."',
    },
  ]);

  const [plans, setPlans] = useState<ResponsePlan[]>([
    {
      id: 'rplan_c891ab02f',
      title: 'Coordinated Multi-Vector Containment — Trojanized APK & Phishing C2',
      incidentId: 'INC-2026-0891',
      riskScore: 92.4,
      confidence: 0.96,
      state: 'AWAITING_APPROVAL',
      actions: [
        {
          id: 'pact_01',
          type: 'BLOCK_DOMAIN',
          target: 'secure-verification-hdfc-portal.net',
          safety: 'HIGH_RISK_MUTATION',
          status: 'AWAITING_APPROVAL',
          approvalRequired: true,
          approvalStatus: 'PENDING',
        },
        {
          id: 'pact_02',
          type: 'QUARANTINE_FILE',
          target: 'sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
          safety: 'HIGH_RISK_MUTATION',
          status: 'AWAITING_APPROVAL',
          approvalRequired: true,
          approvalStatus: 'PENDING',
        },
        {
          id: 'pact_03',
          type: 'FREEZE_UPI_HANDLE',
          target: 'fraudulent.merchant@okhdfcbank',
          safety: 'HIGH_RISK_MUTATION',
          status: 'AWAITING_APPROVAL',
          approvalRequired: true,
          approvalStatus: 'PENDING',
        },
      ],
    },
    {
      id: 'rplan_44109efa1',
      title: 'Voice Clone Impersonation Response — Executive Account Lockdown',
      incidentId: 'INC-2026-0888',
      riskScore: 78.0,
      confidence: 0.91,
      state: 'VERIFIED',
      actions: [
        {
          id: 'pact_11',
          type: 'REVOKE_TOKEN',
          target: 'user_exec_cfo_09',
          safety: 'DESTRUCTIVE',
          status: 'VERIFIED',
          approvalRequired: true,
          approvalStatus: 'APPROVED',
        },
      ],
    },
  ]);

  const handleSimulate = (planId: string) => {
    toast.success(`Simulation complete for plan ${planId}: Zero external mutations verified.`);
    setPlans((prev) =>
      prev.map((p) => (p.id === planId ? { ...p, state: 'SIMULATED' } : p))
    );
  };

  const handleApprove = (planId: string, actionId: string) => {
    toast.success(`Action ${actionId} approved under Four-Eyes policy.`);
    setPlans((prev) =>
      prev.map((p) => {
        if (p.id === planId) {
          const updated = p.actions.map((a) =>
            a.id === actionId ? { ...a, approvalStatus: 'APPROVED', status: 'APPROVED' } : a
          );
          const allAppr = updated.every((a) => a.approvalStatus === 'APPROVED');
          return { ...p, actions: updated, state: allAppr ? 'APPROVED' : p.state };
        }
        return p;
      })
    );
  };

  const handleExecute = (planId: string) => {
    toast.success(`Plan ${planId} executing against provider adapters...`);
    setPlans((prev) =>
      prev.map((p) => (p.id === planId ? { ...p, state: 'EXECUTING' } : p))
    );
    setTimeout(() => {
      toast.success(`Plan ${planId} executed! Initiating post-action verification.`);
      setPlans((prev) =>
        prev.map((p) => {
          if (p.id === planId) {
            return {
              ...p,
              state: 'VERIFIED',
              actions: p.actions.map((a) => ({ ...a, status: 'VERIFIED' })),
            };
          }
          return p;
        })
      );
    }, 1200);
  };

  const handleCopilotAsk = (e: React.FormEvent) => {
    e.preventDefault();
    if (!copilotQuery.trim()) return;

    const q = copilotQuery.trim();
    const userMsg = { role: 'user' as const, text: q };
    let replyText = 'Security Copilot has analyzed your query against current threat intelligence.';
    let nextStep = 'Review active threat plans in the Defense Control Center.';

    if (q.toLowerCase().includes('why') || q.toLowerCase().includes('high risk')) {
      replyText = 'The campaign was classified as Critical Risk (92.4/100) due to 3 converging vectors: SMS OTP Stealer in DEX, Active Phishing C2 link, and Fake UPI Merchant VPA.';
      nextStep = 'Recommended next step: Execute simulated dry-run and submit for SOC Lead approval.';
    } else if (q.toLowerCase().includes('simulate')) {
      replyText = 'Simulation verified 0 external side-effects. DNS sinkhole and UPI freeze rules will be applied without impacting legitimate traffic.';
      nextStep = 'Recommended next step: Request Tier-2 Four-Eyes authorization.';
    }

    setCopilotMessages((prev) => [...prev, userMsg, { role: 'assistant', text: replyText, next: nextStep }]);
    setCopilotQuery('');
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      {/* Top Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold tracking-tight text-slate-100 flex items-center gap-2">
              <Zap className="h-8 w-8 text-cyan-400" />
              Autonomous Defense Control Center
            </h1>
            <Badge variant="info" className="bg-cyan-950/60 text-cyan-400 border border-cyan-800">
              PHASE 5 ENGINE ACTIVE
            </Badge>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Deterministic, policy-governed cyber defense & digital trust orchestration with Four-Eyes authorization.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="secondary" className="border-slate-700 bg-slate-900">
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh Telemetry
          </Button>
          <Button variant="primary" className="bg-cyan-600 hover:bg-cyan-500 text-white shadow-lg shadow-cyan-950/50">
            <Play className="h-4 w-4 mr-2" />
            Trigger Coordinated Scan
          </Button>
        </div>
      </div>

      {/* Metric Tiles */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-5 bg-slate-900/60 border-slate-800 backdrop-blur-md">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Active Threat Plans</span>
            <ShieldAlert className="h-5 w-5 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-slate-100 mt-2">2 Plans</div>
          <div className="text-xs text-amber-400 mt-1">1 Awaiting Approval • 1 Verified</div>
        </Card>

        <Card className="p-5 bg-slate-900/60 border-slate-800 backdrop-blur-md">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Containment SLA</span>
            <Activity className="h-5 w-5 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-emerald-400 mt-2">4.2s Avg</div>
          <div className="text-xs text-slate-400 mt-1">Target: &lt; 15.0s (100% On-Track)</div>
        </Card>

        <Card className="p-5 bg-slate-900/60 border-slate-800 backdrop-blur-md">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Response Effectiveness</span>
            <ShieldCheck className="h-5 w-5 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold text-cyan-400 mt-2">94.6 / 100</div>
          <div className="text-xs text-slate-400 mt-1">Residual Risk Reduction: 85.2%</div>
        </Card>

        <Card className="p-5 bg-slate-900/60 border-slate-800 backdrop-blur-md">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Governance Posture</span>
            <Lock className="h-5 w-5 text-indigo-400" />
          </div>
          <div className="text-2xl font-bold text-indigo-400 mt-2">Strict Default-Deny</div>
          <div className="text-xs text-slate-400 mt-1">Four-Eyes Separation Enforced</div>
        </Card>
      </div>

      {/* Tabs Navigation */}
      <div className="flex gap-2 border-b border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab('plans')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
            activeTab === 'plans' ? 'bg-cyan-950/60 text-cyan-400 border border-cyan-800/80' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Response Plans &amp; Orchestration
        </button>
        <button
          onClick={() => setActiveTab('approvals')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
            activeTab === 'approvals' ? 'bg-cyan-950/60 text-cyan-400 border border-cyan-800/80' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Four-Eyes Approvals
        </button>
        <button
          onClick={() => setActiveTab('simulation')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
            activeTab === 'simulation' ? 'bg-cyan-950/60 text-cyan-400 border border-cyan-800/80' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Dry-Run Simulation Studio
        </button>
        <button
          onClick={() => setActiveTab('copilot')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors flex items-center gap-1.5 ${
            activeTab === 'copilot' ? 'bg-cyan-950/60 text-cyan-400 border border-cyan-800/80' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Bot className="h-4 w-4" />
          Security Copilot
        </button>
        <button
          onClick={() => setActiveTab('effectiveness')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
            activeTab === 'effectiveness' ? 'bg-cyan-950/60 text-cyan-400 border border-cyan-800/80' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Effectiveness Scorecard
        </button>
      </div>

      {/* Tab Content: Response Plans */}
      {activeTab === 'plans' && (
        <div className="space-y-6">
          {plans.map((plan) => (
            <Card key={plan.id} className="p-6 bg-slate-900/50 border-slate-800 space-y-4">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
                <div>
                  <div className="flex items-center gap-3">
                    <h3 className="text-lg font-semibold text-slate-100">{plan.title}</h3>
                    <Badge
                      className={
                        plan.state === 'VERIFIED'
                          ? 'bg-emerald-950/60 text-emerald-400 border-emerald-800'
                          : plan.state === 'AWAITING_APPROVAL'
                          ? 'bg-amber-950/60 text-amber-400 border-amber-800'
                          : 'bg-cyan-950/60 text-cyan-400 border-cyan-800'
                      }
                    >
                      {plan.state}
                    </Badge>
                  </div>
                  <div className="text-xs text-slate-400 mt-1">
                    Incident: <span className="text-cyan-400 font-mono">{plan.incidentId}</span> • Risk Score:{' '}
                    <span className="text-amber-400 font-bold">{plan.riskScore}</span> • Confidence:{' '}
                    <span className="text-slate-200">{(plan.confidence * 100).toFixed(0)}%</span>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  {plan.state === 'AWAITING_APPROVAL' && (
                    <>
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => handleSimulate(plan.id)}
                        className="bg-slate-800 hover:bg-slate-700 text-slate-200"
                      >
                        <Play className="h-3.5 w-3.5 mr-1" />
                        Simulate
                      </Button>
                      <Button
                        variant="primary"
                        size="sm"
                        onClick={() => handleExecute(plan.id)}
                        className="bg-cyan-600 hover:bg-cyan-500 text-white"
                      >
                        <CheckCircle2 className="h-3.5 w-3.5 mr-1" />
                        Execute Plan
                      </Button>
                    </>
                  )}
                  {plan.state === 'VERIFIED' && (
                    <Badge variant="info" className="bg-emerald-950/40 text-emerald-400 border border-emerald-800/80">
                      <CheckCircle2 className="h-3.5 w-3.5 mr-1 inline" />
                      Containment Verified
                    </Badge>
                  )}
                </div>
              </div>

              {/* Actions List */}
              <div className="space-y-3">
                <div className="text-xs font-semibold uppercase tracking-wider text-slate-400">Planned Containment Actions</div>
                <div className="grid grid-cols-1 gap-2">
                  {plan.actions.map((act) => (
                    <div
                      key={act.id}
                      className="p-3 bg-slate-950/60 border border-slate-800 rounded-lg flex items-center justify-between gap-4"
                    >
                      <div className="flex items-center gap-3">
                        <Badge variant="info" className="font-mono text-xs">
                          {act.type}
                        </Badge>
                        <span className="font-mono text-sm text-slate-200">{act.target}</span>
                      </div>

                      <div className="flex items-center gap-3">
                        <span className="text-xs text-slate-400">Safety: {act.safety}</span>
                        <Badge
                          className={
                            act.status === 'VERIFIED'
                              ? 'bg-emerald-950 text-emerald-400 border-emerald-800'
                              : 'bg-slate-800 text-slate-300'
                          }
                        >
                          {act.status}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Tab Content: Four-Eyes Approvals */}
      {activeTab === 'approvals' && (
        <div className="space-y-4">
          <Card className="p-6 bg-slate-900/50 border-slate-800 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <h3 className="text-base font-semibold text-slate-100 flex items-center gap-2">
                  <Lock className="h-5 w-5 text-amber-400" />
                  Pending Four-Eyes Authorization Requests
                </h3>
                <p className="text-xs text-slate-400 mt-1">
                  Separation of duties: The requesting analyst cannot approve their own high-impact actions.
                </p>
              </div>
            </div>

            <div className="space-y-3">
              <div className="p-4 bg-slate-950/60 border border-amber-800/40 rounded-xl space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Badge variant="info" className="bg-amber-950 text-amber-400 border-amber-800">
                      HIGH_RISK_MUTATION
                    </Badge>
                    <span className="text-sm font-semibold text-slate-200">BLOCK_DOMAIN: secure-verification-hdfc-portal.net</span>
                  </div>
                  <span className="text-xs text-slate-400">Expires in 3h 45m</span>
                </div>

                <div className="text-xs text-slate-400 grid grid-cols-2 gap-2">
                  <div>
                    Requester: <span className="text-slate-200">analyst_tier1_rahul</span>
                  </div>
                  <div>
                    Evidence: <span className="text-cyan-400">DEX Trojan SMS Gateway (Verified SHA-256)</span>
                  </div>
                </div>

                <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-800/60">
                  <Button
                    size="sm"
                    variant="secondary"
                    className="border-rose-900 bg-rose-950/40 text-rose-300 hover:bg-rose-900/60"
                  >
                    <X className="h-3.5 w-3.5 mr-1" />
                    Reject
                  </Button>
                  <Button
                    size="sm"
                    variant="primary"
                    onClick={() => handleApprove('rplan_c891ab02f', 'pact_01')}
                    className="bg-emerald-600 hover:bg-emerald-500 text-white"
                  >
                    <Check className="h-3.5 w-3.5 mr-1" />
                    Authorize Action
                  </Button>
                </div>
              </div>
            </div>
          </Card>
        </div>
      )}

      {/* Tab Content: Security Copilot */}
      {activeTab === 'copilot' && (
        <Card className="p-6 bg-slate-900/50 border-slate-800 space-y-4">
          <div className="flex items-center gap-3 border-b border-slate-800 pb-4">
            <Bot className="h-6 w-6 text-cyan-400" />
            <div>
              <h3 className="text-base font-semibold text-slate-100">Security Copilot Analyst Interface</h3>
              <p className="text-xs text-slate-400">Natural language threat explainability and policy guardrail assistant.</p>
            </div>
          </div>

          {/* Conversation history */}
          <div className="space-y-3 max-h-96 overflow-y-auto pr-2">
            {copilotMessages.map((msg, idx) => (
              <div
                key={idx}
                className={`p-4 rounded-xl text-sm ${
                  msg.role === 'assistant'
                    ? 'bg-slate-950/80 border border-slate-800 text-slate-200'
                    : 'bg-cyan-950/40 border border-cyan-800/60 text-cyan-100 ml-8'
                }`}
              >
                <div className="font-semibold text-xs text-slate-400 uppercase tracking-wider mb-1">
                  {msg.role === 'assistant' ? '🤖 TruthShield X Copilot' : '👤 Security Analyst'}
                </div>
                <div>{msg.text}</div>
                {msg.next && (
                  <div className="mt-2 text-xs text-cyan-400 bg-cyan-950/60 p-2 rounded border border-cyan-900">
                    💡 <strong>Next Step:</strong> {msg.next}
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Prompt input */}
          <form onSubmit={handleCopilotAsk} className="flex gap-2 pt-2 border-t border-slate-800">
            <input
              type="text"
              value={copilotQuery}
              onChange={(e) => setCopilotQuery(e.target.value)}
              placeholder="Ask Copilot (e.g. 'Why was this campaign classified as high risk?')..."
              className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-100 focus:outline-none focus:border-cyan-500"
            />
            <Button type="submit" variant="primary" className="bg-cyan-600 hover:bg-cyan-500 text-white">
              <ArrowRight className="h-4 w-4" />
            </Button>
          </form>
        </Card>
      )}

      {/* Tab Content: Effectiveness */}
      {activeTab === 'effectiveness' && (
        <Card className="p-6 bg-slate-900/50 border-slate-800 space-y-6">
          <div>
            <h3 className="text-base font-semibold text-slate-100">Containment Effectiveness Scorecard</h3>
            <p className="text-xs text-slate-400">Empirical measurement of threat reduction and operational speed.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl space-y-2">
              <div className="text-xs text-slate-400 uppercase font-semibold">Overall Containment Score</div>
              <div className="text-3xl font-bold text-emerald-400">94.6 / 100</div>
              <div className="text-xs text-slate-400">Tier: HIGHLY_EFFECTIVE</div>
            </div>

            <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl space-y-2">
              <div className="text-xs text-slate-400 uppercase font-semibold">Mean Time To Containment</div>
              <div className="text-3xl font-bold text-cyan-400">4.20s</div>
              <div className="text-xs text-slate-400">Target SLA: &lt; 15.00s</div>
            </div>

            <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl space-y-2">
              <div className="text-xs text-slate-400 uppercase font-semibold">Residual Risk Reduction</div>
              <div className="text-3xl font-bold text-amber-400">-73.2 pts</div>
              <div className="text-xs text-slate-400">From 92.4 to 19.2</div>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
};
