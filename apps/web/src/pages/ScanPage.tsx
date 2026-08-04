import React, { useState } from 'react';
import { ScanLine, Globe, FileText, QrCode, Video, Music, Smartphone, FileCheck } from 'lucide-react';
import { DashboardLayout } from '../layouts/DashboardLayout';
import { SectionHeader } from '../components/common/SectionHeader';
import { Card } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import { UploadZone } from '../components/ui/UploadZone';
import { TrustScoreGauge } from '../components/common/TrustScoreGauge';
import { mockScanService } from '../services/mockScanService';
import { ScanItem } from '../types';
import { toast } from '../lib/sonner';

type ScanTab = 'URL' | 'IMAGE' | 'PDF' | 'VIDEO' | 'AUDIO' | 'APK' | 'TEXT';

export const ScanPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<ScanTab>('URL');
  const [urlInput, setUrlInput] = useState('');
  const [isScanning, setIsScanning] = useState(false);
  const [scanResult, setScanResult] = useState<ScanItem | null>(null);

  const tabs: { id: ScanTab; label: string; icon: React.ElementType }[] = [
    { id: 'URL', label: 'Website / URL', icon: Globe },
    { id: 'IMAGE', label: 'QR & Images', icon: QrCode },
    { id: 'PDF', label: 'Documents & PDFs', icon: FileText },
    { id: 'VIDEO', label: 'Video / Deepfake', icon: Video },
    { id: 'AUDIO', label: 'Audio / Voice', icon: Music },
    { id: 'APK', label: 'Mobile APK', icon: Smartphone },
    { id: 'TEXT', label: 'Text / Phishing', icon: FileCheck },
  ];

  const handleUrlScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!urlInput.trim()) return;

    setIsScanning(true);
    setScanResult(null);

    try {
      const res = await mockScanService.submitScan({
        scan_type: activeTab,
        target_input: urlInput,
      });

      if (res.success && res.data) {
        setScanResult(res.data);
        toast.success('AI verification complete.');
      }
    } catch (err: any) {
      toast.error('Scan submission failed.');
    } finally {
      setIsScanning(false);
    }
  };

  const handleFileUpload = async (file: File) => {
    setIsScanning(true);
    setScanResult(null);

    try {
      const res = await mockScanService.submitScan({
        scan_type: activeTab,
        target_input: file.name,
      });

      if (res.success && res.data) {
        setScanResult(res.data);
        toast.success(`File ${file.name} verified.`);
      }
    } catch (err: any) {
      toast.error('File scan failed.');
    } finally {
      setIsScanning(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <SectionHeader
          title="Unified AI Threat Scanner"
          description="Upload files, submit URLs, or paste suspicious text to run instant AI multi-modal verification."
          icon={ScanLine}
        />

        {/* Scan Category Selector Tabs */}
        <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => {
                  setActiveTab(tab.id);
                  setScanResult(null);
                }}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all border ${
                  isActive
                    ? 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30 shadow-md'
                    : 'bg-slate-900/60 text-slate-400 border-slate-800 hover:text-white hover:border-slate-700'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Scan Input Area */}
        <Card className="space-y-6">
          {activeTab === 'URL' || activeTab === 'TEXT' ? (
            <form onSubmit={handleUrlScan} className="space-y-4">
              <Input
                label={activeTab === 'URL' ? 'Enter Website URL or Domain' : 'Paste Suspicious Text / Email Content'}
                placeholder={
                  activeTab === 'URL'
                    ? 'https://verify-banking-security.net'
                    : 'Paste email body, SMS text, or job offer details...'
                }
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                leftIcon={activeTab === 'URL' ? <Globe className="w-4 h-4" /> : <FileText className="w-4 h-4" />}
                required
              />
              <Button type="submit" isLoading={isScanning} className="w-full sm:w-auto">
                Execute AI Threat Inspection
              </Button>
            </form>
          ) : (
            <UploadZone onUploadComplete={handleFileUpload} />
          )}
        </Card>

        {/* Scan Result Output */}
        {scanResult && (
          <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-300">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
              AI Verification Results & Rationale
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <TrustScoreGauge
                score={scanResult.trust_score}
                status={scanResult.status}
                size="md"
              />
              <Card className="md:col-span-2 space-y-4">
                <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                  <h4 className="text-sm font-bold text-white truncate max-w-sm">
                    {scanResult.target}
                  </h4>
                  <span className="text-[11px] font-mono text-slate-500">
                    ID: {scanResult.id}
                  </span>
                </div>
                <div className="space-y-2">
                  <p className="text-xs font-semibold uppercase text-cyan-400">AI Summary Rationale</p>
                  <p className="text-xs text-slate-300 leading-relaxed bg-slate-900 p-3.5 rounded-xl border border-slate-800">
                    {scanResult.summary}
                  </p>
                </div>
              </Card>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};
