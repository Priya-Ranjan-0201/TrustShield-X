import React from 'react';

interface CorrelationItem {
  correlation_id: string;
  source_module: string;
  target_module: string;
  source_finding_id: string;
  target_finding_id: string;
  relationship: string;
  confidence: string;
}

interface CrossModalCorrelationPanelProps {
  correlations?: CorrelationItem[];
}

export const CrossModalCorrelationPanel: React.FC<CrossModalCorrelationPanelProps> = ({
  correlations = [
    {
      correlation_id: 'corr_01',
      source_module: 'APK_SECURITY',
      target_module: 'WEBSITE_PHISHING',
      source_finding_id: 'FIND_NET_01',
      target_finding_id: 'FIND_WEB_02',
      relationship: 'CORRELATED_DOMAIN_MATCH',
      confidence: 'HIGH',
    },
    {
      correlation_id: 'corr_02',
      source_module: 'QR_UPI',
      target_module: 'AUDIO_VOICE_CLONE',
      source_finding_id: 'FIND_UPI_03',
      target_finding_id: 'FIND_AUD_01',
      relationship: 'COORDINATED_SCAM_ATTRIBUTION',
      confidence: 'HIGH',
    },
  ],
}) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg space-y-4">
      <div>
        <h3 className="text-base font-bold text-white">Cross-Modal Security Correlations</h3>
        <p className="text-xs text-slate-400">
          Correlated findings across APK, Web, Audio, QR, Document, and Threat Intel domains.
        </p>
      </div>

      <div className="space-y-3">
        {correlations.map((c) => (
          <div key={c.correlation_id} className="bg-slate-950/60 border border-slate-800 p-4 rounded-xl flex items-center justify-between text-xs">
            <div className="flex items-center space-x-3">
              <span className="px-2 py-0.5 font-bold rounded bg-indigo-950 text-indigo-400 border border-indigo-500/20">
                {c.source_module}
              </span>
              <span className="text-slate-500">↔</span>
              <span className="px-2 py-0.5 font-bold rounded bg-orange-950 text-orange-400 border border-orange-500/20">
                {c.target_module}
              </span>
              <span className="text-slate-300 font-semibold">{c.relationship}</span>
            </div>
            <div className="flex items-center space-x-3">
              <span className="text-slate-500 font-mono">{c.source_finding_id} : {c.target_finding_id}</span>
              <span className="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 font-bold border border-emerald-500/30 text-[11px]">
                {c.confidence}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
