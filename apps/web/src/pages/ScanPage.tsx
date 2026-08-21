import React, { useState } from 'react';
import { ScanLine, Globe, FileText, QrCode, Video, Music, Smartphone, FileCheck } from 'lucide-react';
import { DashboardLayout } from '../layouts/DashboardLayout';
import { SectionHeader } from '../components/common/SectionHeader';
import { Card } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import { UploadZone } from '../components/ui/UploadZone';
import { Badge } from '../components/ui/Badge';
import { TrustScoreGauge } from '../components/common/TrustScoreGauge';
import { scanService } from '../services/scanService';
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
      const res = await scanService.submitScan(activeTab, urlInput);

      if (res.success && res.data) {
        setScanResult(res.data);
        toast.success('Artifact submitted to scan engine.');
      }
    } catch (err: any) {
      const msg = err.response?.data?.message || err.response?.data?.detail || err.message || 'Scan submission failed.';
      toast.error(msg);
    } finally {
      setIsScanning(false);
    }
  };

  const handleFileUpload = async (file: File) => {
    setIsScanning(true);
    setScanResult(null);

    try {
      const res = await scanService.submitScan(activeTab, undefined, file);

      if (res.success && res.data) {
        setScanResult(res.data);
        toast.success(`File ${file.name} uploaded and registered.`);
      }
    } catch (err: any) {
      const msg = err.response?.data?.message || err.response?.data?.detail || err.message || 'File scan failed.';
      toast.error(msg);
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
                  <div>
                    <h4 className="text-sm font-bold text-white truncate max-w-sm">
                      {scanResult.target}
                    </h4>
                    {scanResult.module_used && (
                      <p className="text-[11px] text-cyan-400 font-mono mt-0.5">
                        Module: {scanResult.module_used}
                      </p>
                    )}
                  </div>
                  <span className="text-[11px] font-mono text-slate-500">
                    ID: {scanResult.id.substring(0, 8)}...
                  </span>
                </div>

                <div className="space-y-2">
                  <p className="text-xs font-semibold uppercase tracking-wider text-cyan-400">
                    AI Summary & Threat Assessment
                  </p>
                  <p className="text-xs text-slate-300 leading-relaxed bg-slate-900/80 p-3.5 rounded-xl border border-slate-800">
                    {scanResult.summary}
                  </p>
                </div>

                {/* Extracted UPI Payment Details Card */}
                {scanResult.findings?.upi_details && (
                  <div className="p-3.5 rounded-xl bg-slate-900/90 border border-cyan-500/20 space-y-2">
                    <p className="text-xs font-bold text-cyan-400 uppercase tracking-wider">
                      Extracted UPI Transaction Intent
                    </p>
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div>
                        <span className="text-slate-500 block text-[10px]">VPA Handle:</span>
                        <span className="font-mono text-white">{scanResult.findings.upi_details.vpa_handle}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block text-[10px]">Payee Name:</span>
                        <span className="text-white font-semibold">{scanResult.findings.upi_details.payee_name || 'Not Provided'}</span>
                      </div>
                      {scanResult.findings.upi_details.amount && (
                        <div>
                          <span className="text-slate-500 block text-[10px]">Pre-filled Amount:</span>
                          <span className="font-bold text-rose-400">{scanResult.findings.upi_details.currency} {scanResult.findings.upi_details.amount}</span>
                        </div>
                      )}
                      {scanResult.findings.upi_details.note && (
                        <div>
                          <span className="text-slate-500 block text-[10px]">Transaction Note:</span>
                          <span className="text-slate-300 italic">{scanResult.findings.upi_details.note}</span>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Document Trust Engine Results */}
                {scanResult.findings?.document_type && (
                  <div className="space-y-3">
                    {/* Document Type Badge */}
                    <div className="p-3.5 rounded-xl bg-slate-900/90 border border-cyan-500/20 space-y-3">
                      <div className="flex items-center justify-between">
                        <p className="text-xs font-bold text-cyan-400 uppercase tracking-wider">
                          Document Classification
                        </p>
                        <span className="text-[10px] font-mono text-slate-500">
                          OCR: {scanResult.findings.ocr_engine_used || 'N/A'}
                        </span>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="px-3 py-1.5 rounded-lg bg-cyan-500/15 text-cyan-400 text-xs font-bold border border-cyan-500/30">
                          {scanResult.findings.document_type}
                        </span>
                        {scanResult.findings.classification_confidence > 0 && (
                          <span className="text-[11px] text-slate-400">
                            Confidence: {(scanResult.findings.classification_confidence * 100).toFixed(1)}%
                          </span>
                        )}
                        {scanResult.findings.ocr_confidence > 0 && (
                          <span className="text-[11px] text-slate-400">
                            OCR Confidence: {(scanResult.findings.ocr_confidence * 100).toFixed(1)}%
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Extracted Fields Card */}
                    {scanResult.findings.extracted_fields && Object.keys(scanResult.findings.extracted_fields).length > 0 && (
                      <div className="p-3.5 rounded-xl bg-slate-900/90 border border-slate-800 space-y-2">
                        <p className="text-xs font-bold text-cyan-400 uppercase tracking-wider">
                          Extracted Document Fields
                        </p>
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          {Object.entries(scanResult.findings.extracted_fields)
                            .filter(([key]) => !['document_type', 'masking_applied', 'masking_note', 'note'].includes(key))
                            .map(([key, value]) => (
                              <div key={key}>
                                <span className="text-slate-500 block text-[10px] capitalize">
                                  {key.replace(/_/g, ' ')}:
                                </span>
                                <span className="text-white font-mono text-[11px]">
                                  {String(value)}
                                </span>
                              </div>
                            ))}
                        </div>
                        {scanResult.findings.extracted_fields.masking_note && (
                          <p className="text-[10px] text-amber-400/70 italic mt-2 border-t border-slate-800 pt-2">
                            🔒 {scanResult.findings.extracted_fields.masking_note}
                          </p>
                        )}
                      </div>
                    )}

                    {/* Image Quality Metrics */}
                    {scanResult.findings.image_quality_metrics && (
                      <div className="p-3.5 rounded-xl bg-slate-900/90 border border-slate-800 space-y-2">
                        <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                          Image Quality Analysis
                        </p>
                        <div className="grid grid-cols-3 gap-2 text-xs">
                          <div>
                            <span className="text-slate-500 block text-[10px]">Quality Score:</span>
                            <span className="text-white font-bold">
                              {scanResult.findings.image_quality_metrics.quality_score ?? 'N/A'}/100
                            </span>
                          </div>
                          <div>
                            <span className="text-slate-500 block text-[10px]">Resolution:</span>
                            <span className="text-white">
                              {scanResult.findings.image_quality_metrics.resolution_quality || 'N/A'}
                            </span>
                          </div>
                          <div>
                            <span className="text-slate-500 block text-[10px]">Blur:</span>
                            <span className="text-white">
                              {scanResult.findings.image_quality_metrics.blur_assessment || 'N/A'}
                            </span>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Disclaimer Banner */}
                    {scanResult.findings.disclaimer && (
                      <div className="p-3 rounded-xl bg-amber-500/5 border border-amber-500/20 text-[11px] text-amber-400/80 leading-relaxed">
                        ⚠️ {scanResult.findings.disclaimer}
                      </div>
                    )}

                    {/* Masking Notice */}
                    {scanResult.findings.masking_note && (
                      <div className="p-2.5 rounded-lg bg-slate-900/50 border border-slate-800 text-[10px] text-slate-500 leading-relaxed">
                        🔒 {scanResult.findings.masking_note}
                      </div>
                    )}
                  </div>
                )}

                {/* Deepfake Detection Infrastructure Pipeline Results */}
                {scanResult.findings?.pipeline_status && (
                  <div className="space-y-3">
                    <div className="p-3.5 rounded-xl bg-slate-900/90 border border-cyan-500/30 space-y-3">
                      <div className="flex items-center justify-between">
                        <p className="text-xs font-bold text-cyan-400 uppercase tracking-wider">
                          Media Preprocessing & Vision Pipeline
                        </p>
                        <span className="px-2.5 py-1 rounded-md bg-emerald-500/10 text-emerald-400 text-[10px] font-mono border border-emerald-500/30 font-semibold">
                          {scanResult.findings.pipeline_status}
                        </span>
                      </div>

                      {/* Technical Media Metadata Grid */}
                      {scanResult.findings.metadata && (
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs bg-slate-950/60 p-3 rounded-lg border border-slate-800">
                          <div>
                            <span className="text-slate-500 block text-[10px]">Media Type:</span>
                            <span className="text-white font-bold">{scanResult.findings.media_type}</span>
                          </div>
                          <div>
                            <span className="text-slate-500 block text-[10px]">Resolution:</span>
                            <span className="text-white font-mono">{scanResult.findings.metadata.width}x{scanResult.findings.metadata.height}</span>
                          </div>
                          {scanResult.findings.media_type === 'VIDEO' && (
                            <>
                              <div>
                                <span className="text-slate-500 block text-[10px]">Duration / FPS:</span>
                                <span className="text-white font-mono">{scanResult.findings.metadata.duration_sec}s ({scanResult.findings.metadata.fps} FPS)</span>
                              </div>
                              <div>
                                <span className="text-slate-500 block text-[10px]">Codec / Audio:</span>
                                <span className="text-white font-mono">{scanResult.findings.metadata.codec?.toUpperCase()} ({scanResult.findings.metadata.has_audio ? 'Audio Included' : 'Muted'})</span>
                              </div>
                            </>
                          )}
                        </div>
                      )}

                      {/* Frame Sampling & Face Tracking Summary Grid */}
                      <div className="grid grid-cols-2 gap-3 text-xs">
                        <div className="p-3 rounded-lg bg-slate-950/40 border border-slate-800 space-y-1">
                          <span className="text-slate-400 block text-[10px] uppercase font-bold">Extracted Video Frames</span>
                          <p className="text-lg font-bold text-cyan-400 font-mono">
                            {scanResult.findings.total_frames_extracted || 0} Frames
                          </p>
                          <span className="text-[10px] text-slate-500 block">
                            Strategy: {scanResult.findings.frames_summary?.[0]?.sampling_strategy || 'ADAPTIVE'}
                          </span>
                        </div>
                        <div className="p-3 rounded-lg bg-slate-950/40 border border-slate-800 space-y-1">
                          <span className="text-slate-400 block text-[10px] uppercase font-bold">Tracked Face Identities</span>
                          <p className="text-lg font-bold text-emerald-400 font-mono">
                            {scanResult.findings.face_tracks?.length || 0} Face Tracks
                          </p>
                          <span className="text-[10px] text-slate-500 block">
                            Total Detections: {scanResult.findings.total_faces_detected || 0}
                          </span>
                        </div>
                      </div>

                      {/* Neural Deepfake Inference Probability Meter */}
                      {scanResult.findings.fake_probability !== undefined && (
                        <div className="p-3.5 rounded-xl bg-slate-950/80 border border-cyan-500/30 space-y-3">
                          <div className="flex items-center justify-between">
                            <span className="text-xs font-bold text-cyan-400 uppercase tracking-wider">
                              Neural Model Classification
                            </span>
                            <span className="px-2 py-0.5 rounded bg-cyan-500/15 text-cyan-300 font-mono text-[10px] border border-cyan-500/30 font-bold">
                              {scanResult.findings.model_name || 'EfficientNet-B0-Deepfake'}
                            </span>
                          </div>

                          {/* Fake vs Real Bar */}
                          <div className="space-y-1">
                            <div className="flex justify-between text-xs font-semibold">
                              <span className="text-emerald-400 font-mono">
                                Authentic Real: {((1 - scanResult.findings.fake_probability) * 100).toFixed(1)}%
                              </span>
                              <span className="text-rose-400 font-mono">
                                Deepfake Synthetic: {(scanResult.findings.fake_probability * 100).toFixed(1)}%
                              </span>
                            </div>
                            <div className="h-3 w-full bg-slate-900 rounded-full overflow-hidden flex border border-slate-800">
                              <div
                                style={{ width: `${(1 - scanResult.findings.fake_probability) * 100}%` }}
                                className="bg-emerald-500 h-full transition-all duration-500"
                              />
                              <div
                                style={{ width: `${scanResult.findings.fake_probability * 100}%` }}
                                className="bg-rose-500 h-full transition-all duration-500"
                              />
                            </div>
                          </div>

                          <div className="flex items-center justify-between text-[11px] pt-1 text-slate-400 border-t border-slate-800/80">
                            <span>Calibrated Confidence: <strong className="text-white font-mono">{((scanResult.confidence_score ?? 0.9) * 100).toFixed(0)}%</strong></span>
                            <span>Device: <strong className="text-cyan-400 font-mono">{scanResult.findings.explainability?.device_used || 'CPU'}</strong></span>
                          </div>
                        </div>
                      )}

                      {/* Explainability Insights */}
                      {scanResult.findings.explainability?.feature_importance && (
                        <div className="p-3 rounded-lg bg-slate-950/60 border border-slate-800 space-y-2 text-xs">
                          <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                            Neural Explainability & Feature Importance
                          </p>
                          <p className="text-[11px] text-slate-300 leading-relaxed italic">
                            {scanResult.findings.explainability.model_rationale}
                          </p>
                          <div className="grid grid-cols-2 gap-2 text-[10px] pt-1">
                            {Object.entries(scanResult.findings.explainability.feature_importance).map(([feature, val]) => (
                              <div key={feature} className="flex justify-between p-1.5 rounded bg-slate-900/60 border border-slate-800">
                                <span className="text-slate-400 capitalize">{feature.replace(/_/g, ' ')}:</span>
                                <span className="font-mono text-cyan-400">{String(val)}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Face Tracks Detail */}
                      {scanResult.findings.face_tracks && scanResult.findings.face_tracks.length > 0 && (
                        <div className="space-y-1.5 pt-2 border-t border-slate-800">
                          <p className="text-[11px] font-bold text-slate-300 uppercase tracking-wider">
                            Active Face Tracking & Per-Face Risk Records
                          </p>
                          <div className="space-y-1">
                            {scanResult.findings.face_tracks.map((ft: any, idx: number) => (
                              <div key={idx} className="flex items-center justify-between p-2 rounded-lg bg-slate-950/80 border border-slate-800 text-xs">
                                <span className="font-mono text-cyan-400 font-bold">{ft.track_id}</span>
                                <span className="text-slate-300 font-mono text-[11px]">
                                  Fake Prob: <strong className={ft.fake_probability > 0.5 ? 'text-rose-400' : 'text-emerald-400'}>{((ft.fake_probability ?? 0.05) * 100).toFixed(1)}%</strong> (Tracked {ft.total_frames_tracked} frames)
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Audio Preprocessing & Voice Clone Infrastructure Results */}
                {scanResult.findings?.speaker_tracks !== undefined && (
                  <div className="space-y-3">
                    <div className="p-3.5 rounded-xl bg-slate-900/90 border border-purple-500/30 space-y-3">
                      <div className="flex items-center justify-between">
                        <p className="text-xs font-bold text-purple-400 uppercase tracking-wider">
                          Audio DSP & Voice Preprocessing Pipeline
                        </p>
                        <span className="px-2.5 py-1 rounded-md bg-purple-500/10 text-purple-300 text-[10px] font-mono border border-purple-500/30 font-semibold">
                          {scanResult.findings.pipeline_status || 'PREPROCESSING_COMPLETED'}
                        </span>
                      </div>

                      {/* Voice Clone Probability Meter & Calibrated Confidence */}
                      <div className="p-3.5 rounded-lg bg-slate-950/80 border border-slate-800 space-y-2">
                        <div className="flex items-center justify-between text-xs">
                          <span className="text-slate-300 font-bold uppercase tracking-wider text-[11px]">
                            AI Voice Clone Neural Classification
                          </span>
                          <span className="text-[10px] text-purple-300 font-mono bg-purple-500/10 px-2 py-0.5 rounded border border-purple-500/20 font-semibold">
                            ECAPA-TDNN-VoiceClone (PyTorch / CPU / GPU)
                          </span>
                        </div>
                        <div className="space-y-1">
                          <div className="flex items-center justify-between text-xs font-mono">
                            <span className="text-emerald-400 font-bold">
                              Real Voice: {(100 - (scanResult.findings.risk_score ?? 0)).toFixed(1)}%
                            </span>
                            <span className="text-rose-400 font-bold">
                              Clone Prob: {(scanResult.findings.risk_score ?? 0).toFixed(1)}%
                            </span>
                          </div>
                          <div className="h-2.5 w-full bg-slate-800 rounded-full overflow-hidden flex">
                            <div
                              className="h-full bg-emerald-500 transition-all duration-500"
                              style={{ width: `${100 - (scanResult.findings.risk_score ?? 0)}%` }}
                            />
                            <div
                              className="h-full bg-rose-500 transition-all duration-500"
                              style={{ width: `${scanResult.findings.risk_score ?? 0}%` }}
                            />
                          </div>
                        </div>
                        {scanResult.confidence_score && scanResult.confidence_score < 0.60 && (
                          <div className="p-2.5 rounded-md bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs flex items-center gap-2">
                            <span>⚠️</span>
                            <span><strong>Low Confidence Notice:</strong> Audio signal quality, SNR dB, or speech duration is insufficient for high confidence neural verification.</span>
                          </div>
                        )}
                        <div className="flex items-center justify-between text-[11px] text-slate-400 pt-1">
                          <span>Calibrated Confidence: <strong className="text-cyan-400 font-mono">{((scanResult.confidence_score ?? 0.95) * 100).toFixed(1)}%</strong></span>
                          <span>Multi-Speaker Analysis: <strong className="text-purple-300 font-mono">{scanResult.findings.total_speakers_detected || 1} Speaker(s)</strong></span>
                        </div>
                      </div>

                      {/* Technical Audio Metadata Grid */}
                      {scanResult.findings.metadata && (
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs bg-slate-950/60 p-3 rounded-lg border border-slate-800">
                          <div>
                            <span className="text-slate-500 block text-[10px]">Codec / Format:</span>
                            <span className="text-white font-bold">{scanResult.findings.metadata.codec}</span>
                          </div>
                          <div>
                            <span className="text-slate-500 block text-[10px]">Sample Rate:</span>
                            <span className="text-white font-mono">{scanResult.findings.metadata.sample_rate} Hz ({scanResult.findings.metadata.channels === 1 ? 'Mono' : 'Stereo'})</span>
                          </div>
                          <div>
                            <span className="text-slate-500 block text-[10px]">Duration / LUFS:</span>
                            <span className="text-white font-mono">{scanResult.findings.metadata.duration_sec}s ({scanResult.findings.metadata.loudness_lufs} LUFS)</span>
                          </div>
                          <div>
                            <span className="text-slate-500 block text-[10px]">Bitrate / SNR:</span>
                            <span className="text-white font-mono">{scanResult.findings.metadata.bitrate} kbps ({scanResult.findings.quality_metrics?.snr_db ?? 28} dB)</span>
                          </div>
                        </div>
                      )}

                      {/* Speech VAD & Speaker Tracks Summary Grid */}
                      <div className="grid grid-cols-2 gap-3 text-xs">
                        <div className="p-3 rounded-lg bg-slate-950/40 border border-slate-800 space-y-1">
                          <span className="text-slate-400 block text-[10px] uppercase font-bold">Speech VAD Segments</span>
                          <p className="text-lg font-bold text-purple-400 font-mono">
                            {scanResult.findings.speech_segments?.length || 0} Segments
                          </p>
                          <span className="text-[10px] text-slate-500 block">
                            Speech Duration: {scanResult.findings.total_speech_duration_sec || 0}s
                          </span>
                        </div>
                        <div className="p-3 rounded-lg bg-slate-950/40 border border-slate-800 space-y-1">
                          <span className="text-slate-400 block text-[10px] uppercase font-bold">Speaker Diarization Tracks</span>
                          <p className="text-lg font-bold text-cyan-400 font-mono">
                            {scanResult.findings.total_speakers_detected || 0} Speakers
                          </p>
                          <span className="text-[10px] text-slate-500 block">
                            Embedding: ECAPA-TDNN (192-dim)
                          </span>
                        </div>
                      </div>

                      {/* Speaker Tracks Timeline Detail */}
                      {scanResult.findings.speaker_tracks && scanResult.findings.speaker_tracks.length > 0 && (
                        <div className="space-y-1.5 pt-2 border-t border-slate-800">
                          <p className="text-[11px] font-bold text-slate-300 uppercase tracking-wider">
                            Speaker Diarization & Timeline Records
                          </p>
                          <div className="space-y-1">
                            {scanResult.findings.speaker_tracks.map((st: any, idx: number) => (
                              <div key={idx} className="flex items-center justify-between p-2 rounded-lg bg-slate-950/80 border border-slate-800 text-xs">
                                <span className="font-mono text-purple-400 font-bold">{st.speaker_id}</span>
                                <span className="text-slate-300 font-mono text-[11px]">
                                  Speaking Duration: <strong>{st.total_speaking_duration}s</strong> ({st.segment_count} segments)
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Evidence Cards List */}
                {scanResult.findings?.evidence && scanResult.findings.evidence.length > 0 && (
                  <div className="space-y-2 pt-2 border-t border-slate-800">
                    <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                      Discovered Evidence ({scanResult.findings.evidence.length})
                    </p>
                    <div className="space-y-2">
                      {scanResult.findings.evidence.map((ev: any, idx: number) => {
                        const isHigh = ev.severity === 'CRITICAL' || ev.severity === 'HIGH';
                        return (
                          <div
                            key={idx}
                            className={`p-3 rounded-xl border text-xs space-y-1 ${
                              isHigh
                                ? 'bg-rose-500/10 border-rose-500/30 text-rose-300'
                                : 'bg-slate-900/60 border-slate-800 text-slate-300'
                            }`}
                          >
                            <div className="flex items-center justify-between font-semibold">
                              <span className="text-white">{ev.title}</span>
                              <Badge variant={isHigh ? 'danger' : 'neutral'} size="sm">
                                {ev.severity}
                              </Badge>
                            </div>
                            <p className="text-[11px] text-slate-400 leading-relaxed">
                              {ev.description}
                            </p>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                {/* Safety Recommendations */}
                {scanResult.findings?.recommendations && scanResult.findings.recommendations.length > 0 && (
                  <div className="space-y-2 pt-2 border-t border-slate-800">
                    <p className="text-xs font-semibold uppercase tracking-wider text-emerald-400">
                      Safety Recommendations
                    </p>
                    <ul className="space-y-1 text-xs text-slate-300 list-disc list-inside bg-slate-900/50 p-3 rounded-xl border border-slate-800">
                      {scanResult.findings.recommendations.map((rec: string, idx: number) => (
                        <li key={idx}>{rec}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </Card>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};
