/**
 * Governance Policy Management & Simulation Panel (Phase 4.0 Part 8 — Sections 67-68).
 */

import React, { useState } from 'react';
import { GovernancePolicy, PolicySimulation } from '../types';

export const PolicyManagement: React.FC<{
  policies: GovernancePolicy[];
  onSimulatePolicy: (policyId: string) => Promise<PolicySimulation>;
  onCreatePolicy: (name: string, rules: any[]) => void;
}> = ({ policies, onSimulatePolicy, onCreatePolicy }) => {
  const [simulationResult, setSimulationResult] = useState<PolicySimulation | null>(null);
  const [simulating, setSimulating] = useState(false);

  const handleSimulate = async (policyId: string) => {
    setSimulating(true);
    try {
      const res = await onSimulatePolicy(policyId);
      setSimulationResult(res);
    } finally {
      setSimulating(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl flex flex-col gap-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <h3 className="font-semibold text-slate-100 text-sm">Security Policies & Authorization Rules</h3>
        <span className="text-xs text-slate-400 font-mono">{policies.length} Active Policies</span>
      </div>

      {simulationResult && (
        <div className="bg-slate-950 border border-cyan-800/80 p-4 rounded-xl flex flex-col gap-2 text-xs">
          <div className="flex items-center justify-between">
            <span className="font-bold text-cyan-400">Policy Simulation Output (Zero Production Mutation)</span>
            <button onClick={() => setSimulationResult(null)} className="text-slate-500 hover:text-slate-300">
              ✕
            </button>
          </div>
          <div className="grid grid-cols-4 gap-2 text-center mt-1">
            <div className="bg-slate-900 p-2 rounded">
              <div className="text-slate-400 text-[10px]">Affected Users</div>
              <div className="text-sm font-bold text-slate-200">{simulationResult.affected_users_count}</div>
            </div>
            <div className="bg-slate-900 p-2 rounded">
              <div className="text-slate-400 text-[10px]">New Denials</div>
              <div className="text-sm font-bold text-rose-400">{simulationResult.new_denials_count}</div>
            </div>
            <div className="bg-slate-900 p-2 rounded">
              <div className="text-slate-400 text-[10px]">Approvals Req</div>
              <div className="text-sm font-bold text-amber-400">{simulationResult.new_approvals_count}</div>
            </div>
            <div className="bg-slate-900 p-2 rounded">
              <div className="text-slate-400 text-[10px]">Conflicts</div>
              <div className="text-sm font-bold text-emerald-400">{simulationResult.conflicts_detected.length}</div>
            </div>
          </div>
        </div>
      )}

      {/* Policies List */}
      <div className="flex flex-col gap-2.5 max-h-[350px] overflow-y-auto">
        {policies.map((p) => (
          <div
            key={p.policy_id}
            className="bg-slate-950 p-3.5 rounded-lg border border-slate-800 flex items-center justify-between text-xs"
          >
            <div>
              <div className="flex items-center gap-2">
                <span className="font-semibold text-slate-200">{p.name}</span>
                <span className="px-1.5 py-0.5 rounded bg-indigo-950 text-indigo-300 font-mono text-[10px]">
                  v{p.version}
                </span>
                <span className="px-1.5 py-0.5 rounded bg-slate-900 text-slate-400 text-[10px]">
                  Priority {p.priority}
                </span>
              </div>
              <div className="text-[11px] text-slate-400 mt-1">
                Type: {p.policy_type} | Rules: {p.rules.length} conditions
              </div>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => handleSimulate(p.policy_id)}
                disabled={simulating}
                className="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-cyan-300 rounded text-xs font-medium border border-slate-700"
              >
                Dry-Run Simulate
              </button>
              <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 text-[10px]">
                {p.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
