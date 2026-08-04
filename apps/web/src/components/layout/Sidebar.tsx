import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  Shield,
  LayoutDashboard,
  ScanLine,
  History,
  FileText,
  Network,
  Bell,
  User,
  Settings,
  ChevronLeft,
  ChevronRight,
  X,
} from 'lucide-react';
import { useSidebarStore } from '../../store/useSidebarStore';
import { usei18n } from '../../hooks/usei18n';
import { TooltipDisabled } from '../common/TooltipDisabled';

export const Sidebar: React.FC = () => {
  const { isCollapsed, isMobileOpen, toggleCollapse, setMobileOpen } = useSidebarStore();
  const { t } = usei18n();

  const navItems = [
    { label: t('nav.dashboard'), path: '/dashboard', icon: LayoutDashboard },
    { label: t('nav.unified_scan'), path: '/scan', icon: ScanLine },
    { label: t('nav.scan_history'), path: '/history', icon: History },
    { label: t('nav.reports'), path: '/reports', icon: FileText },
    {
      label: t('nav.threat_intel'),
      path: '#',
      icon: Network,
      isPlaceholder: true,
      tooltip: t('placeholders.threatIntelTooltip'),
    },
    { label: t('nav.notifications'), path: '/notifications', icon: Bell },
    { label: t('nav.profile'), path: '/profile', icon: User },
    { label: t('nav.settings'), path: '/settings', icon: Settings },
  ];

  const sidebarContent = (
    <aside
      className={`h-full bg-slate-950/90 backdrop-blur-md border-r border-slate-800/80 flex flex-col justify-between transition-all duration-300 ${
        isCollapsed ? 'w-16' : 'w-60'
      }`}
    >
      {/* Brand Header */}
      <div className="h-16 px-4 flex items-center justify-between border-b border-slate-800/80">
        <NavLink to="/dashboard" className="flex items-center gap-3 overflow-hidden">
          <div className="p-2 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex-shrink-0">
            <Shield className="w-5 h-5" />
          </div>
          {!isCollapsed && (
            <div className="flex flex-col">
              <span className="text-sm font-bold text-white tracking-wider uppercase">
                TruthShield<span className="text-cyan-400">X</span>
              </span>
              <span className="text-[9px] text-slate-400 uppercase font-mono">Cyber Defense</span>
            </div>
          )}
        </NavLink>

        {/* Desktop Collapse Toggle */}
        <button
          onClick={toggleCollapse}
          className="hidden lg:flex p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          title={isCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
        >
          {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {/* Navigation List */}
      <nav className="flex-1 py-4 px-2 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;

          if (item.isPlaceholder) {
            return (
              <div key={item.label} className="px-1">
                <TooltipDisabled tooltipText={item.tooltip} className="w-full">
                  <div
                    className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-500 select-none ${
                      isCollapsed ? 'justify-center' : ''
                    }`}
                  >
                    <Icon className="w-4 h-4 flex-shrink-0" />
                    {!isCollapsed && <span className="truncate">{item.label}</span>}
                  </div>
                </TooltipDisabled>
              </div>
            );
          }

          return (
            <NavLink
              key={item.path}
              to={item.path}
              onClick={() => setMobileOpen(false)}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-semibold transition-all duration-150 ${
                  isActive
                    ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                } ${isCollapsed ? 'justify-center' : ''}`
              }
            >
              <Icon className="w-4 h-4 flex-shrink-0" />
              {!isCollapsed && <span className="truncate">{item.label}</span>}
            </NavLink>
          );
        })}
      </nav>

      {/* Footer Status */}
      {!isCollapsed && (
        <div className="p-4 border-t border-slate-800/80">
          <div className="glass-card p-3 border border-slate-800 space-y-1 text-center">
            <p className="text-[10px] uppercase font-bold text-slate-400">System Status</p>
            <p className="text-xs font-semibold text-emerald-400 flex items-center justify-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
              Shield Active
            </p>
          </div>
        </div>
      )}
    </aside>
  );

  return (
    <>
      {/* Desktop Sidebar */}
      <div className="hidden lg:block h-screen sticky top-0">{sidebarContent}</div>

      {/* Mobile Drawer */}
      {isMobileOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div
            className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm"
            onClick={() => setMobileOpen(false)}
          />
          <div className="fixed inset-y-0 left-0 w-64 z-50 flex">
            {sidebarContent}
            <button
              onClick={() => setMobileOpen(false)}
              className="absolute top-4 right-4 p-2 rounded-lg text-slate-400 hover:text-white"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>
      )}
    </>
  );
};
