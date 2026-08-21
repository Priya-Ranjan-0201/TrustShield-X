/**
 * Investigation Workspace API Service.
 * Communicates with backend endpoints under /api/v1/*.
 */

import {
  InvestigationCase,
  CaseAnalysis,
  CaseNote,
  CaseBookmark,
  CaseTask,
  InvestigationGraph,
  TimelineEvent,
  SearchResultItem,
  InvestigationRole,
} from '../types';

const API_BASE = '/api/v1';

export const investigationApi = {
  // Cases
  async listCases(limit = 50, offset = 0): Promise<InvestigationCase[]> {
    const res = await fetch(`${API_BASE}/cases?limit=${limit}&offset=${offset}`);
    const json = await res.json();
    return json.data || [];
  },

  async getCase(caseId: string): Promise<InvestigationCase> {
    const res = await fetch(`${API_BASE}/cases/${caseId}`);
    const json = await res.json();
    return json.data;
  },

  async createCase(payload: { title: string; description?: string; priority?: string; analysis_ids?: string[] }): Promise<InvestigationCase> {
    const res = await fetch(`${API_BASE}/cases`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const json = await res.json();
    return json.data;
  },

  async getCaseAnalyses(caseId: string): Promise<CaseAnalysis[]> {
    const res = await fetch(`${API_BASE}/cases/${caseId}/analyses`);
    const json = await res.json();
    return json.data || [];
  },

  async getCaseNotes(caseId: string): Promise<CaseNote[]> {
    const res = await fetch(`${API_BASE}/cases/${caseId}/notes`);
    const json = await res.json();
    return json.data || [];
  },

  async createCaseNote(caseId: string, content: string, noteType = 'OBSERVATION'): Promise<CaseNote> {
    const res = await fetch(`${API_BASE}/cases/${caseId}/notes?content=${encodeURIComponent(content)}&note_type=${encodeURIComponent(noteType)}`, {
      method: 'POST',
    });
    const json = await res.json();
    return json.data;
  },

  // Explorers
  async getInvestigationFindings(analysisId: string): Promise<any[]> {
    const res = await fetch(`${API_BASE}/investigations/${analysisId}/findings`);
    const json = await res.json();
    return json.data || [];
  },

  async getInvestigationEvidence(analysisId: string): Promise<any[]> {
    const res = await fetch(`${API_BASE}/investigations/${analysisId}/evidence`);
    const json = await res.json();
    return json.data || [];
  },

  async getInvestigationGraph(analysisId: string, depth = 2): Promise<InvestigationGraph> {
    const res = await fetch(`${API_BASE}/investigations/${analysisId}/graph?depth=${depth}`);
    const json = await res.json();
    return json.data;
  },

  async getInvestigationTimeline(analysisId: string): Promise<TimelineEvent[]> {
    const res = await fetch(`${API_BASE}/investigations/${analysisId}/timeline`);
    const json = await res.json();
    return json.data?.events || [];
  },

  async getInvestigationDataflow(analysisId: string): Promise<any[]> {
    const res = await fetch(`${API_BASE}/investigations/${analysisId}/dataflow`);
    const json = await res.json();
    return json.data || [];
  },

  async getInvestigationBehavior(analysisId: string): Promise<any[]> {
    const res = await fetch(`${API_BASE}/investigations/${analysisId}/behavior`);
    const json = await res.json();
    return json.data || [];
  },

  async getInvestigationThreatIntel(analysisId: string): Promise<any[]> {
    const res = await fetch(`${API_BASE}/investigations/${analysisId}/threat-intelligence`);
    const json = await res.json();
    return json.data || [];
  },

  async searchInvestigation(query: string, analysisId?: string): Promise<SearchResultItem[]> {
    const res = await fetch(`${API_BASE}/investigations/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, analysis_id: analysisId }),
    });
    const json = await res.json();
    return json.data?.results || [];
  },

  async getRoleViewConfig(role: InvestigationRole): Promise<any> {
    const res = await fetch(`${API_BASE}/investigations/views/role/${role}`);
    const json = await res.json();
    return json.data;
  },
};
