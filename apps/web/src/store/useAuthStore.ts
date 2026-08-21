import { create } from 'zustand';
import { User } from '../types';

interface AuthState {
  accessToken: string | null;
  user: User | null;
  isAuthenticated: boolean;
  isInitializing: boolean;
  isInitialized: boolean;
  login: (p1: any, p2?: any) => void;
  logout: () => void | Promise<void>;
  initialize: () => Promise<void>;
  setAuth: (accessToken: string, user: User) => void;
  setAccessToken: (accessToken: string) => void;
  setUser: (user: User) => void;
  clearAuth: () => void;
  setInitializing: (isInitializing: boolean) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  accessToken: null,
  user: null,
  isAuthenticated: false,
  isInitializing: false,
  isInitialized: true,

  login: (p1: any, p2?: any) => {
    let token: string | null = null;
    let user: User | null = null;

    if (typeof p1 === 'string') {
      token = p1;
      user = p2;
    } else {
      user = p1;
      token = p2;
    }

    set({
      accessToken: token,
      user,
      isAuthenticated: true,
      isInitializing: false,
      isInitialized: true,
    });
  },

  logout: () => {
    set({
      accessToken: null,
      user: null,
      isAuthenticated: false,
      isInitializing: false,
      isInitialized: true,
    });
  },

  initialize: async () => {
    set({ isInitializing: false, isInitialized: true });
  },

  setAuth: (accessToken, user) =>
    set({
      accessToken,
      user,
      isAuthenticated: true,
      isInitializing: false,
      isInitialized: true,
    }),

  setAccessToken: (accessToken) =>
    set({
      accessToken,
      isAuthenticated: true,
    }),

  setUser: (user) =>
    set({
      user,
    }),

  clearAuth: () =>
    set({
      accessToken: null,
      user: null,
      isAuthenticated: false,
      isInitializing: false,
      isInitialized: true,
    }),

  setInitializing: (isInitializing) =>
    set({
      isInitializing,
    }),
}));
