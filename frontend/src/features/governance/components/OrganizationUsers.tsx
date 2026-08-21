/**
 * User Lifecycle & Role Management UI (Phase 4.0 Part 8 — Sections 65-66).
 */

import React, { useState } from 'react';
import { UserLifecycle, Role } from '../types';

export const OrganizationUsers: React.FC<{
  users: UserLifecycle[];
  roles: Role[];
  onInviteUser: (email: string, roles: string[], fullName: string) => void;
}> = ({ users, roles, onInviteUser }) => {
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');
  const [selectedRole, setSelectedRole] = useState('SOC_ANALYST');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      onInviteUser(email, [selectedRole], fullName);
      setEmail('');
      setFullName('');
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl flex flex-col gap-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <h3 className="font-semibold text-slate-100 text-sm">Organization Users & Access Lifecycle</h3>
        <span className="text-xs text-slate-400 font-mono">{users.length} Active Members</span>
      </div>

      {/* Invite Form */}
      <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-4 gap-3 bg-slate-950 p-3 rounded-lg border border-slate-800">
        <input
          type="email"
          placeholder="User Email (e.g. analyst@corp.in)"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-lg px-3 py-2"
          required
        />
        <input
          type="text"
          placeholder="Full Name"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          className="bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-lg px-3 py-2"
        />
        <select
          value={selectedRole}
          onChange={(e) => setSelectedRole(e.target.value)}
          className="bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-lg px-2.5 py-2"
        >
          {roles.map((r) => (
            <option key={r.role_id} value={r.name}>
              {r.name} ({r.scope})
            </option>
          ))}
        </select>
        <button
          type="submit"
          className="bg-cyan-700 hover:bg-cyan-600 text-white rounded-lg text-xs font-semibold px-4 py-2 shadow"
        >
          Invite Member
        </button>
      </form>

      {/* User Table */}
      <div className="flex flex-col gap-2 max-h-[300px] overflow-y-auto">
        {users.map((u) => (
          <div
            key={u.user_id}
            className="bg-slate-950 p-3 rounded-lg border border-slate-800/80 flex items-center justify-between text-xs"
          >
            <div className="flex items-center gap-3">
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
              <div>
                <div className="font-semibold text-slate-200">{u.email}</div>
                <div className="text-[10px] text-slate-500">{u.full_name || 'No display name'}</div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="flex gap-1.5">
                {u.roles.map((r, i) => (
                  <span key={i} className="px-2 py-0.5 rounded bg-slate-800 text-cyan-300 font-mono text-[10px]">
                    {r}
                  </span>
                ))}
              </div>
              <span className="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-400 text-[10px]">
                {u.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
