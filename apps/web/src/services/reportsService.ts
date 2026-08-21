import { api } from './api';
import { StandardResponse, ReportItem } from '../types';

export const reportsService = {
  async getReports(): Promise<StandardResponse<ReportItem[]>> {
    const res = await api.get<StandardResponse<ReportItem[]>>('/reports');
    return res.data;
  },
};
