/**
 * Security Alert Center & Alert Inspector (Phase 4.0 Part 6 — Sections 57-59).
 */

import React, { useState } from 'react';
import { SecurityAlert } from '../types';

interface SecurityAlertCenterProps {
  alerts: SecurityAlert[];
  onSelectAlert: (alert: SecurityAlert) => void;
  onAcknowledge: (alertId: string) => void;
  onEscalate: (alertId: string) => void;
  onSuppress: (alertId: string) => void;
  onResolve: (alertId: string) => void;
}

export const SecurityAlertCenter: React.FC<SecurityAlertCenterProps> = ({
  alerts,
  onSelectAlert,
  onAcknowledge,
  onEscalate,
  onSuppress,
  onResolve,
}) => {
  const [filterPriority, setFilterPriority] = useState<string>('ALL');

  const filtered = alerts.filter((a) => {
    if (filterPriority === 'ALL') return true;
    return a.priority === filterPriority;
  });

  const getPriorityBadge = (priority: string) => {
    switch (priority) {
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
          <h3 className="font-semibold text-slate-100 text-sm">Security Alerts</h3>
          <span className="px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 font-mono text-xs">
            {filtered.length}
          </span>
        </div>

        <select
          value={filterPriority}
          onChange={(e) => setFilterPriority(e.target.value)}
          className="bg-slate-950 border border-slate-700 text-slate-200 text-xs rounded-lg px-2.5 py-1"
        >
          <option value="ALL">All Priorities</option>
          <option value="CRITICAL">Critical</option>
          <option value="HIGH">High</option>
          <option value="MEDIUM">Medium</option>
          <option value="LOW">Low</option>
        </select>
      </div>

      <div className="flex flex-col gap-2.5 max-h-[480px] overflow-y-auto">
        {filtered.length === 0 ? (
          <div className="text-center py-10 text-xs text-slate-500">
            No security alerts matching active filter criteria.
          </div>
        ) : (
          filtered.map((alert) => (
            <div
              key={alert.alert_id}
              onClick={() => onSelectAlert(alert)}
              className="bg-slate-950 p-3.5 rounded-lg border border-slate-800/90 text-xs flex flex-col gap-2.5 cursor-pointer transition hover:border-cyan-700/60 shadow-md"
            >
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${getPriorityBadge(alert.priority)}`}>
                      {alert.priority}
                    </span>
                    <span className="font-semibold text-slate-100 text-xs">{alert.title}</span>
                  </div>
                  <p className="text-slate-400 mt-1 text-[11px] leading-relaxed">{alert.description}</p>
                </div>
                <span className="text-[10px] text-slate-500 font-mono">
                  {new Date(alert.created_at).toLocaleTimeString()}
                </span>
              </div>

              <div className="flex items-center justify-between border-t border-slate-800/80 pt-2 text-[11px]">
                <div className="flex items-center gap-2">
                  <span className="text-slate-500">Status:</span>
                  <span className="font-medium text-slate-300">{alert.status}</span>
                </div>

                <div className="flex items-center gap-1.5" onClick={(e) => e.stopPropagation()}>
                  {alert.status === 'NEW' && (
                    <button
                      onClick={() => onAcknowledge(alert.alert_id)}
                      className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded text-[11px] font-medium"
                    >
                      Acknowledge
                    </button>
                  )}
                  {alert.priority !== 'CRITICAL' && (
                    <button
                      onClick={() => onEscalate(alert.alert_id)}
                      className="px-2.5 py-1 bg-amber-900/60 hover:bg-amber-800 text-amber-200 rounded text-[11px] font-medium border border-amber-800"
                    >
                      Escalate
                    </button>
                  )}
                  <button
                    onClick={() => onSuppress(alert.alert_id)}
                    className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-400 rounded text-[11px]"
                  >
                    Suppress
                  </button>
                  {alert.status !== 'RESOLVED' && (
                    <button
                      onClick={() => onResolve(alert.alert_id)}
                      className="px-2.5 py-1 bg-emerald-800/80 hover:bg-emerald-700 text-white rounded text-[11px] font-medium"
                    >
                      Resolve
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export const AlertInspector: React.FC<{ alert: SecurityAlert | null; onClose: () => void }> = ({
  alert,
  onClose,
}) => {
  if (!alert) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-2xl flex flex-col gap-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <h3 className="font-semibold text-slate-100 text-sm">Alert Inspector</h3>
        <button onClick={onClose} className="text-slate-400 hover:text-slate-200 text-sm">
          ✕
        </button>
      </div>

      <div className="flex flex-col gap-1">
        <span className="text-xs font-semibold text-cyan-400">{alert.title}</span>
        <p className="text-xs text-slate-300">{alert.description}</p>
      </div>

      <div className="grid grid-cols-2 gap-3 text-xs">
        <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800">
          <span className="text-slate-500 block">Priority</span>
          <span className="text-rose-400 font-bold">{alert.priority}</span>
        </div>
        <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800">
          <span className="text-slate-500 block">Severity</span>
          <span className="text-amber-400 font-semibold">{alert.severity}</span>
        </div>
        <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800">
          <span className="text-slate-500 block">Confidence</span>
          <span className="text-emerald-400 font-semibold">{alert.confidence}</span>
        </div>
        <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800">
          <span className="text-slate-500 block">Status</span>
          <span className="text-slate-200">{alert.status}</span>
        </div>
      </div>

      <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-xs flex flex-col gap-1">
        <span className="text-slate-500 font-mono text-[10px]">Alert Fingerprint</span>
        <span className="text-slate-400 font-mono break-all text-[11px]">{alert.alert_fingerprint}</span>
      </div>
    </div>
  );
};
