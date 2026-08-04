import { api } from './api';
import { StandardResponse, TokenResponse, User } from '../types';
import { RegisterInput, LoginInput, ProfileUpdateInput, ChangePasswordInput, ForgotPasswordInput, ResetPasswordInput } from '../features/auth/auth.schema';

export interface UserSession {
  id: string;
  device_name?: string;
  browser?: string;
  operating_system?: string;
  ip_address: string;
  country?: string;
  last_activity: string;
  is_active: boolean;
  created_at: string;
  expires_at: string;
  is_current?: boolean;
}

export const authService = {
  async register(data: RegisterInput): Promise<StandardResponse<User>> {
    const res = await api.post<StandardResponse<User>>('/auth/register', data);
    return res.data;
  },

  async login(data: LoginInput): Promise<StandardResponse<TokenResponse>> {
    const res = await api.post<StandardResponse<TokenResponse>>('/auth/login', data);
    return res.data;
  },

  async logout(): Promise<StandardResponse<{ logged_out: boolean }>> {
    const res = await api.post<StandardResponse<{ logged_out: boolean }>>('/auth/logout');
    return res.data;
  },

  async refresh(): Promise<StandardResponse<TokenResponse>> {
    const res = await api.post<StandardResponse<TokenResponse>>('/auth/refresh');
    return res.data;
  },

  async verifyEmail(token: string): Promise<StandardResponse<any>> {
    const res = await api.post<StandardResponse<any>>('/auth/verify-email', { token });
    return res.data;
  },

  async resendVerification(email: string): Promise<StandardResponse<any>> {
    const res = await api.post<StandardResponse<any>>('/auth/resend-verification', { email });
    return res.data;
  },

  async getProfile(): Promise<StandardResponse<User>> {
    const res = await api.get<StandardResponse<User>>('/users/me');
    return res.data;
  },

  async updateProfile(data: ProfileUpdateInput): Promise<StandardResponse<User>> {
    const res = await api.put<StandardResponse<User>>('/users/me', data);
    return res.data;
  },

  async changePassword(data: ChangePasswordInput): Promise<StandardResponse<{ password_changed: boolean }>> {
    const res = await api.put<StandardResponse<{ password_changed: boolean }>>('/users/change-password', data);
    return res.data;
  },

  async getSessions(): Promise<StandardResponse<UserSession[]>> {
    const res = await api.get<StandardResponse<UserSession[]>>('/users/sessions');
    return res.data;
  },

  async revokeSession(sessionId: string): Promise<StandardResponse<any>> {
    const res = await api.delete<StandardResponse<any>>(`/users/sessions/${sessionId}`);
    return res.data;
  },

  async revokeAllSessions(): Promise<StandardResponse<any>> {
    const res = await api.delete<StandardResponse<any>>('/users/sessions');
    return res.data;
  },

  async forgotPassword(data: ForgotPasswordInput): Promise<StandardResponse<any>> {
    const res = await api.post<StandardResponse<any>>('/users/forgot-password', data);
    return res.data;
  },

  async resetPassword(data: ResetPasswordInput): Promise<StandardResponse<any>> {
    const res = await api.post<StandardResponse<any>>('/users/reset-password', data);
    return res.data;
  },
};
