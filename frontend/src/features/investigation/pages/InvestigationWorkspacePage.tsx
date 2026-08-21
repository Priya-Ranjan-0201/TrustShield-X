import React, { useState, useEffect } from 'react';
import { InvestigationRole, InvestigationCase, CaseNote, CaseTask, InvestigationGraph, TimelineEvent } from '../types';
import { investigationApi } from '../services/investigationApi';

import { InvestigationOverview } from '../components/InvestigationOverview';
import { RiskOverviewPanel } from '../components/RiskOverviewPanel';
import { FindingExplorer, FindingItem } from '../components/FindingExplorer';
import { EvidenceExplorer, EvidenceCard } from '../components/EvidenceExplorer';
import { EvidenceGraph } from '../components/EvidenceGraph';
import { InvestigationTimeline } from '../components/InvestigationTimeline';
import { BehaviorChainExplorer } from '../components/BehaviorChainExplorer';
import { DataflowExplorer } from '../components/DataflowExplorer';
import { ThreatIntelligenceExplorer } from '../components/ThreatIntelligenceExplorer';
import { ContradictionExplorer } from '../components/ContradictionExplorer';
import { ReportComparisonPage } from '../components/ReportComparisonPage';
import { CaseWorkspace } from '../components/CaseWorkspace';
import { CrossModalCorrelationPanel } from '../components/CrossModalCorrelationPanel';

export const InvestigationWorkspacePage: React.FC = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [currentRole, setCurrentRole] = useState<InvestigationRole>('ANALYST');
  const [analysisId] = useState('an_prod_sample_01');

  // Sample data states
  const [findings, setFindings] = useState<FindingItem[]>([
    {
      finding_id: 'FIND_AUTH_01',
      category: 'AUTHENTICATION',
      severity: 'HIGH',
      title: 'Hardcoded API Credentials Observed',
      description: 'Static token was discovered in client assets.',
      confidence: 'HIGH',
      risk_contribution: 40.0,
    },
    {
      finding_id: 'FIND_NET_02',
      category: 'NETWORK',
      severity: 'MEDIUM',
      title: 'Unencrypted Cleartext HTTP Traffic',
      description: 'Plaintext socket communication discovered.',
      confidence: 'HIGH',
      risk_contribution: 32.5,
    },
  ]);

  const [evidenceCards, setEvidenceCards] = useState<EvidenceCard[]>([
    {
      card_id: 'EV_01',
      category: 'STORAGE',
      title: 'Credential Asset File',
      observation: 'Secret token matching API key format found in strings.',
      evidence_strength: 'DIRECT',
      confidence: 'HIGH',
      source: 'DEX_PARSER',
      finding_reference: 'FIND_AUTH_01',
    },
    {
      card_id: 'EV_02',
      category: 'NETWORK',
      title: 'Cleartext URL Stream',
      observation: 'Found http://api.untrusted-endpoint.example.com',
      evidence_strength: 'DIRECT',
      confidence: 'HIGH',
      source: 'NETWORK_ANALYZER',
      finding_reference: 'FIND_NET_02',
    },
  ]);

  const [graphData] = useState<InvestigationGraph>({
    analysis_id: analysisId,
    nodes: [
      { id: 'analysis_01', label: 'Analysis Root', type: 'ANALYSIS', category: 'ROOT', confidence: 'HIGH', risk_contribution: 72.5, properties: {} },
      { id: 'risk_01', label: 'High Risk (72.5)', type: 'RISK_FACTOR', category: 'DECISION', confidence: 'HIGH', risk_contribution: 72.5, properties: {} },
      { id: 'f_01', label: 'Hardcoded API Key', type: 'FINDING', category: 'AUTHENTICATION', confidence: 'HIGH', risk_contribution: 40.0, properties: {} },
      { id: 'f_02', label: 'Cleartext HTTP', type: 'FINDING', category: 'NETWORK', confidence: 'HIGH', risk_contribution: 32.5, properties: {} },
      { id: 'ev_01', label: 'Token in strings', type: 'EVIDENCE', category: 'STORAGE', confidence: 'HIGH', risk_contribution: 0, properties: {} },
      { id: 'ev_02', label: 'HTTP endpoint', type: 'EVIDENCE', category: 'NETWORK', confidence: 'HIGH', risk_contribution: 0, properties: {} },
    ],
    edges: [
      { id: 'e1', source: 'analysis_01', target: 'risk_01', relationship: 'DERIVED_FROM', resolution_status: 'RESOLVED', confidence: 'HIGH', metadata: {} },
      { id: 'e2', source: 'f_01', target: 'risk_01', relationship: 'CONTRIBUTES_TO', resolution_status: 'RESOLVED', confidence: 'HIGH', metadata: {} },
      { id: 'e3', source: 'f_02', target: 'risk_01', relationship: 'CONTRIBUTES_TO', resolution_status: 'RESOLVED', confidence: 'HIGH', metadata: {} },
      { id: 'e4', source: 'ev_01', target: 'f_01', relationship: 'SUPPORTS', resolution_status: 'RESOLVED', confidence: 'HIGH', metadata: {} },
      { id: 'e5', source: 'ev_02', target: 'f_02', relationship: 'SUPPORTS', resolution_status: 'RESOLVED', confidence: 'HIGH', metadata: {} },
    ],
    total_nodes: 6,
    total_edges: 5,
    truncated: false,
  });

  const [timelineEvents] = useState<TimelineEvent[]>([
    {
      event_id: 'evt_01',
      analysis_id: analysisId,
      timestamp: '2026-08-14T06:00:00Z',
      event_type: 'ANALYSIS_STARTED',
      title: 'Security Scan Initialized',
      description: 'Multi-module automated scan initiated.',
      severity: 'INFORMATIONAL',
      source_module: 'CORE',
    },
    {
      event_id: 'evt_02',
      analysis_id: analysisId,
      timestamp: '2026-08-14T06:01:00Z',
      event_type: 'EVIDENCE_OBSERVED',
      title: 'Secret Token Extracted',
      description: 'API key discovered in DEX bytecode string pool.',
      severity: 'MEDIUM',
      source_module: 'DEX_PARSER',
    },
    {
      event_id: 'evt_03',
      analysis_id: analysisId,
      timestamp: '2026-08-14T06:02:00Z',
      event_type: 'RISK_ASSESSMENT',
      title: 'Risk Assessed: HIGH_RISK (72.5)',
      description: 'Decision Engine concluded high risk state.',
      severity: 'HIGH',
      source_module: 'RISK_ENGINE',
    },
  ]);

  const [currentCase] = useState<InvestigationCase>({
    case_id: 'CASE_2026_0814_01',
    organization_id: 'org_enterprise_sec',
    title: 'Suspicious Financial Phishing & Exfiltration Investigation',
    description: 'Investigation into APK communicating with unauthorized payment endpoints.',
    status: 'IN_PROGRESS',
    priority: 'HIGH',
    owner_id: 'usr_lead_analyst',
    created_by: 'usr_lead_analyst',
    classification: 'CONFIDENTIAL',
    retention_policy: 'DEFAULT_30D',
    created_at: '2026-08-14T06:00:00Z',
    updated_at: '2026-08-14T06:30:00Z',
    analysis_count: 1,
    note_count: 2,
    task_count: 1,
  });

  const [notes, setNotes] = useState<CaseNote[]>([
    {
      note_id: 'note_01',
      case_id: currentCase.case_id,
      author_id: 'usr_lead_analyst',
      note_type: 'OBSERVATION',
      content: 'Cleartext endpoint appears connected to external payment gateway phishing campaign.',
      visibility: 'INTERNAL',
      created_at: '2026-08-14T06:15:00Z',
    },
  ]);

  const [tasks, setTasks] = useState<CaseTask[]>([
    {
      task_id: 'task_01',
      case_id: currentCase.case_id,
      title: 'Verify endpoint domain registration date',
      description: 'Check WHOIS and DNS records for api.untrusted-endpoint.example.com',
      assigned_to: 'usr_lead_analyst',
      priority: 'HIGH',
      status: 'IN_PROGRESS',
    },
  ]);

  const handleAddNote = (content: string, type: string) => {
    const newNote: CaseNote = {
      note_id: `note_${Date.now()}`,
      case_id: currentCase.case_id,
      author_id: 'usr_lead_analyst',
      note_type: type as any,
      content,
      visibility: 'INTERNAL',
      created_at: new Date().toISOString(),
    };
    setNotes([newNote, ...notes]);
  };

  const handleAddTask = (title: string, priority: string) => {
    const newTask: CaseTask = {
      task_id: `task_${Date.now()}`,
      case_id: currentCase.case_id,
      title,
      description: '',
      assigned_to: 'usr_lead_analyst',
      priority,
      status: 'TODO',
    };
    setTasks([newTask, ...tasks]);
  };

  const navItems = [
    { id: 'overview', label: 'Overview' },
    { id: 'risk', label: 'Risk Assessment' },
    { id: 'findings', label: 'Findings' },
    { id: 'evidence', label: 'Evidence Explorer' },
    { id: 'graph', label: 'Evidence Graph' },
    { id: 'timeline', label: 'Timeline' },
    { id: 'dataflow', label: 'Dataflow' },
    { id: 'behavior', label: 'Behavior Chains' },
    { id: 'threat_intel', label: 'Threat Intel' },
    { id: 'contradictions', label: 'Contradictions' },
    { id: 'correlations', label: 'Cross-Modal' },
    { id: 'comparison', label: 'Version Diff' },
    { id: 'case', label: 'Case Hub' },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Top Workspace Header */}
      <header className="bg-slate-900 border-b border-slate-800 px-6 py-3.5 flex items-center justify-between shadow-md">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-3.5 h-3.5 rounded-sm bg-indigo-500 transform rotate-45"></div>
            <span className="font-extrabold text-base tracking-tight text-white">TruthShield X</span>
          </div>
          <span className="text-slate-600">|</span>
          <div className="flex items-center space-x-2 text-xs">
            <span className="text-slate-400">Investigation Workspace:</span>
            <code className="text-indigo-300 font-mono font-bold bg-slate-950 px-2 py-0.5 rounded border border-slate-800">
              {analysisId}
            </code>
          </div>
        </div>

        {/* Role Switcher */}
        <div className="flex items-center space-x-2">
          <span className="text-xs text-slate-400">Role View:</span>
          <select
            value={currentRole}
            onChange={(e) => setCurrentRole(e.target.value as InvestigationRole)}
            className="bg-slate-950 border border-slate-800 text-xs text-indigo-400 font-semibold rounded-lg px-2.5 py-1 focus:outline-none focus:border-indigo-500"
          >
            <option value="ANALYST">Security Analyst</option>
            <option value="EXECUTIVE">Executive Summary</option>
            <option value="TECHNICAL">Technical Deep-Dive</option>
            <option value="AUDITOR">Compliance Auditor</option>
            <option value="ADMIN">Administrator</option>
          </select>
        </div>
      </header>

      {/* Main Workspace Layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* Navigation Sidebar */}
        <nav className="w-56 bg-slate-900/60 border-r border-slate-800 p-4 space-y-1.5 overflow-y-auto">
          <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider px-3 mb-2 block">
            Navigation
          </span>
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full text-left px-3 py-2 rounded-lg text-xs font-semibold transition flex items-center justify-between ${
                activeTab === item.id
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <span>{item.label}</span>
            </button>
          ))}
        </nav>

        {/* Main Canvas Area */}
        <main className="flex-1 p-6 overflow-y-auto max-w-7xl mx-auto w-full">
          {activeTab === 'overview' && (
            <InvestigationOverview
              analysisId={analysisId}
              riskScore={72.5}
              riskBand="HIGH_RISK"
              confidence="HIGH"
              evidenceSufficiency="SUFFICIENT"
              criticalFindingsCount={1}
              highFindingsCount={1}
              evidenceCount={evidenceCards.length}
              threatMatchCount={1}
              onNavigateTab={setActiveTab}
            />
          )}

          {activeTab === 'risk' && (
            <RiskOverviewPanel
              riskScore={72.5}
              riskBand="HIGH_RISK"
              confidence="HIGH"
              evidenceSufficiency="SUFFICIENT"
              decisionState="FLAGGED"
            />
          )}

          {activeTab === 'findings' && (
            <FindingExplorer findings={findings} />
          )}

          {activeTab === 'evidence' && (
            <EvidenceExplorer evidenceCards={evidenceCards} />
          )}

          {activeTab === 'graph' && (
            <EvidenceGraph graphData={graphData} />
          )}

          {activeTab === 'timeline' && (
            <InvestigationTimeline events={timelineEvents} />
          )}

          {activeTab === 'dataflow' && (
            <DataflowExplorer />
          )}

          {activeTab === 'behavior' && (
            <BehaviorChainExplorer />
          )}

          {activeTab === 'threat_intel' && (
            <ThreatIntelligenceExplorer />
          )}

          {activeTab === 'contradictions' && (
            <ContradictionExplorer />
          )}

          {activeTab === 'correlations' && (
            <CrossModalCorrelationPanel />
          )}

          {activeTab === 'comparison' && (
            <ReportComparisonPage />
          )}

          {activeTab === 'case' && (
            <CaseWorkspace
              currentCase={currentCase}
              notes={notes}
              tasks={tasks}
              onAddNote={handleAddNote}
              onAddTask={handleAddTask}
            />
          )}
        </main>
      </div>
    </div>
  );
};
