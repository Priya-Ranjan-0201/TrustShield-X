import { create } from 'zustand';

interface SidebarState {
  isCollapsed: boolean;
  isMobileOpen: boolean;
  toggleCollapse: () => void;
  setCollapsed: (collapsed: boolean) => void;
  toggleMobile: () => void;
  setMobileOpen: (open: boolean) => void;
}

const initialCollapsed = localStorage.getItem('tsx-sidebar-collapsed') === 'true';

export const useSidebarStore = create<SidebarState>((set) => ({
  isCollapsed: initialCollapsed,
  isMobileOpen: false,

  toggleCollapse: () =>
    set((state) => {
      const next = !state.isCollapsed;
      localStorage.setItem('tsx-sidebar-collapsed', String(next));
      return { isCollapsed: next };
    }),

  setCollapsed: (isCollapsed: boolean) => {
    localStorage.setItem('tsx-sidebar-collapsed', String(isCollapsed));
    set({ isCollapsed });
  },

  toggleMobile: () =>
    set((state) => ({ isMobileOpen: !state.isMobileOpen })),

  setMobileOpen: (isMobileOpen: boolean) => set({ isMobileOpen }),
}));
