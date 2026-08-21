import React, { useState } from 'react';

interface BehaviorFinding {
  finding_id: string;
  finding_type: string;
  category: string;
  evidence_strength: string;
  confidence: string;
  resolution_status: string;
  summary: string;
}

interface BehaviorChain {
  chain_id: string;
  chain_type: str;
  nodes: string[];
  edges: string[];
  start_node: string;
  end_node: string;
  confidence: string;
  resolution_status: string;
}

interface BehaviorConflict {
  conflict_id: string;
  conflict_type: string;
  evidence_a: string;
  evidence_b: string;
  resolution_status: string;
}

export const BehaviorDashboard: React.FC<{ scanId?: string }> = ({ scanId }) => {
  const [findings, setFindings] = useState<BehaviorFinding[]>([
    {
      finding_id: 'find_sms_flow',
      finding_type: 'SMS_DATA_NETWORK_FLOW',
      category: 'SMS_DATA_FLOW',
      evidence_strength: 'DIRECT',
      confidence: 'HIGH',
      resolution_status: 'RESOLVED',
      summary: 'SMS-derived data has a statically supported path toward a network request.',
    },
    {
      finding_id: 'find_loc_collect',
      finding_type: 'LOCATION_COLLECTION',
      category: 'LOCATION_DATA_FLOW',
      evidence_strength: 'DIRECT',
      confidence: 'HIGH',
      resolution_status: 'RESOLVED',
      summary: 'Location data is accessed via Android Location APIs and authorized by manifest permissions.',
    },
  ]);

  const [chains, setChains] = useState<BehaviorChain[]>([
    {
      chain_id: 'chain_sms_net',
      chain_type: 'SMS_TO_NETWORK',
      nodes: ['android.permission.READ_SMS', 'SmsManager.receive', 'DataflowPath', 'OkHttpClient.post'],
      edges: ['USES_PERMISSION', 'CARRIES_DATA', 'SENDS'],
      start_node: 'android.permission.READ_SMS',
      end_node: 'OkHttpClient.post',
      confidence: 'HIGH',
      resolution_status: 'RESOLVED',
    },
  ]);

  const [conflicts, setConflicts] = useState<BehaviorConflict[]>([
    {
      conflict_id: 'conf_1',
      conflict_type: 'CONTRADICTORY_CONFIGURATION',
      evidence_a: 'Manifest: cleartextTrafficPermitted=false',
      evidence_b: 'Code: explicit http:// Endpoint reference',
      resolution_status: 'CONFLICTED',
    },
  ]);

  return (
    <div className="p-6 bg-slate-900 text-white rounded-xl shadow-2xl border border-slate-800 space-y-6">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-2xl font-bold text-amber-400">🧩 Behavioral Correlation & Intelligence Fusion</h2>
          <p className="text-sm text-slate-400">Cross-Module Multi-Source Evidence Correlation & Behavioral Chains</p>
        </div>
        <span className="px-3 py-1 bg-amber-950 text-amber-300 border border-amber-700 text-xs rounded-full font-mono">
          Phase 3.9 — Part 1A.22
        </span>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Correlated Findings</p>
          <p className="text-2xl font-extrabold text-amber-400">{findings.length}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Behavior Chains</p>
          <p className="text-2xl font-extrabold text-cyan-300">{chains.length}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Configuration Conflicts</p>
          <p className="text-2xl font-extrabold text-rose-400">{conflicts.length}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Evidence Strength</p>
          <p className="text-2xl font-extrabold text-emerald-400">DIRECT (Proven)</p>
        </div>
      </div>

      {/* Correlated Findings Table */}
      <div className="space-y-3">
        <h3 className="text-lg font-semibold text-slate-200">Evidence-Backed Behavioral Findings</h3>
        <div className="overflow-x-auto rounded-lg border border-slate-800">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-400 text-xs uppercase tracking-wider">
              <tr>
                <th className="px-4 py-3">Finding ID</th>
                <th className="px-4 py-3">Behavior Type</th>
                <th className="px-4 py-3">Category</th>
                <th className="px-4 py-3">Evidence Strength</th>
                <th className="px-4 py-3">Summary</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {findings.map((f, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40">
                  <td className="px-4 py-3 font-mono text-xs text-slate-300">{f.finding_id}</td>
                  <td className="px-4 py-3 font-bold text-amber-300">{f.finding_type}</td>
                  <td className="px-4 py-3 text-xs">{f.category}</td>
                  <td className="px-4 py-3 text-xs text-emerald-400 font-semibold">{f.evidence_strength}</td>
                  <td className="px-4 py-3 text-xs text-slate-300">{f.summary}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Multi-Stage Behavior Chains */}
      <div className="space-y-3">
        <h3 className="text-lg font-semibold text-slate-200">Multi-Stage Behavior Chains</h3>
        <div className="space-y-2">
          {chains.map((ch, idx) => (
            <div key={idx} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2">
              <div className="flex justify-between items-center">
                <span className="font-mono text-xs text-cyan-400 font-bold">{ch.chain_type} ({ch.chain_id})</span>
                <span className="px-2 py-0.5 text-xs rounded bg-emerald-950 text-emerald-300 border border-emerald-800">{ch.resolution_status}</span>
              </div>
              <p className="font-mono text-xs text-slate-300">
                {ch.nodes.join(' ➔ ')}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
