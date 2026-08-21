import React, { useState } from 'react';
import {
  Radar,
  TrendingUp,
  AlertOctagon,
  Search,
  Activity,
  Flame,
  ShieldAlert,
  Crosshair,
  Sparkles,
  BarChart3,
  RefreshCw,
  ArrowUpRight,
  Clock,
  CheckCircle2,
  ExternalLink,
} from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Card } from '../components/ui/Card';
import { toast } from '../lib/sonner';

export const ThreatIntelligenceCommandCenterPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'warnings' | 'forecasts' | 'anomalies' | 'hunts' | 'calibration'>('warnings');
  const [huntTerm, setHuntTerm] = useState('');
  const [huntResults, setHuntResults] = useState<Array<{ name: string; type: string; risk: number; match: string }>>([
    { name: 'secure-verification-hdfc-portal.net', type: 'DOMAIN', risk: 92.4, match: 'ASN Subnet Cluster 4421' },
    { name: 'sha256:8a4bf012...', type: 'CERTIFICATE', risk: 88.0, match: 'Shared Debug Cert in 3 APKs' },
  ]);

  const handleExecuteHunt = (e: React.FormEvent) => {
    e.preventDefault();
    if (!huntTerm.trim()) return;
    toast.success(`Executed bounded threat hunt for '${huntTerm}' across graph neighbors.`);
    setHuntResults((prev) => [
      { name: huntTerm, type: 'QUERY_TARGET', risk: 75.0, match: 'Direct Graph Correlation' },
      ...prev,
    ]);
    setHuntTerm('');
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold tracking-tight text-slate-100 flex items-center gap-2">
              <Radar className="h-8 w-8 text-cyan-400" />
              Predictive Threat Intelligence &amp; Early Warning
            </h1>
            <Badge variant="info" className="bg-cyan-950/60 text-cyan-400 border border-cyan-800">
              PHASE 6 EARLY-WARNING ACTIVE
            </Badge>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Predictive threat forecasting, continuous threat hunting, statistical anomaly detection &amp; early-warning intelligence.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="secondary" className="border-slate-700 bg-slate-900">
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh Telemetry
          </Button>
          <Button variant="primary" className="bg-cyan-600 hover:bg-cyan-500 text-white shadow-lg shadow-cyan-950/50">
            <Crosshair className="h-4 w-4 mr-2" />
            Launch Threat Hunt
          </Button>
        </div>
      </div>

      {/* Top Metric Tiles */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-5 bg-slate-900/60 border-slate-800 backdrop-blur-md">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Active Early Warnings</span>
            <AlertOctagon className="h-5 w-5 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-amber-400 mt-2">2 Alerts</div>
          <div className="text-xs text-slate-400 mt-1">1 Emerging Campaign • 1 Infra Rotation</div>
        </Card>

        <Card className="p-5 bg-slate-900/60 border-slate-800 backdrop-blur-md">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Campaign Expansion Velocity</span>
            <TrendingUp className="h-5 w-5 text-rose-400" />
          </div>
          <div className="text-2xl font-bold text-rose-400 mt-2">+1.85x / Day</div>
          <div className="text-xs text-slate-400 mt-1">Status: ACCELERATING</div>
        </Card>

        <Card className="p-5 bg-slate-900/60 border-slate-800 backdrop-blur-md">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Telemetry Anomalies</span>
            <Activity className="h-5 w-5 text-indigo-400" />
          </div>
          <div className="text-2xl font-bold text-indigo-400 mt-2">4 Spikes</div>
          <div className="text-xs text-slate-400 mt-1">Max z-score: 4.82 (Domain Burst)</div>
        </Card>

        <Card className="p-5 bg-slate-900/60 border-slate-800 backdrop-blur-md">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Calibration Brier Score</span>
            <CheckCircle2 className="h-5 w-5 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-emerald-400 mt-2">0.082</div>
          <div className="text-xs text-emerald-400 mt-1">Excellent Calibration (&lt; 0.10)</div>
        </Card>
      </div>

      {/* Tabs Navigation */}
      <div className="flex gap-2 border-b border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab('warnings')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
            activeTab === 'warnings' ? 'bg-cyan-950/60 text-cyan-400 border border-cyan-800/80' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Early Warnings
        </button>
        <button
          onClick={() => setActiveTab('forecasts')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
            activeTab === 'forecasts' ? 'bg-cyan-950/60 text-cyan-400 border border-cyan-800/80' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Campaign Forecasts
        </button>
        <button
          onClick={() => setActiveTab('anomalies')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
            activeTab === 'anomalies' ? 'bg-cyan-950/60 text-cyan-400 border border-cyan-800/80' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Statistical Anomalies
        </button>
        <button
          onClick={() => setActiveTab('hunts')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors flex items-center gap-1.5 ${
            activeTab === 'hunts' ? 'bg-cyan-950/60 text-cyan-400 border border-cyan-800/80' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Crosshair className="h-4 w-4" />
          Threat Hunting Console
        </button>
        <button
          onClick={() => setActiveTab('calibration')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
            activeTab === 'calibration' ? 'bg-cyan-950/60 text-cyan-400 border border-cyan-800/80' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Prediction Calibration
        </button>
      </div>

      {/* Tab Content: Early Warnings */}
      {activeTab === 'warnings' && (
        <div className="space-y-4">
          <Card className="p-6 bg-slate-900/50 border-slate-800 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <h3 className="text-base font-semibold text-slate-100 flex items-center gap-2">
                  <ShieldAlert className="h-5 w-5 text-amber-400" />
                  Active Early Warnings
                </h3>
                <p className="text-xs text-slate-400 mt-1">
                  Multi-signal weak pattern convergence evaluated against the Unified Intelligence Graph.
                </p>
              </div>
            </div>

            <div className="space-y-3">
              <div className="p-4 bg-slate-950/60 border border-amber-800/40 rounded-xl space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Badge variant="warning">CROSS_MODAL_CONVERGENCE</Badge>
                    <span className="text-sm font-semibold text-slate-200">
                      Campaign CAMP-2026-0891: Rapid Infrastructure Expansion
                    </span>
                  </div>
                  <span className="text-xs text-slate-400 font-mono">Horizon: 24H • Conf: HIGH (90%)</span>
                </div>
                <p className="text-xs text-slate-300">
                  Convergence detected across 3 Trojanized APK droppers and 2 fresh phishing C2 staging domains. Graph propagation score: 0.72.
                </p>
                <div className="text-xs text-slate-400 flex items-center gap-4 pt-1">
                  <span>Current Risk: <strong className="text-amber-400">65.0</strong></span>
                  <span>Projected Risk: <strong className="text-rose-400">88.0</strong></span>
                  <span className="text-cyan-400 hover:underline cursor-pointer">View Affected Entities (5)</span>
                </div>
              </div>
            </div>
          </Card>
        </div>
      )}

      {/* Tab Content: Campaign Forecasts */}
      {activeTab === 'forecasts' && (
        <Card className="p-6 bg-slate-900/50 border-slate-800 space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <h3 className="text-base font-semibold text-slate-100">Campaign Growth &amp; Expansion Forecast</h3>
              <p className="text-xs text-slate-400 mt-1">Conservative, evidence-grounded next-stage activity estimation.</p>
            </div>
            <Badge variant="danger" className="bg-rose-950/60 text-rose-400 border border-rose-800">
              ACCELERATING EXPANSION
            </Badge>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl space-y-2">
              <div className="text-xs text-slate-400 uppercase font-semibold">Growth Velocity</div>
              <div className="text-2xl font-bold text-rose-400">+1.85x / Day</div>
              <div className="text-xs text-slate-400">5 New Nodes in last 24h</div>
            </div>

            <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl space-y-2">
              <div className="text-xs text-slate-400 uppercase font-semibold">Risk Trajectory</div>
              <div className="text-2xl font-bold text-amber-400">75.0 → 90.0</div>
              <div className="text-xs text-slate-400">Horizon: 72 Hours</div>
            </div>

            <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl space-y-2">
              <div className="text-xs text-slate-400 uppercase font-semibold">Forecast Confidence</div>
              <div className="text-2xl font-bold text-cyan-400">MEDIUM</div>
              <div className="text-xs text-slate-400">Balanced with Counter-Evidence</div>
            </div>
          </div>

          <div className="space-y-3 pt-2">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400">Potential Next-Stage Activities</h4>
            <div className="space-y-2 text-xs text-slate-300">
              <div className="p-3 bg-slate-950/40 rounded border border-slate-800">
                • Potential rotation to fresh C2 fallback domains within 48 hours based on ASN hosting patterns.
              </div>
              <div className="p-3 bg-slate-950/40 rounded border border-slate-800">
                • Potential expansion of phishing SMS distribution radius targeting regional financial institutions.
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* Tab Content: Threat Hunting Console */}
      {activeTab === 'hunts' && (
        <Card className="p-6 bg-slate-900/50 border-slate-800 space-y-4">
          <div className="flex items-center gap-3 border-b border-slate-800 pb-4">
            <Crosshair className="h-6 w-6 text-cyan-400" />
            <div>
              <h3 className="text-base font-semibold text-slate-100">Threat Hunting Console</h3>
              <p className="text-xs text-slate-400">Search indicators, traverse graph neighbors, and pivot across shared infrastructure.</p>
            </div>
          </div>

          <form onSubmit={handleExecuteHunt} className="flex gap-2">
            <input
              type="text"
              value={huntTerm}
              onChange={(e) => setHuntTerm(e.target.value)}
              placeholder="Hunt by domain, hash, APK certificate, UPI VPA, or natural language query..."
              className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-100 focus:outline-none focus:border-cyan-500"
            />
            <Button type="submit" variant="primary" className="bg-cyan-600 hover:bg-cyan-500 text-white">
              <Search className="h-4 w-4 mr-1.5" />
              Hunt
            </Button>
          </form>

          <div className="space-y-2 pt-2">
            <div className="text-xs font-semibold uppercase tracking-wider text-slate-400">Correlated Hunt Matches</div>
            {huntResults.map((r, idx) => (
              <div key={idx} className="p-3 bg-slate-950/60 border border-slate-800 rounded-lg flex items-center justify-between text-xs">
                <div className="flex items-center gap-3">
                  <Badge variant="info">{r.type}</Badge>
                  <span className="font-mono text-slate-200">{r.name}</span>
                </div>
                <div className="flex items-center gap-4">
                  <span className="text-slate-400">Pivot: {r.match}</span>
                  <span className="text-amber-400 font-bold font-mono">Risk: {r.risk}</span>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Tab Content: Anomalies */}
      {activeTab === 'anomalies' && (
        <Card className="p-6 bg-slate-900/50 border-slate-800 space-y-4">
          <div>
            <h3 className="text-base font-semibold text-slate-100">Statistical Anomaly Stream</h3>
            <p className="text-xs text-slate-400">Robust z-score threshold breaches across telemetry streams.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl space-y-2">
              <div className="flex items-center justify-between">
                <Badge variant="danger">z = 4.82</Badge>
                <span className="text-xs text-slate-400">Observed: 42.0 (Baseline: 10.0 ± 2.0)</span>
              </div>
              <div className="text-sm font-semibold text-slate-200">DOMAIN_CREATION_SPIKE</div>
              <p className="text-xs text-slate-400">Sudden burst of 42 newly registered lookalike domains within 1 hour window.</p>
            </div>

            <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl space-y-2">
              <div className="flex items-center justify-between">
                <Badge variant="warning">z = 3.65</Badge>
                <span className="text-xs text-slate-400">Observed: 18.0 (Baseline: 5.0 ± 1.5)</span>
              </div>
              <div className="text-sm font-semibold text-slate-200">SMS_INTERCEPT_VELOCITY_SPIKE</div>
              <p className="text-xs text-slate-400">Elevated rate of SMS receiver registrations across uploaded APK packages.</p>
            </div>
          </div>
        </Card>
      )}

      {/* Tab Content: Prediction Calibration */}
      {activeTab === 'calibration' && (
        <Card className="p-6 bg-slate-900/50 border-slate-800 space-y-6">
          <div>
            <h3 className="text-base font-semibold text-slate-100">Prediction Calibration &amp; Brier Scorecard</h3>
            <p className="text-xs text-slate-400">Empirical validation of historical predictions against observed outcomes.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl space-y-2">
              <div className="text-xs text-slate-400 uppercase font-semibold">Mean Brier Score</div>
              <div className="text-2xl font-bold text-emerald-400">0.0820</div>
              <div className="text-xs text-slate-400">Target: &lt; 0.1500 (Calibrated)</div>
            </div>

            <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl space-y-2">
              <div className="text-xs text-slate-400 uppercase font-semibold">Validated Outcomes</div>
              <div className="text-2xl font-bold text-cyan-400">28 Predictions</div>
              <div className="text-xs text-slate-400">24 Confirmed Occurrences</div>
            </div>

            <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl space-y-2">
              <div className="text-xs text-slate-400 uppercase font-semibold">False Positive Rate</div>
              <div className="text-2xl font-bold text-indigo-400">3.8%</div>
              <div className="text-xs text-slate-400">Within 5.0% Operational Budget</div>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
};
