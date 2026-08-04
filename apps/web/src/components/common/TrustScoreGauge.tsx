import React from 'react';
import { ShieldCheck, ShieldQuestion, ShieldAlert, AlertTriangle, ShieldX } from 'lucide-react';
import { getScoreMeta } from '../../utils/score';

interface TrustScoreGaugeProps {
  score: number;
  status: string;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const TrustScoreGauge: React.FC<TrustScoreGaugeProps> = ({
  score,
  status,
  size = 'md',
  className = '',
}) => {
  const meta = getScoreMeta(score);

  const iconMap = {
    ShieldCheck,
    ShieldQuestion,
    ShieldAlert,
    AlertTriangle,
    ShieldX,
  };

  const IconComponent = iconMap[meta.iconName];

  const sizeClasses = {
    sm: 'w-24 h-24 text-2xl',
    md: 'w-36 h-36 text-4xl',
    lg: 'w-48 h-48 text-5xl',
  };

  return (
    <div
      className={`flex flex-col items-center justify-center p-6 glass-card ${className}`}
      role="img"
      aria-label={`Trust score ${score} out of 100, status ${status}`}
    >
      <div className={`relative flex items-center justify-center ${sizeClasses[size]}`}>
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
          <path
            className="text-slate-800"
            strokeWidth="3.5"
            stroke="currentColor"
            fill="none"
            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
          />
          <path
            strokeDasharray={`${score}, 100`}
            stroke={meta.colorHex}
            strokeWidth="3.5"
            strokeLinecap="round"
            fill="none"
            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
          />
        </svg>
        <span className="absolute font-bold text-white tracking-tight">{score}</span>
      </div>

      {/* Redundant Colorblind-Safe Badge (Icon + Label + Color per Design.md Section 4) */}
      <span
        className={`mt-4 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider text-white flex items-center gap-1.5 border ${meta.badgeBg} ${meta.badgeText} ${meta.badgeBorder}`}
      >
        <IconComponent className="w-3.5 h-3.5" />
        <span>{status}</span>
      </span>
    </div>
  );
};
