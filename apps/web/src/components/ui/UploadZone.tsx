import React, { useState, useRef } from 'react';
import { UploadCloud, File, CheckCircle2 } from 'lucide-react';
import { ProgressBar } from './ProgressBar';
import { Button } from './Button';

interface UploadZoneProps {
  onUploadComplete: (file: File) => void;
  acceptedTypes?: string;
  maxSizeMB?: number;
}

export const UploadZone: React.FC<UploadZoneProps> = ({
  onUploadComplete,
  acceptedTypes = '.pdf,.png,.jpg,.jpeg,.mp4,.mp3,.apk',
  maxSizeMB = 50,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const startSimulatedUpload = (selectedFile: File) => {
    setFile(selectedFile);
    setIsUploading(true);
    setProgress(0);

    // Simulated progress state (setTimeout / interval driven mock per Phase 2 spec)
    let current = 0;
    const interval = setInterval(() => {
      current += 20;
      setProgress(current);
      if (current >= 100) {
        clearInterval(interval);
        setIsUploading(false);
        onUploadComplete(selectedFile);
      }
    }, 150);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      startSimulatedUpload(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      startSimulatedUpload(e.target.files[0]);
    }
  };

  return (
    <div className="w-full space-y-4">
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`glass-card p-8 text-center cursor-pointer border-2 border-dashed transition-all duration-200 flex flex-col items-center justify-center space-y-3 ${
          isDragging
            ? 'border-cyan-500 bg-cyan-500/10'
            : 'border-slate-700 hover:border-cyan-500/50 hover:bg-slate-900/80'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept={acceptedTypes}
          onChange={handleFileSelect}
          className="hidden"
        />

        <div className="p-3 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
          <UploadCloud className="w-6 h-6" />
        </div>

        <div className="space-y-1">
          <p className="text-sm font-semibold text-white">
            Click to upload or drag & drop files here
          </p>
          <p className="text-xs text-slate-400">
            Supports QR, Image, PDF, Video, Audio, APK (Max {maxSizeMB}MB)
          </p>
        </div>
      </div>

      {/* Simulated Upload Progress State */}
      {file && (
        <div className="glass-card p-4 space-y-3 border border-slate-700">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <File className="w-5 h-5 text-cyan-400" />
              <div>
                <p className="text-xs font-semibold text-white">{file.name}</p>
                <p className="text-[11px] text-slate-400">
                  {(file.size / (1024 * 1024)).toFixed(2)} MB
                </p>
              </div>
            </div>
            {progress === 100 && (
              <span className="flex items-center gap-1 text-xs font-semibold text-emerald-400">
                <CheckCircle2 className="w-4 h-4" /> Ready for Scan
              </span>
            )}
          </div>

          <ProgressBar
            progress={progress}
            label={isUploading ? 'Simulated AI Pre-processing Upload...' : 'Upload Complete'}
          />
        </div>
      )}
    </div>
  );
};
