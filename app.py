import React, { useState } from 'react';
import {
  Calendar as CalendarIcon,
  ListTodo,
  Edit,
  Save,
  Archive,
  Trash2,
  Copy,
  Pin,
  Check,
  Search,
  ChevronLeft,
  ChevronRight,
  Flame,
  FileText,
  Eye,
  Code,
  Bold,
  Heading,
  List,
} from 'lucide-react';
import { JournalNote, NoteCategory, GeneralTask } from '../types';
import confetti from 'canvas-confetti';

interface NotesJournalViewProps {
  notes: JournalNote[];
  onUpdateNotes: (newNotes: JournalNote[]) => void;
  generalTasks: GeneralTask[];
  onUpdateGeneralTasks: (newTasks: GeneralTask[]) => void;
  isDark: boolean;
  streakDays: number;
}

const CATEGORIES: NoteCategory[] = [
  'Lectures & Classes',
  'Exam & Tests',
  'Projects & Labs',
  'Reading & Research',
  'General Review',
];

export const NotesJournalView: React.FC<NotesJournalViewProps> = ({
  notes,
  onUpdateNotes,
  generalTasks,
  onUpdateGeneralTasks,
  isDark,
  streakDays,
}) => {
  // Calendar state
  const [selectedDay, setSelectedDay] = useState<number>(17);
  const [monthName, setMonthName] = useState<'October 2026'>('October 2026');

  // Note editor state
  const [noteTitle, setNoteTitle] = useState('');
  const [noteBody, setNoteBody] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<NoteCategory>('Lectures & Classes');
  const [isPreview, setIsPreview] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  // Search & Filter
  const [searchQuery, setSearchQuery] = useState('');
  const [filterCategory, setFilterCategory] = useState<string>('All');

  // New General Task
  const [newTaskText, setNewTaskText] = useState('');

  // Check which days in October have saved entries
  const daysWithEntries = new Set(
    notes.map((n) => {
      const match = n.date.match(/Oct (\d+)/i);
      return match ? parseInt(match[1]) : null;
    }).filter(Boolean)
  );

  const handleSaveNote = (e: React.FormEvent) => {
    e.preventDefault();
    if (!noteTitle.trim() || !noteBody.trim()) return;

    const newNote: JournalNote = {
      id: `note-${Date.now()}`,
      title: noteTitle.trim(),
      body: noteBody.trim(),
      date: `Oct ${selectedDay}, 2026`,
      category: selectedCategory,
      pinned: false,
    };

    onUpdateNotes([newNote, ...notes]);
    setNoteTitle('');
    setNoteBody('');
    setIsPreview(false);

    try {
      confetti({ particleCount: 35, spread: 50 });
    } catch {
      // ignore
    }
  };

  const insertMarkdown = (prefix: string, suffix: string = '') => {
    setNoteBody((prev) => `${prev}${prefix}${suffix}`);
  };

  const handleDeleteNote = (id: string) => {
    onUpdateNotes(notes.filter((n) => n.id !== id));
  };

  const handleTogglePin = (id: string) => {
    onUpdateNotes(notes.map((n) => (n.id === id ? { ...n, pinned: !n.pinned } : n)));
  };

  const handleCopyNote = (n: JournalNote) => {
    navigator.clipboard.writeText(`${n.title}\n\n${n.body}`);
    setCopiedId(n.id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  // General tasks
  const handleAddTask = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTaskText.trim()) return;
    const newTask: GeneralTask = {
      id: `gt-${Date.now()}`,
      text: newTaskText.trim(),
      done: false,
      dueDate: `Oct ${selectedDay}`,
    };
    onUpdateGeneralTasks([newTask, ...generalTasks]);
    setNewTaskText('');
  };

  const handleToggleTask = (id: string) => {
    onUpdateGeneralTasks(generalTasks.map((t) => (t.id === id ? { ...t, done: !t.done } : t)));
  };

  const handleDeleteTask = (id: string) => {
    onUpdateGeneralTasks(generalTasks.filter((t) => t.id !== id));
  };

  const completedGeneralCount = generalTasks.filter((t) => t.done).length;

  // Filter notes
  const filteredNotes = notes
    .filter((n) => {
      const matchesSearch =
        n.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        n.body.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesCat = filterCategory === 'All' || n.category === filterCategory;
      return matchesSearch && matchesCat;
    })
    .sort((a, b) => (b.pinned ? 1 : 0) - (a.pinned ? 1 : 0));

  // Calendar days for October 2026 (Starts on Thursday)
  const prevMonthTrailing = [27, 28, 29, 30];
  const octDays = Array.from({ length: 31 }, (_, i) => i + 1);

  // Simple Markdown renderer
  const renderMarkdown = (text: string) => {
    const lines = text.split('\n');
    return (
      <div className="space-y-2 text-xs leading-relaxed font-sans">
        {lines.map((line, idx) => {
          if (line.startsWith('### ')) {
            return (
              <h4 key={idx} className="font-bold text-sm text-cyan-300 pt-1">
                {line.replace('### ', '')}
              </h4>
            );
          }
          if (line.startsWith('## ')) {
            return (
              <h3 key={idx} className="font-bold text-base text-cyan-400 pt-1">
                {line.replace('## ', '')}
              </h3>
            );
          }
          if (line.startsWith('- ')) {
            return (
              <li key={idx} className="ml-4 list-disc text-slate-200">
                {line.replace('- ', '')}
              </li>
            );
          }
          if (line.startsWith('* ')) {
            return (
              <li key={idx} className="ml-4 list-disc text-amber-300">
                {line.replace('* ', '')}
              </li>
            );
          }
          if (line.trim() === '') {
            return <div key={idx} className="h-1.5" />;
          }
          return (
            <p key={idx} className="text-slate-300">
              {line}
            </p>
          );
        })}
      </div>
    );
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* ================= LEFT COLUMN: CALENDAR & TASKS ================= */}
        <div className="space-y-6">
          {/* Interactive Calendar Matrix */}
          <div className="p-5 rounded-2xl border bg-[#0e1420] border-slate-800/90 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <CalendarIcon className="w-4 h-4 text-cyan-400" />
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-200">
                  Interactive Calendar Matrix
                </h4>
              </div>

              {/* Active Streak Counter */}
              <div className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-purple-950/80 text-purple-300 border border-purple-800 text-[10px] font-mono">
                <Flame className="w-3 h-3 text-purple-400" />
                <span>{streakDays} Days Active Streak</span>
              </div>
            </div>

            <div className="flex items-center justify-between text-xs font-mono text-slate-300 pt-1">
              <span className="font-bold text-slate-100">{monthName}</span>
              <span className="text-[10px] text-cyan-400">
                Selected: Oct {selectedDay}, 2026
              </span>
            </div>

            {/* Weekdays */}
            <div className="grid grid-cols-7 text-center text-[10px] text-slate-400 font-mono font-medium border-b border-slate-800 pb-2">
              <span>Su</span>
              <span>Mo</span>
              <span>Tu</span>
              <span>We</span>
              <span>Th</span>
              <span>Fr</span>
              <span>Sa</span>
            </div>

            {/* Matrix Days */}
            <div className="grid grid-cols-7 text-center gap-1.5 text-xs">
              {prevMonthTrailing.map((d) => (
                <span key={`prev-${d}`} className="py-1.5 text-slate-600 font-mono text-[11px]">
                  {d}
                </span>
              ))}

              {octDays.map((d) => {
                const isSelected = selectedDay === d;
                const isToday = d === 17;
                const hasEntry = daysWithEntries.has(d);

                return (
                  <button
                    key={`oct-${d}`}
                    onClick={() => setSelectedDay(d)}
                    className={`relative py-1.5 rounded-xl text-xs font-mono transition-all flex flex-col items-center justify-center cursor-pointer ${
                      isSelected
                        ? 'bg-cyan-400 text-slate-950 font-bold shadow-md shadow-cyan-400/25'
                        : isToday
                        ? 'bg-cyan-950/80 text-cyan-300 border border-cyan-800 font-semibold'
                        : 'text-slate-300 hover:bg-slate-800/70'
                    }`}
                  >
                    <span>{d}</span>
                    {/* Indicator dot for days with saved entries */}
                    {hasEntry && (
                      <span
                        className={`w-1 h-1 rounded-full mt-0.5 ${
                          isSelected ? 'bg-slate-950' : 'bg-cyan-400'
                        }`}
                      />
                    )}
                  </button>
                );
              })}
            </div>
          </div>

          {/* General Tasks Workspace */}
          <div className="p-5 rounded-2xl border bg-[#0e1420] border-slate-800/90 space-y-4">
            <div className="flex items-center justify-between">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-200 flex items-center gap-2">
                <ListTodo className="w-4 h-4 text-emerald-400" /> General Tasks & Errand Log
              </h4>
              <span className="text-[10px] font-mono bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded">
                {completedGeneralCount} / {generalTasks.length} Completed
              </span>
            </div>

            <form onSubmit={handleAddTask} className="flex gap-2">
              <input
                type="text"
                placeholder="Add personal task or clinic errand..."
                value={newTaskText}
                onChange={(e) => setNewTaskText(e.target.value)}
                className="flex-1 bg-[#080c14] border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 outline-none focus:border-emerald-400"
              />
              <button
                type="submit"
                className="px-4 py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs rounded-lg transition shrink-0 cursor-pointer"
              >
                Add
              </button>
            </form>

            <div className="space-y-2 max-h-52 overflow-y-auto pr-1">
              {generalTasks.map((t) => (
                <div
                  key={t.id}
                  className="flex items-center justify-between p-2.5 rounded-lg bg-[#080c14] border border-slate-800 text-xs hover:border-slate-700 transition"
                >
                  <div className="flex items-center gap-2.5 flex-1 min-w-0 pr-2">
                    <input
                      type="checkbox"
                      checked={t.done}
                      onChange={() => handleToggleTask(t.id)}
                      className="accent-emerald-400 w-3.5 h-3.5 rounded cursor-pointer"
                    />
                    <span
                      className={`truncate ${
                        t.done ? 'line-through text-slate-500' : 'text-slate-200 font-medium'
                      }`}
                    >
                      {t.text}
                    </span>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    {t.dueDate && (
                      <span className="text-[9px] font-mono text-slate-400">{t.dueDate}</span>
                    )}
                    <button
                      onClick={() => handleDeleteTask(t.id)}
                      className="text-slate-600 hover:text-rose-400 text-xs transition"
                      title="Delete task"
                    >
                      ✕
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* ================= RIGHT COLUMN: NOTE EDITOR & ARCHIVE ================= */}
        <div className="space-y-6">
          {/* Note Editor with Markdown Support */}
          <div className="p-5 rounded-2xl border bg-[#0e1420] border-slate-800/90 space-y-3">
            <div className="flex items-center justify-between">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-200 flex items-center gap-2">
                <Edit className="w-4 h-4 text-cyan-400" /> Clinical & Academic Note Editor
              </h4>

              <div className="flex items-center gap-2">
                {/* Preview toggle */}
                <button
                  type="button"
                  onClick={() => setIsPreview(!isPreview)}
                  className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-[10px] font-mono flex items-center gap-1 transition"
                >
                  {isPreview ? <Edit className="w-3 h-3" /> : <Eye className="w-3 h-3 text-cyan-400" />}
                  <span>{isPreview ? 'Edit' : 'Preview'}</span>
                </button>

                <button
                  onClick={handleSaveNote}
                  className="px-3 py-1 bg-cyan-400 hover:bg-cyan-300 text-slate-950 font-bold text-[11px] rounded-lg flex items-center gap-1 transition shadow-sm cursor-pointer"
                >
                  <Save className="w-3 h-3" /> Save Note
                </button>
              </div>
            </div>

            <input
              type="text"
              placeholder="Note Title (e.g., Oral Anatomy Viva Highlights, Apex Locator Pearls)"
              value={noteTitle}
              onChange={(e) => setNoteTitle(e.target.value)}
              className="w-full bg-[#080c14] border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 outline-none focus:border-cyan-500"
            />

            {/* Category Tag Selector */}
            <div className="space-y-1">
              <span className="text-[10px] font-mono uppercase text-slate-400">Category Tag:</span>
              <div className="flex items-center gap-1.5 overflow-x-auto pb-1">
                {CATEGORIES.map((cat) => (
                  <button
                    key={cat}
                    type="button"
                    onClick={() => setSelectedCategory(cat)}
                    className={`text-[10px] px-2.5 py-1 rounded-lg font-mono whitespace-nowrap transition cursor-pointer ${
                      selectedCategory === cat
                        ? 'bg-cyan-400 text-slate-950 font-bold'
                        : 'bg-[#080c14] text-slate-400 hover:text-slate-200 border border-slate-800'
                    }`}
                  >
                    {cat}
                  </button>
                ))}
              </div>
            </div>

            {/* Markdown helper toolbar */}
            {!isPreview && (
              <div className="flex items-center gap-1 pt-1 pb-1 border-t border-slate-800/80 text-slate-400">
                <span className="text-[10px] font-mono text-slate-500 mr-1">Markdown:</span>
                <button
                  type="button"
                  onClick={() => insertMarkdown('**', '**')}
                  className="px-1.5 py-0.5 rounded hover:bg-slate-800 text-[10px] font-bold"
                  title="Bold"
                >
                  B
                </button>
                <button
                  type="button"
                  onClick={() => insertMarkdown('### ')}
                  className="px-1.5 py-0.5 rounded hover:bg-slate-800 text-[10px] font-mono font-bold"
                  title="Heading 3"
                >
                  H3
                </button>
                <button
                  type="button"
                  onClick={() => insertMarkdown('- ')}
                  className="px-1.5 py-0.5 rounded hover:bg-slate-800 text-[10px] font-mono"
                  title="Bullet List"
                >
                  • List
                </button>
              </div>
            )}

            {/* Textarea or Markdown Preview */}
            {isPreview ? (
              <div className="w-full min-h-[140px] max-h-56 overflow-y-auto bg-[#080c14] border border-slate-800 rounded-lg p-3">
                {noteBody.trim() ? (
                  renderMarkdown(noteBody)
                ) : (
                  <p className="text-slate-500 text-xs italic font-mono">No text written yet to preview.</p>
                )}
              </div>
            ) : (
              <textarea
                rows={5}
                placeholder="Write clinical observations, anatomical landmarks, formulas, or markdown notes..."
                value={noteBody}
                onChange={(e) => setNoteBody(e.target.value)}
                className="w-full bg-[#080c14] border border-slate-800 rounded-lg p-3 text-xs text-slate-200 outline-none focus:border-cyan-500 font-mono leading-relaxed"
              />
            )}

            <p className="text-[9px] text-slate-500 font-mono">
              Saved notes are stored persistently in localStorage with search, pin, and copy actions.
            </p>
          </div>

          {/* Saved Notes Container */}
          <div className="p-5 rounded-2xl border bg-[#0e1420] border-slate-800/90 space-y-3">
            <div className="flex items-center justify-between">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-200 flex items-center gap-2">
                <Archive className="w-4 h-4 text-purple-400" /> Saved Notes Container
              </h4>
              <span className="text-[10px] font-mono text-slate-400">
                {filteredNotes.length} saved notes
              </span>
            </div>

            {/* Search bar & Category filter */}
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Search className="w-3.5 h-3.5 text-slate-500 absolute left-2.5 top-2.5" />
                <input
                  type="text"
                  placeholder="Search notes content..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-[#080c14] border border-slate-800 rounded-lg pl-8 pr-3 py-1.5 text-xs text-slate-200 outline-none focus:border-purple-400 font-mono"
                />
              </div>

              <select
                value={filterCategory}
                onChange={(e) => setFilterCategory(e.target.value)}
                className="bg-[#080c14] border border-slate-800 rounded-lg px-2.5 py-1.5 text-xs text-slate-300 font-mono outline-none"
              >
                <option value="All">All Categories</option>
                {CATEGORIES.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </div>

            {/* Notes List */}
            <div className="space-y-3 max-h-72 overflow-y-auto pr-1">
              {filteredNotes.length === 0 ? (
                <div className="p-6 text-center text-xs text-slate-500 font-mono">
                  No notes found matching your search.
                </div>
              ) : (
                filteredNotes.map((note) => (
                  <div
                    key={note.id}
                    className={`p-3.5 rounded-xl border transition-colors space-y-2 relative group ${
                      note.pinned
                        ? 'bg-purple-950/20 border-purple-800/70'
                        : 'bg-[#080c14] border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    <div className="flex items-center justify-between pr-14">
                      <div className="flex items-center gap-2">
                        {note.pinned && <Pin className="w-3 h-3 text-purple-400 fill-purple-400" />}
                        <h5 className="text-xs font-semibold text-slate-200">{note.title}</h5>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-[9px] font-mono px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800">
                          {note.category}
                        </span>
                        <span className="text-[9px] font-mono text-purple-400">{note.date}</span>
                      </div>
                    </div>

                    <div className="text-[11px] text-slate-300 leading-relaxed font-sans max-h-24 overflow-hidden">
                      {renderMarkdown(note.body)}
                    </div>

                    {/* Actions */}
                    <div className="absolute top-2.5 right-2.5 flex items-center gap-1.5 opacity-80 group-hover:opacity-100 transition">
                      <button
                        onClick={() => handleTogglePin(note.id)}
                        className={`p-1 rounded text-xs transition ${
                          note.pinned
                            ? 'text-purple-400 hover:text-purple-300'
                            : 'text-slate-500 hover:text-slate-300'
                        }`}
                        title={note.pinned ? 'Unpin' : 'Pin note'}
                      >
                        <Pin className="w-3 h-3" />
                      </button>

                      <button
                        onClick={() => handleCopyNote(note)}
                        className="p-1 text-slate-500 hover:text-cyan-400 transition"
                        title="Copy note text"
                      >
                        {copiedId === note.id ? (
                          <Check className="w-3 h-3 text-emerald-400" />
                        ) : (
                          <Copy className="w-3 h-3" />
                        )}
                      </button>

                      <button
                        onClick={() => handleDeleteNote(note.id)}
                        className="p-1 text-slate-500 hover:text-rose-400 transition"
                        title="Delete note"
                      >
                        <Trash2 className="w-3 h-3" />
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
