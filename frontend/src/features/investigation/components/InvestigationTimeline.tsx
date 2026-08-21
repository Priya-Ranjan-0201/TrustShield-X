import React, { useState } from 'react';
import { TimelineEvent } from '../types';

interface InvestigationTimelineProps {
  events: TimelineEvent[];
}

export const InvestigationTimeline: React.FC<InvestigationTimelineProps> = ({ events }) => {
  const [filterType, setFilterType] = useState('ALL');

  const filteredEvents = events.filter((e) => {
    if (filterType === 'ALL') return true;
    return e.event_type === filterType;
  });

  const getEventBadge = (type: string) => {
    switch (type) {
      case 'ANALYSIS_STARTED': return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
      case 'EVIDENCE_OBSERVED': return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';
      case 'FINDING_CREATED': return 'bg-red-500/20 text-red-400 border-red-500/30';
      case 'THREAT_MATCH': return 'bg-pink-500/20 text-pink-400 border-pink-500/30';
      case 'RISK_ASSESSMENT': return 'bg-orange-500/20 text-orange-400 border-orange-500/30';
      default: return 'bg-indigo-500/20 text-indigo-400 border-indigo-500/30';
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg space-y-6">
      {/* Header & Filter */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-base font-bold text-white">Investigation Chronology & Provenance Timeline</h3>
          <p className="text-xs text-slate-400">Total {events.length} Authoritative Timeline Records</p>
        </div>
        <select
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
          className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-300 focus:outline-none focus:border-indigo-500"
        >
          <option value="ALL">All Events</option>
          <option value="ANALYSIS_STARTED">Analysis Started</option>
          <option value="EVIDENCE_OBSERVED">Evidence Observed</option>
          <option value="FINDING_CREATED">Finding Flagged</option>
          <option value="THREAT_MATCH">Threat Matches</option>
          <option value="RISK_ASSESSMENT">Risk Evaluated</option>
          <option value="REPORT_GENERATED">Report Generated</option>
        </select>
      </div>

      {/* Timeline Stream */}
      <div className="relative border-l-2 border-slate-800 ml-4 pl-6 space-y-6">
        {filteredEvents.map((evt) => (
          <div key={evt.event_id} className="relative group">
            {/* Timeline Dot */}
            <div className="absolute -left-[31px] top-1 w-3.5 h-3.5 rounded-full bg-slate-800 border-2 border-indigo-500 group-hover:bg-indigo-500 transition"></div>

            <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-4 transition group-hover:border-slate-700">
              <div className="flex items-center justify-between">
                <span className={`px-2 py-0.5 text-xs font-semibold rounded-full border ${getEventBadge(evt.event_type)}`}>
                  {evt.event_type.replace('_', ' ')}
                </span>
                <span className="text-xs font-mono text-slate-500">
                  {new Date(evt.timestamp).toLocaleString()}
                </span>
              </div>
              <h4 className="text-sm font-bold text-white mt-2">{evt.title}</h4>
              <p className="text-xs text-slate-400 mt-1">{evt.description}</p>
              <div className="flex items-center space-x-4 mt-3 text-xs text-slate-500">
                <span>Subsystem: <strong className="text-slate-300">{evt.source_module}</strong></span>
                {evt.related_entity_id && (
                  <span>Entity Ref: <strong className="text-indigo-300 font-mono">{evt.related_entity_id}</strong></span>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
