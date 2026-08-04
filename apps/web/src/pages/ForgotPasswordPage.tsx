import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Mail, ArrowLeft, CheckCircle2 } from 'lucide-react';
import { AuthLayout } from '../layouts/AuthLayout';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import { authService } from '../services/authService';

export const ForgotPasswordPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await authService.forgotPassword({ email });
    } catch (e) {
    } finally {
      setIsLoading(false);
      setIsSubmitted(true);
    }
  };

  return (
    <AuthLayout>
      <div className="glass-card p-8 border border-slate-800 space-y-6">
        <div className="text-center space-y-2">
          <h2 className="text-2xl font-bold text-white tracking-tight">Reset Password</h2>
          <p className="text-xs text-slate-400">
            Enter your account email to receive a password reset instructions link
          </p>
        </div>

        {isSubmitted ? (
          <div className="p-4 glass-card border border-emerald-500/30 bg-emerald-500/5 text-center space-y-3">
            <CheckCircle2 className="w-8 h-8 text-emerald-400 mx-auto" />
            <p className="text-xs text-emerald-300 font-semibold">
              If an account exists with {email}, reset instructions have been sent.
            </p>
            <Link to="/login" className="inline-block text-xs text-cyan-400 hover:underline">
              Return to Sign In
            </Link>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Account Email"
              type="email"
              placeholder="user@truthshield.gov.in"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              leftIcon={<Mail className="w-4 h-4" />}
              required
            />
            <Button type="submit" isLoading={isLoading} className="w-full">
              Send Reset Instructions
            </Button>
          </form>
        )}

        <div className="text-center pt-2 border-t border-slate-800">
          <Link
            to="/login"
            className="text-xs text-slate-400 hover:text-white flex items-center justify-center gap-1.5"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Back to Sign In</span>
          </Link>
        </div>
      </div>
    </AuthLayout>
  );
};
