import React, { useEffect, useState } from 'react';
import { History, Download, Search, Filter } from 'lucide-react';
import { DashboardLayout } from '../layouts/DashboardLayout';
import { SectionHeader } from '../components/common/SectionHeader';
import { Card } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import { Badge } from '../components/ui/Badge';
import { TooltipDisabled } from '../components/common/TooltipDisabled';
import { mockHistoryService } from '../services/mockHistoryService';
import { ScanItem } from '../types';
import { usei18n } from '../hooks/usei18n';

export const HistoryPage: React.FC = () => {
  const { t } = usei18n();
  const [history, setHistory] = useState<ScanItem[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState<string>('ALL');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    mockHistoryService.getScanHistory().then((res) => {
      if (res.success && res.data) {
        setHistory(res.data);
      }
      setIsLoading(false);
    });
  }, []);

  const filteredHistory = history.filter((item) => {
    const matchesSearch = item.target.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesFilter = filterType === 'ALL' || item.scan_type === filterType;
    return matchesSearch && matchesFilter;
  });

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <SectionHeader
          title="Scan History & Logs"
          description="View all previous threat inspections, trust score logs, and verification summaries."
          icon={History}
          action={
            /* Export History Button Placeholder (Visibly disabled with Coming Soon Tooltip) */
            <TooltipDisabled tooltipText={t('placeholders.exportTooltip')}>
              <button
                disabled
                className="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-900 border border-slate-800 text-slate-500 flex items-center gap-2 cursor-not-allowed"
              >
                <Download className="w-4 h-4" />
                <span>Export Report PDF/CSV</span>
              </button>
            </TooltipDisabled>
          }
        />

        {/* Filter Controls */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="w-full sm:w-72">
            <Input
              placeholder="Search history..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              leftIcon={<Search className="w-4 h-4" />}
            />
          </div>

          <div className="flex items-center gap-2 overflow-x-auto w-full sm:w-auto">
            {['ALL', 'URL', 'PDF', 'IMAGE', 'AUDIO', 'APK'].map((type) => (
              <button
                key={type}
                onClick={() => setFilterType(type)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
                  filterType === type
                    ? 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30'
                    : 'bg-slate-900 text-slate-400 border-slate-800 hover:text-white'
                }`}
              >
                {type}
              </button>
            ))}
          </div>
        </div>

        {/* History Table */}
        <Card className="space-y-3">
          {isLoading ? (
            <p className="text-xs text-slate-400">Loading scan history...</p>
          ) : filteredHistory.length === 0 ? (
            <p className="text-xs text-slate-400 text-center py-6">No scan records match filter criteria.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 uppercase text-[10px]">
                    <th className="py-3 px-4">Target Artifact</th>
                    <th className="py-3 px-4">Scan Type</th>
                    <th className="py-3 px-4">Trust Score</th>
                    <th className="py-3 px-4">Status</th>
                    <th className="py-3 px-4">Date & Time</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-slate-300">
                  {filteredHistory.map((item) => (
                    <tr key={item.id} className="hover:bg-slate-900/60 transition-colors">
                      <td className="py-3.5 px-4 font-semibold text-white max-w-xs truncate">
                        {item.target}
                      </td>
                      <td className="py-3.5 px-4 font-mono text-cyan-400">{item.scan_type}</td>
                      <td className="py-3.5 px-4 font-bold font-mono">{item.trust_score}/100</td>
                      <td className="py-3.5 px-4">
                        <Badge
                          variant={item.status === 'DANGEROUS' ? 'danger' : 'success'}
                          className="text-[10px]"
                        >
                          {item.status}
                        </Badge>
                      </td>
                      <td className="py-3.5 px-4 text-slate-400 font-mono">
                        {new Date(item.scanned_at).toLocaleString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card>
      </div>
    </DashboardLayout>
  );
};
