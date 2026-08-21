import React, { useState } from 'react';
import {
  Shield,
  AlertTriangle,
  Activity,
  Target,
  CheckCircle2,
  Clock,
  Users,
  Zap,
  Eye,
  FileSearch,
  ArrowRight,
  Lock,
  Radio,
  Gauge,
} from 'lucide-react';

export const MissionControlCenterPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'incidents' | 'crisis' | 'response' | 'recovery' | 'evidence' | 'timeline'>('overview');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 space-y-8 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400">
            <Shield className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
              Security Mission Control
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-medium">
                All Systems Operational
              </span>
            </h1>
            <p className="text-sm text-slate-400">
              Cyber Crisis Command • Incident Response Orchestration • Unified Defense Coordination
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 rounded-lg text-sm transition-colors">
            <Radio className="w-4 h-4" />
            Crisis Readiness
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg text-sm font-medium transition-colors shadow-lg shadow-red-600/20">
            <AlertTriangle className="w-4 h-4" />
            Declare Incident
          </button>
        </div>
      </div>

      {/* Top Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Active Incidents</div>
          <div className="text-3xl font-bold text-white mt-2">0</div>
          <div className="text-xs text-emerald-400 mt-1">No active incidents</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Critical Alerts</div>
          <div className="text-3xl font-bold text-white mt-2">0</div>
          <div className="text-xs text-emerald-400 mt-1">All clear</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Crisis Status</div>
          <div className="text-xl font-bold text-emerald-400 mt-2">STABLE</div>
          <div className="text-xs text-emerald-400 mt-1">No active crisis</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Services at Risk</div>
          <div className="text-3xl font-bold text-white mt-2">0</div>
          <div className="text-xs text-emerald-400 mt-1">All services healthy</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Pending Actions</div>
          <div className="text-3xl font-bold text-white mt-2">0</div>
          <div className="text-xs text-slate-400 mt-1">No pending approvals</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
          <div className="text-xs text-slate-400 font-medium">Readiness Score</div>
          <div className="text-3xl font-bold text-amber-400 mt-2">97.5</div>
          <div className="text-xs text-amber-400 mt-1">High readiness</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 space-x-8 overflow-x-auto">
        {[
          { id: 'overview', label: 'Mission Overview' },
          { id: 'incidents', label: 'Incident Command' },
          { id: 'crisis', label: 'Crisis Status' },
          { id: 'response', label: 'Response & Authorization' },
          { id: 'recovery', label: 'Recovery & Residual Risk' },
          { id: 'evidence', label: 'Evidence Room' },
          { id: 'timeline', label: 'Timeline & Decisions' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`pb-4 text-sm font-medium transition-colors border-b-2 whitespace-nowrap ${
              activeTab === tab.id
                ? 'border-red-500 text-red-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Crisis Readiness Dimensions */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6">
        <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Gauge className="w-5 h-5 text-amber-400" />
          Crisis Readiness Dimensions
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: 'Detection', score: 85, color: 'text-emerald-400' },
            { label: 'Response', score: 80, color: 'text-emerald-400' },
            { label: 'Communication', score: 75, color: 'text-amber-400' },
            { label: 'Recovery', score: 70, color: 'text-amber-400' },
            { label: 'Governance', score: 90, color: 'text-emerald-400' },
            { label: 'Control Health', score: 88, color: 'text-emerald-400' },
            { label: 'Disaster Recovery', score: 72, color: 'text-amber-400' },
            { label: 'Human Readiness', score: 65, color: 'text-amber-400' },
          ].map((dim) => (
            <div key={dim.label} className="bg-slate-800/50 rounded-lg p-4">
              <div className="text-xs text-slate-400 font-medium">{dim.label}</div>
              <div className={`text-2xl font-bold ${dim.color} mt-1`}>{dim.score}%</div>
              <div className="w-full bg-slate-700 rounded-full h-1.5 mt-2">
                <div
                  className={`h-1.5 rounded-full ${dim.score >= 80 ? 'bg-emerald-500' : 'bg-amber-500'}`}
                  style={{ width: `${dim.score}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Incident Lifecycle Pipeline */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6">
        <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Activity className="w-5 h-5 text-blue-400" />
          Incident Lifecycle Pipeline
        </h2>
        <div className="flex items-center gap-2 overflow-x-auto pb-2">
          {[
            'SIGNAL', 'DETECTION', 'CORRELATION', 'EVIDENCE', 'INCIDENT',
            'CRISIS', 'SIMULATION', 'RESPONSE', 'AUTHORIZATION', 'EXECUTION',
            'VERIFICATION', 'RECOVERY', 'LEARNING',
          ].map((stage, i, arr) => (
            <React.Fragment key={stage}>
              <div className="px-3 py-1.5 bg-slate-800 border border-slate-700 rounded-lg text-xs font-mono text-slate-300 whitespace-nowrap">
                {stage}
              </div>
              {i < arr.length - 1 && <ArrowRight className="w-4 h-4 text-slate-600 flex-shrink-0" />}
            </React.Fragment>
          ))}
        </div>
      </div>

      {/* Safety & Authorization */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6">
          <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
            <Lock className="w-4 h-4 text-indigo-400" />
            Authorization & Safety Invariants
          </h3>
          <div className="space-y-2 text-xs text-slate-300">
            {[
              'RBAC enforcement active',
              'ABAC explicit DENY precedence',
              'Four-eyes approval required for high-impact',
              'Protected targets safeguarded',
              'AI cannot override deterministic policy',
              'Tenant isolation verified',
            ].map((inv) => (
              <div key={inv} className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                {inv}
              </div>
            ))}
          </div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6">
          <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
            <Eye className="w-4 h-4 text-amber-400" />
            Evidence Classification Legend
          </h3>
          <div className="space-y-2 text-xs">
            {[
              { label: 'VERIFIED', color: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' },
              { label: 'STRONGLY_SUPPORTED', color: 'bg-blue-500/20 text-blue-400 border-blue-500/30' },
              { label: 'INFERRED', color: 'bg-indigo-500/20 text-indigo-400 border-indigo-500/30' },
              { label: 'PREDICTED', color: 'bg-amber-500/20 text-amber-400 border-amber-500/30' },
              { label: 'SIMULATED', color: 'bg-purple-500/20 text-purple-400 border-purple-500/30' },
              { label: 'UNVERIFIED', color: 'bg-slate-500/20 text-slate-400 border-slate-500/30' },
              { label: 'CONFLICTING', color: 'bg-red-500/20 text-red-400 border-red-500/30' },
            ].map((cls) => (
              <span key={cls.label} className={`inline-block px-2 py-0.5 rounded border mr-2 font-semibold ${cls.color}`}>
                {cls.label}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MissionControlCenterPage;
