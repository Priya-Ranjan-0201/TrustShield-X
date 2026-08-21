import React from 'react';

interface ReportComparisonProps {
  reportAId?: string;
  reportBId?: string;
  scoreA?: number;
  scoreB?: number;
  bandA?: string;
  bandB?: string;
}

export const ReportComparisonPage: React.FC<ReportComparisonProps> = ({
  reportAId = 'rep_v1_001',
  reportBId = 'rep_v2_002',
  scoreA = 65.0,
  scoreB = 72.5,
  bandA = 'MODERATE_RISK',
  bandB = 'HIGH_RISK',
}) => {
  const scoreDiff = scoreB - scoreA;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg space-y-6">
      <div>
        <h3 className="text-base font-bold text-white">Report Version Differential & Comparison</h3>
        <p className="text-xs text-slate-400">
          Auditable comparative analysis between Report revisions.
        </p>
      </div>

      {/* Top Level Score Comparison Card */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-5 bg-slate-950/60 rounded-xl border border-slate-800">
        <div className="space-y-1">
          <span className="text-xs text-slate-500 font-semibold block">Baseline Version ({reportAId})</span>
          <span className="text-2xl font-bold text-white">{scoreA.toFixed(1)}/100</span>
          <span className="text-xs font-semibold text-yellow-400 block">{bandA}</span>
        </div>

        <div className="space-y-1">
          <span className="text-xs text-slate-500 font-semibold block">Updated Version ({reportBId})</span>
          <span className="text-2xl font-bold text-white">{scoreB.toFixed(1)}/100</span>
          <span className="text-xs font-semibold text-orange-400 block">{bandB}</span>
        </div>

        <div className="space-y-1">
          <span className="text-xs text-slate-500 font-semibold block">Net Risk Delta</span>
          <span className={`text-2xl font-bold ${scoreDiff > 0 ? 'text-red-400' : 'text-emerald-400'}`}>
            {scoreDiff > 0 ? `+${scoreDiff.toFixed(1)}` : scoreDiff.toFixed(1)} pts
          </span>
          <span className="text-xs text-slate-400 block">Authoritative Risk Assessment change</span>
        </div>
      </div>

      {/* Finding Differential Summary */}
      <div className="space-y-3">
        <h4 className="text-sm font-bold text-white">Finding Differences</h4>
        <div className="p-4 bg-slate-950/40 border border-slate-800 rounded-lg space-y-2 text-xs">
          <div className="flex items-center justify-between text-slate-300">
            <span>• Added Finding: <strong className="text-white">Unencrypted Cleartext HTTP Traffic</strong></span>
            <span className="text-red-400 font-bold">+32.5 Risk Contribution</span>
          </div>
          <div className="flex items-center justify-between text-slate-300">
            <span>• Updated Finding: <strong className="text-white">Hardcoded API Credentials Observed</strong></span>
            <span className="text-indigo-300 font-bold">Severity increased LOW → HIGH</span>
          </div>
        </div>
      </div>
    </div>
  );
};
