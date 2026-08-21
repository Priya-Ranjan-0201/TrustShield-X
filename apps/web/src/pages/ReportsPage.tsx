import React, { useEffect, useState } from 'react';
import { FileText, Download, Search } from 'lucide-react';
import { DashboardLayout } from '../layouts/DashboardLayout';
import { SectionHeader } from '../components/common/SectionHeader';
import { Card } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import { Badge } from '../components/ui/Badge';
import { reportsService } from '../services/reportsService';
import { ReportItem } from '../types';

export const ReportsPage: React.FC = () => {
  const [reports, setReports] = useState<ReportItem[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    reportsService.getReports().then((res) => {
      if (res.success && res.data) {
        setReports(res.data);
      }
      setIsLoading(false);
    }).catch(() => setIsLoading(false));
  }, []);

  const filteredReports = reports.filter((rep) =>
    rep.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <SectionHeader
          title="Security Analysis Reports"
          description="Detailed forensic reports, Explainable AI rationales, and PDF audit trails."
          icon={FileText}
        />

        <div className="w-full sm:w-72">
          <Input
            placeholder="Search reports..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            leftIcon={<Search className="w-4 h-4" />}
          />
        </div>

        <Card className="space-y-3">
          {isLoading ? (
            <p className="text-xs text-slate-400">Loading reports...</p>
          ) : (
            <div className="space-y-3">
              {filteredReports.map((rep) => (
                <div
                  key={rep.id}
                  className="flex items-center justify-between p-4 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <div className="p-2.5 rounded-xl bg-slate-950 text-cyan-400 border border-slate-800">
                      <FileText className="w-5 h-5" />
                    </div>
                    <div>
                      <h4 className="text-xs font-bold text-white">{rep.title}</h4>
                      <p className="text-[11px] text-slate-400">
                        Category: {rep.category} • Findings: {rep.findings_count}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <Badge variant={rep.status === 'DANGEROUS' ? 'danger' : 'success'}>
                      {rep.status}
                    </Badge>
                    <a
                      href={rep.download_url}
                      onClick={(e) => e.preventDefault()}
                      className="p-2 rounded-lg bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 transition-colors"
                      title="Download PDF"
                    >
                      <Download className="w-4 h-4" />
                    </a>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </DashboardLayout>
  );
};
