import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Link, useNavigate } from 'react-router-dom';
import { UserPlus, CheckCircle2 } from 'lucide-react';
import { useMutation } from '@tanstack/react-query';

import { registerSchema, RegisterInput } from './auth.schema';
import { authService } from '../../services/authService';
import { Card } from '../../components/ui/Card';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import { Alert } from '../../components/ui/Alert';

export const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterInput>({
    resolver: zodResolver(registerSchema),
  });

  const registerMutation = useMutation({
    mutationFn: authService.register,
    onSuccess: () => {
      setSuccessMessage('Account created successfully! Redirecting to login...');
      setTimeout(() => {
        navigate('/login');
      }, 1500);
    },
    onError: (error: any) => {
      const msg = error.response?.data?.message || 'Registration failed. Please check input values.';
      setErrorMessage(msg);
    },
  });

  const onSubmit = (data: RegisterInput) => {
    setErrorMessage(null);
    setSuccessMessage(null);
    registerMutation.mutate(data);
  };

  return (
    <div className="flex flex-col items-center justify-center py-6">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center space-y-2">
          <div className="inline-flex p-3 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 mb-2">
            <UserPlus className="w-8 h-8" />
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-white">Create Account</h1>
          <p className="text-sm text-slate-400">
            Join TruthShield X for verified AI authenticity protection
          </p>
        </div>

        <Card variant="glass">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {errorMessage && <Alert type="error" message={errorMessage} />}
            {successMessage && <Alert type="success" message={successMessage} />}

            <Input
              label="Full Name"
              placeholder="Aarav Sharma"
              {...register('full_name')}
              error={errors.full_name?.message}
            />

            <Input
              label="Email Address"
              type="email"
              placeholder="aarav@example.com"
              {...register('email')}
              error={errors.email?.message}
            />

            <Input
              label="Phone Number (Optional)"
              type="tel"
              placeholder="+919876543210"
              {...register('phone')}
              error={errors.phone?.message}
            />

            <Input
              label="Password"
              type="password"
              placeholder="Min 10 chars (uppercase, symbol, number)"
              {...register('password')}
              error={errors.password?.message}
              helperText="Must include at least 10 chars, 1 uppercase, 1 lowercase, 1 digit & 1 special character."
            />

            <Button
              type="submit"
              variant="primary"
              className="w-full mt-2"
              isLoading={registerMutation.isPending}
            >
              <span>Register Account</span>
              <CheckCircle2 className="w-4 h-4 ml-2" />
            </Button>
          </form>

          <div className="mt-6 pt-6 border-t border-slate-800 text-center text-sm text-slate-400">
            Already have an account?{' '}
            <Link to="/login" className="text-cyan-400 hover:text-cyan-300 font-medium">
              Sign In
            </Link>
          </div>
        </Card>
      </div>
    </div>
  );
};
