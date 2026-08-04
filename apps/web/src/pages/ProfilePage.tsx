import React, { useEffect, useState } from 'react';
import { User, Lock, Smartphone, ShieldCheck, Laptop, Globe, Trash2 } from 'lucide-react';
import { DashboardLayout } from '../layouts/DashboardLayout';
import { SectionHeader } from '../components/common/SectionHeader';
import { Card } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { authService, UserSession } from '../services/authService';
import { useAuthStore } from '../store/useAuthStore';
import { toast } from '../lib/sonner';

export const ProfilePage: React.FC = () => {
  const { user, setUser } = useAuthStore();

  // Profile Form State
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [phone, setPhone] = useState(user?.phone || '');
  const [isUpdatingProfile, setIsUpdatingProfile] = useState(false);

  // Password Form State
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isChangingPassword, setIsChangingPassword] = useState(false);

  // Active Sessions State
  const [sessions, setSessions] = useState<UserSession[]>([]);
  const [isLoadingSessions, setIsLoadingSessions] = useState(false);

  useEffect(() => {
    fetchProfileAndSessions();
  }, []);

  const fetchProfileAndSessions = async () => {
    try {
      setIsLoadingSessions(true);
      const [profileRes, sessionsRes] = await Promise.all([
        authService.getProfile(),
        authService.getSessions(),
      ]);

      if (profileRes.success && profileRes.data) {
        setUser(profileRes.data);
        setFullName(profileRes.data.full_name);
        setPhone(profileRes.data.phone || '');
      }

      if (sessionsRes.success && sessionsRes.data) {
        setSessions(sessionsRes.data);
      }
    } catch (err: any) {
      console.warn('Real backend profile fetch warning:', err?.message);
    } finally {
      setIsLoadingSessions(false);
    }
  };

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setIsUpdatingProfile(true);
      const res = await authService.updateProfile({
        full_name: fullName,
        phone: phone || undefined,
      });

      if (res.success && res.data) {
        setUser(res.data);
        toast.success('Profile updated successfully.');
      } else {
        toast.error(res.message || 'Profile update failed.');
      }
    } catch (err: any) {
      toast.error(err?.response?.data?.message || 'Failed to update profile.');
    } font-mono finally {
      setIsUpdatingProfile(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      toast.error('New passwords do not match.');
      return;
    }

    try {
      setIsChangingPassword(true);
      const res = await authService.changePassword({
        current_password: currentPassword,
        new_password: newPassword,
      });

      if (res.success) {
        toast.success('Password changed successfully.');
        setCurrentPassword('');
        setNewPassword('');
        setConfirmPassword('');
      } else {
        toast.error(res.message || 'Password change failed.');
      }
    } catch (err: any) {
      toast.error(err?.response?.data?.message || 'Failed to change password.');
    } finally {
      setIsChangingPassword(false);
    }
  };

  const handleRevokeSession = async (sessionId: string) => {
    try {
      const res = await authService.revokeSession(sessionId);
      if (res.success) {
        toast.success('Session revoked.');
        setSessions(sessions.filter((s) => s.id !== sessionId));
      }
    } catch (err: any) {
      toast.error('Failed to revoke session.');
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <SectionHeader
          title="User Profile & Security Settings"
          description="Manage personal account credentials, security preferences, and active device sessions."
          icon={User}
        />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Profile Card (Real API: GET/PUT /users/me) */}
          <Card className="space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <User className="w-4 h-4 text-cyan-400" />
                <span>Account Information</span>
              </h3>
              <Badge variant="info">{user?.role || 'CITIZEN'}</Badge>
            </div>

            <form onSubmit={handleUpdateProfile} className="space-y-4">
              <Input
                label="Full Name"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
              />

              <Input
                label="Email Address"
                value={user?.email || ''}
                disabled
                helperText="Email address cannot be changed."
              />

              <Input
                label="Phone Number"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="+91 98765 43210"
              />

              <div className="flex items-center justify-between pt-2">
                <span className="text-xs text-slate-400">
                  Email Verification:{' '}
                  <span className={user?.email_verified ? 'text-emerald-400' : 'text-amber-400'}>
                    {user?.email_verified ? 'Verified' : 'Unverified'}
                  </span>
                </span>
                <Button type="submit" isLoading={isUpdatingProfile} size="sm">
                  Save Changes
                </Button>
              </div>
            </form>
          </Card>

          {/* Change Password Card (Real API: PUT /users/change-password) */}
          <Card className="space-y-4">
            <div className="pb-3 border-b border-slate-800">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Lock className="w-4 h-4 text-cyan-400" />
                <span>Security Credentials</span>
              </h3>
            </div>

            <form onSubmit={handleChangePassword} className="space-y-4">
              <Input
                label="Current Password"
                type="password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                required
              />

              <Input
                label="New Password"
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
              />

              <Input
                label="Confirm New Password"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />

              <div className="flex justify-end pt-2">
                <Button type="submit" isLoading={isChangingPassword} size="sm">
                  Update Password
                </Button>
              </div>
            </form>
          </Card>
        </div>

        {/* Active Device Sessions Card (Real API: GET/DELETE /users/sessions) */}
        <Card className="space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <div className="flex items-center gap-2">
              <Smartphone className="w-4 h-4 text-cyan-400" />
              <h3 className="text-base font-bold text-white">Active Device Sessions</h3>
            </div>
            <span className="text-xs text-slate-400">{sessions.length} Active Sessions</span>
          </div>

          {isLoadingSessions ? (
            <p className="text-xs text-slate-400 animate-pulse">Loading active sessions...</p>
          ) : sessions.length === 0 ? (
            <div className="p-4 text-center bg-slate-900/50 rounded-xl text-xs text-slate-400">
              No remote device sessions active. Current session only.
            </div>
          ) : (
            <div className="space-y-3">
              {sessions.map((sess) => (
                <div
                  key={sess.id}
                  className="flex items-center justify-between p-3.5 rounded-xl bg-slate-900 border border-slate-800"
                >
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-lg bg-slate-950 text-cyan-400 border border-slate-800">
                      <Laptop className="w-4 h-4" />
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <h4 className="text-xs font-bold text-white">
                          {sess.browser || 'Browser'} on {sess.operating_system || 'OS'}
                        </h4>
                        {sess.is_current && (
                          <Badge variant="success" className="text-[9px]">
                            Current Device
                          </Badge>
                        )}
                      </div>
                      <p className="text-[11px] text-slate-400 font-mono">
                        IP: {sess.ip_address} ({sess.country || 'India'}) • Last Active:{' '}
                        {new Date(sess.last_activity).toLocaleTimeString()}
                      </p>
                    </div>
                  </div>

                  {!sess.is_current && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleRevokeSession(sess.id)}
                      className="text-red-400 hover:text-red-300"
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  )}
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </DashboardLayout>
  );
};
