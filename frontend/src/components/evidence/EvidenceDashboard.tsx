import React, { useState } from 'react';

interface CanonicalFinding {
  finding_id: str;
  finding_type: str;
  title: str;
  status: str;
  confidence_level: str;
  source_count: number;
  independent_source_count: number;
}

export const EvidenceDashboard: React.FC<{ scanId?: string }> = ({ scanId }) => {
  const [findings, setFindings] = useState<CanonicalFinding[]>([
    {
      finding_id: 'finding_network_telemetry',
      finding_type: 'NETWORK_ENDPOINT_OBSERVED',
      title: 'Observed Static Network Endpoint',
      status: 'CORRELATED',
      confidence_level: 'HIGH',
      source_count: 2,
      independent_source_count: 2,
    },
  ]);

  return (
    <div className="p-6 bg-slate-900 text-white rounded-xl shadow-2xl border border-slate-800 space-y-6">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-2xl font-bold text-cyan-400">🔗 Evidence Normalization & Finding Consolidation</h2>
          <p className="text-sm text-slate-400">Canonical Evidence Model, Provenance Preservation, & Confidence Fusion</p>
        </div>
        <span className="px-3 py-1 bg-cyan-950 text-cyan-300 border border-cyan-700 text-xs rounded-full font-mono">
          Phase 3.9 — Part 1A.25
        </span>
      </div>

      {/* Overview Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Canonical Findings</p>
          <p className="text-2xl font-extrabold text-cyan-300">{findings.length}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Deduplicated Evidence</p>
          <p className="text-2xl font-extrabold text-emerald-400">2</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Contradictions</p>
          <p className="text-2xl font-extrabold text-amber-400">0</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Lineage Records</p>
          <p className="text-2xl font-extrabold text-purple-400">1</p>
        </div>
      </div>

      {/* Findings Table */}
      <div className="space-y-3">
        <h3 className="text-lg font-semibold text-slate-200">Consolidated Canonical Findings</h3>
        <div className="overflow-x-auto rounded-lg border border-slate-800">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-400 text-xs uppercase tracking-wider">
              <tr>
                <th className="px-4 py-3">Finding ID</th>
                <th className="px-4 py-3">Finding Type</th>
                <th className="px-4 py-3">Title</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Confidence</th>
                <th className="px-4 py-3">Sources</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {findings.map((f, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40">
                  <td className="px-4 py-3 font-mono text-xs text-cyan-300 font-bold">{f.finding_id}</td>
                  <td className="px-4 py-3 text-xs text-slate-400">{f.finding_type}</td>
                  <td className="px-4 py-3 text-xs font-semibold text-slate-200">{f.title}</td>
                  <td className="px-4 py-3">
                    <span className="px-2 py-0.5 text-xs rounded bg-emerald-950 text-emerald-300 border border-emerald-800 font-bold">
                      {f.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-xs text-slate-300">{f.confidence_level}</td>
                  <td className="px-4 py-3 text-xs text-slate-400 font-mono">
                    {f.independent_source_count} Independent ({f.source_count} Total)
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
