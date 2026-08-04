import { useSidebarStore } from '../store/useSidebarStore';

export function useSidebar() {
  const store = useSidebarStore();
  return store;
}
