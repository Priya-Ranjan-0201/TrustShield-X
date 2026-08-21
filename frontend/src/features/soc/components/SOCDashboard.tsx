/**
 * SOC Metrics & Real-Time Operational Dashboard (Phase 4.0 Part 7 — Section 66).
 */

import React from 'react';
import { SecurityIncident, SOCAlert } from '../types';

export const SOCDashboard: React.FC<{
  incidents: SecurityIncident[];
  alerts: SOCAlert[];
}> = ({ incidents, alerts }) => {
  const activeIncidents = incidents.filter((i) => i.status !== 'CLOSED' && i.status !== 'CANCELLED');
  const criticalIncidents = activeIncidents.filter((i) => i.severity === 'CRITICAL');
  const highIncidents = activeIncidents.filter((i) => i.severity === 'HIGH');
  const unassigned = activeIncidents.filter((i) => !i.owner_id);

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      {/* Active Incidents */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between shadow-lg">
        <div className="flex items-center justify-between">
          <span className="text-xs text-slate-400 font-medium">Active Incidents</span>
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
        </div>
        <div className="mt-2 flex items-baseline gap-2">
          <span className="text-2xl font-bold text-slate-100">{activeIncidents.length}</span>
          <span className="text-xs text-slate-500">total open</span>
        </div>
      </div>

      {/* Critical & High */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between shadow-lg">
        <div className="flex items-center justify-between">
          <span className="text-xs text-rose-400 font-medium">Critical / High</span>
          <span className="text-xs px-1.5 py-0.5 rounded bg-rose-950 text-rose-300 font-mono">SLA 15m</span>
        </div>
        <div className="mt-2 flex items-baseline gap-2">
          <span className="text-2xl font-bold text-rose-400">{criticalIncidents.length + highIncidents.length}</span>
          <span className="text-xs text-slate-500">urgent triage</span>
        </div>
      </div>

      {/* Unassigned */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between shadow-lg">
        <div className="flex items-center justify-between">
          <span className="text-xs text-amber-400 font-medium">Unassigned</span>
          <span className="text-xs px-1.5 py-0.5 rounded bg-amber-950 text-amber-300 font-mono">Action Req</span>
        </div>
        <div className="mt-2 flex items-baseline gap-2">
          <span className="text-2xl font-bold text-amber-400">{unassigned.length}</span>
          <span className="text-xs text-slate-500">pending routing</span>
        </div>
      </div>

      {/* Mean Time to Respond */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between shadow-lg">
        <div className="flex items-center justify-between">
          <span className="text-xs text-cyan-400 font-medium">MTTA / MTTR</span>
          <span className="text-xs px-1.5 py-0.5 rounded bg-cyan-950 text-cyan-300 font-mono">Telemetry</span>
        </div>
        <div className="mt-2 flex items-baseline gap-2">
          <span className="text-2xl font-bold text-cyan-300">4.2m</span>
          <span className="text-xs text-slate-500">avg containment</span>
        </div>
      </div>
    </div>
  );
};
