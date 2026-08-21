/**
 * Append-Only Audit Trail & Compliance Dashboard (Phase 4.0 Part 8 — Sections 69-70).
 */

import React, { useState } from 'react';
import { AuditEvent, ComplianceFramework, ComplianceAssessment } from '../types';

export const AuditDashboard: React.FC<{
  events: AuditEvent[];
  onVerifyIntegrity: () => Promise<{ integrity_status: string }>;
}> = ({ events, onVerifyIntegrity }) => {
  const [integrityStatus, setIntegrityStatus] = useState<string | null>(null);
  const [verifying, setVerifying] = useState(false);

  const handleVerify = async () => {
    setVerifying(true);
    try {
      const res = await onVerifyIntegrity();
      setIntegrityStatus(res.integrity_status);
    } finally {
      setVerifying(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl flex flex-col gap-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2.5">
          <h3 className="font-semibold text-slate-100 text-sm">Append-Only Audit Intelligence & Hash Chain</h3>
          {integrityStatus && (
            <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
              integrityStatus === 'VERIFIED' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' : 'bg-rose-950 text-rose-400 border border-rose-800'
            }`}>
              HASH CHAIN {integrityStatus}
            </span>
          )}
        </div>

        <button
          onClick={handleVerify}
          disabled={verifying}
          className="px-3 py-1 bg-cyan-700 hover:bg-cyan-600 text-white rounded text-xs font-semibold"
        >
          {verifying ? 'Verifying Hashes...' : 'Verify Cryptographic Integrity'}
        </button>
      </div>

      <div className="flex flex-col gap-2 max-h-[300px] overflow-y-auto">
        {events.map((e) => (
          <div
            key={e.audit_id}
            className="bg-slate-950 p-3 rounded-lg border border-slate-800/80 flex items-center justify-between text-xs"
          >
            <div className="flex items-center gap-2.5">
              <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
                e.result === 'SUCCESS' ? 'bg-emerald-950 text-emerald-400' : 'bg-rose-950 text-rose-400'
              }`}>
                {e.result}
              </span>
              <span className="font-semibold text-slate-200">{e.action}</span>
              <span className="text-slate-500 font-mono text-[10px]">by {e.actor_id}</span>
            </div>

            <div className="flex items-center gap-3">
              <span className="text-slate-500 text-[10px] font-mono truncate max-w-[150px]">
                Hash: {e.event_hash.slice(0, 12)}...
              </span>
              <span className="text-slate-400 text-[10px] font-mono">
                {new Date(e.timestamp).toLocaleTimeString()}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
