import React from 'react';
import { Shield } from 'lucide-react';
import { Footer } from '../components/layout/Footer';

interface AuthLayoutProps {
  children: React.ReactNode;
}

export const AuthLayout: React.FC<AuthLayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col justify-between bg-[#020617] text-slate-100 selection:bg-cyan-500 selection:text-slate-950 relative overflow-hidden">
      {/* Background Ambient Cyber Glow Gradients */}
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl pointer-events-none" />

      {/* Brand Header */}
      <header className="p-6 flex items-center justify-between max-w-7xl mx-auto w-full z-10">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
            <Shield className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white tracking-wider uppercase">
              TruthShield<span className="text-cyan-400">X</span>
            </h1>
            <p className="text-[10px] text-slate-400 uppercase font-mono tracking-widest">
              National Digital Trust Platform
            </p>
          </div>
        </div>
      </header>

      {/* Center Form Container */}
      <main className="flex-1 flex items-center justify-center p-4 z-10">
        <div className="w-full max-w-md">{children}</div>
      </main>

      <Footer />
    </div>
  );
};
