import { api } from './api';
import { StandardResponse, ScanItem } from '../types';

export interface ScanEventItem {
  id: string;
  scan_id: string;
  event_type: string;
  description: string;
  event_data: Record<string, any>;
  created_at: string;
}

export const scanService = {
  async submitScan(
    scanType: string,
    targetInput?: string,
    file?: File
  ): Promise<StandardResponse<ScanItem>> {
    const formData = new FormData();
    formData.append('scan_type', scanType);
    if (targetInput) formData.append('target_input', targetInput);
    if (file) formData.append('file', file);

    const res = await api.post<StandardResponse<ScanItem>>('/scan', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return res.data;
  },

  async getHistory(scanType?: string, search?: string): Promise<StandardResponse<ScanItem[]>> {
    const params = new URLSearchParams();
    if (scanType && scanType !== 'ALL') params.append('scan_type', scanType);
    if (search) params.append('search', search);

    const res = await api.get<StandardResponse<ScanItem[]>>(`/scan/history?${params.toString()}`);
    return res.data;
  },

  async getScanDetails(scanId: string): Promise<StandardResponse<ScanItem>> {
    const res = await api.get<StandardResponse<ScanItem>>(`/scan/${scanId}`);
    return res.data;
  },

  async getScanEvents(scanId: string): Promise<StandardResponse<ScanEventItem[]>> {
    const res = await api.get<StandardResponse<ScanEventItem[]>>(`/scan/events/${scanId}`);
    return res.data;
  },

  async deleteScan(scanId: string): Promise<StandardResponse<any>> {
    const res = await api.delete<StandardResponse<any>>(`/scan/${scanId}`);
    return res.data;
  },
};
