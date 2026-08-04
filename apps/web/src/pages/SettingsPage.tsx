import React from 'react';
import { Settings, Sun, Moon, Monitor, Globe, Shield, Bell } from 'lucide-react';
import { DashboardLayout } from '../layouts/DashboardLayout';
import { SectionHeader } from '../components/common/SectionHeader';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { TooltipDisabled } from '../components/common/TooltipDisabled';
import { useThemeStore } from '../store/useThemeStore';
import { usei18n } from '../hooks/usei18n';

export const SettingsPage: React.FC = () => {
  const { theme, setTheme } = useThemeStore();
  const { currentLanguage, changeLanguage } = usei18n();

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <SectionHeader
          title="System Preferences & Settings"
          description="Configure application theme, internationalization, and notification rules."
          icon={Settings}
        />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Functional Theme System Settings */}
          <Card className="space-y-4">
            <div className="pb-3 border-b border-slate-800">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Sun className="w-4 h-4 text-cyan-400" />
                <span>Appearance & Theme System</span>
              </h3>
            </div>

            <div className="grid grid-cols-3 gap-3">
              <button
                onClick={() => setTheme('dark')}
                className={`p-4 rounded-xl border text-center space-y-2 transition-all ${
                  theme === 'dark'
                    ? 'bg-cyan-500/10 border-cyan-500 text-cyan-400 shadow-md'
                    : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-white'
                }`}
              >
                <Moon className="w-6 h-6 mx-auto" />
                <span className="text-xs font-bold block">Dark</span>
              </button>

              <button
                onClick={() => setTheme('light')}
                className={`p-4 rounded-xl border text-center space-y-2 transition-all ${
                  theme === 'light'
                    ? 'bg-cyan-500/10 border-cyan-500 text-cyan-400 shadow-md'
                    : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-white'
                }`}
              >
                <Sun className="w-6 h-6 mx-auto" />
                <span className="text-xs font-bold block">Light</span>
              </button>

              <button
                onClick={() => setTheme('system')}
                className={`p-4 rounded-xl border text-center space-y-2 transition-all ${
                  theme === 'system'
                    ? 'bg-cyan-500/10 border-cyan-500 text-cyan-400 shadow-md'
                    : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-white'
                }`}
              >
                <Monitor className="w-6 h-6 mx-auto" />
                <span className="text-xs font-bold block">System</span>
              </button>
            </div>
          </Card>

          {/* Functional i18n Language Settings */}
          <Card className="space-y-4">
            <div className="pb-3 border-b border-slate-800">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Globe className="w-4 h-4 text-cyan-400" />
                <span>Language & Locale (i18n Foundation)</span>
              </h3>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={() => changeLanguage('en')}
                className={`p-4 rounded-xl border text-center space-y-1 transition-all ${
                  currentLanguage === 'en'
                    ? 'bg-cyan-500/10 border-cyan-500 text-cyan-400'
                    : 'bg-slate-900 border-slate-800 text-slate-400'
                }`}
              >
                <span className="text-sm font-bold block">English</span>
                <span className="text-[10px] text-slate-500 font-mono">Latin Script</span>
              </button>

              <button
                onClick={() => changeLanguage('hi')}
                className={`p-4 rounded-xl border text-center space-y-1 transition-all ${
                  currentLanguage === 'hi'
                    ? 'bg-cyan-500/10 border-cyan-500 text-cyan-400'
                    : 'bg-slate-900 border-slate-800 text-slate-400'
                }`}
              >
                <span className="text-sm font-bold block">हिन्दी</span>
                <span className="text-[10px] text-slate-500 font-mono">Devanagari Script</span>
              </button>
            </div>
          </Card>

          {/* Security Rules Placeholder (Visibly disabled with tooltip) */}
          <TooltipDisabled
            tooltipText="Security Hardening & 2FA Enforcement rule settings will ship in Phase 22."
            className="w-full"
          >
            <Card className="space-y-3 text-left">
              <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-2">
                  <Shield className="w-4 h-4 text-cyan-400" />
                  <span>Security & 2FA Preferences (Placeholder)</span>
                </h3>
                <Badge variant="neutral">COMING SOON</Badge>
              </div>
              <p className="text-xs text-slate-500">
                Hardware WebAuthn security key registration and biometric SMS 2FA rules will be configured here.
              </p>
            </Card>
          </TooltipDisabled>

          {/* Notification Rules Placeholder */}
          <TooltipDisabled
            tooltipText="Real-time WebPush & Telegram Bot notification preferences will activate in Phase 21."
            className="w-full"
          >
            <Card className="space-y-3 text-left">
              <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-2">
                  <Bell className="w-4 h-4 text-cyan-400" />
                  <span>Notification Channel Rules (Placeholder)</span>
                </h3>
                <Badge variant="neutral">COMING SOON</Badge>
              </div>
              <p className="text-xs text-slate-500">
                WebPush desktop alerts and real-time SMS fraud escalation triggers will be managed here.
              </p>
            </Card>
          </TooltipDisabled>
        </div>
      </div>
    </DashboardLayout>
  );
};
