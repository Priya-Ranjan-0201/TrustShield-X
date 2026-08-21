import React from 'react';

interface ThreatIndicator {
  ioc: string;
  type: string;
  match_type: string;
  provider: string;
  freshness: 'CURRENT' | 'STALE' | 'EXPIRED' | 'UNKNOWN';
  confidence: string;
  first_seen?: string;
  last_seen?: string;
}

interface ThreatIntelligenceExplorerProps {
  indicators?: ThreatIndicator[];
}

export const ThreatIntelligenceExplorer: React.FC<ThreatIntelligenceExplorerProps> = ({
  indicators = [
    {
      ioc: 'api.untrusted-endpoint.example.com',
      type: 'DOMAIN',
      match_type: 'EXACT_DOMAIN',
      provider: 'ThreatVault Global Intelligence',
      freshness: 'CURRENT',
      confidence: 'HIGH',
      first_seen: '2026-08-01',
      last_seen: '2026-08-14',
    },
  ],
}) => {
  const getFreshnessBadge = (f: string) => {
    switch (f) {
      case 'CURRENT': return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';
      case 'STALE': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'EXPIRED': return 'bg-slate-500/20 text-slate-400 border-slate-500/30';
      default: return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg space-y-4">
      <div>
        <h3 className="text-base font-bold text-white">Threat Intelligence Corroboration</h3>
        <p className="text-xs text-slate-400">
          Normalized IOC matches cross-referenced with enterprise threat feeds.
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-950/80 text-slate-400 uppercase tracking-wider font-semibold border-b border-slate-800">
            <tr>
              <th className="px-4 py-3">Indicator (IOC)</th>
              <th className="px-4 py-3">Type</th>
              <th className="px-4 py-3">Provider</th>
              <th className="px-4 py-3">Freshness</th>
              <th className="px-4 py-3">Confidence</th>
              <th className="px-4 py-3">Observation Window</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/80">
            {indicators.map((ind, idx) => (
              <tr key={idx} className="hover:bg-slate-800/40 transition">
                <td className="px-4 py-3 font-mono font-bold text-white">{ind.ioc}</td>
                <td className="px-4 py-3 text-indigo-400">{ind.type}</td>
                <td className="px-4 py-3 text-slate-300">{ind.provider}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded-full border text-[11px] font-bold ${getFreshnessBadge(ind.freshness)}`}>
                    {ind.freshness}
                  </span>
                </td>
                <td className="px-4 py-3 text-emerald-400 font-bold">{ind.confidence}</td>
                <td className="px-4 py-3 text-slate-400">
                  {ind.first_seen} → {ind.last_seen}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
