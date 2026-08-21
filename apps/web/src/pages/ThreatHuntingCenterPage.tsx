import React, { useState } from 'react';
import { 
  Crosshair, 
  Search, 
  Layers, 
  Compass, 
  AlertTriangle, 
  GitBranch, 
  TrendingUp, 
  CheckCircle2, 
  XCircle, 
  Terminal,
  Activity,
  Play
} from 'lucide-react';

interface ThreatHuntItem {
  id: string;
  title: string;
  type: string;
  status: string;
  confidence: number;
  supporting: number;
  counter: number;
}

export const ThreatHuntingCenterPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'hunts' | 'hypotheses' | 'paths' | 'warnings' | 'predictions'>('hunts');

  const [hunts] = useState<ThreatHuntItem[]>([
    {
      id: 'hpt_8812a',
      title: 'Hunt for Domain Lookalike Phishing Infrastructure',
      type: 'PHISHING_CAMPAIGN',
      status: 'SUPPORTED',
      confidence: 0.88,
      supporting: 4,
      counter: 1
    },
    {
      id: 'hpt_9901c',
      title: 'Shared Certificate Serial in Banking Dropper APKs',
      type: 'MALWARE_CAMPAIGN',
      status: 'ACTIVE',
      confidence: 0.92,
      supporting: 6,
      counter: 0
    }
  ]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 space-y-8 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-rose-500/10 border border-rose-500/30 rounded-xl text-rose-400">
            <Crosshair className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
              Autonomous Threat Hunting Center
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30 font-medium">
                Proactive Hunting Active
              </span>
            </h1>
            <p className="text-sm text-slate-400">
              Hypothesis-Driven Threat Discovery, Anti-Confirmation-Bias Reasoning, Attack-Path Modeling & Predictive Defense
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 rounded-lg text-sm transition-colors">
            <Terminal className="w-4 h-4" />
            Hunt DSL Console
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white rounded-lg text-sm font-medium transition-colors shadow-lg shadow-rose-600/20">
            <Play className="w-4 h-4" />
            Launch Autonomous Hunt
          </button>
        </div>
      </div>

      {/* Tabs Navigation */}
      <div className="flex border-b border-slate-800 space-x-8">
        {[
          { id: 'hunts', label: 'Active Hunts' },
          { id: 'hypotheses', label: 'Hypotheses & Counter-Evidence' },
          { id: 'paths', label: 'Attack Paths' },
          { id: 'warnings', label: 'Early Warnings' },
          { id: 'predictions', label: 'Horizon Predictions & Calibration' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`pb-4 text-sm font-medium transition-colors border-b-2 ${
              activeTab === tab.id
                ? 'border-rose-500 text-rose-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Main Content */}
      <div className="space-y-4">
        {hunts.map((hunt) => (
          <div key={hunt.id} className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 hover:border-slate-700 transition-colors">
            <div className="flex items-start justify-between">
              <div>
                <div className="flex items-center gap-3">
                  <span className="px-2 py-0.5 rounded bg-slate-800 text-xs font-mono text-rose-300">
                    {hunt.type}
                  </span>
                  <h3 className="text-base font-semibold text-white">{hunt.title}</h3>
                  <span className="px-2 py-0.5 text-xs font-bold rounded bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">
                    {hunt.status}
                  </span>
                </div>
                <div className="flex items-center gap-6 mt-3 text-xs text-slate-400">
                  <span className="flex items-center gap-1 text-emerald-400 font-semibold">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    Supporting Evidence: {hunt.supporting}
                  </span>
                  <span className="flex items-center gap-1 text-amber-400 font-semibold">
                    <XCircle className="w-3.5 h-3.5" />
                    Counter-Evidence Checked: {hunt.counter}
                  </span>
                  <span>Anti-Confirmation-Bias: <strong>Verified</strong></span>
                </div>
              </div>

              <div className="text-right">
                <div className="text-xs text-slate-400">Hypothesis Confidence</div>
                <div className="text-2xl font-bold text-rose-400">{(hunt.confidence * 100).toFixed(0)}%</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ThreatHuntingCenterPage;
