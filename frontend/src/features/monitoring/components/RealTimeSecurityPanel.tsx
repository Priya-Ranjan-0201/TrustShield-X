/**
 * Real-Time Security Stream Panel (Phase 4.0 Part 6 — Section 51).
 *
 * Displays streaming security events, live alert notifications, and feed statuses.
 */

import React from 'react';
import { IntelligenceEvent, SecurityAlert } from '../types';

interface RealTimeSecurityPanelProps {
  events: IntelligenceEvent[];
  alerts: SecurityAlert[];
  onSelectAlert?: (alert: SecurityAlert) => void;
}

export const RealTimeSecurityPanel: React.FC<RealTimeSecurityPanelProps> = ({
  events,
  alerts,
  onSelectAlert,
}) => {
  return (
    <div className="flex flex-col gap-4 bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping"></span>
          <h3 className="font-semibold text-slate-100 text-sm">Live Intelligence Stream</h3>
        </div>
        <span className="text-xs text-slate-400 font-mono">
          {events.length} events observed
        </span>
      </div>

      <div className="flex flex-col gap-2.5 max-h-[380px] overflow-y-auto pr-1">
        {events.length === 0 ? (
          <div className="text-center py-8 text-xs text-slate-500">
            Awaiting incoming threat feed synchronization events...
          </div>
        ) : (
          events.map((evt) => (
            <div
              key={evt.event_id}
              className="bg-slate-950 p-3 rounded-lg border border-slate-800/80 text-xs flex flex-col gap-1.5 transition hover:border-slate-700"
            >
              <div className="flex items-center justify-between">
                <span className="px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 font-mono font-semibold text-[10px]">
                  {evt.event_type}
                </span>
                <span className="text-slate-500 text-[10px]">
                  {new Date(evt.timestamp).toLocaleTimeString()}
                </span>
              </div>
              <p className="text-slate-300 text-[11px] leading-relaxed">
                {evt.provenance || `State transition recorded for entity ${evt.entity_id || 'UNKNOWN'}`}
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
