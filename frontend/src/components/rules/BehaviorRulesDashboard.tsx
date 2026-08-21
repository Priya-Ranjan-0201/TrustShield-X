import React, { useState } from 'react';

interface BehaviorRule {
  rule_id: string;
  rule_version: string;
  namespace: string;
  name: string;
  description: string;
  status: string;
  severity_hint: string;
}

interface BehaviorRuleEvaluation {
  evaluation_id: string;
  rule_id: string;
  rule_version: string;
  namespace: string;
  state: string;
  confidence: string;
  evidence_provenance: string;
}

export const BehaviorRulesDashboard: React.FC<{ scanId?: string }> = ({ scanId }) => {
  const [rules, setRules] = useState<BehaviorRule[]>([
    {
      rule_id: 'RULE-DATAFLOW-001',
      rule_version: '1.0.0',
      namespace: 'DATAFLOW',
      name: 'Sensitive SMS Data Reaches Network Sink',
      description: 'Detects SMS permission and SMS API data flowing to a network endpoint.',
      status: 'ACTIVE',
      severity_hint: 'HIGH',
    },
    {
      rule_id: 'RULE-NETWORK-001',
      rule_version: '1.0.0',
      namespace: 'NETWORK',
      name: 'Static Network Endpoint Observed',
      description: 'Detects static HTTP/HTTPS network endpoint usage.',
      status: 'ACTIVE',
      severity_hint: 'MEDIUM',
    },
  ]);

  const [evaluations, setEvaluations] = useState<BehaviorRuleEvaluation[]>([
    {
      evaluation_id: 'eval_RULE-DATAFLOW-001',
      rule_id: 'RULE-DATAFLOW-001',
      rule_version: '1.0.0',
      namespace: 'DATAFLOW',
      state: 'MATCHED',
      confidence: 'HIGH',
      evidence_provenance: 'Verified Technical Evidence',
    },
    {
      evaluation_id: 'eval_RULE-NETWORK-001',
      rule_id: 'RULE-NETWORK-001',
      rule_version: '1.0.0',
      namespace: 'NETWORK',
      state: 'MATCHED',
      confidence: 'HIGH',
      evidence_provenance: 'Verified Technical Evidence',
    },
  ]);

  return (
    <div className="p-6 bg-slate-900 text-white rounded-xl shadow-2xl border border-slate-800 space-y-6">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-2xl font-bold text-amber-400">⚡ Behavior Pattern & Rule Evaluation Engine</h2>
          <p className="text-sm text-slate-400">Deterministic Evaluation of Technical Intelligence Against Declarative Rule Catalog</p>
        </div>
        <span className="px-3 py-1 bg-amber-950 text-amber-300 border border-amber-700 text-xs rounded-full font-mono">
          Phase 3.9 — Part 1A.24
        </span>
      </div>

      {/* Overview Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Rules Evaluated</p>
          <p className="text-2xl font-extrabold text-cyan-300">{rules.length}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Matched Rules</p>
          <p className="text-2xl font-extrabold text-emerald-400">
            {evaluations.filter(e => e.state === 'MATCHED').length}
          </p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Not Evaluable</p>
          <p className="text-2xl font-extrabold text-slate-400">
            {evaluations.filter(e => e.state === 'NOT_EVALUABLE').length}
          </p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Rule Pack Version</p>
          <p className="text-2xl font-extrabold text-amber-300">v1.0.0</p>
        </div>
      </div>

      {/* Rule Evaluations Table */}
      <div className="space-y-3">
        <h3 className="text-lg font-semibold text-slate-200">Rule Evaluation Findings</h3>
        <div className="overflow-x-auto rounded-lg border border-slate-800">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-400 text-xs uppercase tracking-wider">
              <tr>
                <th className="px-4 py-3">Rule ID</th>
                <th className="px-4 py-3">Namespace</th>
                <th className="px-4 py-3">Evaluation State</th>
                <th className="px-4 py-3">Confidence</th>
                <th className="px-4 py-3">Evidence Provenance</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {evaluations.map((e, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40">
                  <td className="px-4 py-3 font-mono text-xs text-amber-300 font-bold">{e.rule_id}</td>
                  <td className="px-4 py-3 text-xs text-cyan-300">{e.namespace}</td>
                  <td className="px-4 py-3">
                    <span className="px-2 py-0.5 text-xs rounded bg-emerald-950 text-emerald-300 border border-emerald-800 font-bold">
                      {e.state}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-xs text-slate-300">{e.confidence}</td>
                  <td className="px-4 py-3 text-xs text-slate-400 font-mono">{e.evidence_provenance}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
