import React from 'react';

interface ProgressBarProps {
  progress: number; // 0 to 100
  label?: string;
  className?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  progress,
  label,
  className = '',
}) => {
  const clampedProgress = Math.min(100, Math.max(0, progress));

  return (
    <div className={`w-full space-y-1.5 ${className}`}>
      {label && (
        <div className="flex items-center justify-between text-xs font-semibold text-slate-300">
          <span>{label}</span>
          <span className="text-cyan-400 font-mono">{clampedProgress}%</span>
        </div>
      )}
      <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden border border-slate-700/50">
        <div
          className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full transition-all duration-300 ease-out"
          style={{ width: `${clampedProgress}%` }}
        />
      </div>
    </div>
  );
};
