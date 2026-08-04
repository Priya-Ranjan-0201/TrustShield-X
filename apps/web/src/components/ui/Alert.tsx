import React from 'react';
import { AlertTriangle, CheckCircle, AlertCircle, Info } from 'lucide-react';

interface AlertProps {
  type?: 'error' | 'success' | 'warning' | 'info';
  title?: string;
  message: string;
  className?: string;
}

export const Alert: React.FC<AlertProps> = ({ type = 'error', title, message, className = '' }) => {
  const styles = {
    error: 'bg-red-500/10 border-red-500/30 text-red-300 icon-red-400',
    success: 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300 icon-emerald-400',
    warning: 'bg-amber-500/10 border-amber-500/30 text-amber-300 icon-amber-400',
    info: 'bg-cyan-500/10 border-cyan-500/30 text-cyan-300 icon-cyan-400',
  };

  const icons = {
    error: AlertCircle,
    success: CheckCircle,
    warning: AlertTriangle,
    info: Info,
  };

  const IconComponent = icons[type];

  return (
    <div className={`flex items-start gap-3 p-4 border rounded-xl backdrop-blur-sm text-sm ${styles[type]} ${className}`} role="alert">
      <IconComponent className="w-5 h-5 flex-shrink-0 mt-0.5" />
      <div className="space-y-1">
        {title && <p className="font-semibold">{title}</p>}
        <p className="leading-relaxed">{message}</p>
      </div>
    </div>
  );
};
