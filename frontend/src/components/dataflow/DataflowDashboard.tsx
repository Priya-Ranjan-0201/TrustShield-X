import React, { useState } from 'react';

interface DataflowPath {
  path_id: string;
  source_id: string;
  sink_id: string;
  path_nodes: string[];
  flow_classification: string;
  confidence: string;
  resolution_status: string;
}

interface DataflowMetrics {
  methods_analyzed: number;
  instructions_analyzed: number;
  sources_count: number;
  sinks_count: number;
  paths_count: number;
  taint_labels_count: number;
  unresolved_boundaries_count: number;
}

export const DataflowDashboard: React.FC<{ scanId?: string }> = ({ scanId }) => {
  const [metrics, setMetrics] = useState<DataflowMetrics>({
    methods_analyzed: 120,
    instructions_analyzed: 1440,
    sources_count: 2,
    sinks_count: 2,
    paths_count: 2,
    taint_labels_count: 2,
    unresolved_boundaries_count: 0,
  });

  const [paths, setPaths] = useState<DataflowPath[]>([
    {
      path_id: 'path_src_1_snk_1',
      source_id: 'src_location',
      sink_id: 'snk_http',
      path_nodes: ['LocationManager.getLastKnownLocation', 'JSONSerializer', 'OkHttpClient.post'],
      flow_classification: 'SOURCE_TO_NETWORK',
      confidence: 'HIGH',
      resolution_status: 'RESOLVED',
    },
    {
      path_id: 'path_src_2_snk_2',
      source_id: 'src_sms',
      sink_id: 'snk_db',
      path_nodes: ['SmsManager.receive', 'OTPParser', 'RoomDatabase.insert'],
      flow_classification: 'SOURCE_TO_STORAGE',
      confidence: 'VERY_HIGH',
      resolution_status: 'RESOLVED',
    },
  ]);

  return (
    <div className="p-6 bg-slate-900 text-white rounded-xl shadow-2xl border border-slate-800 space-y-6">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-2xl font-bold text-cyan-400">⚡ Dataflow & Information-Flow Intelligence</h2>
          <p className="text-sm text-slate-400">Static Source-to-Sink Tracking, Taint Propagation, & Security Boundary Analysis</p>
        </div>
        <span className="px-3 py-1 bg-cyan-950 text-cyan-300 border border-cyan-700 text-xs rounded-full font-mono">
          Phase 3.9 — Part 1A.21
        </span>
      </div>

      {/* Metrics Bar */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Analyzed Methods</p>
          <p className="text-2xl font-extrabold text-white">{metrics.methods_analyzed}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Data Sources</p>
          <p className="text-2xl font-extrabold text-amber-400">{metrics.sources_count}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Security Sinks</p>
          <p className="text-2xl font-extrabold text-rose-400">{metrics.sinks_count}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Source-Sink Paths</p>
          <p className="text-2xl font-extrabold text-cyan-300">{metrics.paths_count}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Taint Labels</p>
          <p className="text-2xl font-extrabold text-indigo-300">{metrics.taint_labels_count}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Unresolved Boundaries</p>
          <p className="text-2xl font-extrabold text-emerald-400">{metrics.unresolved_boundaries_count}</p>
        </div>
      </div>

      {/* Source-to-Sink Path Explorer */}
      <div className="space-y-3">
        <h3 className="text-lg font-semibold text-slate-200">Reconstructed Source-to-Sink Dataflow Paths</h3>
        <div className="overflow-x-auto rounded-lg border border-slate-800">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-400 text-xs uppercase tracking-wider">
              <tr>
                <th className="px-4 py-3">Path ID</th>
                <th className="px-4 py-3">Propagation Chain</th>
                <th className="px-4 py-3">Classification</th>
                <th className="px-4 py-3">Confidence</th>
                <th className="px-4 py-3">State</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {paths.map((p, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40">
                  <td className="px-4 py-3 font-mono text-xs text-slate-300">{p.path_id}</td>
                  <td className="px-4 py-3 font-mono text-xs text-cyan-300">
                    {p.path_nodes.join(' ➔ ')}
                  </td>
                  <td className="px-4 py-3">
                    <span className="px-2 py-0.5 text-xs rounded bg-cyan-950 text-cyan-300 border border-cyan-800">
                      {p.flow_classification}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-slate-300 font-semibold">{p.confidence}</td>
                  <td className="px-4 py-3 text-emerald-400 text-xs font-mono">{p.resolution_status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
