import React from 'react';

interface BehaviorChain {
  chain_id: string;
  title: string;
  stages: { stage: string; action: string }[];
  status: string;
  confidence: string;
}

interface BehaviorChainExplorerProps {
  chains?: BehaviorChain[];
}

export const BehaviorChainExplorer: React.FC<BehaviorChainExplorerProps> = ({
  chains = [
    {
      chain_id: 'chain_01',
      title: 'Credential Harvest & Exfiltration Behavior Chain',
      stages: [
        { stage: '1. Launch', action: 'BOOT_COMPLETED BroadcastReceiver registered in AndroidManifest' },
        { stage: '2. Persistence', action: 'Foreground Service background worker spawned' },
        { stage: '3. Collection', action: 'Read SharedPreferences / Account auth tokens' },
        { stage: '4. Processing', action: 'Base64 obfuscated payload serialization' },
        { stage: '5. Exfiltration', action: 'Cleartext HTTP socket dispatch to remote IP' },
      ],
      status: 'RESOLVED',
      confidence: 'HIGH',
    },
  ],
}) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg space-y-6">
      <div>
        <h3 className="text-base font-bold text-white">Multi-Stage Behavior Execution Chains</h3>
        <p className="text-xs text-slate-400">
          Reconstructed execution flow verified by Program Graph & Behavioral Fusion Engine.
        </p>
      </div>

      <div className="space-y-6">
        {chains.map((chain) => (
          <div key={chain.chain_id} className="bg-slate-950/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <span className="font-mono text-xs text-indigo-400 bg-indigo-950 px-2 py-0.5 rounded border border-indigo-500/20">
                  {chain.chain_id}
                </span>
                <h4 className="text-sm font-bold text-white">{chain.title}</h4>
              </div>
              <span className="px-2 py-0.5 text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-full">
                {chain.status}
              </span>
            </div>

            {/* Stages Visual Flow */}
            <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
              {chain.stages.map((stg, idx) => (
                <div key={idx} className="bg-slate-900 border border-slate-800 p-3 rounded-lg text-xs space-y-1 relative">
                  <span className="text-indigo-400 font-bold block">{stg.stage}</span>
                  <p className="text-slate-300 text-[11px] leading-relaxed">{stg.action}</p>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
