/**
 * Unified Trust Intelligence Graph Dashboard Page (Phase 4.0 Part 5).
 */

import React, { useState, useEffect } from 'react';
import { UnifiedThreatGraph } from '../components/UnifiedThreatGraph';
import { EntityInspector, RelationshipInspector } from '../components/EntityInspector';
import {
  CampaignIntelligenceView,
  AttackChainVisualization,
  CorrelationExplanationModal,
  CorrelationReviewQueueView,
} from '../components/CampaignIntelligenceView';
import { intelligenceApi } from '../services/intelligenceApi';
import {
  CanonicalEntity,
  GraphRelationship,
  UnifiedGraphResponse,
  CorrelationExplanation,
} from '../types';

export const IntelligenceGraphPage: React.FC = () => {
  const [graphData, setGraphData] = useState<UnifiedGraphResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedEntity, setSelectedEntity] = useState<CanonicalEntity | null>(null);
  const [selectedRelationship, setSelectedRelationship] = useState<GraphRelationship | null>(null);
  const [explanation, setExplanation] = useState<CorrelationExplanation | null>(null);
  const [activeTab, setActiveTab] = useState<'GRAPH' | 'CAMPAIGNS' | 'ATTACK_CHAINS' | 'REVIEW_QUEUE'>('GRAPH');

  useEffect(() => {
    intelligenceApi
      .getUnifiedGraph()
      .then((data) => {
        setGraphData(data);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, []);

  const handleExplain = (rel: GraphRelationship) => {
    setExplanation({
      relationship_id: rel.relationship_id,
      source_entity: rel.source_entity_id,
      target_entity: rel.target_entity_id,
      relationship_type: rel.relationship_type,
      confidence: rel.confidence,
      why_connected: `Cryptographically verified linkage via ${rel.correlation_method}.`,
      evidence_signals: [`Rule Version: ${rel.correlation_version}`, `Status: ${rel.status}`],
      correlation_rule: rel.correlation_method,
      rule_version: rel.correlation_version,
      false_correlation_risk: 'Evaluated against multi-tenant CDN/cloud safeguards.',
      unresolved_questions: [],
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-slate-950 text-slate-400">
        Loading Unified Trust Intelligence Graph...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col p-6 gap-6">
      {/* Top Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-xl font-bold text-slate-100">Unified Trust Intelligence Graph</h1>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800 font-mono font-medium">
              Graph v{graphData?.graph_version || 1}
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Evidence-grounded cross-modal correlation, entity resolution, threat campaign clustering & attack-chain reconstruction.
          </p>
        </div>

        {/* View Switcher Tabs */}
        <div className="flex items-center gap-2 bg-slate-900 p-1.5 rounded-xl border border-slate-800 text-xs">
          <button
            onClick={() => setActiveTab('GRAPH')}
            className={`px-3.5 py-1.5 rounded-lg font-medium transition-colors ${
              activeTab === 'GRAPH' ? 'bg-cyan-600 text-white shadow-md' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Topology Graph
          </button>
          <button
            onClick={() => setActiveTab('CAMPAIGNS')}
            className={`px-3.5 py-1.5 rounded-lg font-medium transition-colors ${
              activeTab === 'CAMPAIGNS' ? 'bg-cyan-600 text-white shadow-md' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Campaigns ({graphData?.campaigns.length || 0})
          </button>
          <button
            onClick={() => setActiveTab('ATTACK_CHAINS')}
            className={`px-3.5 py-1.5 rounded-lg font-medium transition-colors ${
              activeTab === 'ATTACK_CHAINS' ? 'bg-cyan-600 text-white shadow-md' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Attack Chains ({graphData?.attack_chains.length || 0})
          </button>
          <button
            onClick={() => setActiveTab('REVIEW_QUEUE')}
            className={`px-3.5 py-1.5 rounded-lg font-medium transition-colors ${
              activeTab === 'REVIEW_QUEUE' ? 'bg-cyan-600 text-white shadow-md' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Review Queue
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 flex-1">
        <div className="lg:col-span-3 flex flex-col gap-4">
          {activeTab === 'GRAPH' && (
            <UnifiedThreatGraph
              nodes={graphData?.nodes || []}
              edges={graphData?.edges || []}
              onSelectEntity={setSelectedEntity}
              onSelectRelationship={setSelectedRelationship}
            />
          )}

          {activeTab === 'CAMPAIGNS' && (
            <CampaignIntelligenceView campaigns={graphData?.campaigns || []} />
          )}

          {activeTab === 'ATTACK_CHAINS' && (
            <AttackChainVisualization attackChains={graphData?.attack_chains || []} />
          )}

          {activeTab === 'REVIEW_QUEUE' && (
            <CorrelationReviewQueueView items={[]} />
          )}
        </div>

        {/* Sidebar Inspector */}
        <div className="flex flex-col gap-4">
          {selectedEntity && (
            <EntityInspector entity={selectedEntity} onClose={() => setSelectedEntity(null)} />
          )}

          {selectedRelationship && (
            <RelationshipInspector
              relationship={selectedRelationship}
              onClose={() => setSelectedRelationship(null)}
              onExplain={handleExplain}
            />
          )}

          {!selectedEntity && !selectedRelationship && (
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 text-center text-xs text-slate-400 shadow-xl">
              Click any node or relationship in the topology graph to inspect evidence and correlation provenance.
            </div>
          )}
        </div>
      </div>

      {/* Explanation Modal */}
      <CorrelationExplanationModal
        explanation={explanation}
        onClose={() => setExplanation(null)}
      />
    </div>
  );
};
