import React from 'react';
import { ShieldCheck } from 'lucide-react';

interface EmptyStateProps {
  title: string;
  description: string;
  action?: React.ReactNode;
  icon?: React.ElementType;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title,
  description,
  action,
  icon: Icon = ShieldCheck,
}) => {
  return (
    <div className="glass-card p-12 text-center flex flex-col items-center justify-center space-y-4">
      <div className="p-4 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
        <Icon className="w-8 h-8" />
      </div>
      <div className="max-w-md space-y-1">
        <h3 className="text-lg font-bold text-white tracking-tight">{title}</h3>
        <p className="text-xs text-slate-400 leading-relaxed">{description}</p>
      </div>
      {action && <div className="pt-2">{action}</div>}
    </div>
  );
};
