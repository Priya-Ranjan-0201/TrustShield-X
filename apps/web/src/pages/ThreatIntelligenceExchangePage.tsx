import React, { useState } from 'react';
import { 
  Globe, 
  Share2, 
  ShieldCheck, 
  AlertOctagon, 
  Lock, 
  RefreshCw, 
  EyeOff, 
  Activity, 
  CheckCircle2, 
  Database,
  Radio,
  FileCode
} from 'lucide-react';

interface FederatedIntelItem {
  id: string;
  type: string;
  identifier: string;
  scope: string;
  confidence: number;
  verification: string;
  source: string;
}

export const ThreatIntelligenceExchangePage: React.FC = () => {
  const [activeScope, setActiveScope] = useState<'my' | 'shared' | 'global' | 'sources' | 'conflicts' | 'quarantine'>('global');

  const [intelList] = useState<FederatedIntelItem[]>([
    {
      id: 'fio_99182',
      type: 'DOMAIN',
      identifier: 'fake-kyc-auth-portal.com',
      scope: 'GLOBAL',
      confidence: 0.96,
      verification: 'VERIFIED',
      source: 'Internal SOC & Partner Corroboration'
    },
    {
      id: 'fio_77124',
      type: 'APK_HASH',
      identifier: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
      scope: 'COMMUNITY',
      confidence: 0.91,
      verification: 'CORROBORATED',
      source: 'FS-ISAC STIX/TAXII 2.1'
    }
  ]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 space-y-8 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-sky-500/10 border border-sky-500/30 rounded-xl text-sky-400">
            <Globe className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
              Threat Intelligence Exchange
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-sky-500/20 text-sky-300 border border-sky-500/30 font-medium">
                Federated Network Live
              </span>
            </h1>
            <p className="text-sm text-slate-400">
              Privacy-Preserving Federated Digital Trust Graph, STIX/TAXII Feeds & Continuous Security Knowledge Evolution
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 rounded-lg text-sm transition-colors">
            <FileCode className="w-4 h-4" />
            STIX/TAXII 2.1 Sync
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition-colors shadow-lg shadow-indigo-600/20">
            <Share2 className="w-4 h-4" />
            Submit Intelligence
          </button>
        </div>
      </div>

      {/* Scope Navigation */}
      <div className="flex border-b border-slate-800 space-x-8">
        {[
          { id: 'global', label: 'Global Intelligence' },
          { id: 'shared', label: 'Trusted Shared (Partners)' },
          { id: 'my', label: 'My Private Intelligence' },
          { id: 'sources', label: 'Feed Registry & Reputation' },
          { id: 'conflicts', label: 'Intelligence Conflicts' },
          { id: 'quarantine', label: 'Quarantine & Poisoning Defense' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveScope(tab.id as any)}
            className={`pb-4 text-sm font-medium transition-colors border-b-2 ${
              activeScope === tab.id
                ? 'border-sky-500 text-sky-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Main Content */}
      <div className="space-y-4">
        {intelList.map((item) => (
          <div key={item.id} className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 hover:border-slate-700 transition-colors">
            <div className="flex items-start justify-between">
              <div>
                <div className="flex items-center gap-3">
                  <span className="px-2 py-0.5 rounded bg-slate-800 text-xs font-mono text-indigo-300">
                    {item.type}
                  </span>
                  <h3 className="text-base font-semibold text-white font-mono">{item.identifier}</h3>
                  <span className="px-2 py-0.5 text-xs font-bold rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                    {item.verification}
                  </span>
                </div>
                <div className="flex items-center gap-4 mt-3 text-xs text-slate-400">
                  <span>Scope: <strong className="text-sky-400">{item.scope}</strong></span>
                  <span>Source: <strong className="text-slate-300">{item.source}</strong></span>
                  <span className="flex items-center gap-1 text-emerald-400">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    Zero Customer PII Leaked
                  </span>
                </div>
              </div>

              <div className="text-right">
                <div className="text-xs text-slate-400">Calibrated Confidence</div>
                <div className="text-xl font-bold text-sky-400">{(item.confidence * 100).toFixed(0)}%</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ThreatIntelligenceExchangePage;
