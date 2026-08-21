/**
 * Entity & Relationship Inspectors (Phase 4.0 Part 5 — Sections 65-66).
 */

import React from 'react';
import { CanonicalEntity, GraphRelationship } from '../types';

interface EntityInspectorProps {
  entity: CanonicalEntity | null;
  onClose: () => void;
}

export const EntityInspector: React.FC<EntityInspectorProps> = ({ entity, onClose }) => {
  if (!entity) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-2xl flex flex-col gap-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <span className="px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 text-xs font-mono font-semibold border border-cyan-800">
            {entity.entity_type}
          </span>
          <h3 className="font-semibold text-slate-100 text-sm">{entity.display_value}</h3>
        </div>
        <button onClick={onClose} className="text-slate-400 hover:text-slate-200 text-sm">
          ✕
        </button>
      </div>

      <div className="grid grid-cols-2 gap-3 text-xs">
        <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800/80">
          <span className="text-slate-500 block">Resolution Status</span>
          <span className="text-slate-200 font-medium">{entity.resolution_status}</span>
        </div>
        <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800/80">
          <span className="text-slate-500 block">Confidence</span>
          <span className="text-emerald-400 font-semibold">{entity.confidence}</span>
        </div>
        <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800/80">
          <span className="text-slate-500 block">Source Count</span>
          <span className="text-slate-200">{entity.source_count} observations</span>
        </div>
        <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800/80">
          <span className="text-slate-500 block">Privacy Classification</span>
          <span className="text-amber-400">{entity.privacy_classification}</span>
        </div>
      </div>

      <div className="text-xs bg-slate-950 p-3 rounded-lg border border-slate-800/80">
        <span className="text-slate-500 block mb-1 font-mono">Normalized Value Hash</span>
        <span className="text-slate-400 font-mono break-all text-[11px]">{entity.value_hash}</span>
      </div>

      {entity.aliases && entity.aliases.length > 0 && (
        <div className="text-xs">
          <span className="text-slate-400 font-semibold block mb-1.5">Known Aliases:</span>
          <div className="flex flex-wrap gap-1.5">
            {entity.aliases.map((alias, idx) => (
              <span key={idx} className="bg-slate-800 text-slate-300 px-2 py-0.5 rounded text-[11px]">
                {alias}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

interface RelationshipInspectorProps {
  relationship: GraphRelationship | null;
  onClose: () => void;
  onExplain?: (rel: GraphRelationship) => void;
}

export const RelationshipInspector: React.FC<RelationshipInspectorProps> = ({
  relationship,
  onClose,
  onExplain,
}) => {
  if (!relationship) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-2xl flex flex-col gap-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <span className="px-2 py-0.5 rounded bg-blue-950 text-blue-400 text-xs font-mono font-semibold border border-blue-800">
            {relationship.relationship_type}
          </span>
          <span className="text-xs text-slate-400">Relationship Inspector</span>
        </div>
        <button onClick={onClose} className="text-slate-400 hover:text-slate-200 text-sm">
          ✕
        </button>
      </div>

      <div className="grid grid-cols-2 gap-3 text-xs">
        <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800/80">
          <span className="text-slate-500 block">Confidence</span>
          <span className="text-cyan-400 font-semibold">{relationship.confidence}</span>
        </div>
        <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800/80">
          <span className="text-slate-500 block">Evidence Strength</span>
          <span className="text-emerald-400">{relationship.evidence_strength}</span>
        </div>
        <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800/80">
          <span className="text-slate-500 block">Correlation Method</span>
          <span className="text-slate-300 font-mono text-[11px]">{relationship.correlation_method}</span>
        </div>
        <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800/80">
          <span className="text-slate-500 block">Status</span>
          <span className="text-slate-200">{relationship.status}</span>
        </div>
      </div>

      <button
        onClick={() => onExplain?.(relationship)}
        className="w-full mt-2 py-2 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-medium text-xs rounded-lg shadow-lg"
      >
        Why are these connected? (Explain)
      </button>
    </div>
  );
};
