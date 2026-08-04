import { z } from 'zod';

const COMMON_PASSWORDS = [
  '123456', '123456789', '12345678', '12345', '1234567', '1234', '1234567890', '0123456789',
  '111111', '000000', '123123', '654321', '987654321', '123321', '11111111', '00000000',
  'qwerty', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm', 'qwertz', 'azerty', 'qwerty123',
  'password', 'password123', 'password123!', 'pass1234', 'password1!', 'admin', 'admin123',
  'admin1234', 'administrator', 'root', 'user', 'default', 'system', 'service', 'guest',
  'test', 'testing', 'master', 'access', 'secret', 'supersecret', 'secret123', 'changeme',
  'letmein', 'welcome', 'welcome1', 'welcome123', 'welcome2026', 'trustshield', 'truthshield',
  'truthshield123', 'truthshield#1', 'truthshield2026', 'football', 'baseball', 'basketball',
  'soccer', 'monkey', 'dragon', 'pokemon', 'superman', 'batman', 'spiderman', 'avengers',
  'shadow', 'sunshine', 'princess', 'angel', 'freedom', 'iloveyou', 'iloveyou123', 'godbless'
];

export const passwordSchema = z
  .string()
  .min(10, 'Password must be at least 10 characters long')
  .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
  .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
  .regex(/\d/, 'Password must contain at least one digit')
  .regex(/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/]/, 'Password must contain at least one special character')
  .refine(
    (val) => !COMMON_PASSWORDS.includes(val.toLowerCase()),
    'Password is too common and easily guessable'
  );

export const registerSchema = z.object({
  full_name: z.string().min(2, 'Full name must be at least 2 characters').max(100),
  email: z.string().email('Please enter a valid email address'),
  password: passwordSchema,
  phone: z.string().optional().refine((val) => !val || /^\+?[1-9]\d{1,14}$/.test(val), {
    message: 'Please enter a valid phone number (e.g. +919876543210)',
  }),
});

export const loginSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(1, 'Password is required'),
});

export const profileUpdateSchema = z.object({
  full_name: z.string().min(2, 'Full name must be at least 2 characters').max(100).optional(),
  phone: z.string().optional().refine((val) => !val || /^\+?[1-9]\d{1,14}$/.test(val), {
    message: 'Please enter a valid phone number (e.g. +919876543210)',
  }),
});

export const changePasswordSchema = z
  .object({
    current_password: z.string().min(1, 'Current password is required'),
    new_password: passwordSchema,
    confirm_password: z.string().min(1, 'Please confirm your new password'),
  })
  .refine((data) => data.new_password === data.confirm_password, {
    message: 'New passwords do not match',
    path: ['confirm_password'],
  });

export const forgotPasswordSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
});

export const resetPasswordSchema = z
  .object({
    token: z.string().min(1, 'Reset token is required'),
    new_password: passwordSchema,
    confirm_password: z.string().min(1, 'Please confirm your new password'),
  })
  .refine((data) => data.new_password === data.confirm_password, {
    message: 'New passwords do not match',
    path: ['confirm_password'],
  });

export type RegisterInput = z.infer<typeof registerSchema>;
export type LoginInput = z.infer<typeof loginSchema>;
export type ProfileUpdateInput = z.infer<typeof profileUpdateSchema>;
export type ChangePasswordInput = z.infer<typeof changePasswordSchema>;
export type ForgotPasswordInput = z.infer<typeof forgotPasswordSchema>;
export type ResetPasswordInput = z.infer<typeof resetPasswordSchema>;
