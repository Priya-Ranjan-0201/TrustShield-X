import React, { Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ProtectedRoute } from './ProtectedRoute';
import { ErrorBoundary } from './ErrorBoundary';
import { Skeleton } from '../components/ui/Skeleton';

// Page Components
import { LoginPage } from '../pages/LoginPage';
import { RegisterPage } from '../pages/RegisterPage';
import { ForgotPasswordPage } from '../pages/ForgotPasswordPage';
import { ResetPasswordPage } from '../pages/ResetPasswordPage';
import { DashboardPage } from '../pages/DashboardPage';
import { ScanPage } from '../pages/ScanPage';
import { HistoryPage } from '../pages/HistoryPage';
import { ReportsPage } from '../pages/ReportsPage';
import { NotificationsPage } from '../pages/NotificationsPage';
import { ProfilePage } from '../pages/ProfilePage';
import { SettingsPage } from '../pages/SettingsPage';
import { NotFoundPage } from '../pages/NotFoundPage';

const PageLoadingFallback = () => (
  <div className="min-h-screen bg-[#020617] p-8 flex items-center justify-center">
    <div className="w-full max-w-xl space-y-4">
      <Skeleton className="h-12 w-3/4" />
      <Skeleton className="h-64 w-full" />
    </div>
  </div>
);

export const AppRouter: React.FC = () => {
  return (
    <ErrorBoundary sectionName="Global Application Router">
      <Suspense fallback={<PageLoadingFallback />}>
        <Routes>
          {/* Public Auth Routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />
          <Route path="/reset-password" element={<ResetPasswordPage />} />

          {/* Protected Main App Routes */}
          <Route
            path="/"
            element={<Navigate to="/dashboard" replace />}
          />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Dashboard Module">
                  <DashboardPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/scan"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Scan Module">
                  <ScanPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/history"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="History Module">
                  <HistoryPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/reports"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Reports Module">
                  <ReportsPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/notifications"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Notifications Module">
                  <NotificationsPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Profile Module">
                  <ProfilePage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/settings"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Settings Module">
                  <SettingsPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />

          {/* 404 Fallback */}
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Suspense>
    </ErrorBoundary>
  );
};
