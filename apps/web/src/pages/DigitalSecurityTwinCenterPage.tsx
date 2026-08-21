import React, { useState } from 'react';
import { 
  Boxes, 
  Play, 
  ShieldCheck, 
  ShieldAlert, 
  HelpCircle, 
  RotateCcw, 
  Layers, 
  Server, 
  CheckCircle2, 
  ArrowRight,
  TrendingDown,
  Sparkles
} from 'lucide-react';

interface StrategyItem {
  name: string;
  action: string;
  riskReduction: number;
  exposureReduction: number;
  safetyScore: number;
  reversibility: string;
  impact: string;
}

export const DigitalSecurityTwinCenterPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'scenarios' | 'whatif' | 'responses' | 'dr'>('overview');

  const [strategies] = useState<StrategyItem[]>([
    {
      name: 'Isolate Compromised Host',
      action: 'ISOLATE_ASSET',
      riskReduction: 40,
      exposureReduction: 45,
      safetyScore: 0.88,
      reversibility: 'HIGH',
      impact: 'MEDIUM'
    },
    {
      name: 'Rotate Synthetic Credentials',
      action: 'ROTATE_SYNTHETIC_CREDENTIALS',
      riskReduction: 25,
      exposureReduction: 30,
      safetyScore: 0.95,
      reversibility: 'HIGH',
      impact: 'LOW'
    },
    {
      name: 'Block External C2 on Edge WAF',
      action: 'BLOCK_INDICATOR',
      riskReduction: 20,
      exposureReduction: 20,
      safetyScore: 0.90,
      reversibility: 'HIGH',
      impact: 'LOW'
    }
  ]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 space-y-8 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-cyan-500/10 border border-cyan-500/30 rounded-xl text-cyan-400">
            <Boxes className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
              Digital Security Twin Center
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 font-medium">
                Simulation Sandbox Isolated (Zero-Mutation)
              </span>
            </h1>
            <p className="text-sm text-slate-400">
              Safe Attack Simulation, Response Validation, What-If Counterfactual Reasoning & Pre-Incident Defense
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 rounded-lg text-sm transition-colors">
            <RotateCcw className="w-4 h-4" />
            Reset Twin State
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg text-sm font-medium transition-colors shadow-lg shadow-cyan-600/20">
            <Play className="w-4 h-4" />
            Simulate Attack Scenario
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 space-x-8">
        {[
          { id: 'overview', label: 'Twin Overview & Controls' },
          { id: 'scenarios', label: 'Attack Scenarios' },
          { id: 'whatif', label: 'What-If Reasoning' },
          { id: 'responses', label: 'Response Strategy Validation' },
          { id: 'dr', label: 'Disaster Recovery Simulation' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`pb-4 text-sm font-medium transition-colors border-b-2 ${
              activeTab === tab.id
                ? 'border-cyan-500 text-cyan-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Response Comparison Table */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-white">Pre-Incident Response Strategy Comparison</h2>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl overflow-hidden">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-800/50 text-slate-400 text-xs font-semibold uppercase tracking-wider">
              <tr>
                <th className="py-3 px-4">Strategy Candidate</th>
                <th className="py-3 px-4">Risk Reduction</th>
                <th className="py-3 px-4">Exposure Drop</th>
                <th className="py-3 px-4">Safety Score</th>
                <th className="py-3 px-4">Reversibility</th>
                <th className="py-3 px-4">Collateral Impact</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {strategies.map((strat, idx) => (
                <tr key={idx} className="hover:bg-slate-800/30 transition-colors">
                  <td className="py-3.5 px-4 font-medium text-white flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4 text-cyan-400" />
                    {strat.name}
                  </td>
                  <td className="py-3.5 px-4 text-emerald-400 font-semibold">-{strat.riskReduction} pts</td>
                  <td className="py-3.5 px-4 text-emerald-400 font-semibold">-{strat.exposureReduction}%</td>
                  <td className="py-3.5 px-4 font-bold text-cyan-300">{(strat.safetyScore * 100).toFixed(0)}%</td>
                  <td className="py-3.5 px-4">
                    <span className="px-2 py-0.5 text-xs rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-medium">
                      {strat.reversibility}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-slate-400">{strat.impact}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default DigitalSecurityTwinCenterPage;
