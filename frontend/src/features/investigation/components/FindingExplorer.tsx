import React, { useState } from 'react';

export interface FindingItem {
  finding_id: string;
  category: string;
  severity: string;
  title: string;
  description: string;
  confidence: string;
  risk_contribution?: number;
  evidence_ids?: string[];
}

interface FindingExplorerProps {
  findings: FindingItem[];
  onSelectFinding?: (finding: FindingItem) => void;
  onOpenEvidence?: (evidenceId: string) => void;
}

export const FindingExplorer: React.FC<FindingExplorerProps> = ({
  findings,
  onSelectFinding,
  onOpenEvidence,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [severityFilter, setSeverityFilter] = useState('ALL');
  const [categoryFilter, setCategoryFilter] = useState('ALL');
  const [expandedFindingId, setExpandedFindingId] = useState<string | null>(null);

  const filteredFindings = findings.filter((f) => {
    const matchesSearch =
      f.finding_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      f.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      f.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      f.category.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesSeverity = severityFilter === 'ALL' || f.severity === severityFilter;
    const matchesCategory = categoryFilter === 'ALL' || f.category === categoryFilter;
    return matchesSearch && matchesSeverity && matchesCategory;
  });

  const getSeverityBadge = (sev: string) => {
    switch (sev) {
      case 'CRITICAL': return 'bg-red-500/20 text-red-400 border-red-500/30';
      case 'HIGH': return 'bg-orange-500/20 text-orange-400 border-orange-500/30';
      case 'MEDIUM': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      default: return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
    }
  };

  return (
    <div className="space-y-4">
      {/* Search & Filter Header */}
      <div className="flex flex-col md:flex-row gap-3 bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg">
        <input
          type="text"
          placeholder="Search findings by ID, title, description, rule..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
        />
        <div className="flex space-x-2">
          <select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-300 focus:outline-none focus:border-indigo-500"
          >
            <option value="ALL">All Severities</option>
            <option value="CRITICAL">Critical</option>
            <option value="HIGH">High</option>
            <option value="MEDIUM">Medium</option>
            <option value="LOW">Low</option>
          </select>
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-300 focus:outline-none focus:border-indigo-500"
          >
            <option value="ALL">All Categories</option>
            <option value="AUTHENTICATION">Authentication</option>
            <option value="NETWORK">Network</option>
            <option value="STORAGE">Storage</option>
            <option value="DATAFLOW">Dataflow</option>
            <option value="BEHAVIOR">Behavior</option>
          </select>
        </div>
      </div>

      {/* Findings List */}
      <div className="space-y-3">
        {filteredFindings.length === 0 ? (
          <div className="text-center py-12 bg-slate-900 border border-slate-800 rounded-xl text-slate-500 text-sm">
            No findings match your search and filter criteria.
          </div>
        ) : (
          filteredFindings.map((f) => {
            const isExpanded = expandedFindingId === f.finding_id;
            return (
              <div
                key={f.finding_id}
                className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg transition hover:border-slate-700"
              >
                <div className="flex items-start justify-between">
                  <div className="space-y-1">
                    <div className="flex items-center space-x-3">
                      <span className="font-mono text-xs text-indigo-400 bg-indigo-950/60 px-2 py-0.5 rounded border border-indigo-500/20">
                        {f.finding_id}
                      </span>
                      <span className={`px-2 py-0.5 text-xs font-bold rounded-full border ${getSeverityBadge(f.severity)}`}>
                        {f.severity}
                      </span>
                      <span className="text-xs text-slate-400 font-semibold">{f.category}</span>
                    </div>
                    <h4 className="text-base font-bold text-white mt-1">{f.title}</h4>
                    <p className="text-sm text-slate-400">{f.description}</p>
                  </div>
                  <button
                    onClick={() => setExpandedFindingId(isExpanded ? null : f.finding_id)}
                    className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold px-2 py-1 bg-slate-800 rounded"
                  >
                    {isExpanded ? 'Collapse' : 'Details'}
                  </button>
                </div>

                {isExpanded && (
                  <div className="mt-4 pt-4 border-t border-slate-800/80 text-xs text-slate-300 space-y-2">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <span className="text-slate-500 font-semibold block">Confidence Level</span>
                        <span className="text-white font-bold">{f.confidence}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 font-semibold block">Authoritative Risk Contribution</span>
                        <span className="text-orange-400 font-bold">
                          {f.risk_contribution ? `+${f.risk_contribution.toFixed(1)} pts` : 'Evaluated by Risk Engine'}
                        </span>
                      </div>
                    </div>
                    <div className="flex space-x-2 mt-3 pt-2">
                      <button
                        onClick={() => onSelectFinding?.(f)}
                        className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded font-semibold text-xs transition"
                      >
                        Inspect in Graph
                      </button>
                    </div>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
