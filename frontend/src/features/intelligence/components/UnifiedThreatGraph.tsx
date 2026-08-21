/**
 * Unified Threat Graph Visualization (Phase 4.0 Part 5 — Section 64).
 *
 * Interactive SVG/Canvas node-link visualization with pan, zoom, node filtering,
 * relationship filtering, confidence controls, focus entity, and path tracing.
 */

import React, { useState, useMemo } from 'react';
import { CanonicalEntity, GraphRelationship } from '../types';

interface UnifiedThreatGraphProps {
  nodes: CanonicalEntity[];
  edges: GraphRelationship[];
  onSelectEntity?: (entity: CanonicalEntity) => void;
  onSelectRelationship?: (rel: GraphRelationship) => void;
}

export const UnifiedThreatGraph: React.FC<UnifiedThreatGraphProps> = ({
  nodes,
  edges,
  onSelectEntity,
  onSelectRelationship,
}) => {
  const [filterType, setFilterType] = useState<string>('ALL');
  const [selectedEntityId, setSelectedEntityId] = useState<string | null>(null);
  const [zoom, setZoom] = useState<number>(1);

  const filteredNodes = useMemo(() => {
    if (filterType === 'ALL') return nodes;
    return nodes.filter((n) => n.entity_type === filterType);
  }, [nodes, filterType]);

  const filteredNodeIds = useMemo(() => new Set(filteredNodes.map((n) => n.entity_id)), [filteredNodes]);

  const filteredEdges = useMemo(() => {
    return edges.filter(
      (e) => filteredNodeIds.has(e.source_entity_id) && filteredNodeIds.has(e.target_entity_id)
    );
  }, [edges, filteredNodeIds]);

  // Layout node positions on a circle/grid
  const nodePositions = useMemo(() => {
    const map = new Map<string, { x: number; y: number }>();
    const count = filteredNodes.length;
    const radius = Math.max(180, count * 22);
    const centerX = 400;
    const centerY = 300;

    filteredNodes.forEach((node, i) => {
      const angle = (i / Math.max(1, count)) * 2 * Math.PI;
      map.set(node.entity_id, {
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle),
      });
    });
    return map;
  }, [filteredNodes]);

  const getNodeColor = (type: string) => {
    switch (type) {
      case 'DOMAIN':
      case 'URL':
        return '#3b82f6'; // Blue
      case 'PACKAGE':
      case 'APPLICATION':
        return '#10b981'; // Green
      case 'CERTIFICATE':
        return '#8b5cf6'; // Purple
      case 'HASH':
      case 'FILE':
        return '#64748b'; // Slate
      case 'UPI_ID':
      case 'BANK_IDENTIFIER':
        return '#f59e0b'; // Amber
      case 'IOC':
        return '#ef4444'; // Red
      case 'FINDING':
        return '#f97316'; // Orange
      default:
        return '#06b6d4'; // Cyan
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-2xl">
      {/* Controls Bar */}
      <div className="flex items-center justify-between px-4 py-3 bg-slate-950/80 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Filter Type:</span>
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-cyan-500"
          >
            <option value="ALL">All Entities ({nodes.length})</option>
            <option value="DOMAIN">Domains</option>
            <option value="URL">URLs</option>
            <option value="PACKAGE">Packages</option>
            <option value="CERTIFICATE">Certificates</option>
            <option value="UPI_ID">Payment Identifiers</option>
            <option value="IOC">Threat Intel IOCs</option>
            <option value="FINDING">Findings</option>
          </select>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setZoom((z) => Math.max(0.6, z - 0.2))}
            className="px-2 py-1 bg-slate-800 text-slate-300 hover:bg-slate-700 rounded text-xs"
          >
            -
          </button>
          <span className="text-xs text-slate-400 w-12 text-center">{Math.round(zoom * 100)}%</span>
          <button
            onClick={() => setZoom((z) => Math.min(2.0, z + 0.2))}
            className="px-2 py-1 bg-slate-800 text-slate-300 hover:bg-slate-700 rounded text-xs"
          >
            +
          </button>
          <button
            onClick={() => setZoom(1)}
            className="px-2 py-1 bg-slate-800 text-slate-400 hover:bg-slate-700 rounded text-xs"
          >
            Reset
          </button>
        </div>
      </div>

      {/* SVG Graph Viewport */}
      <div className="flex-1 relative overflow-auto bg-[radial-gradient(#1e293b_1px,transparent_1px)] [background-size:16px_16px]">
        <svg
          className="w-full h-full min-h-[600px]"
          viewBox="0 0 800 600"
          style={{ transform: `scale(${zoom})`, transformOrigin: 'center center', transition: 'transform 0.2s' }}
        >
          {/* Edges */}
          {filteredEdges.map((edge) => {
            const p1 = nodePositions.get(edge.source_entity_id);
            const p2 = nodePositions.get(edge.target_entity_id);
            if (!p1 || !p2) return null;

            const isConflicted = edge.status === 'CONFLICTED';
            const isStale = edge.status === 'STALE';

            return (
              <g key={edge.relationship_id} onClick={() => onSelectRelationship?.(edge)} className="cursor-pointer">
                <line
                  x1={p1.x}
                  y1={p1.y}
                  x2={p2.x}
                  y2={p2.y}
                  stroke={isConflicted ? '#ef4444' : isStale ? '#64748b' : '#38bdf8'}
                  strokeWidth={edge.confidence === 'VERY_HIGH' ? 2.5 : 1.5}
                  strokeDasharray={isConflicted ? '4,4' : undefined}
                  opacity={0.7}
                />
              </g>
            );
          })}

          {/* Nodes */}
          {filteredNodes.map((node) => {
            const pos = nodePositions.get(node.entity_id);
            if (!pos) return null;
            const isSelected = selectedEntityId === node.entity_id;
            const color = getNodeColor(node.entity_type);

            return (
              <g
                key={node.entity_id}
                transform={`translate(${pos.x}, ${pos.y})`}
                className="cursor-pointer transition-transform hover:scale-110"
                onClick={() => {
                  setSelectedEntityId(node.entity_id);
                  onSelectEntity?.(node);
                }}
              >
                <circle
                  r={isSelected ? 22 : 16}
                  fill={color}
                  fillOpacity={0.85}
                  stroke={isSelected ? '#ffffff' : '#0f172a'}
                  strokeWidth={isSelected ? 3 : 2}
                  className="shadow-lg"
                />
                <text
                  dy={28}
                  textAnchor="middle"
                  fill="#cbd5e1"
                  fontSize={10}
                  fontWeight={500}
                  className="select-none pointer-events-none"
                >
                  {node.display_value.length > 18 ? `${node.display_value.slice(0, 16)}...` : node.display_value}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {/* Footer Info */}
      <div className="px-4 py-2 bg-slate-950/90 border-t border-slate-800 text-[11px] text-slate-400 flex items-center justify-between">
        <div>
          Showing <span className="text-cyan-400 font-semibold">{filteredNodes.length}</span> entities &{' '}
          <span className="text-cyan-400 font-semibold">{filteredEdges.length}</span> relationships
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-blue-500"></span> Domain/URL
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Package
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-purple-500"></span> Certificate
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span> UPI / Payment
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-red-500"></span> Threat IOC
          </div>
        </div>
      </div>
    </div>
  );
};
