import React, { useState, useEffect } from 'react';

interface NetworkEndpoint {
  url: str;
  scheme: str;
  host: str;
  port: number;
  is_cleartext: boolean;
  library: str;
}

interface NetworkMetrics {
  endpoints_count: number;
  domains_count: number;
  ips_count: number;
  libraries_count: number;
  cleartext_count: number;
}

export const NetworkDashboard: React.FC<{ scanId?: string }> = ({ scanId }) => {
  const [metrics, setMetrics] = useState<NetworkMetrics>({
    endpoints_count: 1,
    domains_count: 1,
    ips_count: 1,
    libraries_count: 1,
    cleartext_count: 0,
  });

  const [endpoints, setEndpoints] = useState<NetworkEndpoint[]>([
    {
      url: 'https://api.bank.com/v1/auth',
      scheme: 'https',
      host: 'api.bank.com',
      port: 443,
      is_cleartext: false,
      library: 'OkHttp',
    },
  ]);

  return (
    <div className="p-6 bg-slate-900 text-white rounded-xl shadow-2xl border border-slate-800 space-y-6">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-2xl font-bold text-cyan-400">🌐 Network Communication Intelligence</h2>
          <p className="text-sm text-slate-400">Static HTTP/HTTPS, Sockets, DNS, gRPC, MQTT, & Hardware Networking Analysis</p>
        </div>
        <span className="px-3 py-1 bg-cyan-950 text-cyan-300 border border-cyan-700 text-xs rounded-full font-mono">
          Phase 3.8 — Part 1A.19
        </span>
      </div>

      {/* Metrics Bar */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Total Endpoints</p>
          <p className="text-2xl font-extrabold text-white">{metrics.endpoints_count}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Domains</p>
          <p className="text-2xl font-extrabold text-cyan-300">{metrics.domains_count}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">IP Addresses</p>
          <p className="text-2xl font-extrabold text-indigo-300">{metrics.ips_count}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Libraries</p>
          <p className="text-2xl font-extrabold text-emerald-300">{metrics.libraries_count}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Cleartext Traffic</p>
          <p className={`text-2xl font-extrabold ${metrics.cleartext_count > 0 ? 'text-amber-400' : 'text-emerald-400'}`}>
            {metrics.cleartext_count}
          </p>
        </div>
      </div>

      {/* Endpoint Table */}
      <div className="space-y-3">
        <h3 className="text-lg font-semibold text-slate-200">Discovered Endpoints</h3>
        <div className="overflow-x-auto rounded-lg border border-slate-800">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-400 text-xs uppercase tracking-wider">
              <tr>
                <th className="px-4 py-3">URL</th>
                <th className="px-4 py-3">Host</th>
                <th className="px-4 py-3">Port</th>
                <th className="px-4 py-3">Library</th>
                <th className="px-4 py-3">TLS Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {endpoints.map((ep, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40">
                  <td className="px-4 py-3 font-mono text-xs text-cyan-300 truncate max-w-xs">{ep.url}</td>
                  <td className="px-4 py-3 text-slate-200">{ep.host}</td>
                  <td className="px-4 py-3 text-slate-400">{ep.port}</td>
                  <td className="px-4 py-3 text-slate-300">{ep.library}</td>
                  <td className="px-4 py-3">
                    <span
                      className={`px-2 py-0.5 text-xs rounded ${
                        ep.is_cleartext ? 'bg-amber-950 text-amber-300 border border-amber-800' : 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                      }`}
                    >
                      {ep.is_cleartext ? 'Cleartext HTTP' : 'Encrypted HTTPS'}
                    </span>
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
