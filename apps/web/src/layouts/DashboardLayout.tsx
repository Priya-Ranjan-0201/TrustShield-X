import React from 'react';
import { Sidebar } from '../components/layout/Sidebar';
import { Header } from '../components/layout/Header';
import { Footer } from '../components/layout/Footer';
import { Breadcrumbs } from '../components/layout/Breadcrumbs';
import { NotificationsDrawer } from '../components/layout/NotificationsDrawer';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-[#020617] text-slate-100 flex relative">
      {/* Sidebar Navigation */}
      <Sidebar />

      {/* Main App Canvas */}
      <div className="flex-1 flex flex-col min-w-0 min-h-screen">
        <Header />

        <main className="flex-1 p-4 lg:p-6 space-y-4 max-w-7xl w-full mx-auto">
          <Breadcrumbs />
          {children}
        </main>

        <Footer />
      </div>

      {/* Slide-over Drawer */}
      <NotificationsDrawer />
    </div>
  );
};
