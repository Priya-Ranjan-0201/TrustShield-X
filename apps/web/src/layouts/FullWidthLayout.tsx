import React from 'react';
import { Header } from '../components/layout/Header';
import { Footer } from '../components/layout/Footer';

interface FullWidthLayoutProps {
  children: React.ReactNode;
}

export const FullWidthLayout: React.FC<FullWidthLayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-[#020617] text-slate-100 flex flex-col justify-between">
      <Header />
      <main className="flex-1 w-full">{children}</main>
      <Footer />
    </div>
  );
};
