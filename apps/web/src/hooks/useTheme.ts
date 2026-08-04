import { useThemeStore } from '../store/useThemeStore';

export function useTheme() {
  const { theme, resolvedTheme, setTheme } = useThemeStore();
  return { theme, resolvedTheme, setTheme };
}
