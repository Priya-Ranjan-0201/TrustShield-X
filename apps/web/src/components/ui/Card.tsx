import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  variant?: 'glass' | 'solid';
}

export const Card: React.FC<CardProps> = ({ children, className = '', variant = 'glass' }) => {
  return (
    <div className={`${variant === 'glass' ? 'glass-card' : 'bg-slate-900 border border-slate-800 rounded-xl'} p-6 ${className}`}>
      {children}
    </div>
  );
};
