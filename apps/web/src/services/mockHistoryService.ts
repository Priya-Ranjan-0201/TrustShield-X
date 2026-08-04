import { StandardResponse, ScanItem } from '../types';

export const mockHistoryService = {
  async getScanHistory(): Promise<StandardResponse<ScanItem[]>> {
    await new Promise((resolve) => setTimeout(resolve, 250));

    return {
      success: true,
      message: "Scan history retrieved.",
      data: [
        {
          id: "hist-001",
          target: "https://hdfc-netbanking-verify.scam.in",
          scan_type: "URL",
          trust_score: 14,
          status: "DANGEROUS",
          scanned_at: new Date(Date.now() - 1000 * 60 * 20).toISOString(),
          summary: "Phishing site imitating HDFC NetBanking.",
        },
        {
          id: "hist-002",
          target: "Aadhaar_Card_Verified.pdf",
          scan_type: "PDF",
          trust_score: 98,
          status: "TRUSTED",
          scanned_at: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
          summary: "Authentic UIDAI e-Aadhaar document.",
        },
        {
          id: "hist-003",
          target: "Voice_Recording_CEO.mp3",
          scan_type: "AUDIO",
          trust_score: 28,
          status: "DANGEROUS",
          scanned_at: new Date(Date.now() - 1000 * 60 * 360).toISOString(),
          summary: "AI ElevenLabs voice clone detected.",
        },
        {
          id: "hist-004",
          target: "UPI_Merchant_QR.png",
          scan_type: "IMAGE",
          trust_score: 84,
          status: "LOW RISK",
          scanned_at: new Date(Date.now() - 1000 * 60 * 1440).toISOString(),
          summary: "Valid NPCI merchant VPA.",
        },
        {
          id: "hist-005",
          target: "SBI_Rewards_Mod.apk",
          scan_type: "APK",
          trust_score: 8,
          status: "DANGEROUS",
          scanned_at: new Date(Date.now() - 1000 * 60 * 2880).toISOString(),
          summary: "Banking Trojan spyware detected inside APK.",
        },
      ],
      meta: {
        traceId: "mock-trace-history-001",
        timestamp: new Date().toISOString(),
        version: "v1",
      },
    };
  },
};
