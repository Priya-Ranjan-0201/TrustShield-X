/**
 * Real-Time Trust Monitoring & Continuous Intelligence Page (Phase 4.0 Part 6).
 */

import React, { useState, useEffect } from 'react';
import { RealTimeSecurityPanel } from '../components/RealTimeSecurityPanel';
import { SecurityAlertCenter, AlertInspector } from '../components/SecurityAlertCenter';
import { ThreatFeedHealthPanel, IncidentOverviewPanel } from '../components/ThreatFeedHealthPanel';
import { monitoringApi } from '../services/monitoringApi';
import {
  ThreatFeedConfiguration,
  SecurityAlert,
  SecurityIncident,
  IntelligenceEvent,
} from '../types';

export const ContinuousMonitoringPage: React.FC = () => {
  const [feeds, setFeeds] = useState<ThreatFeedConfiguration[]>([]);
  const [alerts, setAlerts] = useState<SecurityAlert[]>([]);
  const [incidents, setIncidents] = useState<SecurityIncident[]>([]);
  const [events, setEvents] = useState<IntelligenceEvent[]>([]);
  const [selectedAlert, setSelectedAlert] = useState<SecurityAlert | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const loadData = async () => {
    try {
      const [f, a, inc, evts] = await Promise.all([
        monitoringApi.listFeeds(),
        monitoringApi.listAlerts(),
        monitoringApi.listIncidents(),
        monitoringApi.listRealtimeEvents(),
      ]);
      setFeeds(f);
      setAlerts(a);
      setIncidents(inc);
      setEvents(evts);
      setLoading(false);
    } catch {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000); // 5s auto-refresh
    return () => clearInterval(interval);
  }, []);

  const handleSyncFeed = async (feedId: string) => {
    await monitoringApi.syncFeed(feedId);
    loadData();
  };

  const handleAcknowledge = async (alertId: string) => {
    await monitoringApi.acknowledgeAlert(alertId, 'Acknowledged from monitoring console');
    loadData();
  };

  const handleEscalate = async (alertId: string) => {
    await monitoringApi.escalateAlert(alertId, 'CRITICAL', 'Manual analyst escalation');
    loadData();
  };

  const handleSuppress = async (alertId: string) => {
    await monitoringApi.suppressAlert(alertId, 'Temporary analyst suppression');
    loadData();
  };

  const handleResolve = async (alertId: string) => {
    await monitoringApi.resolveAlert(alertId);
    loadData();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-slate-950 text-slate-400">
        Loading Continuous Trust Monitoring Platform...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col p-6 gap-6">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-xl font-bold text-slate-100">Real-Time Trust Monitoring & Continuous Intelligence</h1>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800 font-mono font-medium">
              LIVE SYSTEM
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Continuous threat feed synchronization, event-driven reassessment, alert deduplication & multi-channel notification routing.
          </p>
        </div>

        <button
          onClick={loadData}
          className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700 shadow"
        >
          Refresh Feeds & Alerts
        </button>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 flex flex-col gap-6">
          <SecurityAlertCenter
            alerts={alerts}
            onSelectAlert={setSelectedAlert}
            onAcknowledge={handleAcknowledge}
            onEscalate={handleEscalate}
            onSuppress={handleSuppress}
            onResolve={handleResolve}
          />

          <ThreatFeedHealthPanel feeds={feeds} onSyncFeed={handleSyncFeed} />
        </div>

        <div className="flex flex-col gap-6">
          {selectedAlert && (
            <AlertInspector alert={selectedAlert} onClose={() => setSelectedAlert(null)} />
          )}

          <RealTimeSecurityPanel events={events} alerts={alerts} onSelectAlert={setSelectedAlert} />

          <IncidentOverviewPanel incidents={incidents} />
        </div>
      </div>
    </div>
  );
};
