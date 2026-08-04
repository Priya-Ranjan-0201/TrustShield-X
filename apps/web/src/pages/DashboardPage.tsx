import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  ShieldCheck,
  ScanLine,
  FileText,
  AlertTriangle,
  Zap,
  Lock,
  ArrowRight,
  TrendingUp,
  Shield,
  Layers,
} from 'lucide-react';
import { DashboardLayout } from '../layouts/DashboardLayout';
import { TrustScoreGauge } from '../components/common/TrustScoreGauge';
import { StatisticCard } from '../components/common/StatisticCard';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { TooltipDisabled } from '../components/common/TooltipDisabled';
import { mockDashboardService, DashboardData } from '../services/mockDashboardService';
import { useAuthStore } from '../store/useAuthStore';
import { usei18n } from '../hooks/usei18n';

export const DashboardPage: React.FC = () => {
  const { user } = useAuthStore();
  const { t } = usei18n();
  const navigate = useNavigate();

  const [data, setData] = useState<DashboardData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    mockDashboardService.getDashboardData().then((res) => {
      if (res.success && res.data) {
        setData(res.data);
      }
      setIsLoading(false);
    });
  }, []);

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Welcome Card Widget */}
        <div className="glass-card p-6 bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="space-y-1">
            <span className="text-[11px] font-mono uppercase tracking-widest text-cyan-400 font-bold">
              National Digital Defense Operational Console
            </span>
            <h1 className="text-2xl font-bold text-white tracking-tight">
              {t('dashboard.welcome')}, {user?.full_name || 'Citizen'}
            </h1>
            <p className="text-xs text-slate-400 max-w-xl">
              Real-time AI monitoring active. Your account is secured with multi-layer threat detection.
            </p>
          </div>
          <Button
            onClick={() => navigate('/scan')}
            leftIcon={<ScanLine className="w-4 h-4" />}
            size="md"
          >
            Launch Unified Scanner
          </Button>
        </div>

        {/* Top Grid: Trust Score Gauge & Quick Statistics */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Trust Score Gauge Widget (Explicit Requirement: Renders actual TrustScoreGauge component with static score 94) */}
          <div className="lg:col-span-1 space-y-2">
            <div className="flex items-center justify-between px-1">
              <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                {t('dashboard.trustScoreTitle')}
              </h2>
              <Badge variant="success">94/100 TRUSTED</Badge>
            </div>
            <TrustScoreGauge score={data?.trustScore || 94} status="TRUSTED" />
          </div>

          {/* Quick Statistics Grid */}
          <div className="lg:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-4">
            <StatisticCard
              label="Total Security Verifications"
              value={data?.totalScans || 1248}
              change="+14% this month"
              changeType="positive"
              icon={ScanLine}
            />

            <StatisticCard
              label="Threats & Phishing Blocked"
              value={data?.threatsBlocked || 312}
              change="+8% neutralized"
              changeType="positive"
              icon={ShieldCheck}
            />

            <StatisticCard
              label="Active Security Alerts"
              value={data?.activeAlerts || 2}
              change="2 Action Required"
              changeType="negative"
              icon={AlertTriangle}
            />

            <StatisticCard
              label="Protection Coverage"
              value="100%"
              change="Zero Trust Enforced"
              changeType="positive"
              icon={Zap}
            />
          </div>
        </div>

        {/* Middle Grid: Recent Activity & Quick Actions */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Recent Activity Feed */}
          <div className="lg:col-span-2 space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                {t('dashboard.recentActivity')}
              </h3>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => navigate('/history')}
                rightIcon={<ArrowRight className="w-3.5 h-3.5" />}
              >
                View History
              </Button>
            </div>

            <Card className="space-y-3">
              {isLoading ? (
                <p className="text-xs text-slate-400">Loading verifications...</p>
              ) : (
                data?.recentActivity.map((act) => (
                  <div
                    key={act.id}
                    className="flex items-center justify-between p-3.5 rounded-xl bg-slate-900/60 border border-slate-800/80 hover:border-slate-700 transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <div
                        className={`p-2 rounded-lg border ${
                          act.status === 'DANGEROUS'
                            ? 'bg-red-500/10 text-red-400 border-red-500/20'
                            : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                        }`}
                      >
                        <Shield className="w-4 h-4" />
                      </div>
                      <div>
                        <h4 className="text-xs font-bold text-white truncate max-w-xs sm:max-w-sm">
                          {act.target}
                        </h4>
                        <p className="text-[11px] text-slate-400">{act.summary}</p>
                      </div>
                    </div>

                    <div className="text-right space-y-1">
                      <Badge
                        variant={act.status === 'DANGEROUS' ? 'danger' : 'success'}
                        className="text-[10px]"
                      >
                        {act.status} ({act.trust_score})
                      </Badge>
                      <p className="text-[10px] text-slate-500 font-mono">
                        {new Date(act.scanned_at).toLocaleTimeString([], {
                          hour: '2-digit',
                          minute: '2-digit',
                        })}
                      </p>
                    </div>
                  </div>
                ))
              )}
            </Card>
          </div>

          {/* Right Column: Quick Actions & Security Tips */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <div className="space-y-3">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                {t('dashboard.quickActions')}
              </h3>
              <Card className="space-y-2">
                <Button
                  variant="secondary"
                  className="w-full justify-start text-xs"
                  onClick={() => navigate('/scan')}
                  leftIcon={<ScanLine className="w-4 h-4 text-cyan-400" />}
                >
                  Verify URL / Link Authenticity
                </Button>
                <Button
                  variant="secondary"
                  className="w-full justify-start text-xs"
                  onClick={() => navigate('/scan')}
                  leftIcon={<FileText className="w-4 h-4 text-cyan-400" />}
                >
                  Inspect PDF Document Signature
                </Button>
                <Button
                  variant="secondary"
                  className="w-full justify-start text-xs"
                  onClick={() => navigate('/scan')}
                  leftIcon={<Lock className="w-4 h-4 text-cyan-400" />}
                >
                  Check UPI QR Code Safety
                </Button>
              </Card>
            </div>

            {/* Security Tips */}
            <div className="space-y-3">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                {t('dashboard.securityTips')}
              </h3>
              <div className="glass-card p-4 border border-cyan-500/30 bg-cyan-500/5 space-y-2">
                <div className="flex items-center gap-2 text-cyan-400 font-bold text-xs">
                  <Lock className="w-4 h-4" />
                  <span>Verify UPI VPA Handles</span>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Never approve UPI payment requests from unknown numbers claiming to be bank or government rewards.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Placeholders Grid (Explicit Requirement: Scan Statistics & Threat Summary render as disabled placeholders with tooltip) */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Scan Statistics Placeholder */}
          <TooltipDisabled
            tooltipText="Scan Engine Statistics live telemetry graph will activate in Phase 4."
            className="w-full"
          >
            <Card className="space-y-2 text-left">
              <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-cyan-400" />
                  <span>Scan Statistics & Performance Metrics (Placeholder)</span>
                </h3>
                <Badge variant="neutral">COMING SOON</Badge>
              </div>
              <p className="text-xs text-slate-500">
                Detailed telemetry breakdown of scan types (URL, PDF, Video, Audio, APK) will populate here upon Phase 4 gateway connection.
              </p>
            </Card>
          </TooltipDisabled>

          {/* Threat Summary Placeholder */}
          <TooltipDisabled
            tooltipText="Threat Summary scam radar intelligence feed will activate in Phase 17."
            className="w-full"
          >
            <Card className="space-y-2 text-left">
              <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-2">
                  <Layers className="w-4 h-4 text-cyan-400" />
                  <span>Threat Radar & Scam Vector Summary (Placeholder)</span>
                </h3>
                <Badge variant="neutral">COMING SOON</Badge>
              </div>
              <p className="text-xs text-slate-500">
                Geographic threat heatmap and scam campaign cluster radar will be enabled upon Neo4j Knowledge Graph deployment.
              </p>
            </Card>
          </TooltipDisabled>
        </div>
      </div>
    </DashboardLayout>
  );
};
