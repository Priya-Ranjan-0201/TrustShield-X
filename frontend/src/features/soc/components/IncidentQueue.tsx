/**
 * Incident Queue & Triage Table (Phase 4.0 Part 7 — Section 67).
 */

import React, { useState } from 'react';
import { SecurityIncident } from '../types';

export const IncidentQueue: React.FC<{
  incidents: SecurityIncident[];
  onSelectIncident: (inc: SecurityIncident) => void;
  onAssignIncident: (incidentId: string) => void;
}> = ({ incidents, onSelectIncident, onAssignIncident }) => {
  const [filterSeverity, setFilterSeverity] = useState<string>('ALL');

  const filtered = incidents.filter((i) => {
    if (filterSeverity === 'ALL') return true;
    return i.severity === filterSeverity;
  });

  const getSeverityBadge = (sev: string) => {
    switch (sev) {
      case 'CRITICAL':
        return 'bg-rose-950 text-rose-400 border-rose-800';
      case 'HIGH':
        return 'bg-amber-950 text-amber-400 border-amber-800';
      case 'MEDIUM':
        return 'bg-blue-950 text-blue-400 border-blue-800';
      default:
        return 'bg-slate-800 text-slate-400 border-slate-700';
    }
  };

  return (
    <div className="flex flex-col gap-4 bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-3">
          <h3 className="font-semibold text-slate-100 text-sm">SOC Incident Triage Queue</h3>
          <span className="px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 font-mono text-xs">
            {filtered.length}
          </span>
        </div>

        <select
          value={filterSeverity}
          onChange={(e) => setFilterSeverity(e.target.value)}
          className="bg-slate-950 border border-slate-700 text-slate-200 text-xs rounded-lg px-2.5 py-1"
        >
          <option value="ALL">All Severities</option>
          <option value="CRITICAL">Critical</option>
          <option value="HIGH">High</option>
          <option value="MEDIUM">Medium</option>
          <option value="LOW">Low</option>
        </select>
      </div>

      <div className="flex flex-col gap-2.5 max-h-[500px] overflow-y-auto">
        {filtered.length === 0 ? (
          <div className="text-center py-10 text-xs text-slate-500">
            No incidents matching filter criteria.
          </div>
        ) : (
          filtered.map((inc) => (
            <div
              key={inc.incident_id}
              onClick={() => onSelectIncident(inc)}
              className="bg-slate-950 p-4 rounded-lg border border-slate-800 text-xs flex flex-col gap-2 cursor-pointer transition hover:border-cyan-700/60 shadow-md"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-2">
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${getSeverityBadge(inc.severity)}`}>
                    {inc.severity}
                  </span>
                  <span className="font-mono text-slate-400 font-semibold">{inc.incident_number}</span>
                  <span className="font-semibold text-slate-100 text-xs">{inc.title}</span>
                </div>
                <span className="text-[10px] text-slate-500 font-mono">
                  {new Date(inc.detected_at).toLocaleTimeString()}
                </span>
              </div>

              <p className="text-slate-400 text-[11px] line-clamp-2">{inc.description}</p>

              <div className="flex items-center justify-between border-t border-slate-800/80 pt-2 text-[11px]">
                <div className="flex items-center gap-3 text-slate-500">
                  <span>Type: <strong className="text-slate-300">{inc.incident_type}</strong></span>
                  <span>Alerts: <strong className="text-slate-300">{inc.source_alert_count}</strong></span>
                  <span>Owner: <strong className="text-cyan-400">{inc.owner_id || 'UNASSIGNED'}</strong></span>
                </div>

                <div className="flex items-center gap-2" onClick={(e) => e.stopPropagation()}>
                  {!inc.owner_id && (
                    <button
                      onClick={() => onAssignIncident(inc.incident_id)}
                      className="px-2.5 py-1 bg-cyan-700 hover:bg-cyan-600 text-white rounded text-[11px] font-medium"
                    >
                      Assign to Me
                    </button>
                  )}
                  <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-medium">
                    {inc.status}
                  </span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
