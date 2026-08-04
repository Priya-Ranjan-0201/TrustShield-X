export * from './api';

export interface User {
  id: string;
  full_name: string;
  email: string;
  phone?: string | null;
  role: string;
  status: string;
  email_verified: boolean;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export type TrustStatus = 'TRUSTED' | 'LOW RISK' | 'MEDIUM RISK' | 'HIGH RISK' | 'DANGEROUS';

export interface ScanItem {
  id: string;
  target: string;
  scan_type: 'URL' | 'IMAGE' | 'VIDEO' | 'AUDIO' | 'PDF' | 'APK' | 'TEXT';
  trust_score: number;
  status: TrustStatus;
  scanned_at: string;
  summary: string;
}

export interface NotificationItem {
  id: string;
  title: string;
  message: string;
  read: boolean;
  created_at: string;
  severity: 'info' | 'warning' | 'critical' | 'success';
}

export interface ReportItem {
  id: string;
  title: string;
  category: string;
  trust_score: number;
  status: TrustStatus;
  created_at: string;
  findings_count: number;
  download_url: string;
}
