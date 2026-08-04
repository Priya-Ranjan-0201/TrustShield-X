import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { ShieldCheck, ArrowRight } from 'lucide-react';
import { useMutation } from '@tanstack/react-query';

import { loginSchema, LoginInput } from './auth.schema';
import { authService } from '../../services/authService';
import { useAuthStore } from '../../store/useAuthStore';
import { Card } from '../../components/ui/Card';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import { Alert } from '../../components/ui/Alert';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const setAuth = useAuthStore((state) => state.setAuth);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const from = (location.state as any)?.from?.pathname || '/profile';

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginInput>({
    resolver: zodResolver(loginSchema),
  });

  const loginMutation = useMutation({
    mutationFn: authService.login,
    onSuccess: async (res) => {
      if (res.data?.access_token) {
        // Fetch user profile using access token
        const profileRes = await authService.getProfile();
        if (profileRes.data) {
          setAuth(res.data.access_token, profileRes.data);
          navigate(from, { replace: true });
        }
      }
    },
    onError: (error: any) => {
      const msg = error.response?.data?.message || 'Login failed. Please check your credentials.';
      setErrorMessage(msg);
    },
  });

  const onSubmit = (data: LoginInput) => {
    setErrorMessage(null);
    loginMutation.mutate(data);
  };

  return (
    <div className="flex flex-col items-center justify-center py-6">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center space-y-2">
          <div className="inline-flex p-3 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 mb-2">
            <ShieldCheck className="w-8 h-8" />
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-white">Welcome Back</h1>
          <p className="text-sm text-slate-400">
            Sign in to access your TruthShield X trust dashboard
          </p>
        </div>

        <Card variant="glass">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {errorMessage && <Alert type="error" message={errorMessage} />}

            <Input
              label="Email Address"
              type="email"
              placeholder="name@example.com"
              {...register('email')}
              error={errors.email?.message}
            />

            <div className="space-y-1">
              <div className="flex items-center justify-between">
                <label className="block text-xs font-semibold tracking-wider text-slate-300 uppercase">
                  Password
                </label>
                <Link to="/forgot-password" className="text-xs text-cyan-400 hover:text-cyan-300">
                  Forgot password?
                </Link>
              </div>
              <Input
                type="password"
                placeholder="••••••••••••"
                {...register('password')}
                error={errors.password?.message}
              />
            </div>

            <Button
              type="submit"
              variant="primary"
              className="w-full mt-2"
              isLoading={loginMutation.isPending}
            >
              <span>Sign In</span>
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </form>

          <div className="mt-6 pt-6 border-t border-slate-800 text-center text-sm text-slate-400">
            Don't have an account?{' '}
            <Link to="/register" className="text-cyan-400 hover:text-cyan-300 font-medium">
              Create an account
            </Link>
          </div>
        </Card>
      </div>
    </div>
  );
};
