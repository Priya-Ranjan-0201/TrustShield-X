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
import { DefenseControlCenterPage } from '../pages/DefenseControlCenterPage';
import { DigitalTrustCommandCenterPage } from '../pages/DigitalTrustCommandCenterPage';
import { ThreatIntelligenceCommandCenterPage } from '../pages/ThreatIntelligenceCommandCenterPage';
import { DigitalExposureCenterPage } from '../pages/DigitalExposureCenterPage';
import { SecurityCommandCenterPage } from '../pages/SecurityCommandCenterPage';
import { ThreatIntelligenceExchangePage } from '../pages/ThreatIntelligenceExchangePage';
import { ThreatHuntingCenterPage } from '../pages/ThreatHuntingCenterPage';
import { DigitalSecurityTwinCenterPage } from '../pages/DigitalSecurityTwinCenterPage';
import { SecurityAssuranceCenterPage } from '../pages/SecurityAssuranceCenterPage';
import { GovernanceFabricCenterPage } from '../pages/GovernanceFabricCenterPage';
import { MissionControlCenterPage } from '../pages/MissionControlCenterPage';
import { CollectiveDefenseCenterPage } from '../pages/CollectiveDefenseCenterPage';
import { AdaptiveDefenseCenterPage } from '../pages/AdaptiveDefenseCenterPage';
import { CyberResilienceTwinCenterPage } from '../pages/CyberResilienceTwinCenterPage';
import { CyberSecurityKnowledgeCenterPage } from '../pages/CyberSecurityKnowledgeCenterPage';
import { SecurityCopilotCenterPage } from '../pages/SecurityCopilotCenterPage';
import { AutonomousSOCCenterPage } from '../pages/AutonomousSOCCenterPage';
import { ThreatIntelligenceCenterPage } from '../pages/ThreatIntelligenceCenterPage';
import { CyberResilienceCommandCenterPage } from '../pages/CyberResilienceCommandCenterPage';
import { ContinuousSecurityAssuranceCenterPage } from '../pages/ContinuousSecurityAssuranceCenterPage';
import { AutonomousSecurityEngineeringCenterPage } from '../pages/AutonomousSecurityEngineeringCenterPage';
import { CyberDefenseDigitalTwinLabPage } from '../pages/CyberDefenseDigitalTwinLabPage';
import { GlobalThreatIntelligenceCommandCenterPage } from '../pages/GlobalThreatIntelligenceCommandCenterPage';
import { GlobalCyberDefenseCoordinationCenterPage } from '../pages/GlobalCyberDefenseCoordinationCenterPage';
import { GlobalSecurityMissionControlPage } from '../pages/GlobalSecurityMissionControlPage';
import { AutonomousDefenseCenterPage } from '../pages/AutonomousDefenseCenterPage';
import { AISecurityGovernancePage } from '../pages/AISecurityGovernancePage';
import { EnterpriseGovernancePage } from '../pages/EnterpriseGovernancePage';
import { GlobalThreatIntelligencePage } from '../pages/GlobalThreatIntelligencePage';
import { ZeroTrustExposurePage } from '../pages/ZeroTrustExposurePage';
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
          <Route
            path="/defense-control"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Defense Control Center">
                  <DefenseControlCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/trust-command-center"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Digital Trust Command Center">
                  <DigitalTrustCommandCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/threat-intelligence-command"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Threat Intelligence Command Center">
                  <ThreatIntelligenceCommandCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/exposure-center"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Digital Exposure Center">
                  <DigitalExposureCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/command-center"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Security Command Center">
                  <SecurityCommandCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/intelligence-exchange"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Threat Intelligence Exchange">
                  <ThreatIntelligenceExchangePage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/threat-hunting"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Autonomous Threat Hunting Center">
                  <ThreatHuntingCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/digital-twin"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Digital Security Twin Center">
                  <DigitalSecurityTwinCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/assurance"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Continuous Security Assurance Center">
                  <SecurityAssuranceCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/governance-fabric"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Continuous Governance & Audit Fabric">
                  <GovernanceFabricCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/mission-control"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Security Mission Control">
                  <MissionControlCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/collective-defense"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Collective Defense Center">
                  <CollectiveDefenseCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/adaptive-defense"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Adaptive Defense Center">
                  <AdaptiveDefenseCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/cyber-resilience-twin"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Cyber Resilience Digital Twin">
                  <CyberResilienceTwinCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/knowledge-fabric"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Cyber Security Knowledge Fabric">
                  <CyberSecurityKnowledgeCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/copilot"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Security Copilot & Cyber Command Center">
                  <SecurityCopilotCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/soc-orchestration"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Autonomous SOC Orchestration & Closed-Loop SOAR">
                  <AutonomousSOCCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/threat-intelligence-center"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Cyber Threat Intelligence Fabric & Collaborative Defense">
                  <ThreatIntelligenceCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/cyber-resilience-command-center"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Cyber Resilience & Autonomous Recovery Command Center">
                  <CyberResilienceCommandCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/continuous-security-assurance-center"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Continuous Security Assurance Center">
                  <ContinuousSecurityAssuranceCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/autonomous-security-engineering-center"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Autonomous Security Engineering Center">
                  <AutonomousSecurityEngineeringCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/cyber-defense-digital-twin-lab"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Cyber Defense Digital Twin Lab">
                  <CyberDefenseDigitalTwinLabPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/global-threat-intelligence-command-center"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Global Threat Intelligence Command Center">
                  <GlobalThreatIntelligenceCommandCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/global-cyber-defense-coordination-center"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Global Cyber Defense Coordination Center">
                  <GlobalCyberDefenseCoordinationCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/global-security-mission-control"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Global Security Mission Control">
                  <GlobalSecurityMissionControlPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/autonomous-defense-center"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Autonomous Defense Center">
                  <AutonomousDefenseCenterPage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/ai-security-governance"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="AI Security & Governance Control Plane">
                  <AISecurityGovernancePage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/enterprise-governance"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Enterprise Security & Compliance Operating System">
                  <EnterpriseGovernancePage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/threat-intelligence-fusion"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Global Cyber Threat Intelligence Fusion Control Plane">
                  <GlobalThreatIntelligencePage />
                </ErrorBoundary>
              </ProtectedRoute>
            }
          />
          <Route
            path="/zero-trust-exposure"
            element={
              <ProtectedRoute>
                <ErrorBoundary sectionName="Zero-Trust Architecture & Continuous Exposure Management">
                  <ZeroTrustExposurePage />
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
