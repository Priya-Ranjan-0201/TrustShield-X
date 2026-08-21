import React, { useState } from 'react';

interface RiskAssessment {
  risk_score: number;
  risk_band: string;
  confidence_level: string;
  evidence_sufficiency: string;
  decision_state: string;
  primary_risk_category: string;
}

export const RiskDashboard: React.FC<{ scanId?: string }> = ({ scanId }) => {
  const [assessment, setAssessment] = useState<RiskAssessment>({
    risk_score: 25.0,
    risk_band: 'LOW_RISK',
    confidence_level: 'HIGH',
    evidence_sufficiency: 'SUFFICIENT',
    decision_state: 'LOW_RISK',
    primary_risk_category: 'NETWORK_THREAT',
  });

  return (
    <div className="p-6 bg-slate-900 text-white rounded-xl shadow-2xl border border-slate-800 space-y-6">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-2xl font-bold text-rose-400">🛡️ Enterprise Cybersecurity Risk & Decision Engine</h2>
          <p className="text-sm text-slate-400">Policy-based Risk Aggregation, Evidence Sufficiency, & Explainable Assessment</p>
        </div>
        <span className="px-3 py-1 bg-rose-950 text-rose-300 border border-rose-700 text-xs rounded-full font-mono">
          Phase 3.9 — Part 1B
        </span>
      </div>

      {/* Main Score Gauge */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-800/60 p-5 rounded-lg border border-slate-700/50 flex flex-col justify-center items-center">
          <p className="text-xs text-slate-400 font-semibold uppercase tracking-wider mb-1">Cybersecurity Risk Score</p>
          <div className="text-5xl font-extrabold text-amber-400 font-mono">
            {assessment.risk_score.toFixed(1)}
            <span className="text-lg text-slate-500 font-sans">/100</span>
          </div>
          <span className="mt-2 px-3 py-0.5 text-xs font-bold rounded-full bg-amber-950 text-amber-300 border border-amber-800">
            {assessment.risk_band}
          </span>
        </div>

        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Confidence Level</p>
          <p className="text-2xl font-extrabold text-emerald-400">{assessment.confidence_level}</p>
          <p className="text-xs text-slate-400 mt-2">Evidence Sufficiency</p>
          <p className="text-base font-bold text-cyan-300">{assessment.evidence_sufficiency}</p>
        </div>

        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Decision State</p>
          <p className="text-2xl font-extrabold text-indigo-300">{assessment.decision_state}</p>
          <p className="text-xs text-slate-400 mt-2">Primary Risk Category</p>
          <p className="text-base font-bold text-purple-300">{assessment.primary_risk_category}</p>
        </div>

        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Policy Version</p>
          <p className="text-2xl font-extrabold text-slate-300">v1.0.0</p>
          <p className="text-xs text-slate-400 mt-2">Reproducibility</p>
          <p className="text-base font-bold text-emerald-400">Deterministic</p>
        </div>
      </div>

      {/* Risk Factors Explanation */}
      <div className="bg-slate-950 p-5 rounded-lg border border-slate-800 space-y-3">
        <h3 className="text-base font-semibold text-slate-200">Score Explanation & Contributing Factors</h3>
        <p className="text-sm text-slate-300 leading-relaxed">
          Application evaluated as <span className="font-bold text-amber-400">LOW_RISK</span> with score <span className="font-mono text-cyan-300">25.0/100</span> based on observed static network endpoint indicators and corroborating behavioral rule matches across independent intelligence layers.
        </p>
      </div>
    </div>
  );
};
