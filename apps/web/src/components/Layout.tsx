import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShieldCheck, User, LogOut } from 'lucide-react';
import { useAuthStore } from '../store/useAuthStore';
import { authService } from '../services/authService';
import { Button } from './ui/Button';

export const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, isAuthenticated, clearAuth } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await authService.logout();
    } catch {
      // Ignore logout errors
    } finally {
      clearAuth();
      navigate('/login');
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#020617] text-[#F8FAFC]">
      {/* Navigation Header */}
      <header className="sticky top-0 z-30 backdrop-blur-md bg-slate-950/80 border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 group-hover:border-cyan-500/60 transition-all">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <span className="font-bold text-lg tracking-tight text-white flex items-center gap-1">
              TruthShield <span className="text-cyan-400">X</span>
            </span>
          </Link>

          <nav className="flex items-center gap-4">
            {isAuthenticated && user ? (
              <div className="flex items-center gap-3">
                <Link
                  to="/profile"
                  className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 hover:text-white hover:border-slate-700 text-sm transition-all"
                >
                  <User className="w-4 h-4 text-cyan-400" />
                  <span>{user.full_name}</span>
                  <span className="ml-1 px-1.5 py-0.5 rounded text-[10px] uppercase font-semibold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                    {user.role}
                  </span>
                </Link>

                <Button variant="outline" size="sm" onClick={handleLogout} className="flex items-center gap-1.5">
                  <LogOut className="w-4 h-4" />
                  <span>Logout</span>
                </Button>
              </div>
            ) : (
              <div className="flex items-center gap-3">
                <Link to="/login" className="text-sm font-medium text-slate-300 hover:text-white transition-all">
                  Sign In
                </Link>
                <Link to="/register">
                  <Button variant="primary" size="sm">
                    Get Started
                  </Button>
                </Link>
              </div>
            )}
          </nav>
        </div>
      </header>

      {/* Main Body */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
        {children}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 py-6 text-center text-xs text-slate-500">
        <p>TruthShield X — National Digital Trust Platform. All Rights Reserved.</p>
      </footer>
    </div>
  );
};
