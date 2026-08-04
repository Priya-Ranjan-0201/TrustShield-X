import React, { useState } from 'react';
import {
  Shield,
  Search,
  Bell,
  Sun,
  Moon,
  Monitor,
  Menu,
  User as UserIcon,
  LogOut,
  ChevronDown,
  Globe,
} from 'lucide-react';
import { useAuthStore } from '../../store/useAuthStore';
import { useThemeStore } from '../../store/useThemeStore';
import { useSidebarStore } from '../../store/useSidebarStore';
import { useNotificationStore } from '../../store/useNotificationStore';
import { usei18n } from '../../hooks/usei18n';
import { TooltipDisabled } from '../common/TooltipDisabled';
import { Avatar } from '../ui/Avatar';
import { Badge } from '../ui/Badge';
import { useNavigate } from 'react-router-dom';

export const Header: React.FC = () => {
  const { user, logout } = useAuthStore();
  const { theme, resolvedTheme, setTheme } = useThemeStore();
  const { toggleMobile } = useSidebarStore();
  const { notifications, toggleDrawer } = useNotificationStore();
  const { t, currentLanguage, changeLanguage } = usei18n();
  const navigate = useNavigate();

  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const unreadCount = notifications.filter((n) => !n.read).length;

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-10 w-full h-16 bg-slate-950/80 backdrop-blur-md border-b border-slate-800/80 px-4 lg:px-6 flex items-center justify-between">
      {/* Left: Mobile Menu Toggle & Search Bar Placeholder */}
      <div className="flex items-center gap-3 flex-1 max-w-md">
        <button
          onClick={toggleMobile}
          className="lg:hidden p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800"
          aria-label="Toggle Navigation Drawer"
        >
          <Menu className="w-5 h-5" />
        </button>

        {/* Search Bar Placeholder (Explicit Decision: Visibly disabled with Coming Soon Tooltip) */}
        <TooltipDisabled
          tooltipText={t('placeholders.searchTooltip')}
          className="w-full max-w-sm hidden sm:block"
        >
          <div className="relative flex items-center w-full">
            <Search className="absolute left-3.5 w-4 h-4 text-slate-500" />
            <input
              type="text"
              disabled
              placeholder={t('common.search')}
              className="w-full bg-slate-900/60 text-xs text-slate-400 placeholder-slate-600 rounded-xl pl-9 pr-4 py-2 border border-slate-800 cursor-not-allowed"
            />
          </div>
        </TooltipDisabled>
      </div>

      {/* Right Actions */}
      <div className="flex items-center gap-3">
        {/* Language Switcher */}
        <button
          onClick={() => changeLanguage(currentLanguage === 'en' ? 'hi' : 'en')}
          className="p-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/80 border border-slate-800 transition-colors flex items-center gap-1.5 text-xs font-semibold"
          title="Switch Language"
        >
          <Globe className="w-4 h-4 text-cyan-400" />
          <span className="uppercase">{currentLanguage}</span>
        </button>

        {/* Theme Toggle Button */}
        <button
          onClick={() =>
            setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')
          }
          className="p-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/80 border border-slate-800 transition-colors"
          title={`Theme: ${theme}`}
          aria-label="Toggle Light/Dark Theme"
        >
          {resolvedTheme === 'dark' ? (
            <Sun className="w-4 h-4 text-amber-400" />
          ) : (
            <Moon className="w-4 h-4 text-cyan-400" />
          )}
        </button>

        {/* Notifications Bell with Unread Badge */}
        <button
          onClick={toggleDrawer}
          className="relative p-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/80 border border-slate-800 transition-colors"
          aria-label="Open Notifications Drawer"
        >
          <Bell className="w-4 h-4 text-slate-300" />
          {unreadCount > 0 && (
            <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-cyan-500 text-slate-950 font-bold text-[10px] flex items-center justify-center animate-pulse">
              {unreadCount}
            </span>
          )}
        </button>

        {/* User Menu Dropdown */}
        <div className="relative">
          <button
            onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
            className="flex items-center gap-2.5 p-1.5 rounded-xl hover:bg-slate-800/60 transition-colors border border-transparent hover:border-slate-800"
          >
            <Avatar name={user?.full_name || 'User'} size="sm" />
            <div className="hidden md:block text-left">
              <p className="text-xs font-semibold text-white leading-tight">
                {user?.full_name || 'Citizen'}
              </p>
              <p className="text-[10px] text-cyan-400 font-mono">
                {user?.role || 'CITIZEN'}
              </p>
            </div>
            <ChevronDown className="w-3.5 h-3.5 text-slate-400 hidden md:block" />
          </button>

          {isUserMenuOpen && (
            <div className="absolute right-0 mt-2 w-48 glass-card border border-slate-700 shadow-2xl py-2 z-50">
              <div className="px-4 py-2 border-b border-slate-800">
                <p className="text-xs font-bold text-white">{user?.full_name}</p>
                <p className="text-[11px] text-slate-400 truncate">{user?.email}</p>
              </div>
              <button
                onClick={() => {
                  setIsUserMenuOpen(false);
                  navigate('/profile');
                }}
                className="w-full text-left px-4 py-2 text-xs text-slate-300 hover:bg-slate-800 hover:text-white flex items-center gap-2"
              >
                <UserIcon className="w-3.5 h-3.5 text-cyan-400" />
                <span>Profile & Sessions</span>
              </button>
              <button
                onClick={handleLogout}
                className="w-full text-left px-4 py-2 text-xs text-red-400 hover:bg-red-500/10 flex items-center gap-2 border-t border-slate-800 mt-1"
              >
                <LogOut className="w-3.5 h-3.5" />
                <span>{t('nav.logout')}</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
