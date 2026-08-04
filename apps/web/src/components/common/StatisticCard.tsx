import React from 'react';

interface StatisticCardProps {
  label: string;
  value: string | number;
  change?: string;
  changeType?: 'positive' | 'negative' | 'neutral';
  icon: React.ElementType;
}

export const StatisticCard: React.FC<StatisticCardProps> = ({
  label,
  value,
  change,
  changeType = 'neutral',
  icon: Icon,
}) => {
  const changeColors = {
    positive: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
    negative: 'text-red-400 bg-red-500/10 border-red-500/20',
    neutral: 'text-slate-400 bg-slate-800 border-slate-700',
  };

  return (
    <div className="glass-card p-5 space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">{label}</span>
        <div className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-cyan-400">
          <Icon className="w-4 h-4" />
        </div>
      </div>
      <div className="flex items-baseline justify-between">
        <span className="text-2xl font-bold text-white tracking-tight">{value}</span>
        {change && (
          <span className={`px-2 py-0.5 rounded text-[11px] font-semibold border ${changeColors[changeType]}`}>
            {change}
          </span>
        )}
      </div>
    </div>
  );
};
