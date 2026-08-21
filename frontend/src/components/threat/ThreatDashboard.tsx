import React, { useState } from 'react';

interface ThreatIndicator {
  indicator_id: string;
  indicator_type: string;
  normalized_value: string;
  source_module: str;
  confidence: string;
}

interface ThreatMatch {
  match_id: string;
  indicator_id: string;
  source_id: string;
  match_type: string;
  reputation: string;
  confidence: string;
  freshness_state: string;
  provenance: string;
}

interface ThreatSource {
  source_id: string;
  provider: string;
  source_type: string;
  reliability: string;
  version: string;
  status: string;
}

export const ThreatDashboard: React.FC<{ scanId?: string }> = ({ scanId }) => {
  const [indicators, setIndicators] = useState<ThreatIndicator[]>([
    {
      indicator_id: 'ind_url_1',
      indicator_type: 'URL',
      normalized_value: 'https://api.bank.com/v1/telemetry',
      source_module: 'NETWORK_INTELLIGENCE',
      confidence: 'HIGH',
    },
  ]);

  const [matches, setMatches] = useState<ThreatMatch[]>([
    {
      match_id: 'match_1',
      indicator_id: 'ind_url_1',
      source_id: 'src_internal_db',
      match_type: 'EXACT_MATCH',
      reputation: 'SUSPICIOUS_REPORTED',
      confidence: 'HIGH',
      freshness_state: 'CURRENT',
      provenance: 'TruthShield Threat Feed v2026.1',
    },
  ]);

  const [sources, setSources] = useState<ThreatSource[]>([
    {
      source_id: 'src_internal_db',
      provider: 'TruthShield Internal IOC Database',
      source_type: 'OFFLINE_DATABASE',
      reliability: 'VERY_HIGH',
      version: '2026.1',
      status: 'ACTIVE',
    },
  ]);

  return (
    <div className="p-6 bg-slate-900 text-white rounded-xl shadow-2xl border border-slate-800 space-y-6">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-2xl font-bold text-rose-400">🌐 Threat Intelligence & External Indicator Correlation</h2>
          <p className="text-sm text-slate-400">Cross-Referencing Statically Observed Indicators Against Versioned Threat Feeds</p>
        </div>
        <span className="px-3 py-1 bg-rose-950 text-rose-300 border border-rose-700 text-xs rounded-full font-mono">
          Phase 3.9 — Part 1A.23
        </span>
      </div>

      {/* Overview Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Observed Indicators</p>
          <p className="text-2xl font-extrabold text-cyan-300">{indicators.length}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Threat Intelligence Matches</p>
          <p className="text-2xl font-extrabold text-rose-400">{matches.length}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Active Feed Sources</p>
          <p className="text-2xl font-extrabold text-emerald-400">{sources.length}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Feed Freshness</p>
          <p className="text-2xl font-extrabold text-amber-300">CURRENT</p>
        </div>
      </div>

      {/* Threat Matches Table */}
      <div className="space-y-3">
        <h3 className="text-lg font-semibold text-slate-200">Threat Intelligence Matches</h3>
        <div className="overflow-x-auto rounded-lg border border-slate-800">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-400 text-xs uppercase tracking-wider">
              <tr>
                <th className="px-4 py-3">Match ID</th>
                <th className="px-4 py-3">Indicator</th>
                <th className="px-4 py-3">Match Type</th>
                <th className="px-4 py-3">Reputation Claim</th>
                <th className="px-4 py-3">Source & Provenance</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {matches.map((m, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40">
                  <td className="px-4 py-3 font-mono text-xs text-slate-300">{m.match_id}</td>
                  <td className="px-4 py-3 font-mono text-xs text-cyan-300">{m.indicator_id}</td>
                  <td className="px-4 py-3 text-xs text-amber-300 font-bold">{m.match_type}</td>
                  <td className="px-4 py-3">
                    <span className="px-2 py-0.5 text-xs rounded bg-rose-950 text-rose-300 border border-rose-800">
                      {m.reputation}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-xs text-slate-400 font-mono">{m.provenance}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
