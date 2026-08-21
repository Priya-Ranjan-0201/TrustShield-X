import React, { useState } from 'react';

interface RiskFactor {
  id: string;
  title: string;
  category: string;
  contribution: number;
  confidence: string;
  evidenceStrength: string;
  supportingFindings: string[];
}

interface RiskOverviewPanelProps {
  riskScore: number;
  riskBand: string;
  confidence: string;
  evidenceSufficiency: string;
  decisionState: string;
  riskFactors?: RiskFactor[];
}

export const RiskOverviewPanel: React.FC<RiskOverviewPanelProps> = ({
  riskScore,
  riskBand,
  confidence,
  evidenceSufficiency,
  decisionState,
  riskFactors = [
    {
      id: 'RF_AUTH_01',
      title: 'Credential Exposure Risk',
      category: 'AUTHENTICATION',
      contribution: 40.0,
      confidence: 'HIGH',
      evidenceStrength: 'DIRECT',
      supportingFindings: ['Hardcoded API Key', 'Unencrypted Token Storage'],
    },
    {
      id: 'RF_NET_02',
      title: 'Insecure Cleartext Transport',
      category: 'NETWORK',
      contribution: 32.5,
      confidence: 'HIGH',
      evidenceStrength: 'DIRECT',
      supportingFindings: ['Plaintext HTTP Socket Usage'],
    },
  ],
}) => {
  const [selectedFactor, setSelectedFactor] = useState<RiskFactor | null>(null);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Left Column: Authoritative Risk Breakdown */}
      <div className="lg:col-span-2 space-y-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg">
          <h3 className="text-base font-bold text-white mb-4">Authoritative Decision Engine Verdict</h3>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 p-4 bg-slate-950/60 rounded-lg border border-slate-800/80">
            <div>
              <span className="text-xs text-slate-500 font-semibold block">Risk Score</span>
              <span className="text-2xl font-black text-white">{riskScore.toFixed(1)}/100</span>
            </div>
            <div>
              <span className="text-xs text-slate-500 font-semibold block">Risk Band</span>
              <span className="text-sm font-bold text-orange-400">{riskBand}</span>
            </div>
            <div>
              <span className="text-xs text-slate-500 font-semibold block">Confidence</span>
              <span className="text-sm font-bold text-indigo-400">{confidence}</span>
            </div>
            <div>
              <span className="text-xs text-slate-500 font-semibold block">Decision State</span>
              <span className="text-sm font-bold text-cyan-400">{decisionState}</span>
            </div>
          </div>
        </div>

        {/* Contributing Risk Factors List */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg">
          <h3 className="text-base font-bold text-white mb-4">Contributing Risk Factors</h3>
          <div className="space-y-3">
            {riskFactors.map((rf) => (
              <div
                key={rf.id}
                onClick={() => setSelectedFactor(rf)}
                className={`p-4 rounded-lg border cursor-pointer transition ${
                  selectedFactor?.id === rf.id
                    ? 'bg-indigo-950/40 border-indigo-500/50'
                    : 'bg-slate-950/40 border-slate-800/80 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <span className="px-2 py-0.5 text-xs font-mono bg-slate-800 text-slate-300 rounded">
                      {rf.id}
                    </span>
                    <span className="text-sm font-bold text-white">{rf.title}</span>
                  </div>
                  <span className="text-xs font-bold text-orange-400">+{rf.contribution.toFixed(1)} pts</span>
                </div>
                <div className="flex items-center space-x-4 mt-2 text-xs text-slate-400">
                  <span>Category: <strong className="text-slate-300">{rf.category}</strong></span>
                  <span>Strength: <strong className="text-indigo-300">{rf.evidenceStrength}</strong></span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Right Column: Risk Factor Drill-Down Inspector */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg h-fit">
        <h3 className="text-base font-bold text-white mb-4">Risk Factor Inspector</h3>
        {selectedFactor ? (
          <div className="space-y-4 text-sm">
            <div>
              <span className="text-xs text-slate-500 font-semibold block">Risk Factor ID</span>
              <span className="font-mono text-indigo-300 font-bold">{selectedFactor.id}</span>
            </div>
            <div>
              <span className="text-xs text-slate-500 font-semibold block">Title & Category</span>
              <span className="text-white font-semibold">{selectedFactor.title}</span>
              <span className="text-xs text-slate-400 block mt-0.5">{selectedFactor.category}</span>
            </div>
            <div>
              <span className="text-xs text-slate-500 font-semibold block">Risk Contribution</span>
              <span className="text-orange-400 font-bold">+{selectedFactor.contribution.toFixed(1)} to Total Risk Score</span>
            </div>
            <div>
              <span className="text-xs text-slate-500 font-semibold block">Evidence Strength</span>
              <span className="text-emerald-400 font-semibold">{selectedFactor.evidenceStrength}</span>
            </div>
            <div>
              <span className="text-xs text-slate-500 font-semibold block">Supporting Findings</span>
              <ul className="list-disc list-inside text-xs text-slate-300 space-y-1 mt-1">
                {selectedFactor.supportingFindings.map((sf, idx) => (
                  <li key={idx}>{sf}</li>
                ))}
              </ul>
            </div>
          </div>
        ) : (
          <div className="text-center py-12 text-slate-500 text-sm">
            Select a risk factor to inspect its authoritative contribution and evidence links.
          </div>
        )}
      </div>
    </div>
  );
};
