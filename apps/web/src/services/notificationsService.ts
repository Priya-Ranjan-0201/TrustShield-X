import { api } from './api';
import { StandardResponse, NotificationItem } from '../types';

export const notificationsService = {
  async getNotifications(): Promise<StandardResponse<NotificationItem[]>> {
    const res = await api.get<StandardResponse<NotificationItem[]>>('/notifications');
    return res.data;
  },

  async markAsRead(id: string): Promise<StandardResponse<any>> {
    const res = await api.put<StandardResponse<any>>(`/notifications/${id}/read`);
    return res.data;
  },

  async markAllAsRead(): Promise<StandardResponse<any>> {
    const res = await api.put<StandardResponse<any>>('/notifications/read-all');
    return res.data;
  },
};
