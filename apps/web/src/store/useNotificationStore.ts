import { create } from 'zustand';
import { NotificationItem } from '../types';

interface NotificationState {
  notifications: NotificationItem[];
  isDrawerOpen: boolean;
  setNotifications: (notifications: NotificationItem[]) => void;
  markAsRead: (id: string) => void;
  markAllAsRead: () => void;
  toggleDrawer: () => void;
  setDrawerOpen: (open: boolean) => void;
}

export const useNotificationStore = create<NotificationState>((set) => ({
  notifications: [],
  isDrawerOpen: false,

  setNotifications: (notifications) => set({ notifications }),

  markAsRead: (id) =>
    set((state) => ({
      notifications: state.notifications.map((n) =>
        n.id === id ? { ...n, read: true } : n
      ),
    })),

  markAllAsRead: () =>
    set((state) => ({
      notifications: state.notifications.map((n) => ({ ...n, read: true })),
    })),

  toggleDrawer: () => set((state) => ({ isDrawerOpen: !state.isDrawerOpen })),

  setDrawerOpen: (isDrawerOpen) => set({ isDrawerOpen }),
}));
