import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldAlert, ArrowLeft } from 'lucide-react';
import { Button } from '../components/ui/Button';

export const NotFoundPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-[#020617] text-white flex flex-col items-center justify-center p-6 text-center space-y-4">
      <div className="p-4 rounded-3xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
        <ShieldAlert className="w-12 h-12" />
      </div>
      <h1 className="text-6xl font-extrabold tracking-tight text-white font-mono">404</h1>
      <h2 className="text-xl font-bold text-slate-200">Page Not Found</h2>
      <p className="text-xs text-slate-400 max-w-sm">
        The requested URL or resource does not exist or has been relocated within the TruthShield X system.
      </p>
      <Link to="/dashboard">
        <Button variant="primary" leftIcon={<ArrowLeft className="w-4 h-4" />}>
          Return to Dashboard
        </Button>
      </Link>
    </div>
  );
};
