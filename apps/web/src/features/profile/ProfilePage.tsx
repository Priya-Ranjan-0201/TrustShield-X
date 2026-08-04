import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { User, ShieldCheck, CheckCircle2, AlertTriangle, KeyRound, Save, Mail, Sparkles, Laptop, Smartphone, Globe, LogOut, ShieldAlert } from 'lucide-react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { profileUpdateSchema, changePasswordSchema, ProfileUpdateInput, ChangePasswordInput } from '../auth/auth.schema';
import { authService, UserSession } from '../../services/authService';
import { useAuthStore } from '../../store/useAuthStore';
import { Card } from '../../components/ui/Card';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import { Alert } from '../../components/ui/Alert';

export const ProfilePage: React.FC = () => {
  const { user, setUser } = useAuthStore();
  const queryClient = useQueryClient();

  const [profileMsg, setProfileMsg] = useState<{ type: 'success' | 'error'; message: string } | null>(null);
  const [pwMsg, setPwMsg] = useState<{ type: 'success' | 'error'; message: string } | null>(null);
  const [sessionMsg, setSessionMsg] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  // 1. Fetch Active Sessions
  const { data: sessionData, isLoading: isSessionsLoading } = useQuery({
    queryKey: ['active-sessions'],
    queryFn: authService.getSessions,
  });

  const sessions = sessionData?.data || [];

  // Revoke Single Session Mutation
  const revokeSessionMutation = useMutation({
    mutationFn: authService.revokeSession,
    onSuccess: () => {
      setSessionMsg({ type: 'success', message: 'Session revoked successfully.' });
      queryClient.invalidateQueries({ queryKey: ['active-sessions'] });
    },
    onError: (err: any) => {
      setSessionMsg({ type: 'error', message: err.response?.data?.message || 'Failed to revoke session.' });
    },
  });

  // Revoke All Sessions Mutation
  const revokeAllMutation = useMutation({
    mutationFn: authService.revokeAllSessions,
    onSuccess: () => {
      setSessionMsg({ type: 'success', message: 'All other active sessions have been terminated.' });
      queryClient.invalidateQueries({ queryKey: ['active-sessions'] });
    },
    onError: (err: any) => {
      setSessionMsg({ type: 'error', message: err.response?.data?.message || 'Failed to revoke all sessions.' });
    },
  });

  // 2. Profile Update Form
  const {
    register: regProfile,
    handleSubmit: handleProfileSubmit,
    formState: { errors: profileErrors },
  } = useForm<ProfileUpdateInput>({
    resolver: zodResolver(profileUpdateSchema),
    defaultValues: {
      full_name: user?.full_name || '',
      phone: user?.phone || '',
    },
  });

  const profileMutation = useMutation({
    mutationFn: authService.updateProfile,
    onSuccess: (res) => {
      if (res.data) {
        setUser(res.data);
        setProfileMsg({ type: 'success', message: 'Profile details updated successfully.' });
      }
    },
    onError: (error: any) => {
      setProfileMsg({
        type: 'error',
        message: error.response?.data?.message || 'Failed to update profile.',
      });
    },
  });

  // 3. Change Password Form
  const {
    register: regPw,
    handleSubmit: handlePwSubmit,
    reset: resetPwForm,
    formState: { errors: pwErrors },
  } = useForm<ChangePasswordInput>({
    resolver: zodResolver(changePasswordSchema),
  });

  const pwMutation = useMutation({
    mutationFn: authService.changePassword,
    onSuccess: () => {
      setPwMsg({ type: 'success', message: 'Password updated successfully.' });
      resetPwForm();
    },
    onError: (error: any) => {
      setPwMsg({
        type: 'error',
        message: error.response?.data?.message || 'Failed to change password.',
      });
    },
  });

  if (!user) return null;

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl glass-card border border-cyan-500/30 bg-gradient-to-r from-slate-900 via-slate-900 to-cyan-950/30">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-2xl bg-cyan-500/20 border border-cyan-500/40 flex items-center justify-center text-cyan-400 text-2xl font-bold shadow-lg shadow-cyan-500/20">
            {user.full_name.charAt(0).toUpperCase()}
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white flex items-center gap-2">
              {user.full_name}
              <Sparkles className="w-5 h-5 text-cyan-400" />
            </h1>
            <p className="text-sm text-slate-400 flex items-center gap-2 mt-0.5">
              <Mail className="w-3.5 h-3.5" />
              <span>{user.email}</span>
            </p>
          </div>
        </div>

        {/* Redundant Badges */}
        <div className="flex flex-wrap items-center gap-2">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Active Account</span>
          </span>

          {user.email_verified ? (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Email Verified</span>
            </span>
          ) : (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/30">
              <AlertTriangle className="w-3.5 h-3.5" />
              <span>Unverified</span>
            </span>
          )}

          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold uppercase bg-slate-800 text-slate-200 border border-slate-700">
            <User className="w-3.5 h-3.5 text-cyan-400" />
            <span>{user.role}</span>
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Form 1: Edit Profile Details */}
        <Card variant="glass" className="space-y-6">
          <div className="flex items-center gap-2.5 pb-4 border-b border-slate-800">
            <User className="w-5 h-5 text-cyan-400" />
            <h2 className="text-lg font-bold text-white">Profile Details</h2>
          </div>

          {profileMsg && <Alert type={profileMsg.type} message={profileMsg.message} />}

          <form onSubmit={handleProfileSubmit((data) => profileMutation.mutate(data))} className="space-y-4">
            <Input
              label="Full Name"
              {...regProfile('full_name')}
              error={profileErrors.full_name?.message}
            />

            <Input
              label="Email Address"
              value={user.email}
              disabled
              helperText="Email address cannot be changed."
            />

            <Input
              label="Phone Number"
              placeholder="+919876543210"
              {...regProfile('phone')}
              error={profileErrors.phone?.message}
            />

            <div className="pt-2">
              <Button
                type="submit"
                variant="primary"
                className="w-full"
                isLoading={profileMutation.isPending}
              >
                <Save className="w-4 h-4 mr-2" />
                <span>Save Changes</span>
              </Button>
            </div>
          </form>
        </Card>

        {/* Form 2: Change Password */}
        <Card variant="glass" className="space-y-6">
          <div className="flex items-center gap-2.5 pb-4 border-b border-slate-800">
            <KeyRound className="w-5 h-5 text-cyan-400" />
            <h2 className="text-lg font-bold text-white">Security & Password</h2>
          </div>

          {pwMsg && <Alert type={pwMsg.type} message={pwMsg.message} />}

          <form onSubmit={handlePwSubmit((data) => pwMutation.mutate(data))} className="space-y-4">
            <Input
              label="Current Password"
              type="password"
              placeholder="••••••••••••"
              {...regPw('current_password')}
              error={pwErrors.current_password?.message}
            />

            <Input
              label="New Password"
              type="password"
              placeholder="••••••••••••"
              {...regPw('new_password')}
              error={pwErrors.new_password?.message}
            />

            <Input
              label="Confirm New Password"
              type="password"
              placeholder="••••••••••••"
              {...regPw('confirm_password')}
              error={pwErrors.confirm_password?.message}
            />

            <div className="pt-2">
              <Button
                type="submit"
                variant="secondary"
                className="w-full"
                isLoading={pwMutation.isPending}
              >
                <KeyRound className="w-4 h-4 mr-2 text-cyan-400" />
                <span>Update Password</span>
              </Button>
            </div>
          </form>
        </Card>
      </div>

      {/* Active Sessions Management Section */}
      <Card variant="glass" className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
          <div className="flex items-center gap-2.5">
            <Globe className="w-5 h-5 text-cyan-400" />
            <div>
              <h2 className="text-lg font-bold text-white">Active Device Sessions</h2>
              <p className="text-xs text-slate-400">Manage and terminate active logged-in device sessions</p>
            </div>
          </div>

          <Button
            variant="outline"
            size="sm"
            onClick={() => revokeAllMutation.mutate()}
            isLoading={revokeAllMutation.isPending}
            className="text-red-400 border-red-500/30 hover:border-red-500/60 hover:bg-red-950/20"
          >
            <ShieldAlert className="w-4 h-4 mr-1.5" />
            <span>Terminate All Other Sessions</span>
          </Button>
        </div>

        {sessionMsg && <Alert type={sessionMsg.type} message={sessionMsg.message} />}

        {isSessionsLoading ? (
          <p className="text-sm text-slate-400 py-4 text-center">Loading active sessions...</p>
        ) : sessions.length === 0 ? (
          <p className="text-sm text-slate-400 py-4 text-center">No active sessions found.</p>
        ) : (
          <div className="divide-y divide-slate-800/60">
            {sessions.map((s: UserSession) => (
              <div key={s.id} className="py-4 flex items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-300">
                    {s.device_name?.includes('Mobile') ? (
                      <Smartphone className="w-5 h-5 text-cyan-400" />
                    ) : (
                      <Laptop className="w-5 h-5 text-cyan-400" />
                    )}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <p className="text-sm font-semibold text-white">
                        {s.browser || 'Browser'} on {s.operating_system || 'Device'}
                      </p>
                      {s.is_current && (
                        <span className="px-2 py-0.5 rounded text-[10px] uppercase font-bold bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                          Current Session
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-slate-400 mt-0.5">
                      IP: {s.ip_address} • Last Active: {new Date(s.last_activity).toLocaleString()}
                    </p>
                  </div>
                </div>

                {!s.is_current && (
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => revokeSessionMutation.mutate(s.id)}
                    isLoading={revokeSessionMutation.isPending}
                    className="text-xs text-slate-400 hover:text-red-400"
                  >
                    <LogOut className="w-3.5 h-3.5 mr-1" />
                    <span>Revoke</span>
                  </Button>
                )}
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
};
