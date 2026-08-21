import React, { useState } from 'react';

interface ExecSummary {
  headline: string;
  overall_assessment: string;
  primary_concern: string;
  top_findings: string[];
  risk_explanation: string;
  recommended_action: string;
  confidence_statement: string;
  limitations: string[];
}

export const TrustNarrativePanel: React.FC<{ reportId?: string }> = ({ reportId }) => {
  const [exec] = useState<ExecSummary>({
    headline: 'Digital Trust Assessment — Low Risk',
    overall_assessment: 'The analysis identified low-severity indicators. No immediate action is required.',
    primary_concern: '',
    top_findings: [],
    risk_explanation: 'Risk Score: 25.0 / 100 — Risk Band: LOW_RISK — Confidence: HIGH — Evidence Sufficiency: SUFFICIENT.',
    recommended_action: 'Continue monitoring. No immediate action is required.',
    confidence_statement: 'The assessment confidence is HIGH with sufficient evidence.',
    limitations: ['Static analysis cannot evaluate server-side dynamic payload decryption at runtime.'],
  });

  return (
    <div className="p-6 bg-slate-900 text-white rounded-xl shadow-2xl border border-slate-800 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-2xl font-bold text-violet-400">📖 Trust Narrative</h2>
          <p className="text-sm text-slate-400">Report: <span className="font-mono text-slate-300">{reportId || 'rep_sample'}</span></p>
        </div>
        <span className="px-3 py-1 bg-violet-950 text-violet-300 border border-violet-700 text-xs rounded-full font-mono">
          Phase 4.0 — Part 2
        </span>
      </div>

      {/* Executive Summary */}
      <div className="bg-gradient-to-r from-violet-950/50 to-slate-900 p-5 rounded-lg border border-violet-900/50">
        <h3 className="text-lg font-bold text-violet-300 mb-2">Executive Summary</h3>
        <p className="text-xl font-semibold text-white mb-3">{exec.headline}</p>
        <p className="text-sm text-slate-300 mb-4">{exec.overall_assessment}</p>
        <div className="bg-slate-800/60 p-3 rounded-md border border-slate-700/50 mb-3">
          <p className="text-xs text-slate-400 uppercase tracking-wider mb-1">Risk Explanation</p>
          <p className="text-sm text-amber-300 font-mono">{exec.risk_explanation}</p>
        </div>
        <p className="text-sm text-slate-300">{exec.confidence_statement}</p>
      </div>

      {/* Why This Risk? */}
      <div className="bg-slate-800/60 p-5 rounded-lg border border-slate-700/50">
        <h3 className="text-base font-semibold text-amber-300 mb-2">Why This Risk?</h3>
        <p className="text-sm text-slate-300">{exec.risk_explanation}</p>
      </div>

      {/* What Should You Do? */}
      <div className="bg-slate-800/60 p-5 rounded-lg border border-slate-700/50">
        <h3 className="text-base font-semibold text-emerald-300 mb-2">What Should You Do?</h3>
        <p className="text-sm text-slate-300">{exec.recommended_action}</p>
      </div>

      {/* Limitations */}
      <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
        <h3 className="text-sm font-semibold text-slate-400 mb-2">Limitations & Uncertainty</h3>
        <ul className="list-disc list-inside text-xs text-slate-500 space-y-1">
          {exec.limitations.map((lim, idx) => (
            <li key={idx}>{lim}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};
