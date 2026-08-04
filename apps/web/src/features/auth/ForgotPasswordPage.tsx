import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Link } from 'react-router-dom';
import { KeyRound, ArrowLeft, Send } from 'lucide-react';
import { useMutation } from '@tanstack/react-query';

import { forgotPasswordSchema, ForgotPasswordInput } from './auth.schema';
import { authService } from '../../services/authService';
import { Card } from '../../components/ui/Card';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import { Alert } from '../../components/ui/Alert';

export const ForgotPasswordPage: React.FC = () => {
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ForgotPasswordInput>({
    resolver: zodResolver(forgotPasswordSchema),
  });

  const forgotMutation = useMutation({
    mutationFn: authService.forgotPassword,
    onSuccess: (res) => {
      setSuccessMessage(
        res.data?.info || 'If an account exists for this email, password reset instructions have been initiated (Structure Stub).'
      );
    },
    onError: (error: any) => {
      setErrorMessage(error.response?.data?.message || 'Password reset request failed.');
    },
  });

  const onSubmit = (data: ForgotPasswordInput) => {
    setErrorMessage(null);
    setSuccessMessage(null);
    forgotMutation.mutate(data);
  };

  return (
    <div className="flex flex-col items-center justify-center py-6">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center space-y-2">
          <div className="inline-flex p-3 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 mb-2">
            <KeyRound className="w-8 h-8" />
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-white">Reset Password</h1>
          <p className="text-sm text-slate-400">
            Enter your registered email address to receive password reset instructions
          </p>
        </div>

        <Card variant="glass">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {errorMessage && <Alert type="error" message={errorMessage} />}
            {successMessage && <Alert type="info" message={successMessage} />}

            <Input
              label="Email Address"
              type="email"
              placeholder="name@example.com"
              {...register('email')}
              error={errors.email?.message}
            />

            <Button
              type="submit"
              variant="primary"
              className="w-full mt-2"
              isLoading={forgotMutation.isPending}
            >
              <span>Send Reset Instructions</span>
              <Send className="w-4 h-4 ml-2" />
            </Button>
          </form>

          <div className="mt-6 pt-6 border-t border-slate-800 text-center text-sm text-slate-400">
            <Link to="/login" className="inline-flex items-center text-cyan-400 hover:text-cyan-300 font-medium">
              <ArrowLeft className="w-4 h-4 mr-1.5" />
              Back to Sign In
            </Link>
          </div>
        </Card>
      </div>
    </div>
  );
};
