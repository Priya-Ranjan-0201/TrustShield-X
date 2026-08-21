import React, { useState } from 'react';
import { InvestigationCase, CaseNote, CaseTask } from '../types';

interface CaseWorkspaceProps {
  currentCase: InvestigationCase;
  notes?: CaseNote[];
  tasks?: CaseTask[];
  onAddNote?: (content: string, type: string) => void;
  onAddTask?: (title: string, priority: string) => void;
}

export const CaseWorkspace: React.FC<CaseWorkspaceProps> = ({
  currentCase,
  notes = [],
  tasks = [],
  onAddNote,
  onAddTask,
}) => {
  const [newNoteContent, setNewNoteContent] = useState('');
  const [newNoteType, setNewNoteType] = useState('OBSERVATION');
  const [newTaskTitle, setNewTaskTitle] = useState('');

  const handleCreateNote = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newNoteContent.trim()) return;
    onAddNote?.(newNoteContent, newNoteType);
    setNewNoteContent('');
  };

  const handleCreateTask = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;
    onAddTask?.(newTaskTitle, 'MEDIUM');
    setNewTaskTitle('');
  };

  return (
    <div className="space-y-6">
      {/* Case Header Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg flex items-center justify-between">
        <div>
          <div className="flex items-center space-x-3">
            <span className="font-mono text-xs text-indigo-400 bg-indigo-950 px-2 py-0.5 rounded border border-indigo-500/20">
              {currentCase.case_id}
            </span>
            <span className="px-2.5 py-0.5 text-xs font-bold bg-blue-500/20 text-blue-400 border border-blue-500/30 rounded-full">
              {currentCase.status}
            </span>
            <span className="text-xs text-slate-400 font-semibold">Priority: {currentCase.priority}</span>
          </div>
          <h2 className="text-xl font-bold text-white mt-2">{currentCase.title}</h2>
          <p className="text-xs text-slate-400 mt-1">{currentCase.description || 'No description provided.'}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Analyst Notes Section */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="text-base font-bold text-white">Analyst Notes & Hypotheses ({notes.length})</h3>
            <span className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">Analyst Generated</span>
          </div>

          <form onSubmit={handleCreateNote} className="space-y-2">
            <textarea
              placeholder="Record observation, hypothesis, or follow-up note..."
              value={newNoteContent}
              onChange={(e) => setNewNoteContent(e.target.value)}
              rows={2}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
            />
            <div className="flex items-center justify-between">
              <select
                value={newNoteType}
                onChange={(e) => setNewNoteType(e.target.value)}
                className="bg-slate-950 border border-slate-800 rounded px-2 py-1 text-xs text-slate-300"
              >
                <option value="OBSERVATION">Observation</option>
                <option value="HYPOTHESIS">Hypothesis</option>
                <option value="FOLLOW_UP">Follow-up</option>
                <option value="INVESTIGATION">Investigation</option>
              </select>
              <button
                type="submit"
                className="px-3 py-1 bg-indigo-600 hover:bg-indigo-500 text-white rounded text-xs font-semibold"
              >
                Post Note
              </button>
            </div>
          </form>

          <div className="space-y-3 max-h-64 overflow-y-auto">
            {notes.map((n) => (
              <div key={n.note_id} className="bg-slate-950/60 border border-slate-800 p-3 rounded-lg text-xs space-y-1">
                <div className="flex items-center justify-between">
                  <span className="text-indigo-400 font-bold">{n.note_type}</span>
                  <span className="text-[10px] text-slate-500 font-mono">
                    {new Date(n.created_at).toLocaleTimeString()}
                  </span>
                </div>
                <p className="text-slate-300">{n.content}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Case Workflow Tasks */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="text-base font-bold text-white">Investigation Tasks ({tasks.length})</h3>
            <span className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">Workflow Only</span>
          </div>

          <form onSubmit={handleCreateTask} className="flex space-x-2">
            <input
              type="text"
              placeholder="Add investigation task..."
              value={newTaskTitle}
              onChange={(e) => setNewTaskTitle(e.target.value)}
              className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
            />
            <button
              type="submit"
              className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded text-xs font-semibold"
            >
              Add Task
            </button>
          </form>

          <div className="space-y-2 max-h-64 overflow-y-auto">
            {tasks.map((t) => (
              <div key={t.task_id} className="flex items-center justify-between bg-slate-950/60 border border-slate-800 p-3 rounded-lg text-xs">
                <span className="text-slate-200">{t.title}</span>
                <span className="px-2 py-0.5 rounded bg-slate-800 text-[10px] font-mono text-slate-400">
                  {t.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
