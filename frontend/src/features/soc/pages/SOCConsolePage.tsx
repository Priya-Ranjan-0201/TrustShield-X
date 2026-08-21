/**
 * Security Operations Center (SOC) Console Main Page (Phase 4.0 Part 7).
 */

import React, { useState, useEffect } from 'react';
import { SOCDashboard } from '../components/SOCDashboard';
import { IncidentQueue } from '../components/IncidentQueue';
import { IncidentResponseView } from '../components/IncidentResponseView';
import { socApi } from '../services/socApi';
import { SecurityIncident, SOCAlert, TriageResult, ResponsePlaybook } from '../types';

export const SOCConsolePage: React.FC = () => {
  const [incidents, setIncidents] = useState<SecurityIncident[]>([]);
  const [alerts, setAlerts] = useState<SOCAlert[]>([]);
  const [playbooks, setPlaybooks] = useState<ResponsePlaybook[]>([]);
  const [selectedIncident, setSelectedIncident] = useState<SecurityIncident | null>(null);
  const [triageResult, setTriageResult] = useState<TriageResult | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const loadData = async () => {
    try {
      const [incs, alts, pbs] = await Promise.all([
        socApi.listIncidents(),
        socApi.listAlerts(),
        socApi.listPlaybooks(),
      ]);
      setIncidents(incs);
      setAlerts(alts);
      setPlaybooks(pbs);
      setLoading(false);
    } catch {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleAssign = async (incidentId: string) => {
    await socApi.assignIncident(incidentId, 'lead_analyst@trustshield.internal');
    loadData();
  };

  const handleTriage = async (incidentId: string) => {
    const res = await socApi.triageIncident(incidentId);
    setTriageResult(res);
    loadData();
  };

  const handleCreateAction = async (actionType: string, target: string, reason: string) => {
    if (!selectedIncident) return;
    await socApi.createAction(selectedIncident.incident_id, {
      action_type: actionType,
      target,
      reason,
      requires_approval: true,
    });
    alert(`Remediation action '${actionType}' submitted for four-eyes authorization.`);
    loadData();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-slate-950 text-slate-400">
        Loading Security Operations Center (SOC) Console...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col p-6 gap-6">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-xl font-bold text-slate-100">Security Operations Center (SOC) Console</h1>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800 font-mono font-semibold">
              SOAR ACTIVE
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Automated alert correlation, evidence-backed triage, playbooks, and controlled human-in-the-loop remediation.
          </p>
        </div>

        <button
          onClick={loadData}
          className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700 shadow"
        >
          Refresh Console
        </button>
      </div>

      {/* Metrics Row */}
      <SOCDashboard incidents={incidents} alerts={alerts} />

      {/* Main Content Area */}
      {selectedIncident ? (
        <IncidentResponseView
          incident={selectedIncident}
          triage={triageResult}
          playbooks={playbooks}
          onTriage={handleTriage}
          onCreateAction={handleCreateAction}
          onClose={() => {
            setSelectedIncident(null);
            setTriageResult(null);
          }}
        />
      ) : (
        <IncidentQueue
          incidents={incidents}
          onSelectIncident={(inc) => {
            setSelectedIncident(inc);
            setTriageResult(null);
          }}
          onAssignIncident={handleAssign}
        />
      )}
    </div>
  );
};
