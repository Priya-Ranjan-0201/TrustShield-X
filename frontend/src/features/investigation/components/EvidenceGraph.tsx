import React, { useState } from 'react';
import { InvestigationGraph, GraphNode, GraphEdge } from '../types';

interface EvidenceGraphProps {
  graphData: InvestigationGraph;
  onSelectNode?: (node: GraphNode) => void;
}

export const EvidenceGraph: React.FC<EvidenceGraphProps> = ({
  graphData,
  onSelectNode,
}) => {
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [zoomLevel, setZoomLevel] = useState(1.0);

  const getNodeColor = (type: string) => {
    switch (type) {
      case 'ANALYSIS': return '#6366f1'; // Indigo
      case 'RISK_FACTOR': return '#f97316'; // Orange
      case 'FINDING': return '#ef4444'; // Red
      case 'EVIDENCE': return '#10b981'; // Emerald
      case 'IOC': return '#ec4899'; // Pink
      default: return '#94a3b8'; // Slate
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg space-y-4">
      {/* Graph Toolbar */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-base font-bold text-white">Interactive Evidence & Decision Graph</h3>
          <p className="text-xs text-slate-400">
            {graphData.total_nodes} Authoritative Nodes, {graphData.total_edges} Verified Edges
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setZoomLevel((z) => Math.min(z + 0.2, 2.0))}
            className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-xs font-bold text-slate-200 rounded border border-slate-700"
          >
            + Zoom In
          </button>
          <button
            onClick={() => setZoomLevel((z) => Math.max(z - 0.2, 0.6))}
            className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-xs font-bold text-slate-200 rounded border border-slate-700"
          >
            - Zoom Out
          </button>
          <button
            onClick={() => setZoomLevel(1.0)}
            className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-xs font-bold text-slate-200 rounded border border-slate-700"
          >
            Reset
          </button>
        </div>
      </div>

      {/* SVG Canvas */}
      <div className="relative bg-slate-950 rounded-xl border border-slate-800 h-[480px] overflow-hidden flex items-center justify-center">
        <svg
          className="w-full h-full cursor-grab active:cursor-grabbing"
          style={{ transform: `scale(${zoomLevel})`, transformOrigin: 'center center' }}
        >
          {/* Render Graph Edges */}
          {graphData.edges.map((edge, idx) => {
            const sourceIndex = graphData.nodes.findIndex((n) => n.id === edge.source);
            const targetIndex = graphData.nodes.findIndex((n) => n.id === edge.target);

            // Compute circular layout coordinates
            const total = graphData.nodes.length;
            const cx = 400;
            const cy = 240;
            const r = 160;

            const angleA = (sourceIndex >= 0 ? sourceIndex : idx) * ((2 * Math.PI) / total);
            const angleB = (targetIndex >= 0 ? targetIndex : idx + 1) * ((2 * Math.PI) / total);

            const x1 = sourceIndex === 0 ? cx : cx + r * Math.cos(angleA);
            const y1 = sourceIndex === 0 ? cy : cy + r * Math.sin(angleA);
            const x2 = targetIndex === 0 ? cx : cx + r * Math.cos(angleB);
            const y2 = targetIndex === 0 ? cy : cy + r * Math.sin(angleB);

            return (
              <line
                key={edge.id}
                x1={x1}
                y1={y1}
                x2={x2}
                y2={y2}
                stroke="#334155"
                strokeWidth="2"
                strokeDasharray={edge.resolution_status === 'PARTIAL' ? '4 4' : undefined}
              />
            );
          })}

          {/* Render Graph Nodes */}
          {graphData.nodes.map((node, idx) => {
            const total = graphData.nodes.length;
            const cx = 400;
            const cy = 240;
            const r = 160;
            const angle = idx * ((2 * Math.PI) / total);
            const x = idx === 0 ? cx : cx + r * Math.cos(angle);
            const y = idx === 0 ? cy : cy + r * Math.sin(angle);
            const isSelected = selectedNode?.id === node.id;

            return (
              <g
                key={node.id}
                onClick={() => {
                  setSelectedNode(node);
                  onSelectNode?.(node);
                }}
                className="cursor-pointer"
              >
                <circle
                  cx={x}
                  cy={y}
                  r={isSelected ? 18 : 14}
                  fill={getNodeColor(node.type)}
                  stroke={isSelected ? '#ffffff' : '#1e293b'}
                  strokeWidth={isSelected ? 3 : 2}
                />
                <text
                  x={x}
                  y={y + 26}
                  textAnchor="middle"
                  fill="#94a3b8"
                  fontSize="10"
                  fontWeight="bold"
                  className="pointer-events-none select-none"
                >
                  {node.label.length > 18 ? `${node.label.substring(0, 16)}...` : node.label}
                </text>
              </g>
            );
          })}
        </svg>

        {/* Selected Node Details Floating Overlay */}
        {selectedNode && (
          <div className="absolute bottom-4 right-4 bg-slate-900/90 backdrop-blur border border-slate-700 p-4 rounded-lg shadow-2xl max-w-sm text-xs">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{selectedNode.label}</span>
              <button
                onClick={() => setSelectedNode(null)}
                className="text-slate-400 hover:text-white"
              >
                ✕
              </button>
            </div>
            <p className="text-slate-400 font-mono">Type: {selectedNode.type}</p>
            {selectedNode.risk_contribution > 0 && (
              <p className="text-orange-400 font-semibold mt-1">
                Risk Contribution: +{selectedNode.risk_contribution.toFixed(1)}
              </p>
            )}
          </div>
        )}
      </div>

      {/* Graph Legend */}
      <div className="flex flex-wrap items-center gap-4 text-xs text-slate-400 pt-2 border-t border-slate-800">
        <div className="flex items-center space-x-1.5">
          <div className="w-3 h-3 rounded-full bg-indigo-500"></div>
          <span>Analysis Root</span>
        </div>
        <div className="flex items-center space-x-1.5">
          <div className="w-3 h-3 rounded-full bg-orange-500"></div>
          <span>Risk Factor</span>
        </div>
        <div className="flex items-center space-x-1.5">
          <div className="w-3 h-3 rounded-full bg-red-500"></div>
          <span>Finding</span>
        </div>
        <div className="flex items-center space-x-1.5">
          <div className="w-3 h-3 rounded-full bg-emerald-500"></div>
          <span>Evidence Card</span>
        </div>
        <div className="flex items-center space-x-1.5">
          <div className="w-3 h-3 rounded-full bg-pink-500"></div>
          <span>Threat IOC</span>
        </div>
      </div>
    </div>
  );
};
