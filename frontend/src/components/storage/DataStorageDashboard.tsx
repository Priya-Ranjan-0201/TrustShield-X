import React, { useState } from 'react';

interface StorageLocation {
  location_path: string;
  location_type: string;
  access_permission: string;
  is_encrypted: boolean;
  source_method: string;
}

interface StorageMetrics {
  locations_count: number;
  databases_count: number;
  tables_count: number;
  queries_count: number;
  preferences_count: number;
  sensitive_locations_count: number;
}

export const DataStorageDashboard: React.FC<{ scanId?: string }> = ({ scanId }) => {
  const [metrics, setMetrics] = useState<StorageMetrics>({
    locations_count: 1,
    databases_count: 1,
    tables_count: 1,
    queries_count: 1,
    preferences_count: 1,
    sensitive_locations_count: 1,
  });

  const [locations, setLocations] = useState<StorageLocation[]>([
    {
      location_path: '/data/data/com.bank/files',
      location_type: 'INTERNAL_FILES',
      access_permission: 'READ_WRITE',
      is_encrypted: false,
      source_method: 'com.bank.StorageClient.init',
    },
    {
      location_path: '/data/data/com.bank/databases/app_vault.db',
      location_type: 'SQLITE_DATABASE',
      access_permission: 'READ_WRITE',
      is_encrypted: true,
      source_method: 'com.bank.db.RoomDatabase.build',
    },
  ]);

  return (
    <div className="p-6 bg-slate-900 text-white rounded-xl shadow-2xl border border-slate-800 space-y-6">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-2xl font-bold text-emerald-400">💾 Data Storage & Filesystem Intelligence</h2>
          <p className="text-sm text-slate-400">Static Filesystem, Room/SQLite DBs, SharedPreferences, SAF, & Data Lineage Analysis</p>
        </div>
        <span className="px-3 py-1 bg-emerald-950 text-emerald-300 border border-emerald-700 text-xs rounded-full font-mono">
          Phase 3.9 — Part 1A.20
        </span>
      </div>

      {/* Metrics Bar */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Storage Locations</p>
          <p className="text-2xl font-extrabold text-white">{metrics.locations_count}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Databases</p>
          <p className="text-2xl font-extrabold text-cyan-300">{metrics.databases_count}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Tables</p>
          <p className="text-2xl font-extrabold text-indigo-300">{metrics.tables_count}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">SQL Queries</p>
          <p className="text-2xl font-extrabold text-emerald-300">{metrics.queries_count}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Preferences</p>
          <p className="text-2xl font-extrabold text-purple-300">{metrics.preferences_count}</p>
        </div>
        <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400">Sensitive Locations</p>
          <p className="text-2xl font-extrabold text-amber-400">{metrics.sensitive_locations_count}</p>
        </div>
      </div>

      {/* Storage Locations Table */}
      <div className="space-y-3">
        <h3 className="text-lg font-semibold text-slate-200">Discovered Storage Locations</h3>
        <div className="overflow-x-auto rounded-lg border border-slate-800">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-400 text-xs uppercase tracking-wider">
              <tr>
                <th className="px-4 py-3">Location Path</th>
                <th className="px-4 py-3">Type</th>
                <th className="px-4 py-3">Access</th>
                <th className="px-4 py-3">Encryption</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {locations.map((loc, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40">
                  <td className="px-4 py-3 font-mono text-xs text-emerald-300 truncate max-w-xs">{loc.location_path}</td>
                  <td className="px-4 py-3 text-slate-200">{loc.location_type}</td>
                  <td className="px-4 py-3 text-slate-400">{loc.access_permission}</td>
                  <td className="px-4 py-3">
                    <span
                      className={`px-2 py-0.5 text-xs rounded ${
                        loc.is_encrypted ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' : 'bg-slate-800 text-slate-300'
                      }`}
                    >
                      {loc.is_encrypted ? 'Encrypted at Rest' : 'Plaintext'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
