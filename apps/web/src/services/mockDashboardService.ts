import { StandardResponse, ScanItem, NotificationItem } from '../types';

export interface DashboardData {
  trustScore: number;
  trustStatus: 'TRUSTED';
  totalScans: number;
  threatsBlocked: number;
  activeAlerts: number;
  recentActivity: ScanItem[];
  recentNotifications: NotificationItem[];
}

export const mockDashboardService = {
  async getDashboardData(): Promise<StandardResponse<DashboardData>> {
    // Simulated network delay
    await new Promise((resolve) => setTimeout(resolve, 300));

    return {
      success: true,
      message: "Dashboard metrics fetched successfully.",
      data: {
        trustScore: 94,
        trustStatus: "TRUSTED",
        totalScans: 1248,
        threatsBlocked: 312,
        activeAlerts: 2,
        recentActivity: [
          {
            id: "scan-001",
            target: "https://secure-bank-login.phish-verify.net",
            scan_type: "URL",
            trust_score: 12,
            status: "DANGEROUS",
            scanned_at: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
            summary: "Brand impersonation & credential harvester detected.",
          },
          {
            id: "scan-002",
            target: "Payment_Receipt_UPI.pdf",
            scan_type: "PDF",
            trust_score: 96,
            status: "TRUSTED",
            scanned_at: new Date(Date.now() - 1000 * 60 * 45).toISOString(),
            summary: "Document verified. Authentic digital signature.",
          },
          {
            id: "scan-003",
            target: "Job_Offer_Letter_AI.docx",
            scan_type: "TEXT",
            trust_score: 42,
            status: "HIGH RISK",
            scanned_at: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
            summary: "Fake recruiter template & non-existent company domain.",
          },
          {
            id: "scan-004",
            target: "UPI_Payment_QR.png",
            scan_type: "IMAGE",
            trust_score: 88,
            status: "LOW RISK",
            scanned_at: new Date(Date.now() - 1000 * 60 * 300).toISOString(),
            summary: "Verified merchant VPA address.",
          },
        ],
        recentNotifications: [
          {
            id: "notif-001",
            title: "Phishing Target Intercepted",
            message: "Block rule applied to fake banking domain in Chrome Extension.",
            read: false,
            created_at: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
            severity: "critical",
          },
          {
            id: "notif-002",
            title: "Security Verification Complete",
            message: "Uploaded invoice PDF signature verified successfully.",
            read: true,
            created_at: new Date(Date.now() - 1000 * 60 * 180).toISOString(),
            severity: "success",
          },
        ],
      },
      meta: {
        traceId: "mock-trace-dashboard-001",
        timestamp: new Date().toISOString(),
        version: "v1",
      },
    };
  },
};
