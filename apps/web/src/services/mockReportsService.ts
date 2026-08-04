import { StandardResponse, ReportItem } from '../types';

export const mockReportsService = {
  async getReports(): Promise<StandardResponse<ReportItem[]>> {
    await new Promise((resolve) => setTimeout(resolve, 250));

    return {
      success: true,
      message: "Security reports list retrieved.",
      data: [
        {
          id: "rep-001",
          title: "Comprehensive Phishing Incident Report #410",
          category: "Brand Impersonation",
          trust_score: 14,
          status: "DANGEROUS",
          created_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(),
          findings_count: 5,
          download_url: "/reports/download/rep-001.pdf",
        },
        {
          id: "rep-002",
          title: "Document Verification Audit Report #209",
          category: "Identity Verification",
          trust_score: 98,
          status: "TRUSTED",
          created_at: new Date(Date.now() - 1000 * 60 * 60 * 12).toISOString(),
          findings_count: 0,
          download_url: "/reports/download/rep-002.pdf",
        },
        {
          id: "rep-003",
          title: "Deepfake Audio Analysis Rationale #104",
          category: "Voice Biometrics",
          trust_score: 28,
          status: "DANGEROUS",
          created_at: new Date(Date.now() - 1000 * 60 * 60 * 48).toISOString(),
          findings_count: 4,
          download_url: "/reports/download/rep-003.pdf",
        },
      ],
      meta: {
        traceId: "mock-trace-reports-001",
        timestamp: new Date().toISOString(),
        version: "v1",
      },
    };
  },
};
