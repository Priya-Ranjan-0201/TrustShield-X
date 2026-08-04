import { StandardResponse, NotificationItem } from '../types';

export const mockNotificationsService = {
  async getNotifications(): Promise<StandardResponse<NotificationItem[]>> {
    await new Promise((resolve) => setTimeout(resolve, 200));

    return {
      success: true,
      message: "Notifications list retrieved.",
      data: [
        {
          id: "notif-101",
          title: "Phishing Target Intercepted",
          message: "Block rule applied to fake banking domain in Chrome Extension.",
          read: false,
          created_at: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
          severity: "critical",
        },
        {
          id: "notif-102",
          title: "Malicious APK Blocked",
          message: "Trojan embedded inside fake SBI Rewards APK neutralized.",
          read: false,
          created_at: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
          severity: "critical",
        },
        {
          id: "notif-103",
          title: "Security Verification Complete",
          message: "Uploaded invoice PDF signature verified successfully.",
          read: true,
          created_at: new Date(Date.now() - 1000 * 60 * 360).toISOString(),
          severity: "success",
        },
        {
          id: "notif-104",
          title: "System Update Complete",
          message: "TruthShield X AI model weights updated to v2.4.",
          read: true,
          created_at: new Date(Date.now() - 1000 * 60 * 1440).toISOString(),
          severity: "info",
        },
      ],
      meta: {
        traceId: "mock-trace-notif-001",
        timestamp: new Date().toISOString(),
        version: "v1",
      },
    };
  },
};
