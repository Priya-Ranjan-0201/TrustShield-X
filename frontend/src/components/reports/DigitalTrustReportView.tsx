import React, { useState } from 'react';

interface ReportDocument {
  report_id: str;
  analysis_id: str;
  trust_overview: {
    risk_score: number;
    risk_band: string;
    confidence: string;
    evidence_sufficiency: string;
    analysis_status: string;
  };
  recommendations: string[];
}

export const DigitalTrustReportView: React.FC<{ reportId?: string }> = ({ reportId }) => {
  const [doc, setDoc] = useState<ReportDocument>({
    report_id: reportId || 'rep_sample',
    analysis_id: 'analysis_sample',
    trust_overview: {
      risk_score: 25.0,
      risk_band: 'LOW_RISK',
      confidence: 'HIGH',
      evidence_sufficiency: 'SUFFICIENT',
      analysis_status: 'COMPLETED',
    },
    recommendations: [
      'Maintain active monitoring on network communication endpoints.',
      'Enforce periodic security re-scans upon application updates.',
    ],
  });

  return (
    <div className="p-6 bg-slate-900 text-white rounded-xl shadow-2xl border border-slate-800 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-2xl font-bold text-cyan-400">🛡️ Automated Digital Trust Report</h2>
          <p className="text-sm text-slate-400">Report ID: <span className="font-mono text-slate-300">{doc.report_id}</span> | Schema: <span className="font-mono text-cyan-300">v4.0.0</span></p>
        </div>
        <span className="px-3 py-1 bg-cyan-950 text-cyan-300 border border-cyan-700 text-xs rounded-full font-mono">
          Phase 4.0 — Part 1
        </span>
      </div>

      {/* Trust Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-800/60 p-5 rounded-lg border border-slate-700/50 flex flex-col justify-center items-center">
          <p className="text-xs text-slate-400 font-semibold uppercase tracking-wider mb-1">Authoritative Risk Score</p>
          <div className="text-5xl font-extrabold text-amber-400 font-mono">
            {doc.trust_overview.risk_score.toFixed(1)}
            <span className="text-lg text-slate-500 font-sans">/100</span>
          </div>
          <span className="mt-2 px-3 py-0.5 text-xs font-bold rounded-full bg-amber-950 text-amber-300 border border-amber-800">
            {doc.trust_overview.risk_band}
          </span>
        </div>

        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Confidence Level</p>
          <p className="text-2xl font-extrabold text-emerald-400">{doc.trust_overview.confidence}</p>
          <p className="text-xs text-slate-400 mt-2">Evidence Sufficiency</p>
          <p className="text-base font-bold text-cyan-300">{doc.trust_overview.evidence_sufficiency}</p>
        </div>

        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Analysis Status</p>
          <p className="text-2xl font-extrabold text-indigo-300">{doc.trust_overview.analysis_status}</p>
          <p className="text-xs text-slate-400 mt-2">Report Version</p>
          <p className="text-base font-bold text-purple-300">v1.0.0</p>
        </div>
      </div>

      {/* Actionable Recommendations */}
      <div className="bg-slate-950 p-5 rounded-lg border border-slate-800 space-y-3">
        <h3 className="text-base font-semibold text-slate-200">Actionable Security Recommendations</h3>
        <ul className="list-disc list-inside text-sm text-slate-300 space-y-1">
          {doc.recommendations.map((rec, idx) => (
            <li key={idx}>{rec}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};
