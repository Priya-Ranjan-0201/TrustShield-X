/**
 * Threat Feed Health & Continuous Intelligence Admin Views (Phase 4.0 Part 6 — Sections 60-61, 96-98).
 */

import React from 'react';
import { ThreatFeedConfiguration, SecurityIncident } from '../types';

export const ThreatFeedHealthPanel: React.FC<{
  feeds: ThreatFeedConfiguration[];
  onSyncFeed: (feedId: string) => void;
}> = ({ feeds, onSyncFeed }) => {
  return (
    <div className="flex flex-col gap-4 bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <h3 className="font-semibold text-slate-100 text-sm">Threat Intelligence Feeds</h3>
        <span className="text-xs text-slate-400 font-mono">{feeds.length} feeds configured</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
        {feeds.map((feed) => (
          <div
            key={feed.feed_id}
            className="bg-slate-950 p-4 rounded-lg border border-slate-800 flex flex-col gap-3 justify-between"
          >
            <div>
              <div className="flex items-center justify-between">
                <span className="px-2 py-0.5 rounded bg-blue-950 text-blue-400 border border-blue-800 text-[10px] font-mono font-bold">
                  {feed.provider_type}
                </span>
                <span className="text-xs px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 font-medium">
                  {feed.trust_level}
                </span>
              </div>
              <h4 className="font-semibold text-slate-100 text-xs mt-2">{feed.provider_name}</h4>
              <p className="text-slate-500 font-mono text-[11px] truncate mt-0.5">{feed.endpoint}</p>
            </div>

            <div className="flex items-center justify-between border-t border-slate-800/80 pt-2.5 text-xs">
              <span className="text-slate-400 text-[11px]">Interval: {feed.poll_interval}</span>
              <button
                onClick={() => onSyncFeed(feed.feed_id)}
                className="px-3 py-1 bg-cyan-700 hover:bg-cyan-600 text-white rounded text-[11px] font-medium transition"
              >
                Sync Now
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export const IncidentOverviewPanel: React.FC<{ incidents: SecurityIncident[] }> = ({ incidents }) => {
  return (
    <div className="flex flex-col gap-4 bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <h3 className="font-semibold text-slate-100 text-sm">Active Security Incidents</h3>
        <span className="text-xs text-slate-400 font-mono">{incidents.length} incidents</span>
      </div>

      <div className="flex flex-col gap-2.5">
        {incidents.length === 0 ? (
          <div className="text-center py-6 text-xs text-slate-500">
            No active security incidents detected.
          </div>
        ) : (
          incidents.map((inc) => (
            <div
              key={inc.incident_id}
              className="bg-slate-950 p-3.5 rounded-lg border border-slate-800 text-xs flex items-center justify-between"
            >
              <div>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-800 text-[10px] font-bold">
                    {inc.priority}
                  </span>
                  <span className="font-semibold text-slate-200">{inc.title}</span>
                </div>
                <span className="text-[11px] text-slate-500 mt-1 block">
                  {inc.alert_count} alerts • {inc.entity_count} entities correlated
                </span>
              </div>
              <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-300 font-medium text-[11px]">
                {inc.status}
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
