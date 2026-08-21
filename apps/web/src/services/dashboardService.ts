import { api } from './api';
import { StandardResponse, ScanItem, NotificationItem } from '../types';

export interface DashboardData {
  trustScore: number;
  trustStatus: 'TRUSTED' | 'MEDIUM RISK' | 'DANGEROUS';
  totalScans: number;
  threatsBlocked: number;
  activeAlerts: number;
  recentActivity: ScanItem[];
  recentNotifications: NotificationItem[];
}

export const dashboardService = {
  async getDashboardData(): Promise<StandardResponse<DashboardData>> {
    const [statsRes, activityRes] = await Promise.all([
      api.get<StandardResponse<any>>('/dashboard/stats'),
      api.get<StandardResponse<any>>('/dashboard/recent-activity'),
    ]);

    const stats = statsRes.data.data;
    const recentActivity = activityRes.data.data;

    return {
      success: true,
      message: "Dashboard telemetry fetched.",
      data: {
        trustScore: stats.trustScore,
        trustStatus: stats.trustStatus,
        totalScans: stats.totalScans,
        threatsBlocked: stats.threatsBlocked,
        activeAlerts: stats.activeAlerts,
        recentActivity: recentActivity || [],
        recentNotifications: [],
      },
      meta: statsRes.data.meta,
    };
  },
};
