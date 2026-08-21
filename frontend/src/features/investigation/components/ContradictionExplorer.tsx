import React from 'react';

interface ContradictionItem {
  id: string;
  finding_title: string;
  evidence_a: string;
  evidence_b: string;
  source_a: string;
  source_b: string;
  resolution_status: string;
  explanation: string;
}

interface ContradictionExplorerProps {
  contradictions?: ContradictionItem[];
}

export const ContradictionExplorer: React.FC<ContradictionExplorerProps> = ({
  contradictions = [
    {
      id: 'CONTRA_01',
      finding_title: 'Cleartext HTTP vs NetworkSecurityConfig HTTPS Enforce',
      evidence_a: 'Plaintext URL observed in DEX bytecodes: http://api.untrusted-endpoint.example.com',
      evidence_b: 'NetworkSecurityConfig XML enforces cleartextTrafficPermitted="false" for standard domains',
      source_a: 'DEX Instruction Parser',
      source_b: 'Android Manifest & Resource Parser',
      resolution_status: 'RESOLVED_OVERRIDE',
      explanation: 'App uses raw socket bypass which ignores platform NetworkSecurityConfig constraints.',
    },
  ],
}) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg space-y-6">
      <div>
        <h3 className="text-base font-bold text-white">Evidence Contradiction & Conflict Resolution</h3>
        <p className="text-xs text-slate-400">
          Transparent display of conflicting signals resolved by Evidence Consolidation Engine.
        </p>
      </div>

      <div className="space-y-4">
        {contradictions.map((c) => (
          <div key={c.id} className="bg-slate-950/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <div className="flex items-center justify-between">
              <span className="font-mono text-xs text-indigo-400 bg-indigo-950 px-2 py-0.5 rounded border border-indigo-500/20">
                {c.id}
              </span>
              <span className="px-2 py-0.5 text-xs font-semibold bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 rounded-full">
                {c.resolution_status}
              </span>
            </div>

            <h4 className="text-sm font-bold text-white">{c.finding_title}</h4>

            {/* Conflicting Evidence Side-by-Side */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div className="bg-slate-900 border border-slate-800 p-3 rounded-lg space-y-1">
                <span className="text-indigo-400 font-bold block">Signal A ({c.source_a})</span>
                <p className="text-slate-300 leading-relaxed">{c.evidence_a}</p>
              </div>
              <div className="bg-slate-900 border border-slate-800 p-3 rounded-lg space-y-1">
                <span className="text-orange-400 font-bold block">Signal B ({c.source_b})</span>
                <p className="text-slate-300 leading-relaxed">{c.evidence_b}</p>
              </div>
            </div>

            <div className="bg-indigo-950/30 border border-indigo-500/20 p-3 rounded-lg text-xs text-indigo-200">
              <strong className="text-white block mb-0.5">Authoritative Resolution Rationale:</strong>
              {c.explanation}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
