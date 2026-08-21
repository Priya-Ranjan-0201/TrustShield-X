import React, { useState } from 'react';
import { 
  ShieldCheck, ShieldAlert, KeyRound, Smartphone, Laptop, 
  Network, Globe, AlertTriangle, Crosshair, Sparkles, 
  Lock, CheckCircle2, XCircle, RefreshCw, Layers, 
  Terminal, UserCheck, Activity, Shield, Radar,
  Database, Server, Cpu, FileText, ArrowRight, Eye,
  Sliders, ShieldX, Clock, Link, Check, Search, Filter,
  Share2, Zap, AlertCircle, Compass, HardDrive, CornerDownRight
} from 'lucide-react';

export const ZeroTrustExposurePage: React.FC = () => {
  type NavTab = 
    | 'trust_overview'
    | 'identities'
    | 'devices'
    | 'sessions'
    | 'access_decisions'
    | 'policies'
    | 'asset_inventory'
    | 'external_attack_surface'
    | 'exposures'
    | 'vulnerabilities'
    | 'attack_paths'
    | 'crown_jewels'
    | 'exposure_drift'
    | 'remediation'
    | 'security_graph';

  const [activeTab, setActiveTab] = useState<NavTab>('trust_overview');
  
  const [evaluating, setEvaluating] = useState(false);
  const [lastDecision, setLastDecision] = useState<{
    decision: string;
    reason: string;
    subject: string;
    resource: string;
    confidence: number;
    violated_condition?: string;
  } | null>({
    decision: 'ALLOW',
    reason: 'FULL_ZERO_TRUST_VERIFIED',
    subject: 'secops-lead@truthshield.io',
    resource: 'DB-MAIN-CORE-VAULT',
    confidence: 0.99
  });

  const handleSimulateEvaluation = async (scenario: 'compromised' | 'anomalous' | 'clean' | 'breakglass') => {
    setEvaluating(true);
    try {
      await new Promise(r => setTimeout(r, 450));
      if (scenario === 'compromised') {
        setLastDecision({
          decision: 'QUARANTINE',
          reason: 'COMPROMISED_ENTITY_DETECTED (Jailbroken mobile device with active keylogger hook)',
          subject: 'analyst-temp@truthshield.io',
          resource: 'DB-MAIN-CORE-VAULT',
          confidence: 1.0,
          violated_condition: 'INTEGRITY_COMPROMISE_FLAG_SET'
        });
      } else if (scenario === 'anomalous') {
        setLastDecision({
          decision: 'STEP_UP',
          reason: 'STEP_UP_AUTHENTICATION_REQUIRED (Impossible travel anomaly detected: Delhi &rarr; Frankfurt in 10 mins)',
          subject: 'engineer-01@truthshield.io',
          resource: 'K8S-CLUSTER-PROD',
          confidence: 0.92,
          violated_condition: 'CONDITIONAL_TRUST_OR_ELEVATED_RISK'
        });
      } else if (scenario === 'breakglass') {
        setLastDecision({
          decision: 'ALLOW',
          reason: 'BREAK_GLASS_ACCESS_VERIFIED (Dual-signed approval + Hardware FIDO2 + SHA-256 Audit Trail)',
          subject: 'incident-commander@truthshield.io',
          resource: 'ALL_INFRA_ROOT',
          confidence: 0.99,
          violated_condition: 'MANDATORY_EMERGENCY_REVIEW_SCHEDULED'
        });
      } else {
        setLastDecision({
          decision: 'ALLOW',
          reason: 'FULL_ZERO_TRUST_VERIFIED (mTLS 1.3, BitLocker active, EDR healthy, MFA confirmed)',
          subject: 'alice-secops@truthshield.io',
          resource: 'CIPHER-KEYSTORE-VAULT',
          confidence: 0.99
        });
      }
    } finally {
      setEvaluating(false);
    }
  };

  const navItems: { id: NavTab; label: string; icon: React.ReactNode; badge?: string }[] = [
    { id: 'trust_overview', label: 'TRUST OVERVIEW', icon: <Radar className="h-4 w-4" /> },
    { id: 'identities', label: 'IDENTITIES', icon: <UserCheck className="h-4 w-4" /> },
    { id: 'devices', label: 'DEVICES', icon: <Laptop className="h-4 w-4" /> },
    { id: 'sessions', label: 'SESSIONS', icon: <Activity className="h-4 w-4" /> },
    { id: 'access_decisions', label: 'ACCESS DECISIONS', icon: <ShieldCheck className="h-4 w-4" /> },
    { id: 'policies', label: 'POLICIES', icon: <Sliders className="h-4 w-4" /> },
    { id: 'asset_inventory', label: 'ASSET INVENTORY', icon: <Server className="h-4 w-4" /> },
    { id: 'external_attack_surface', label: 'EXTERNAL ATTACK SURFACE', icon: <Globe className="h-4 w-4" /> },
    { id: 'exposures', label: 'EXPOSURES', icon: <AlertTriangle className="h-4 w-4" />, badge: '3' },
    { id: 'vulnerabilities', label: 'VULNERABILITIES', icon: <AlertCircle className="h-4 w-4" /> },
    { id: 'attack_paths', label: 'ATTACK PATHS', icon: <Crosshair className="h-4 w-4" /> },
    { id: 'crown_jewels', label: 'CROWN JEWELS', icon: <Lock className="h-4 w-4" />, badge: '18' },
    { id: 'exposure_drift', label: 'EXPOSURE DRIFT', icon: <RefreshCw className="h-4 w-4" /> },
    { id: 'remediation', label: 'REMEDIATION', icon: <CheckCircle2 className="h-4 w-4" /> },
    { id: 'security_graph', label: 'SECURITY GRAPH', icon: <Network className="h-4 w-4" /> }
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 lg:p-8 space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2 bg-indigo-500/10 border border-indigo-500/30 rounded-xl">
              <ShieldCheck className="h-8 w-8 text-indigo-400" />
            </div>
            <div>
              <h1 className="text-2xl lg:text-3xl font-extrabold tracking-tight text-white flex items-center gap-3">
                Zero-Trust & Continuous Exposure Center
                <span className="text-xs bg-indigo-950 text-indigo-300 border border-indigo-700/50 px-2.5 py-0.5 rounded-full font-mono">
                  PHASE 34 ACTIVE
                </span>
              </h1>
              <p className="text-sm text-slate-400 mt-0.5">
                Continuous Identity Verification, Dynamic 8D Access Decisions, EASM, Graph Attack Paths & Verified Remediation
              </p>
            </div>
          </div>
        </div>
        
        {/* Trust Posture Badge */}
        <div className="flex items-center gap-4 bg-slate-900/80 border border-slate-800 rounded-xl px-4 py-2.5 shadow-lg shadow-black/40">
          <div className="text-right">
            <div className="text-[11px] text-slate-400 font-medium">Continuous Zero-Trust Assurance</div>
            <div className="text-sm font-bold text-emerald-400 flex items-center gap-1.5 justify-end">
              <Check className="h-4 w-4" /> OPTIMAL MATURITY (98.4%)
            </div>
          </div>
          <div className="h-8 w-[1px] bg-slate-800" />
          <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800/80 px-2.5 py-1 rounded font-mono font-bold">
            NEVER TRUST &bull; ALWAYS VERIFY
          </span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-5">
        <div className="bg-slate-900/70 border border-slate-800 p-5 rounded-xl relative overflow-hidden backdrop-blur-sm">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Active Zero-Trust Sessions</span>
            <Activity className="h-4 w-4 text-indigo-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">1,420</div>
          <div className="text-xs text-emerald-400 mt-2 flex items-center gap-1 font-medium">
            <CheckCircle2 className="h-3.5 w-3.5" /> 100% MFA & Device Posture Grounded
          </div>
        </div>

        <div className="bg-slate-900/70 border border-slate-800 p-5 rounded-xl relative overflow-hidden backdrop-blur-sm">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">External Attack Surface</span>
            <Globe className="h-4 w-4 text-cyan-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">384 <span className="text-sm text-slate-400 font-normal">Assets</span></div>
          <div className="text-xs text-cyan-300 mt-2 flex items-center gap-1 font-medium">
            <Radar className="h-3.5 w-3.5" /> Continuous EASM Perimeter Scan Active
          </div>
        </div>

        <div className="bg-slate-900/70 border border-slate-800 p-5 rounded-xl relative overflow-hidden backdrop-blur-sm">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Open Exposures Tracked</span>
            <AlertTriangle className="h-4 w-4 text-amber-400" />
          </div>
          <div className="text-3xl font-extrabold text-amber-400">3 <span className="text-sm text-slate-400 font-normal font-sans">Findings</span></div>
          <div className="text-xs text-amber-300/80 mt-2 flex items-center gap-1 font-medium">
            0 Exploitable Crown Jewel Attack Paths
          </div>
        </div>

        <div className="bg-slate-900/70 border border-slate-800 p-5 rounded-xl relative overflow-hidden backdrop-blur-sm">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs uppercase tracking-wider font-semibold">Crown Jewels Isolated</span>
            <Lock className="h-4 w-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-extrabold text-emerald-400">18 / 18</div>
          <div className="text-xs text-slate-400 mt-2 flex items-center gap-1 font-medium">
            Microsegmentation 100% Enforced
          </div>
        </div>
      </div>

      {/* Navigation Bar (15 views) */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-2 border-b border-slate-800 scrollbar-thin scrollbar-thumb-slate-800">
        {navItems.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-3.5 py-2 font-medium text-xs rounded-lg transition-all flex items-center gap-2 whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/50 shadow-sm'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/80 border border-transparent'
            }`}
          >
            {tab.icon}
            {tab.label}
            {tab.badge && (
              <span className="text-[10px] bg-slate-800 text-slate-300 px-1.5 py-0.2 rounded-full font-mono">
                {tab.badge}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Tab 1: TRUST OVERVIEW (Dashboard) */}
      {activeTab === 'trust_overview' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <Radar className="h-5 w-5 text-indigo-400" /> Continuous 7-Dimensional Trust Scorecard
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-2">
                {[
                  { label: 'Identity Trust', score: '98%', status: 'TRUSTED', color: 'text-emerald-400' },
                  { label: 'Device Posture', score: '94%', status: 'COMPLIANT', color: 'text-emerald-400' },
                  { label: 'Session Trust', score: '99%', status: 'ACTIVE_MFA', color: 'text-emerald-400' },
                  { label: 'Resource Risk', score: '0.15', status: 'LOW_RISK', color: 'text-cyan-400' },
                  { label: 'Exposure Level', score: '0.10', status: 'CONTAINED', color: 'text-cyan-400' },
                  { label: 'Policy Compliance', score: '99.2%', status: 'STRICT', color: 'text-emerald-400' },
                  { label: 'Threat Context', score: '0.04', status: 'BENIGN', color: 'text-emerald-400' },
                  { label: 'Overall Confidence', score: '98.5%', status: 'VERIFIED', color: 'text-indigo-400 font-bold' }
                ].map((dim, idx) => (
                  <div key={idx} className="bg-slate-950 border border-slate-800 p-3.5 rounded-lg">
                    <div className="text-[11px] text-slate-400 font-medium">{dim.label}</div>
                    <div className={`text-xl font-extrabold ${dim.color} mt-1`}>{dim.score}</div>
                    <div className="text-[10px] text-slate-500 font-mono mt-0.5">{dim.status}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <Activity className="h-5 w-5 text-cyan-400" /> High-Risk Identifications & Untrusted Assets
              </h2>
              <div className="space-y-3">
                {[
                  { title: 'Untrusted Device Access Attempt', target: 'dev-win-contractor-99', type: 'DEVICE_UNTRUSTED', desc: 'Missing disk encryption + out-of-date OS build (KB5039211 missing)', sev: 'HIGH' },
                  { title: 'Unknown External Subdomain Discovered', target: 'dev-api-test.truthshield.io', type: 'UNKNOWN_EXTERNAL_ASSET', desc: 'Discovered via Certificate Transparency log, unmanaged in inventory', sev: 'MEDIUM' },
                  { title: 'Potential Privilege Accumulation', target: 'analyst-contractor@truthshield.io', type: 'EXCESS_PRIVILEGE', desc: 'Unused administrative role granted 45 days ago without active session', sev: 'LOW' }
                ].map((item, idx) => (
                  <div key={idx} className="bg-slate-950 border border-slate-800 p-3.5 rounded-lg flex items-center justify-between">
                    <div>
                      <div className="text-sm font-semibold text-slate-200 flex items-center gap-2">
                        <span>{item.title}</span>
                        <span className="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded font-mono">{item.type}</span>
                      </div>
                      <div className="text-xs text-slate-400 mt-1">{item.desc} &bull; <span className="font-mono text-cyan-400">{item.target}</span></div>
                    </div>
                    <span className={`text-xs px-2.5 py-1 rounded font-mono font-bold ${
                      item.sev === 'HIGH' ? 'bg-rose-950 text-rose-300 border border-rose-800' :
                      item.sev === 'MEDIUM' ? 'bg-amber-950 text-amber-300 border border-amber-800' :
                      'bg-slate-800 text-slate-300'
                    }`}>
                      {item.sev}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-indigo-400" /> Interactive Zero-Trust Engine Simulator
              </h2>
              <p className="text-xs text-slate-400 leading-relaxed">
                Test real-time 8D evaluation rules against active policy invariants and verify automated containment decisions.
              </p>
              <div className="space-y-2.5 pt-2">
                <button
                  disabled={evaluating}
                  onClick={() => handleSimulateEvaluation('clean')}
                  className="w-full bg-emerald-950/40 hover:bg-emerald-900/40 border border-emerald-700/50 text-emerald-300 py-2 px-3.5 rounded-lg font-medium text-xs flex items-center justify-between transition-colors"
                >
                  <span className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4" /> Compliant Device &amp; MFA Request</span>
                  <span className="font-mono text-[10px] bg-emerald-900/80 px-2 py-0.5 rounded">&rarr; ALLOW</span>
                </button>

                <button
                  disabled={evaluating}
                  onClick={() => handleSimulateEvaluation('anomalous')}
                  className="w-full bg-amber-950/40 hover:bg-amber-900/40 border border-amber-700/50 text-amber-300 py-2 px-3.5 rounded-lg font-medium text-xs flex items-center justify-between transition-colors"
                >
                  <span className="flex items-center gap-2"><KeyRound className="h-4 w-4" /> Anomalous IP Geolocation Hop</span>
                  <span className="font-mono text-[10px] bg-amber-900/80 px-2 py-0.5 rounded">&rarr; STEP_UP</span>
                </button>

                <button
                  disabled={evaluating}
                  onClick={() => handleSimulateEvaluation('compromised')}
                  className="w-full bg-rose-950/40 hover:bg-rose-900/40 border border-rose-700/50 text-rose-300 py-2 px-3.5 rounded-lg font-medium text-xs flex items-center justify-between transition-colors"
                >
                  <span className="flex items-center gap-2"><ShieldAlert className="h-4 w-4" /> Jailbroken / Rooted Endpoint</span>
                  <span className="font-mono text-[10px] bg-rose-900/80 px-2 py-0.5 rounded">&rarr; QUARANTINE</span>
                </button>

                <button
                  disabled={evaluating}
                  onClick={() => handleSimulateEvaluation('breakglass')}
                  className="w-full bg-indigo-950/40 hover:bg-indigo-900/40 border border-indigo-700/50 text-indigo-300 py-2 px-3.5 rounded-lg font-medium text-xs flex items-center justify-between transition-colors"
                >
                  <span className="flex items-center gap-2"><Lock className="h-4 w-4" /> Emergency Break-Glass Request</span>
                  <span className="font-mono text-[10px] bg-indigo-900/80 px-2 py-0.5 rounded">&rarr; AUDITED</span>
                </button>
              </div>

              {lastDecision && (
                <div className="mt-4 bg-slate-950 border border-slate-800 p-3.5 rounded-lg text-xs space-y-1.5 font-mono">
                  <div className="text-slate-400 uppercase tracking-wider text-[10px] font-bold">Latest Evaluation Result:</div>
                  <div className="text-slate-200"><span className="text-slate-400">Subject:</span> {lastDecision.subject}</div>
                  <div className="text-slate-200"><span className="text-slate-400">Decision:</span> <span className={`font-bold ${
                    lastDecision.decision === 'ALLOW' ? 'text-emerald-400' :
                    lastDecision.decision === 'STEP_UP' ? 'text-amber-400' :
                    'text-rose-400'
                  }`}>{lastDecision.decision}</span></div>
                  <div className="text-slate-400 leading-normal"><span className="text-slate-500">Reason:</span> {lastDecision.reason}</div>
                  {lastDecision.violated_condition && (
                    <div className="text-rose-400/90 text-[11px]"><span className="text-slate-500">Condition:</span> {lastDecision.violated_condition}</div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: IDENTITIES */}
      {activeTab === 'identities' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <UserCheck className="h-5 w-5 text-indigo-400" /> Continuous Identity Security &amp; Behavioral Profiles
            </h2>
            <span className="text-xs text-slate-400 font-mono">Total Verified Identities: 1,420</span>
          </div>
          <div className="space-y-3">
            {[
              { id: 'USR-101', name: 'Alice SecOps Lead', email: 'alice@truthshield.io', role: 'SECURITY_ADMIN', trust: 'TRUSTED', score: 0.98, mfa: 'FIDO2_PASSKEY', dev: 'DEV-001-MAC' },
              { id: 'USR-102', name: 'Bob Core Dev', email: 'bob@truthshield.io', role: 'DEV_ENGINEER', trust: 'CONDITIONAL', score: 0.74, mfa: 'TOTP_APP', dev: 'DEV-002-LNX' },
              { id: 'USR-103', name: 'Charlie Temp Contractor', email: 'charlie@external-partner.io', role: 'ANALYST', trust: 'TRUSTED', score: 0.91, mfa: 'FIDO2_PASSKEY', dev: 'DEV-003-WIN' },
              { id: 'USR-104', name: 'Service AI Engine Agent', email: 'service-ai@truthshield.internal', role: 'M2M_AGENT', trust: 'TRUSTED', score: 1.0, mfa: 'SPIFFE_MTLS', dev: 'K8S-POD-09' }
            ].map((u, idx) => (
              <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div>
                  <div className="font-semibold text-slate-100 text-sm flex items-center gap-2">
                    <span>{u.name}</span>
                    <span className="text-xs font-mono text-cyan-400">({u.id})</span>
                  </div>
                  <div className="text-xs text-slate-400 font-mono mt-1">
                    {u.email} &bull; Role: <span className="text-slate-300">{u.role}</span> &bull; Primary MFA: <span className="text-slate-300">{u.mfa}</span>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-right font-mono">
                    <span className="text-xs font-bold text-emerald-400">{u.trust}</span>
                    <div className="text-[11px] text-slate-400">Confidence: {(u.score * 100).toFixed(0)}%</div>
                  </div>
                  <button className="text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded transition-colors font-medium">
                    Profile Detail
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 3: DEVICES */}
      {activeTab === 'devices' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <Laptop className="h-5 w-5 text-indigo-400" /> Device Trust &amp; Endpoint Posture Validation
            </h2>
            <span className="text-xs text-slate-400 font-mono">Registered Endpoints: 1,890</span>
          </div>
          <div className="space-y-3">
            {[
              { id: 'DEV-001-MAC', host: 'alice-mbp-m3.corp', os: 'macOS Sonoma 14.5', posture: 10.0, state: 'TRUSTED', edr: 'Active', enc: 'FileVault Enabled', cert: 'Valid' },
              { id: 'DEV-002-LNX', host: 'build-worker-prod-04', os: 'Ubuntu 22.04 LTS', posture: 10.0, state: 'TRUSTED', edr: 'Active', enc: 'LUKS Encrypted', cert: 'Valid' },
              { id: 'DEV-003-WIN', host: 'charlie-thinkpad.ext', os: 'Windows 11 Enterprise', posture: 6.5, state: 'CONDITIONAL', edr: 'Active', enc: 'BitLocker Warning', cert: 'Valid' },
              { id: 'DEV-004-IOS', host: 'temp-mobile-iphone15', os: 'iOS 17.5.1', posture: 0.0, state: 'QUARANTINED', edr: 'N/A', enc: 'Compromised', cert: 'Revoked' }
            ].map((d, idx) => (
              <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div>
                  <div className="font-semibold text-slate-100 text-sm flex items-center gap-2">
                    <span>{d.host}</span>
                    <span className="text-xs font-mono text-cyan-400">({d.id})</span>
                  </div>
                  <div className="text-xs text-slate-400 font-mono mt-1">
                    {d.os} &bull; EDR: {d.edr} &bull; Encryption: {d.enc} &bull; Client Cert: {d.cert}
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`text-xs px-2.5 py-1 rounded font-mono font-bold ${
                    d.state === 'TRUSTED' ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' :
                    d.state === 'CONDITIONAL' ? 'bg-amber-950 text-amber-300 border border-amber-800' :
                    'bg-rose-950 text-rose-300 border border-rose-800'
                  }`}>
                    {d.state} ({d.posture}/10)
                  </span>
                  {d.state === 'QUARANTINED' && (
                    <span className="text-xs text-rose-400 bg-rose-950/60 border border-rose-800 px-2 py-1 rounded font-mono">
                      ISOLATED
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 4: SESSIONS */}
      {activeTab === 'sessions' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <Activity className="h-5 w-5 text-indigo-400" /> Active Session Security &amp; Continuous Drift Monitoring
            </h2>
            <span className="text-xs text-slate-400 font-mono">Active Zero-Trust Sessions: 1,420</span>
          </div>
          <div className="space-y-3">
            {[
              { id: 'SESS-88192', user: 'alice@truthshield.io', ip: '203.0.113.19', state: 'ACTIVE', age: '14 mins', risk: 0.1, dev: 'DEV-001-MAC' },
              { id: 'SESS-88193', user: 'engineer-01@truthshield.io', ip: '198.51.100.42', state: 'SUSPENDED', age: '32 mins', risk: 8.5, dev: 'DEV-002-LNX', anomaly: 'IP_ADDRESS_HIJACK_DETECTED' },
              { id: 'SESS-88194', user: 'analyst-temp@truthshield.io', ip: '192.0.2.88', state: 'REAUTH_REQUIRED', age: '120 mins', risk: 4.2, dev: 'DEV-003-WIN', anomaly: 'SESSION_TTL_REAUTH' }
            ].map((s, idx) => (
              <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div>
                  <div className="font-semibold text-slate-100 text-sm flex items-center gap-2">
                    <span className="font-mono text-cyan-300">{s.id}</span>
                    <span>&bull; {s.user}</span>
                  </div>
                  <div className="text-xs text-slate-400 font-mono mt-1">
                    IP: {s.ip} &bull; Bound Device: {s.dev} &bull; Duration: {s.age}
                    {s.anomaly && <span className="text-rose-400 font-bold ml-2">[{s.anomaly}]</span>}
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`text-xs px-2.5 py-1 rounded font-mono font-bold ${
                    s.state === 'ACTIVE' ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' :
                    s.state === 'SUSPENDED' ? 'bg-rose-950 text-rose-300 border border-rose-800' :
                    'bg-amber-950 text-amber-300 border border-amber-800'
                  }`}>
                    {s.state} (Risk: {s.risk})
                  </span>
                  <button className="text-xs bg-rose-950 hover:bg-rose-900 text-rose-300 border border-rose-800 px-2.5 py-1 rounded font-mono transition-colors">
                    Revoke
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 5: ACCESS DECISIONS */}
      {activeTab === 'access_decisions' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <ShieldCheck className="h-5 w-5 text-indigo-400" /> 8D Dynamic Zero-Trust Access Authorization Audit
          </h2>
          <div className="space-y-3">
            {[
              { id: 'ZTD-9912', subj: 'alice@truthshield.io', res: 'CIPHER-KEYSTORE-VAULT', act: 'WRITE_DEK', dec: 'ALLOW', reason: 'FULL_ZERO_TRUST_VERIFIED', conf: 0.99, time: '10:48:12' },
              { id: 'ZTD-9913', subj: 'charlie@external.io', res: 'DB-MAIN-CORE-VAULT', act: 'EXPORT_RAW', dec: 'DENY', reason: 'RESTRICTED_RESOURCE_REQUIRES_FULL_TRUST', conf: 0.98, time: '10:47:30' },
              { id: 'ZTD-9914', subj: 'engineer-01@truthshield.io', res: 'K8S-PROD-CLUSTER', act: 'DEPLOY_CONTAINER', dec: 'STEP_UP', reason: 'STEP_UP_AUTHENTICATION_REQUIRED', conf: 0.92, time: '10:45:19' },
              { id: 'ZTD-9915', subj: 'analyst-contractor@truthshield.io', res: 'CREDIT-CARD-INDEX', act: 'SELECT', dec: 'DENY', reason: 'INSUFFICIENT_IDENTITY_CONFIDENCE', conf: 0.95, time: '10:42:01' }
            ].map((d, idx) => (
              <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div>
                  <div className="text-sm font-semibold text-slate-200">
                    <span className="font-mono text-cyan-300">{d.subj}</span> &rarr; <span className="font-mono text-indigo-300">{d.res}</span> ({d.act})
                  </div>
                  <div className="text-xs text-slate-400 font-mono mt-1">
                    Decision ID: {d.id} &bull; Reason: <span className="text-slate-300">{d.reason}</span> &bull; {d.time}
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`text-xs px-2.5 py-1 rounded font-mono font-bold ${
                    d.dec === 'ALLOW' ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' :
                    d.dec === 'STEP_UP' ? 'bg-amber-950 text-amber-300 border border-amber-800' :
                    'bg-rose-950 text-rose-300 border border-rose-800'
                  }`}>
                    {d.dec}
                  </span>
                  <span className="text-xs text-slate-400 font-mono">{(d.conf * 100).toFixed(0)}% Conf</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 6: POLICIES */}
      {activeTab === 'policies' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <Sliders className="h-5 w-5 text-indigo-400" /> Active Zero-Trust &amp; Micro-segmentation Policies
          </h2>
          <div className="space-y-3">
            {[
              { name: 'ZT_POLICY_HIGHLY_RESTRICTED', rule: 'Require Hardware FIDO2 + EDR Active + BitLocker + Risk Score <= 3.0', action: 'STRICT_ALLOW_OR_DENY', scope: 'Zone:DATABASE, Vault' },
              { name: 'ZT_POLICY_RESTRICTED', rule: 'Require Full Identity Trust + Compliant Device + Risk Score <= 4.0', action: 'STEP_UP_ON_RISK', scope: 'Zone:APPLICATION' },
              { name: 'ZT_MICROSEGMENT_DEFAULT_DENY', rule: 'East-West inter-zone flow forbidden unless explicitly allowlisted', action: 'DEFAULT_DENY', scope: 'All Zones' }
            ].map((p, idx) => (
              <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div>
                  <div className="text-sm font-semibold text-indigo-300 font-mono">{p.name}</div>
                  <div className="text-xs text-slate-300 mt-1">{p.rule}</div>
                  <div className="text-xs text-slate-500 font-mono mt-0.5">Scope: {p.scope}</div>
                </div>
                <span className="text-xs bg-slate-800 text-slate-300 px-2.5 py-1 rounded font-mono self-start md:self-auto">
                  {p.action}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 7: ASSET INVENTORY */}
      {activeTab === 'asset_inventory' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <Server className="h-5 w-5 text-indigo-400" /> Authoritative Asset Inventory
            </h2>
            <span className="text-xs text-slate-400 font-mono">Approved Assets: 384</span>
          </div>
          <div className="space-y-3">
            {[
              { id: 'ASSET-PROD-01', name: 'Primary Auth Gateway', type: 'API_GATEWAY', owner: 'SecOps', crit: 'CRITICAL', env: 'PRODUCTION', exp: 'EXTERNAL' },
              { id: 'ASSET-PROD-02', name: 'Core Transaction Database', type: 'DATABASE', owner: 'DBA Team', crit: 'CRITICAL', env: 'PRODUCTION', exp: 'INTERNAL' },
              { id: 'ASSET-PROD-03', name: 'Threat Intelligence Ingestion Worker', type: 'WORKER_SERVICE', owner: 'ThreatOps', crit: 'HIGH', env: 'PRODUCTION', exp: 'INTERNAL' }
            ].map((a, idx) => (
              <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div>
                  <div className="text-sm font-semibold text-slate-200 flex items-center gap-2">
                    <span>{a.name}</span>
                    <span className="text-xs font-mono text-cyan-400">({a.id})</span>
                  </div>
                  <div className="text-xs text-slate-400 font-mono mt-1">
                    Type: {a.type} &bull; Owner: {a.owner} &bull; Env: {a.env} &bull; Exposure: {a.exp}
                  </div>
                </div>
                <span className="text-xs bg-rose-950 text-rose-300 border border-rose-800 px-2.5 py-1 rounded font-mono font-bold self-start md:self-auto">
                  {a.crit}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 8: EXTERNAL ATTACK SURFACE */}
      {activeTab === 'external_attack_surface' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <Globe className="h-5 w-5 text-cyan-400" /> External Attack Surface Management (EASM)
            </h2>
            <button className="text-xs bg-cyan-950 hover:bg-cyan-900 text-cyan-300 border border-cyan-800 px-3 py-1.5 rounded font-medium flex items-center gap-1.5 transition-colors">
              <Radar className="h-3.5 w-3.5" /> Trigger Perimeter Rescan
            </button>
          </div>
          <div className="space-y-3">
            {[
              { target: 'api.truthshield.io', type: 'DOMAIN', ports: [80, 443], cert: 'Valid (89 days)', tech: 'FastAPI, Envoy Proxy, TLS 1.3', status: 'MANAGED' },
              { target: 'auth.truthshield.io', type: 'DOMAIN', ports: [443], cert: 'Valid (120 days)', tech: 'OAuth2/OIDC, NGINX', status: 'MANAGED' },
              { target: 'dev-api-test.truthshield.io', type: 'SUBDOMAIN', ports: [8080], cert: 'Self-Signed (Expired)', tech: 'Node.js Express', status: 'SHADOW_IT_DETECTED' }
            ].map((item, idx) => (
              <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div>
                  <div className="text-sm font-semibold text-white font-mono flex items-center gap-2">
                    <span className="text-cyan-400">{item.target}</span>
                    <span className="text-xs bg-slate-800 text-slate-300 px-2 py-0.5 rounded font-sans">{item.type}</span>
                  </div>
                  <div className="text-xs text-slate-400 font-mono mt-1">
                    Open Ports: {item.ports.join(', ')} &bull; Cert: {item.cert} &bull; Tech: {item.tech}
                  </div>
                </div>
                <span className={`text-xs px-2.5 py-1 rounded font-mono font-bold self-start md:self-auto ${
                  item.status === 'SHADOW_IT_DETECTED' ? 'bg-amber-950 text-amber-300 border border-amber-800' : 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                }`}>
                  {item.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 9: EXPOSURES */}
      {activeTab === 'exposures' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-amber-400" /> Active Exposure Findings &amp; Reachability Evidence
          </h2>
          <div className="space-y-3">
            {[
              { id: 'EXP-101', type: 'PUBLICLY_REACHABLE', asset: 'api.truthshield.io:443', sev: 'LOW', reach: 'REACHABLE', status: 'VERIFIED_LEGITIMATE' },
              { id: 'EXP-102', type: 'EXPOSED_STORAGE', asset: 'truthshield-dev-logs-s3', sev: 'HIGH', reach: 'REACHABLE', status: 'OPEN_ACTION_REQUIRED' },
              { id: 'EXP-103', type: 'EXPIRED_CERTIFICATE', asset: 'staging-auth.truthshield.io:443', sev: 'MEDIUM', reach: 'REACHABLE', status: 'REMEDIATION_IN_PROGRESS' }
            ].map((exp, idx) => (
              <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div>
                  <div className="text-sm font-semibold text-white font-mono flex items-center gap-2">
                    <span className="text-cyan-400">{exp.asset}</span>
                    <span className="text-xs bg-slate-800 text-slate-300 px-2 py-0.5 rounded font-sans">{exp.type}</span>
                  </div>
                  <div className="text-xs text-slate-400 font-mono mt-1">Finding ID: {exp.id} &bull; Reachability: {exp.reach}</div>
                </div>
                <div className="text-right">
                  <span className={`text-xs px-2.5 py-1 rounded font-mono font-bold ${
                    exp.sev === 'HIGH' ? 'bg-rose-950 text-rose-300 border border-rose-800' : 'bg-slate-800 text-slate-300'
                  }`}>
                    {exp.sev}
                  </span>
                  <div className="text-[10px] text-slate-400 mt-1 font-mono">{exp.status}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 10: VULNERABILITIES */}
      {activeTab === 'vulnerabilities' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <AlertCircle className="h-5 w-5 text-indigo-400" /> Vulnerability Exposure Correlation &amp; Exploitability Evidence
          </h2>
          <div className="space-y-3">
            {[
              { cve: 'CVE-2024-3094', cvss: 10.0, epss: '95%', exploitability: 'VERIFIED', reach: 'REACHABLE', asset: 'ext-gateway-01', note: 'Backdoor in XZ Utils confirmed actively tested in wild' },
              { cve: 'CVE-2024-21626', cvss: 8.6, epss: '64%', exploitability: 'LIKELY', reach: 'BLOCKED_BY_MICROSEGMENT', asset: 'runc-container-daemon', note: 'Public PoC exists; reachability blocked by network isolation' },
              { cve: 'CVE-2024-99999', cvss: 7.5, epss: '12%', exploitability: 'EXPLOITABILITY_UNVERIFIED', reach: 'NOT_VERIFIED', asset: 'internal-helper-node', note: 'Version match only; no active exploit evidence' }
            ].map((v, idx) => (
              <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div>
                  <div className="text-sm font-semibold text-slate-100 font-mono flex items-center gap-2">
                    <span className="text-rose-400">{v.cve}</span>
                    <span className="text-xs bg-slate-800 text-slate-300 px-2 py-0.5 rounded font-sans">CVSS: {v.cvss} | EPSS: {v.epss}</span>
                  </div>
                  <div className="text-xs text-slate-300 mt-1">{v.note}</div>
                  <div className="text-xs text-slate-500 font-mono mt-0.5">Asset: {v.asset} &bull; Reachability: {v.reach}</div>
                </div>
                <span className={`text-xs px-2.5 py-1 rounded font-mono font-bold self-start md:self-auto ${
                  v.exploitability === 'VERIFIED' ? 'bg-rose-950 text-rose-300 border border-rose-800' :
                  v.exploitability === 'LIKELY' ? 'bg-amber-950 text-amber-300 border border-amber-800' :
                  'bg-slate-800 text-slate-400'
                }`}>
                  {v.exploitability}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 11: ATTACK PATHS */}
      {activeTab === 'attack_paths' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <Crosshair className="h-5 w-5 text-rose-400" /> Multi-Stage Attack Path &amp; Blast Radius Analysis
          </h2>
          <div className="space-y-4">
            <div className="bg-slate-950 border border-slate-800 p-5 rounded-lg space-y-3">
              <div className="flex items-center justify-between">
                <div className="font-semibold text-sm text-slate-100">
                  Path ID: <span className="font-mono text-rose-400">PATH-EXT-01</span> (Internet &rarr; Public Ingress &rarr; App Cluster &rarr; Crown Jewel Vault)
                </div>
                <span className="text-xs bg-rose-950 text-rose-300 border border-rose-800 px-2.5 py-0.5 rounded font-mono font-bold">
                  VERIFIED REACHABLE
                </span>
              </div>
              <div className="flex items-center gap-2 text-xs font-mono text-slate-300 overflow-x-auto py-2">
                <span className="bg-slate-900 border border-slate-700 px-3 py-1.5 rounded">1. Web Ingress (443)</span>
                <span>&rarr;</span>
                <span className="bg-slate-900 border border-slate-700 px-3 py-1.5 rounded">2. App Cluster (CVE-2024-XXXX)</span>
                <span>&rarr;</span>
                <span className="bg-slate-900 border border-slate-700 px-3 py-1.5 rounded">3. Microsegment Bypass</span>
                <span>&rarr;</span>
                <span className="bg-rose-950 border border-rose-700 text-rose-300 px-3 py-1.5 rounded font-bold">4. Crown Jewel (DB-VAULT)</span>
              </div>
              <div className="text-xs text-slate-400 flex items-center justify-between pt-1">
                <div>Calculated Blast Radius Factor: <span className="font-mono text-amber-400 font-bold">4.5x</span></div>
                <div className="text-slate-300">Recommended Action: <span className="text-indigo-400 font-semibold font-mono">ENFORCE_MICROSEGMENT_RULE_DB</span></div>
              </div>
            </div>

            <div className="bg-slate-950 border border-slate-800 p-5 rounded-lg space-y-3">
              <div className="flex items-center justify-between">
                <div className="font-semibold text-sm text-slate-100">
                  Path ID: <span className="font-mono text-amber-400">PATH-AI-CANDIDATE-02</span> (AI Synthesized Hypothetical Lateral Pivot)
                </div>
                <span className="text-xs bg-amber-950 text-amber-300 border border-amber-800 px-2.5 py-0.5 rounded font-mono font-bold">
                  CANDIDATE_ATTACK_PATH
                </span>
              </div>
              <p className="text-xs text-slate-400">
                AI hypothesis: Requires unverified SSH credential hopping. Lacks telemetry reachability proof.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Tab 12: CROWN JEWELS */}
      {activeTab === 'crown_jewels' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <Lock className="h-5 w-5 text-emerald-400" /> Crown Jewel Registry &amp; Critical Asset Protection
            </h2>
            <span className="text-xs text-slate-400 font-mono">Protected Crown Jewels: 18</span>
          </div>
          <div className="space-y-3">
            {[
              { id: 'JEWEL-01', name: 'Master Encryption Key Keystore (HSM)', type: 'CIPHER_KEYSTORE', sens: 'HIGHLY_RESTRICTED', owner: 'SecOps Director', status: '100% ISOLATED' },
              { id: 'JEWEL-02', name: 'Customer PII Transaction Database', type: 'DATABASE', sens: 'RESTRICTED', owner: 'Chief Data Officer', status: '100% ISOLATED' },
              { id: 'JEWEL-03', name: 'Core OIDC/SAML Identity Provider', type: 'IDENTITY_PROVIDER', sens: 'HIGHLY_RESTRICTED', owner: 'IAM Lead', status: '100% ISOLATED' }
            ].map((j, idx) => (
              <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div>
                  <div className="text-sm font-semibold text-slate-100 flex items-center gap-2">
                    <span>{j.name}</span>
                    <span className="text-xs font-mono text-cyan-400">({j.id})</span>
                  </div>
                  <div className="text-xs text-slate-400 font-mono mt-1">
                    Resource Type: {j.type} &bull; Sensitivity: <span className="text-rose-400">{j.sens}</span> &bull; Owner: {j.owner}
                  </div>
                </div>
                <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800 px-2.5 py-1 rounded font-mono font-bold self-start md:self-auto">
                  {j.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 13: EXPOSURE DRIFT */}
      {activeTab === 'exposure_drift' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <RefreshCw className="h-5 w-5 text-indigo-400" /> Continuous Exposure &amp; Policy Drift Tracking
          </h2>
          <div className="space-y-3">
            {[
              { id: 'DRIFT-01', asset: 'k8s-ingress-prod-02', type: 'EXPOSURE_DRIFT', desc: 'Port 8080 newly exposed due to ingress configuration commit #44a8b2', sev: 'HIGH', time: '12 mins ago' },
              { id: 'DRIFT-02', asset: 'analyst-contractor@truthshield.io', type: 'PRIVILEGE_DRIFT', desc: 'New administrative IAM policy attached without change control approval', sev: 'HIGH', time: '28 mins ago' },
              { id: 'DRIFT-03', asset: 'staging-auth.truthshield.io', type: 'ZERO_TRUST_DRIFT', desc: 'Device posture compliance degraded below 7.0 threshold', sev: 'MEDIUM', time: '1 hour ago' }
            ].map((d, idx) => (
              <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div>
                  <div className="text-sm font-semibold text-slate-100 flex items-center gap-2">
                    <span className="font-mono text-cyan-400">{d.asset}</span>
                    <span className="text-xs bg-slate-800 text-slate-300 px-2 py-0.5 rounded font-mono">{d.type}</span>
                  </div>
                  <div className="text-xs text-slate-300 mt-1">{d.desc}</div>
                  <div className="text-xs text-slate-500 font-mono mt-0.5">Drift ID: {d.id} &bull; Detected: {d.time}</div>
                </div>
                <span className="text-xs bg-rose-950 text-rose-300 border border-rose-800 px-2.5 py-1 rounded font-mono font-bold self-start md:self-auto">
                  {d.sev}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 14: REMEDIATION */}
      {activeTab === 'remediation' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <CheckCircle2 className="h-5 w-5 text-emerald-400" /> Verified Remediation &amp; Independent Rescan Validation
            </h2>
            <span className="text-xs text-slate-400 font-mono">Requirement: Ticket Closed &ne; Resolved</span>
          </div>
          <div className="space-y-3">
            {[
              { id: 'ACT-501', title: 'Close Port 8080 on Internal Load Balancer', type: 'CONFIGURE', status: 'CONFIRMED_REMEDIATED', scanPassed: true },
              { id: 'ACT-502', title: 'Rotate AWS IAM API Access Key', type: 'ROTATE_CREDENTIAL', status: 'CONFIRMED_REMEDIATED', scanPassed: true },
              { id: 'ACT-503', title: 'Patch OpenSSL Version in App Containers', type: 'PATCH', status: 'REMEDIATION_NOT_VERIFIED', scanPassed: false }
            ].map((act, idx) => (
              <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div>
                  <div className="text-sm font-semibold text-slate-200 font-mono">{act.title}</div>
                  <div className="text-xs text-slate-400 mt-0.5">Action ID: {act.id} &bull; Type: {act.type}</div>
                </div>
                <div className="text-right">
                  <span className={`text-xs px-2.5 py-1 rounded font-mono font-bold ${
                    act.scanPassed ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' : 'bg-amber-950 text-amber-300 border border-amber-800'
                  }`}>
                    {act.status}
                  </span>
                  <div className="text-[10px] text-slate-400 mt-1 font-mono">
                    {act.scanPassed ? 'Rescan: PASSED' : 'Rescan: PENDING_PROOF'}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 15: SECURITY GRAPH */}
      {activeTab === 'security_graph' && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <Network className="h-5 w-5 text-cyan-400" /> Security Graph Explorer &amp; Temporal Lineage
            </h2>
            <span className="text-xs text-slate-400 font-mono">11 Node Types &bull; 9 Edge Types</span>
          </div>
          <div className="bg-slate-950 border border-slate-800 p-5 rounded-lg space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono">
              <div className="bg-slate-900 p-3 rounded border border-slate-800"><span className="text-indigo-400">IDENTITY</span> &bull; 1,420 Nodes</div>
              <div className="bg-slate-900 p-3 rounded border border-slate-800"><span className="text-cyan-400">DEVICE</span> &bull; 1,890 Nodes</div>
              <div className="bg-slate-900 p-3 rounded border border-slate-800"><span className="text-emerald-400">RESOURCE</span> &bull; 4,210 Nodes</div>
              <div className="bg-slate-900 p-3 rounded border border-slate-800"><span className="text-rose-400">VULNERABILITY</span> &bull; 34 Nodes</div>
            </div>
            <div className="border-t border-slate-800 pt-3 text-xs text-slate-400">
              Active Relationships: <span className="text-slate-200 font-mono">AUTHENTICATES, ACCESSES, CONNECTS_TO, DEPENDS_ON, EXPOSES, PROTECTS, REACHES, TRUSTS, AUTHORIZED_FOR</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ZeroTrustExposurePage;
