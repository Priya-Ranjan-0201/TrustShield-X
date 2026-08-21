import React, { useState } from 'react';

export interface EvidenceCard {
  card_id: string;
  category: string;
  title: string;
  observation: string;
  evidence_strength: string;
  confidence: string;
  source?: string;
  finding_reference?: string;
  provenance?: string;
}

interface EvidenceExplorerProps {
  evidenceCards: EvidenceCard[];
  onSelectEvidence?: (card: EvidenceCard) => void;
}

export const EvidenceExplorer: React.FC<EvidenceExplorerProps> = ({
  evidenceCards,
  onSelectEvidence,
}) => {
  const [selectedCard, setSelectedCard] = useState<EvidenceCard | null>(evidenceCards[0] || null);

  const getStrengthBadge = (str: string) => {
    switch (str) {
      case 'DIRECT': return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';
      case 'CORROBORATED': return 'bg-indigo-500/20 text-indigo-400 border-indigo-500/30';
      case 'INDIRECT': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      default: return 'bg-slate-500/20 text-slate-400 border-slate-500/30';
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Evidence Cards List */}
      <div className="lg:col-span-2 space-y-3">
        <h3 className="text-base font-bold text-white mb-2">Corroborated Evidence Cards ({evidenceCards.length})</h3>
        {evidenceCards.map((card) => {
          const isSelected = selectedCard?.card_id === card.card_id;
          return (
            <div
              key={card.card_id}
              onClick={() => {
                setSelectedCard(card);
                onSelectEvidence?.(card);
              }}
              className={`p-4 rounded-xl border cursor-pointer transition shadow-lg ${
                isSelected
                  ? 'bg-indigo-950/40 border-indigo-500/50'
                  : 'bg-slate-900 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs text-indigo-400 bg-indigo-950/60 px-2 py-0.5 rounded border border-indigo-500/20">
                  {card.card_id}
                </span>
                <span className={`px-2.5 py-0.5 text-xs font-bold rounded-full border ${getStrengthBadge(card.evidence_strength)}`}>
                  {card.evidence_strength}
                </span>
              </div>
              <h4 className="text-sm font-bold text-white mt-2">{card.title}</h4>
              <p className="text-xs text-slate-400 mt-1 line-clamp-2">{card.observation}</p>
              <div className="flex items-center space-x-4 mt-3 text-xs text-slate-500">
                <span>Source: <strong className="text-slate-300">{card.source || 'Core'}</strong></span>
                {card.finding_reference && (
                  <span>Linked Finding: <strong className="text-indigo-300 font-mono">{card.finding_reference}</strong></span>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Evidence Inspector Side Panel */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg h-fit">
        <h3 className="text-base font-bold text-white mb-4">Evidence Detail Inspector</h3>
        {selectedCard ? (
          <div className="space-y-4 text-sm">
            <div>
              <span className="text-xs text-slate-500 font-semibold block">Evidence Card ID</span>
              <span className="font-mono text-indigo-300 font-bold">{selectedCard.card_id}</span>
            </div>
            <div>
              <span className="text-xs text-slate-500 font-semibold block">Observation Statement</span>
              <p className="text-slate-200 mt-1 bg-slate-950/60 p-3 rounded-lg border border-slate-800 text-xs">
                {selectedCard.observation}
              </p>
            </div>
            <div className="grid grid-cols-2 gap-3 text-xs">
              <div>
                <span className="text-slate-500 font-semibold block">Evidence Strength</span>
                <span className="text-emerald-400 font-bold">{selectedCard.evidence_strength}</span>
              </div>
              <div>
                <span className="text-slate-500 font-semibold block">Confidence</span>
                <span className="text-indigo-400 font-bold">{selectedCard.confidence}</span>
              </div>
            </div>
            <div>
              <span className="text-xs text-slate-500 font-semibold block">Source Subsystem</span>
              <span className="text-slate-300 text-xs font-mono">{selectedCard.source || 'Standard Analyzer'}</span>
            </div>
            {selectedCard.provenance && (
              <div>
                <span className="text-xs text-slate-500 font-semibold block">Provenance Lineage</span>
                <span className="text-slate-400 text-xs font-mono">{selectedCard.provenance}</span>
              </div>
            )}
          </div>
        ) : (
          <div className="text-center py-12 text-slate-500 text-sm">
            Select an evidence card to inspect details.
          </div>
        )}
      </div>
    </div>
  );
};
