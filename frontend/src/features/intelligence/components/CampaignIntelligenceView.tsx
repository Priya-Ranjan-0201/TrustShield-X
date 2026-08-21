/**
 * Campaign, Attack Chain & Review Queue Views (Phase 4.0 Part 5 — Sections 67, 68, 69, 82).
 */

import React from 'react';
import { ThreatCampaign, AttackChain, CorrelationExplanation, CorrelationReviewItem } from '../types';

export const CampaignIntelligenceView: React.FC<{ campaigns: ThreatCampaign[] }> = ({ campaigns }) => {
  if (!campaigns || campaigns.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-center text-slate-400 text-sm">
        No coordinated threat campaigns detected in active graph scope.
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4">
      <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">
        Detected Threat Campaigns ({campaigns.length})
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {campaigns.map((camp) => (
          <div key={camp.campaign_id} className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col gap-3">
            <div className="flex items-start justify-between">
              <div>
                <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-800">
                  {camp.campaign_type}
                </span>
                <h4 className="text-sm font-semibold text-slate-100 mt-1">{camp.name}</h4>
              </div>
              <span className="text-xs px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 font-medium">
                {camp.confidence}
              </span>
            </div>

            <div className="grid grid-cols-3 gap-2 text-xs">
              <div className="bg-slate-950 p-2 rounded border border-slate-800/80">
                <span className="text-slate-500 block">Entities</span>
                <span className="text-slate-200 font-semibold">{camp.entity_count}</span>
              </div>
              <div className="bg-slate-950 p-2 rounded border border-slate-800/80">
                <span className="text-slate-500 block">Links</span>
                <span className="text-slate-200 font-semibold">{camp.relationship_count}</span>
              </div>
              <div className="bg-slate-950 p-2 rounded border border-slate-800/80">
                <span className="text-slate-500 block">Attribution</span>
                <span className="text-slate-400">{camp.threat_actor}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export const AttackChainVisualization: React.FC<{ attackChains: AttackChain[] }> = ({ attackChains }) => {
  if (!attackChains || attackChains.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-center text-slate-400 text-sm">
        No active attack chains reconstructed.
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-5">
      <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">
        Reconstructed Attack Chains ({attackChains.length})
      </h3>
      {attackChains.map((chain) => (
        <div key={chain.chain_id} className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col gap-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div>
              <h4 className="text-sm font-semibold text-slate-100">{chain.title}</h4>
              <span className="text-xs text-slate-400">Entry Point: {chain.entry_point}</span>
            </div>
            <span className="text-xs px-2.5 py-1 rounded bg-amber-950 text-amber-400 border border-amber-800 font-medium">
              Confidence: {chain.confidence}
            </span>
          </div>

          <div className="flex flex-col gap-3">
            {chain.steps.map((step) => {
              const isMissing = step.step_state === 'MISSING_STEP';
              const isPossible = step.step_state === 'POSSIBLE_STEP';
              return (
                <div
                  key={step.step_id}
                  className={`p-3 rounded-lg border text-xs flex items-start justify-between ${
                    isMissing
                      ? 'bg-slate-950/60 border-dashed border-slate-700 text-slate-400'
                      : isPossible
                      ? 'bg-amber-950/20 border-amber-800/60 text-amber-200'
                      : 'bg-slate-950 border-slate-800 text-slate-200'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <span className="w-5 h-5 rounded-full bg-slate-800 text-cyan-400 font-bold flex items-center justify-center text-[10px]">
                      {step.step_number}
                    </span>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-slate-100">{step.title}</span>
                        <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 font-mono">
                          {step.stage}
                        </span>
                      </div>
                      <p className="text-slate-400 mt-1">{step.description}</p>
                      {step.missing_evidence_note && (
                        <p className="text-amber-400/80 mt-1 text-[11px] italic">
                          ⚠️ {step.missing_evidence_note}
                        </p>
                      )}
                    </div>
                  </div>
                  <span className="text-[11px] font-mono font-medium text-slate-400">
                    {step.step_state}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
};

export const CorrelationExplanationModal: React.FC<{
  explanation: CorrelationExplanation | null;
  onClose: () => void;
}> = ({ explanation, onClose }) => {
  if (!explanation) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-xl max-w-lg w-full p-6 shadow-2xl flex flex-col gap-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <h3 className="font-semibold text-slate-100 text-sm">Why are these connected?</h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200 text-sm">✕</button>
        </div>

        <div className="text-xs text-slate-300 leading-relaxed bg-slate-950 p-3.5 rounded-lg border border-slate-800">
          {explanation.why_connected}
        </div>

        <div className="flex flex-col gap-2 text-xs">
          <span className="text-slate-400 font-semibold">Supporting Signals:</span>
          <ul className="list-disc list-inside text-slate-300 space-y-1">
            {explanation.evidence_signals.map((sig, idx) => (
              <li key={idx}>{sig}</li>
            ))}
          </ul>
        </div>

        <div className="bg-amber-950/20 border border-amber-800/50 p-3 rounded-lg text-xs text-amber-300">
          <span className="font-semibold block mb-0.5">False-Correlation Safeguards:</span>
          {explanation.false_correlation_risk}
        </div>

        <button
          onClick={onClose}
          className="mt-2 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium text-xs rounded-lg"
        >
          Close
        </button>
      </div>
    </div>
  );
};

export const CorrelationReviewQueueView: React.FC<{ items: CorrelationReviewItem[] }> = ({ items }) => {
  if (!items || items.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-center text-slate-400 text-sm">
        No pending correlation reviews. All relationships confirmed.
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3">
      <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">
        Analyst Correlation Review Queue ({items.length})
      </h3>
      <div className="flex flex-col gap-2">
        {items.map((item) => (
          <div key={item.review_id} className="bg-slate-900 border border-slate-800 rounded-lg p-3.5 flex items-center justify-between text-xs">
            <div>
              <span className="font-semibold text-slate-200">{item.source_entity_value}</span>
              <span className="text-slate-500 mx-2">→ ({item.relationship_type}) →</span>
              <span className="font-semibold text-slate-200">{item.target_entity_value}</span>
              <span className="block text-[11px] text-amber-400 mt-1">Flagged: {item.flag_reason}</span>
            </div>
            <div className="flex items-center gap-2">
              <button className="px-3 py-1 bg-emerald-700 hover:bg-emerald-600 text-white rounded font-medium">Confirm</button>
              <button className="px-3 py-1 bg-rose-700 hover:bg-rose-600 text-white rounded font-medium">Reject</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
