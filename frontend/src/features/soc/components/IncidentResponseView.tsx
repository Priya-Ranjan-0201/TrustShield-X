/**
 * Comprehensive Incident Response Workspace & Playbook Orchestrator (Phase 4.0 Part 7 — Sections 68-71).
 */

import React, { useState } from 'react';
import { SecurityIncident, TriageResult, ResponsePlaybook, ResponseAction } from '../types';

export const IncidentResponseView: React.FC<{
  incident: SecurityIncident;
  triage: TriageResult | null;
  playbooks: ResponsePlaybook[];
  onTriage: (incidentId: string) => void;
  onCreateAction: (actionType: string, target: string, reason: string) => void;
  onClose: () => void;
}> = ({ incident, triage, playbooks, onTriage, onCreateAction, onClose }) => {
  const [selectedActionType, setSelectedActionType] = useState<string>('BLOCK_DOMAIN');
  const [targetInput, setTargetInput] = useState<string>('');
  const [reasonInput, setReasonInput] = useState<string>('Identified malicious asset during SOC triage');

  const matchingPlaybook = playbooks.find((p) => p.incident_types.includes(incident.incident_type));

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-2xl flex flex-col gap-6">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="px-2.5 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-800 font-bold text-xs">
              {incident.severity}
            </span>
            <span className="font-mono text-cyan-400 font-bold text-sm">{incident.incident_number}</span>
            <h2 className="text-base font-bold text-slate-100">{incident.title}</h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">{incident.description}</p>
        </div>
        <button onClick={onClose} className="text-slate-400 hover:text-slate-200 text-base">
          ✕
        </button>
      </div>

      {/* Overview Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
        <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
          <span className="text-slate-500 block">Incident Type</span>
          <span className="text-slate-200 font-semibold">{incident.incident_type}</span>
        </div>
        <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
          <span className="text-slate-500 block">Status</span>
          <span className="text-cyan-400 font-semibold">{incident.status}</span>
        </div>
        <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
          <span className="text-slate-500 block">Owner</span>
          <span className="text-slate-200">{incident.owner_id || 'UNASSIGNED'}</span>
        </div>
        <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
          <span className="text-slate-500 block">Correlated Alerts</span>
          <span className="text-amber-400 font-bold">{incident.source_alert_count}</span>
        </div>
      </div>

      {/* Automated Triage Section */}
      <div className="bg-slate-950 border border-slate-800/90 rounded-xl p-4 flex flex-col gap-3">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-slate-200 text-xs">Automated Triage & Assessment</h3>
          {!triage && (
            <button
              onClick={() => onTriage(incident.incident_id)}
              className="px-3 py-1 bg-cyan-700 hover:bg-cyan-600 text-white rounded text-xs font-medium"
            >
              Run AI Triage
            </button>
          )}
        </div>

        {triage ? (
          <div className="flex flex-col gap-2.5 text-xs text-slate-300">
            <p className="bg-slate-900 p-3 rounded border border-slate-800 leading-relaxed text-[11px]">
              {triage.summary}
            </p>

            {triage.uncertainties.length > 0 && (
              <div className="bg-amber-950/40 border border-amber-800/80 p-2.5 rounded text-[11px] text-amber-300">
                <strong>Identified Uncertainties:</strong>
                <ul className="list-disc ml-4 mt-1">
                  {triage.uncertainties.map((u, i) => (
                    <li key={i}>{u}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ) : (
          <p className="text-xs text-slate-500 italic">No triage run yet. Click 'Run AI Triage' to evaluate.</p>
        )}
      </div>

      {/* Response Action Dispatcher */}
      <div className="bg-slate-950 border border-slate-800/90 rounded-xl p-4 flex flex-col gap-3">
        <h3 className="font-semibold text-slate-200 text-xs">Remediation & Containment Dispatch</h3>
        <p className="text-[11px] text-slate-400">
          High-impact actions (blocking domains/IPs, isolating devices) require explicit human-in-the-loop authorization.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <select
            value={selectedActionType}
            onChange={(e) => setSelectedActionType(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-lg px-2.5 py-2"
          >
            <option value="BLOCK_DOMAIN">BLOCK_DOMAIN (DNS Sinkhole)</option>
            <option value="BLOCK_IP">BLOCK_IP (Firewall Drop)</option>
            <option value="QUARANTINE_FILE">QUARANTINE_FILE (EDR Vault)</option>
            <option value="ISOLATE_DEVICE">ISOLATE_DEVICE (NAC VLAN)</option>
            <option value="REVOKE_TOKEN">REVOKE_TOKEN (IAM Invalidation)</option>
            <option value="COLLECT_EVIDENCE">COLLECT_EVIDENCE (Forensics)</option>
          </select>

          <input
            type="text"
            placeholder="Target (e.g. phishing-bank.in)"
            value={targetInput}
            onChange={(e) => setTargetInput(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-lg px-3 py-2"
          />

          <button
            onClick={() => {
              if (targetInput) {
                onCreateAction(selectedActionType, targetInput, reasonInput);
                setTargetInput('');
              }
            }}
            className="px-4 py-2 bg-rose-800 hover:bg-rose-700 text-white rounded-lg text-xs font-semibold shadow"
          >
            Submit for Authorization
          </button>
        </div>
      </div>
    </div>
  );
};
