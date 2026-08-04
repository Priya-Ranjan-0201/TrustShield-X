import React from 'react';
import { Bell, CheckCheck } from 'lucide-react';
import { DashboardLayout } from '../layouts/DashboardLayout';
import { SectionHeader } from '../components/common/SectionHeader';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { useNotificationStore } from '../store/useNotificationStore';

export const NotificationsPage: React.FC = () => {
  const { notifications, markAsRead, markAllAsRead } = useNotificationStore();

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <SectionHeader
          title="Security Notifications & Alerts"
          description="Real-time threat notifications, system security events, and audit logs."
          icon={Bell}
          action={
            <Button
              variant="outline"
              size="sm"
              onClick={markAllAsRead}
              leftIcon={<CheckCheck className="w-4 h-4 text-cyan-400" />}
            >
              Mark All as Read
            </Button>
          }
        />

        <Card className="space-y-3">
          {notifications.map((notif) => (
            <div
              key={notif.id}
              onClick={() => markAsRead(notif.id)}
              className={`p-4 rounded-xl border transition-all cursor-pointer ${
                notif.read
                  ? 'bg-slate-900/40 border-slate-800/80 opacity-75'
                  : 'bg-slate-900 border-slate-700 shadow-md'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <h4 className="text-sm font-bold text-white">{notif.title}</h4>
                    <Badge variant={notif.severity === 'critical' ? 'danger' : 'info'}>
                      {notif.severity}
                    </Badge>
                  </div>
                  <p className="text-xs text-slate-300">{notif.message}</p>
                </div>
                <span className="text-[10px] text-slate-500 font-mono">
                  {new Date(notif.created_at).toLocaleString()}
                </span>
              </div>
            </div>
          ))}
        </Card>
      </div>
    </DashboardLayout>
  );
};
