import React from 'react';

interface InvestigationOverviewProps {
  analysisId: string;
  riskScore: number;
  riskBand: string;
  confidence: string;
  evidenceSufficiency: string;
  criticalFindingsCount: number;
  highFindingsCount: number;
  evidenceCount: number;
  threatMatchCount: number;
  onNavigateTab: (tab: string) => void;
}

export const InvestigationOverview: React.FC<InvestigationOverviewProps> = ({
  analysisId,
  riskScore,
  riskBand,
  confidence,
  evidenceSufficiency,
  criticalFindingsCount,
  highFindingsCount,
  evidenceCount,
  threatMatchCount,
  onNavigateTab,
}) => {
  const getBadgeColor = (band: string) => {
    switch (band) {
      case 'CRITICAL_RISK': return 'bg-red-500/20 text-red-400 border-red-500/30';
      case 'HIGH_RISK': return 'bg-orange-500/20 text-orange-400 border-orange-500/30';
      case 'MODERATE_RISK': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'LOW_RISK': return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
      default: return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
          <span className="text-xs uppercase tracking-wider font-semibold text-slate-400">Authoritative Risk</span>
          <div className="flex items-baseline space-x-3 mt-2">
            <span className="text-3xl font-extrabold text-white">{riskScore.toFixed(1)}</span>
            <span className="text-xs text-slate-500">/ 100</span>
          </div>
          <div className="mt-3">
            <span className={`inline-block px-2.5 py-1 text-xs font-semibold rounded-full border ${getBadgeColor(riskBand)}`}>
              {riskBand.replace('_', ' ')}
            </span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
          <span className="text-xs uppercase tracking-wider font-semibold text-slate-400">Confidence & Sufficiency</span>
          <div className="mt-2 space-y-1">
            <div className="text-sm font-semibold text-slate-200">
              Confidence: <span className="text-indigo-400">{confidence}</span>
            </div>
            <div className="text-sm font-semibold text-slate-200">
              Sufficiency: <span className="text-cyan-400">{evidenceSufficiency}</span>
            </div>
          </div>
          <p className="text-xs text-slate-500 mt-2">Validated by Evidence Fusion Engine</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg cursor-pointer hover:border-slate-700 transition" onClick={() => onNavigateTab('findings')}>
          <span className="text-xs uppercase tracking-wider font-semibold text-slate-400">Security Findings</span>
          <div className="flex items-center space-x-4 mt-2">
            <div>
              <span className="text-2xl font-bold text-red-400">{criticalFindingsCount}</span>
              <span className="text-xs text-slate-500 block">Critical</span>
            </div>
            <div>
              <span className="text-2xl font-bold text-orange-400">{highFindingsCount}</span>
              <span className="text-xs text-slate-500 block">High</span>
            </div>
          </div>
          <span className="text-xs text-indigo-400 mt-2 block hover:underline">Explore findings →</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg cursor-pointer hover:border-slate-700 transition" onClick={() => onNavigateTab('evidence')}>
          <span className="text-xs uppercase tracking-wider font-semibold text-slate-400">Corroborated Evidence</span>
          <div className="flex items-baseline space-x-3 mt-2">
            <span className="text-3xl font-extrabold text-white">{evidenceCount}</span>
            <span className="text-xs text-slate-500">Cards</span>
          </div>
          <span className="text-xs text-indigo-400 mt-3 block hover:underline">Inspect evidence graph →</span>
        </div>
      </div>

      {/* Investigation Action Banner */}
      <div className="bg-gradient-to-r from-indigo-950/40 via-slate-900 to-slate-900 border border-indigo-500/20 rounded-xl p-6 flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white">Interactive Security Investigation Active</h3>
          <p className="text-sm text-slate-400 mt-1">
            Analysis ID: <code className="text-indigo-300 font-mono">{analysisId}</code> — Drill down across findings, evidence, threat intelligence, and call graph behaviors.
          </p>
        </div>
        <div className="flex space-x-3">
          <button onClick={() => onNavigateTab('graph')} className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold rounded-lg shadow transition">
            Launch Evidence Graph
          </button>
          <button onClick={() => onNavigateTab('timeline')} className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-semibold rounded-lg border border-slate-700 transition">
            View Timeline
          </button>
        </div>
      </div>
    </div>
  );
};
