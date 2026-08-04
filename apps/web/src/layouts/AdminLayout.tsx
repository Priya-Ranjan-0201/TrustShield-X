import React from 'react';
import { DashboardLayout } from './DashboardLayout';
import { Badge } from '../components/ui/Badge';
import { ShieldCheck } from 'lucide-react';

interface AdminLayoutProps {
  children: React.ReactNode;
}

export const AdminLayout: React.FC<AdminLayoutProps> = ({ children }) => {
  return (
    <DashboardLayout>
      <div className="space-y-4">
        <div className="flex items-center justify-between p-4 glass-card border border-amber-500/30 bg-amber-500/5">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-amber-400" />
            <span className="text-xs font-semibold text-amber-300">
              Government & Enterprise Administrator Mode Active
            </span>
          </div>
          <Badge variant="warning">ADMIN ZONE</Badge>
        </div>
        {children}
      </div>
    </DashboardLayout>
  );
};
