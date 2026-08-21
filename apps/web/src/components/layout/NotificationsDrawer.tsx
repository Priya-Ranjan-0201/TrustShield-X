import React, { useEffect } from 'react';
import { Drawer } from '../ui/Drawer';
import { useNotificationStore } from '../../store/useNotificationStore';
import { notificationsService } from '../../services/notificationsService';
import { Check, AlertTriangle, Info, ShieldAlert } from 'lucide-react';
import { Badge } from '../ui/Badge';
import { EmptyState } from '../ui/EmptyState';

export const NotificationsDrawer: React.FC = () => {
  const { notifications, isDrawerOpen, setDrawerOpen, setNotifications, markAsRead, markAllAsRead } =
    useNotificationStore();

  useEffect(() => {
    if (isDrawerOpen) {
      notificationsService.getNotifications().then((res) => {
        if (res.success && res.data) {
          setNotifications(res.data);
        }
      }).catch(() => {});
    }
  }, [isDrawerOpen, setNotifications]);

  const handleMarkRead = async (id: string) => {
    markAsRead(id);
    await notificationsService.markAsRead(id);
  };

  const handleMarkAllRead = async () => {
    markAllAsRead();
    await notificationsService.markAllAsRead();
  };

  const severityIcons = {
    info: <Info className="w-4 h-4 text-cyan-400" />,
    success: <Check className="w-4 h-4 text-emerald-400" />,
    warning: <AlertTriangle className="w-4 h-4 text-amber-400" />,
    critical: <ShieldAlert className="w-4 h-4 text-red-400" />,
  };

  return (
    <Drawer
      isOpen={isDrawerOpen}
      onClose={() => setDrawerOpen(false)}
      title="Notifications & Security Alerts"
    >
      <div className="space-y-4">
        {notifications.length > 0 && (
          <div className="flex items-center justify-between pb-2 border-b border-slate-800">
            <span className="text-xs text-slate-400">
              {notifications.filter((n) => !n.read).length} Unread Alerts
            </span>
            <button
              onClick={markAllAsRead}
              className="text-xs font-semibold text-cyan-400 hover:underline"
            >
              Mark all as read
            </button>
          </div>
        )}

        {notifications.length === 0 ? (
          <EmptyState
            title="No Notifications"
            description="You are all caught up! Zero unread security alerts."
          />
        ) : (
          <div className="space-y-2.5">
            {notifications.map((notif) => (
              <div
                key={notif.id}
                onClick={() => markAsRead(notif.id)}
                className={`p-3.5 rounded-xl border transition-all cursor-pointer ${
                  notif.read
                    ? 'bg-slate-900/40 border-slate-800/80 opacity-75'
                    : 'bg-slate-900 border-slate-700 shadow-md'
                }`}
              >
                <div className="flex items-start gap-3">
                  <div className="p-2 rounded-lg bg-slate-950 border border-slate-800">
                    {severityIcons[notif.severity]}
                  </div>
                  <div className="flex-1 space-y-1">
                    <div className="flex items-center justify-between">
                      <h4 className="text-xs font-bold text-white">{notif.title}</h4>
                      <span className="text-[10px] text-slate-500 font-mono">
                        {new Date(notif.created_at).toLocaleTimeString([], {
                          hour: '2-digit',
                          minute: '2-digit',
                        })}
                      </span>
                    </div>
                    <p className="text-xs text-slate-300 leading-relaxed">{notif.message}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </Drawer>
  );
};
