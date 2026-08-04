import { StandardResponse, ScanItem } from '../types';

export interface ScanRequestPayload {
  scan_type: 'URL' | 'IMAGE' | 'VIDEO' | 'AUDIO' | 'PDF' | 'APK' | 'TEXT';
  target_input: string;
}

export const mockScanService = {
  async submitScan(payload: ScanRequestPayload): Promise<StandardResponse<ScanItem>> {
    // Simulated scan processing delay
    await new Promise((resolve) => setTimeout(resolve, 800));

    const isSuspicious = payload.target_input.toLowerCase().includes('phish') || payload.target_input.toLowerCase().includes('fake');
    const score = isSuspicious ? 18 : 92;
    const status = isSuspicious ? 'DANGEROUS' : 'TRUSTED';

    return {
      success: true,
      message: "Unified scan completed successfully.",
      data: {
        id: `scan-${Date.now()}`,
        target: payload.target_input,
        scan_type: payload.scan_type,
        trust_score: score,
        status: status as any,
        scanned_at: new Date().toISOString(),
        summary: isSuspicious
          ? "Deep learning model detected synthetic artifacts & malicious intent."
          : "Verified authentic artifact. Zero threats detected.",
      },
      meta: {
        traceId: `mock-trace-scan-${Date.now()}`,
        timestamp: new Date().toISOString(),
        version: "v1",
      },
    };
  },
};
