import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="w-full py-4 px-6 border-t border-slate-800/60 bg-slate-950/60 text-xs text-slate-500 flex flex-col sm:flex-row items-center justify-between gap-2">
      <div>
        <p>© 2026 TruthShield X. National Digital Trust Platform (SIH 2026).</p>
      </div>
      <div className="flex items-center gap-4 text-[11px]">
        <a href="#privacy" className="hover:text-slate-300 transition-colors">
          Privacy Policy
        </a>
        <a href="#terms" className="hover:text-slate-300 transition-colors">
          Terms of Service
        </a>
        <a href="#security" className="hover:text-slate-300 transition-colors">
          Security Disclosure
        </a>
      </div>
    </footer>
  );
};
