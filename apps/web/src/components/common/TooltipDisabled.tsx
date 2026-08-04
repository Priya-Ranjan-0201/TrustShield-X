import React, { useState } from 'react';
import { Info } from 'lucide-react';

interface TooltipDisabledProps {
  children: React.ReactNode;
  tooltipText: string;
  className?: string;
}

export const TooltipDisabled: React.FC<TooltipDisabledProps> = ({
  children,
  tooltipText,
  className = '',
}) => {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <div
      className={`relative inline-block cursor-not-allowed opacity-60 hover:opacity-75 transition-opacity ${className}`}
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
      onFocus={() => setIsVisible(true)}
      onBlur={() => setIsVisible(false)}
    >
      <div className="pointer-events-none">{children}</div>

      {isVisible && (
        <div
          role="tooltip"
          className="absolute z-30 bottom-full mb-2 left-1/2 transform -translate-x-1/2 w-48 px-3 py-2 text-xs text-slate-200 bg-slate-900 border border-slate-700 rounded-lg shadow-xl backdrop-blur-md flex items-start gap-1.5"
        >
          <Info className="w-3.5 h-3.5 text-cyan-400 flex-shrink-0 mt-0.5" />
          <span className="leading-snug">{tooltipText}</span>
        </div>
      )}
    </div>
  );
};
