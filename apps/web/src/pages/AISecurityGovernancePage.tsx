import React, { useState } from 'react';
import { 
  Bot, Shield, AlertOctagon, CheckCircle2, Lock, 
  RotateCcw, Sparkles, Terminal, FileCode2, Layers, 
  Database, Activity, Zap, Eye, Check, X, ShieldAlert, 
  Binary, Cpu, ShieldCheck
} from 'lucide-react';

export const AISecurityGovernancePage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'inventory' | 'models' | 'prompt_rag' | 'agents' | 'incidents' | 'red_team'>('inventory');
  
  const [quarantining, setQuarantining] = useState(false);
  const [quarantinedModel, setQuarantinedModel] = useState<string | null>(null);

  const handleQuarantine = async (modelId: string) => {
    setQuarantining(true);
    try {
      await new Promise(r => setTimeout(r, 600));
      setQuarantinedModel(modelId);
    } finally {
      setQuarantining(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <Bot className="h-8 w-8 text-cyan-400" />
            <h1 className="text-3xl font-bold tracking-tight text-white">
              AI Security & Model Governance Control Plane
            </h1>
          </div>
          <p className="text-slate-400 mt-1">
            Trustworthy AI Operations, Prompt-Injection Defense, Secure RAG, AI Agent Sandboxing & Model Supply-Chain Security
          </p>
        </div>
        
        {/* Risk Level Badge */}
        <div className="flex items-center gap-3 bg-slate-900 border border-slate-800 rounded-xl px-4 py-2">
          <div className="text-xs text-slate-400">Overall AI Risk:</div>
          <div className="flex items-center gap-2">
            <span className="text-sm font-bold text-emerald-400">LOW (0.08)</span>
            <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded font-mono">
              SECURE
            </span>
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Registered AI Assets</span>
            <Cpu className="h-4 w-4 text-cyan-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">24</div>
          <div className="text-xs text-cyan-400 mt-1 font-medium">Models, Agents, Tools & RAGs</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Prompt Injections Blocked</span>
            <ShieldAlert className="h-4 w-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-extrabold text-emerald-400">100%</div>
          <div className="text-xs text-emerald-400 mt-1 font-medium">Zero Jailbreak Bypasses</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Model Artifact Integrity</span>
            <ShieldCheck className="h-4 w-4 text-amber-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">VERIFIED</div>
          <div className="text-xs text-amber-400 mt-1 font-medium">SHA-256 Checksum Matched</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Agent Tool Governance</span>
            <Lock className="h-4 w-4 text-indigo-400" />
          </div>
          <div className="text-3xl font-extrabold text-indigo-400">ENFORCED</div>
          <div className="text-xs text-indigo-400 mt-1 font-medium">Strict Allowlist & Loop Guard</div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 gap-6">
        {(['inventory', 'models', 'prompt_rag', 'agents', 'incidents', 'red_team'] as const).map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`pb-3 text-sm font-semibold capitalize transition ${
              activeTab === tab 
                ? 'border-b-2 border-cyan-400 text-cyan-400' 
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            {tab.replace('_', ' ')}
          </button>
        ))}
      </div>

      {/* Tab Contents */}
      {activeTab === 'inventory' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Binary className="h-5 w-5 text-cyan-400" />
              Active AI Models & Classifiers
            </h2>
            <div className="space-y-3">
              <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 flex items-center justify-between">
                <div>
                  <div className="font-bold text-white">C2 Multi-Modal Detection Engine</div>
                  <div className="text-xs text-slate-400">DeBERTa-V3 | Checksum: e3b0c442... | Risk: HIGH</div>
                </div>
                <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded font-mono">
                  DEPLOYED
                </span>
              </div>
              <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 flex items-center justify-between">
                <div>
                  <div className="font-bold text-white">Deepfake Voice & Speech Biometric Analyzer</div>
                  <div className="text-xs text-slate-400">AudioSpectrogram ResNet | Checksum: a8f9c120... | Risk: CRITICAL</div>
                </div>
                <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded font-mono">
                  DEPLOYED
                </span>
              </div>
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Database className="h-5 w-5 text-amber-400" />
              Dataset Governance & Provenance
            </h2>
            <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-white">Verified Threat Intelligence Training Set 2026</span>
                <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded font-mono">
                  VERIFIED_CLEAN
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Source: TruthShield Verified Feeds | Integrity: Zero anomalous label clusters detected.
              </p>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'prompt_rag' && (
        <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Terminal className="h-5 w-5 text-emerald-400" />
            Prompt & Secure RAG Architecture
          </h2>
          <div className="bg-slate-950 p-5 rounded-lg border border-slate-800 space-y-3">
            <div className="flex items-center justify-between">
              <span className="font-bold text-white">Indirect Injection Shielding & Document Isolation</span>
              <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded font-mono">
                DATA_ISOLATION_ACTIVE
              </span>
            </div>
            <p className="text-xs text-slate-300">
              Retrieved documents from RAG pipelines are treated strictly as inert DATA and filtered for embedded instruction overrides before context insertion.
            </p>
            <div className="text-xs font-mono text-cyan-400 bg-slate-900/80 p-3 rounded border border-slate-800">
              ✓ Direct Jailbreak Patterns Blocked: "Ignore previous instructions", "Reveal system prompt"<br/>
              ✓ Cross-Tenant Vector Isolation: Enforced on all embedding similarity queries<br/>
              ✓ Claim Grounding: All security statements mandate supporting telemetry citations
            </div>
          </div>
        </div>
      )}

      {activeTab === 'models' && (
        <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <ShieldAlert className="h-5 w-5 text-rose-400" />
              Model Lifecycle & Incident Quarantine
            </h2>
          </div>
          <div className="bg-slate-950 p-5 rounded-lg border border-slate-800 space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <div className="font-bold text-white">mdl_c2_neural_classifier (v2.1.0)</div>
                <div className="text-xs text-slate-400">Drift Status: STABLE | Precision: 0.97 | Latency: 28.5ms</div>
              </div>
              <button
                onClick={() => handleQuarantine("mdl_c2_neural_classifier")}
                disabled={quarantining || quarantinedModel === "mdl_c2_neural_classifier"}
                className="flex items-center gap-1.5 bg-rose-600 hover:bg-rose-500 text-white px-3 py-1.5 rounded-lg text-xs font-semibold transition"
              >
                <AlertOctagon className="h-4 w-4" />
                {quarantinedModel === "mdl_c2_neural_classifier" ? "Model Quarantined" : "Emergency Quarantine"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
