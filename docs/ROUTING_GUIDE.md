# TruthShield X — Routing & Protection Guide

## Route Structure
- `/login`: User Authentication Sign In
- `/register`: User Registration
- `/forgot-password`: Password Reset Request
- `/reset-password`: Set New Password
- `/dashboard`: Protected Dashboard Console
- `/scan`: Protected Unified AI Threat Scanner
- `/history`: Protected Scan History & Audit Logs
- `/reports`: Protected Security Analysis Reports
- `/notifications`: Protected Notifications List
- `/profile`: Protected User Profile & Session Manager (Wired to real backend)
- `/settings`: Protected System Preferences & Theme Settings
- `404`: NotFound Page

## Protected Route Guard (`ProtectedRoute.tsx`)
Unauthenticated attempts to access protected routes redirect to `/login` and save the intended target URL in `location.state.from`. Post-successful login, the user is redirected back to their intended target destination.
