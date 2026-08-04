import React, { forwardRef } from 'react';
import { AlertCircle, CheckCircle } from 'lucide-react';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  success?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  helperText?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, success, leftIcon, rightIcon, helperText, className = '', disabled, id, ...props }, ref) => {
    const inputId = id || (label ? label.toLowerCase().replace(/\s+/g, '-') : undefined);

    return (
      <div className="w-full space-y-1.5">
        {label && (
          <label htmlFor={inputId} className="block text-xs font-semibold uppercase tracking-wider text-slate-300">
            {label}
          </label>
        )}
        <div className="relative flex items-center">
          {leftIcon && <div className="absolute left-3.5 text-slate-400 pointer-events-none">{leftIcon}</div>}

          <input
            id={inputId}
            ref={ref}
            disabled={disabled}
            className={`w-full bg-slate-900/60 text-slate-100 text-sm placeholder-slate-500 rounded-xl px-4 py-2.5 border transition-all duration-150 focus:outline-none ${
              leftIcon ? 'pl-10' : ''
            } ${rightIcon || error || success ? 'pr-10' : ''} ${
              error
                ? 'border-red-500 bg-red-500/5 focus:ring-2 focus:ring-red-500/30'
                : success
                ? 'border-emerald-500 bg-emerald-500/5 focus:ring-2 focus:ring-emerald-500/30'
                : 'border-slate-700/80 hover:border-cyan-500/50 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/30'
            } ${disabled ? 'opacity-50 bg-slate-900/30 cursor-not-allowed border-slate-800' : ''} ${className}`}
            {...props}
          />

          {error ? (
            <div className="absolute right-3.5 text-red-400 pointer-events-none">
              <AlertCircle className="w-4 h-4" />
            </div>
          ) : success ? (
            <div className="absolute right-3.5 text-emerald-400 pointer-events-none">
              <CheckCircle className="w-4 h-4" />
            </div>
          ) : rightIcon ? (
            <div className="absolute right-3.5 text-slate-400">{rightIcon}</div>
          ) : null}
        </div>

        {error ? (
          <p className="text-xs text-red-400 flex items-center gap-1 mt-1">{error}</p>
        ) : helperText ? (
          <p className="text-xs text-slate-400 mt-1">{helperText}</p>
        ) : null}
      </div>
    );
  }
);

Input.displayName = 'Input';
