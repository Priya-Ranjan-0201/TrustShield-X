import { create } from 'zustand';

export type Theme = 'dark' | 'light' | 'system';

interface ThemeState {
  theme: Theme;
  resolvedTheme: 'dark' | 'light';
  setTheme: (theme: Theme) => void;
}

const getSystemTheme = (): 'dark' | 'light' =>
  window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
    ? 'dark'
    : 'light';

const applyThemeToDOM = (resolved: 'dark' | 'light') => {
  const root = document.documentElement;
  if (resolved === 'dark') {
    root.classList.add('dark');
    root.classList.remove('light');
  } else {
    root.classList.add('light');
    root.classList.remove('dark');
  }
};

const initialTheme = (localStorage.getItem('tsx-theme') as Theme) || 'system';
const initialResolved = initialTheme === 'system' ? getSystemTheme() : initialTheme;
applyThemeToDOM(initialResolved);

export const useThemeStore = create<ThemeState>((set) => ({
  theme: initialTheme,
  resolvedTheme: initialResolved,

  setTheme: (theme: Theme) => {
    localStorage.setItem('tsx-theme', theme);
    const resolved = theme === 'system' ? getSystemTheme() : theme;
    applyThemeToDOM(resolved);
    set({ theme, resolvedTheme: resolved });
  },
}));

// Listen to OS system theme changes
if (window.matchMedia) {
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    const currentTheme = useThemeStore.getState().theme;
    if (currentTheme === 'system') {
      const newResolved = e.matches ? 'dark' : 'light';
      applyThemeToDOM(newResolved);
      useThemeStore.setState({ resolvedTheme: newResolved });
    }
  });
}
