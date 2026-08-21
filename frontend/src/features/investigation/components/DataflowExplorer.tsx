import React from 'react';

interface DataflowPath {
  flow_id: string;
  source: string;
  transformation: string;
  sink: string;
  destination: string;
  protocol: string;
  resolution_status: string;
  confidence: string;
}

interface DataflowExplorerProps {
  flows?: DataflowPath[];
}

export const DataflowExplorer: React.FC<DataflowExplorerProps> = ({
  flows = [
    {
      flow_id: 'flow_01',
      source: 'SharedPreferences.getString("auth_token")',
      transformation: 'JSONObject.put() -> Base64.encodeToString()',
      sink: 'HttpURLConnection.getOutputStream().write()',
      destination: 'api.untrusted-endpoint.example.com:80',
      protocol: 'HTTP (Cleartext)',
      resolution_status: 'RESOLVED',
      confidence: 'HIGH',
    },
  ],
}) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg space-y-6">
      <div>
        <h3 className="text-base font-bold text-white">Source-to-Sink Information Flow Paths</h3>
        <p className="text-xs text-slate-400">
          Deterministic taint propagation traces discovered across DEX bytecodes.
        </p>
      </div>

      <div className="space-y-4">
        {flows.map((f) => (
          <div key={f.flow_id} className="bg-slate-950/60 border border-slate-800 rounded-xl p-5 space-y-4">
            <div className="flex items-center justify-between">
              <span className="font-mono text-xs text-indigo-400 bg-indigo-950 px-2 py-0.5 rounded border border-indigo-500/20">
                {f.flow_id}
              </span>
              <div className="flex items-center space-x-2">
                <span className="px-2 py-0.5 text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-full">
                  {f.resolution_status}
                </span>
                <span className="px-2 py-0.5 text-xs font-semibold bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 rounded-full">
                  {f.confidence} Confidence
                </span>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs">
              <div className="bg-slate-900 border border-slate-800 p-3 rounded-lg">
                <span className="text-slate-500 font-semibold block">Source API</span>
                <code className="text-emerald-400 block mt-1 break-all font-mono text-[11px]">{f.source}</code>
              </div>
              <div className="bg-slate-900 border border-slate-800 p-3 rounded-lg">
                <span className="text-slate-500 font-semibold block">Transformation</span>
                <code className="text-yellow-400 block mt-1 break-all font-mono text-[11px]">{f.transformation}</code>
              </div>
              <div className="bg-slate-900 border border-slate-800 p-3 rounded-lg">
                <span className="text-slate-500 font-semibold block">Sink API</span>
                <code className="text-red-400 block mt-1 break-all font-mono text-[11px]">{f.sink}</code>
              </div>
              <div className="bg-slate-900 border border-slate-800 p-3 rounded-lg">
                <span className="text-slate-500 font-semibold block">Destination & Protocol</span>
                <span className="text-white block mt-1 font-mono text-[11px]">{f.destination}</span>
                <span className="text-orange-400 text-[10px] block">{f.protocol}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
