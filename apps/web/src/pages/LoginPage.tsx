import React, { useState } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { Mail, Lock, ShieldCheck, AlertCircle } from 'lucide-react';
import { AuthLayout } from '../layouts/AuthLayout';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import { useAuthStore } from '../store/useAuthStore';
import { authService } from '../services/authService';
import { toast } from '../lib/sonner';

export const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuthStore();

  // Redirect target preserved from ProtectedRoute
  const from = (location.state as any)?.from?.pathname || '/dashboard';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    setIsLoading(true);

    try {
      const response = await authService.login({ email, password });
      if (response.success && response.data) {
        // Fetch current user profile after login
        const profileRes = await authService.getProfile();
        if (profileRes.success && profileRes.data) {
          login(profileRes.data, response.data.access_token);
          toast.success('Sign in successful.');
          navigate(from, { replace: true });
        }
      } else {
        setErrorMessage(response.message || 'Invalid credentials.');
      }
    } catch (err: any) {
      setErrorMessage(
        err?.response?.data?.message || 'Authentication failed. Please check credentials.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthLayout>
      <div className="glass-card p-8 border border-slate-800 space-y-6">
        <div className="text-center space-y-2">
          <div className="p-3 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 w-fit mx-auto">
            <ShieldCheck className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Sign In to TruthShield X</h2>
          <p className="text-xs text-slate-400">
            Enter your credentials to access the National Digital Trust Platform
          </p>
        </div>

        {errorMessage && (
          <div className="p-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>{errorMessage}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Email Address"
            type="email"
            placeholder="citizen@truthshield.gov.in"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            leftIcon={<Mail className="w-4 h-4" />}
            required
          />

          <Input
            label="Password"
            type="password"
            placeholder="••••••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            leftIcon={<Lock className="w-4 h-4" />}
            required
          />

          <div className="flex items-center justify-between text-xs">
            <Link to="/forgot-password" className="text-cyan-400 hover:underline">
              Forgot Password?
            </Link>
          </div>

          <Button type="submit" isLoading={isLoading} className="w-full">
            Sign In
          </Button>
        </form>

        <div className="text-center text-xs text-slate-400 pt-2 border-t border-slate-800">
          Don't have an account?{' '}
          <Link to="/register" className="text-cyan-400 font-semibold hover:underline">
            Register Account
          </Link>
        </div>
      </div>
    </AuthLayout>
  );
};
