import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Link, useSearchParams, useNavigate } from 'react-router-dom';
import { Lock, CheckCircle2 } from 'lucide-react';
import { useMutation } from '@tanstack/react-query';

import { resetPasswordSchema, ResetPasswordInput } from './auth.schema';
import { authService } from '../../services/authService';
import { Card } from '../../components/ui/Card';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import { Alert } from '../../components/ui/Alert';

export const ResetPasswordPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const tokenFromUrl = searchParams.get('token') || '';

  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ResetPasswordInput>({
    resolver: zodResolver(resetPasswordSchema),
    defaultValues: {
      token: tokenFromUrl,
    },
  });

  const resetMutation = useMutation({
    mutationFn: authService.resetPassword,
    onSuccess: (res) => {
      setSuccessMessage(res.data?.info || 'Password reset validated (Structure Stub). Redirecting...');
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    },
    onError: (error: any) => {
      setErrorMessage(error.response?.data?.message || 'Failed to reset password.');
    },
  });

  const onSubmit = (data: ResetPasswordInput) => {
    setErrorMessage(null);
    setSuccessMessage(null);
    resetMutation.mutate(data);
  };

  return (
    <div className="flex flex-col items-center justify-center py-6">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center space-y-2">
          <div className="inline-flex p-3 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 mb-2">
            <Lock className="w-8 h-8" />
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-white">Set New Password</h1>
          <p className="text-sm text-slate-400">
            Choose a new strong password for your account
          </p>
        </div>

        <Card variant="glass">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {errorMessage && <Alert type="error" message={errorMessage} />}
            {successMessage && <Alert type="success" message={successMessage} />}

            <Input
              label="Reset Token"
              placeholder="Paste token if not in URL"
              {...register('token')}
              error={errors.token?.message}
            />

            <Input
              label="New Password"
              type="password"
              placeholder="••••••••••••"
              {...register('new_password')}
              error={errors.new_password?.message}
            />

            <Input
              label="Confirm New Password"
              type="password"
              placeholder="••••••••••••"
              {...register('confirm_password')}
              error={errors.confirm_password?.message}
            />

            <Button
              type="submit"
              variant="primary"
              className="w-full mt-2"
              isLoading={resetMutation.isPending}
            >
              <span>Confirm New Password</span>
              <CheckCircle2 className="w-4 h-4 ml-2" />
            </Button>
          </form>

          <div className="mt-6 pt-6 border-t border-slate-800 text-center text-sm text-slate-400">
            <Link to="/login" className="text-cyan-400 hover:text-cyan-300 font-medium">
              Back to Sign In
            </Link>
          </div>
        </Card>
      </div>
    </div>
  );
};
