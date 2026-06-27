import { useCallback, useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { FiArrowLeft, FiUserPlus, FiMessageSquare, FiSave, FiCpu } from "react-icons/fi";

import axios from "../api/axios";
import PageLayout from "../components/PageLayout";

export default function MeetingDetails() {
  const { id } = useParams();
  const meetingId = Number(id);
  const user = JSON.parse(localStorage.getItem("user"));

  const [meeting, setMeeting] = useState(null);
  const [attendees, setAttendees] = useState([]);
  const [notes, setNotes] = useState([]);
  const [summary, setSummary] = useState(null);
  const [attendeeForm, setAttendeeForm] = useState({ user_id: "" });
  const [noteForm, setNoteForm] = useState("");
  const [summaryForm, setSummaryForm] = useState({
    summary: "",
    action_items: "",
    risks: "",
    decisions: "",
  });

  const load = useCallback(async () => {
    const [meetingRes, attendeesRes, notesRes, summaryRes] = await Promise.all([
      axios.get(`/meetings/${meetingId}`),
      axios.get(`/meetings/${meetingId}/attendees`),
      axios.get(`/meetings/${meetingId}/notes`),
      axios.get(`/meetings/${meetingId}/summary`).catch(() => ({ data: null })),
    ]);
    setMeeting(meetingRes.data);
    setAttendees(attendeesRes.data || []);
    setNotes(notesRes.data || []);
    setSummary(summaryRes.data);
    if (summaryRes.data) {
      setSummaryForm({
        summary: summaryRes.data.summary || "",
        action_items: summaryRes.data.action_items || "",
        risks: summaryRes.data.risks || "",
        decisions: summaryRes.data.decisions || "",
      });
    }
  }, [meetingId]);

  useEffect(() => {
    load().catch(console.error);
  }, [load]);

  const addAttendee = async (e) => {
    e.preventDefault();
    await axios.post(`/meetings/${meetingId}/attendees`, {
      meeting_id: meetingId,
      user_id: Number(attendeeForm.user_id),
    });
    setAttendeeForm({ user_id: "" });
    await load();
  };

  const addNote = async (e) => {
    e.preventDefault();
    await axios.post(`/meetings/${meetingId}/notes`, {
      meeting_id: meetingId,
      notes: noteForm,
      created_by: user?.id,
    });
    setNoteForm("");
    await load();
  };

  const generateSummary = async (e) => {
    e.preventDefault();
    await axios.post(`/meetings/${meetingId}/summary`, {
      meeting_id: meetingId,
      summary: summaryForm.summary,
      action_items: summaryForm.action_items,
      risks: summaryForm.risks,
      decisions: summaryForm.decisions,
    });
    await load();
  };

  if (!meeting) {
    return (
      <PageLayout>
        <div className="rounded-3xl border bg-white p-8">Loading meeting...</div>
      </PageLayout>
    );
  }

  return (
    <PageLayout>
      <div className="mb-6 flex items-center gap-3">
        <Link to="/meetings" className="inline-flex items-center gap-2 rounded-xl border bg-white px-4 py-2 text-sm font-medium">
          <FiArrowLeft />
          Back
        </Link>
        <span className={`rounded-full px-3 py-1 text-xs font-semibold ${meeting.status === "SCHEDULED" ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-slate-600"}`}>
          {meeting.status}
        </span>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <section className="lg:col-span-2 rounded-3xl border bg-white p-6 shadow-sm">
          <p className="text-xs uppercase tracking-[0.3em] text-violet-600">Meeting</p>
          <h1 className="text-3xl font-black mt-2">{meeting.title}</h1>
          <p className="text-slate-500 mt-3">{meeting.description || "No description provided."}</p>

          <div className="mt-6 grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="text-xs uppercase tracking-wide text-slate-500">Project</p>
              <p className="text-lg font-bold">{meeting.project_id}</p>
            </div>
            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="text-xs uppercase tracking-wide text-slate-500">Start</p>
              <p className="text-lg font-bold">{new Date(meeting.start_time).toLocaleString()}</p>
            </div>
            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="text-xs uppercase tracking-wide text-slate-500">End</p>
              <p className="text-lg font-bold">{new Date(meeting.end_time).toLocaleString()}</p>
            </div>
          </div>
        </section>

        <section className="rounded-3xl border bg-white p-6 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
          <FiCpu className="text-violet-600" />
            <h2 className="text-xl font-bold">AI Summary</h2>
          </div>
          <form className="space-y-3" onSubmit={generateSummary}>
            <textarea className="w-full rounded-xl border px-4 py-3 min-h-24" placeholder="Summary" value={summaryForm.summary} onChange={(e) => setSummaryForm({ ...summaryForm, summary: e.target.value })} />
            <textarea className="w-full rounded-xl border px-4 py-3 min-h-20" placeholder="Action items" value={summaryForm.action_items} onChange={(e) => setSummaryForm({ ...summaryForm, action_items: e.target.value })} />
            <textarea className="w-full rounded-xl border px-4 py-3 min-h-20" placeholder="Risks" value={summaryForm.risks} onChange={(e) => setSummaryForm({ ...summaryForm, risks: e.target.value })} />
            <textarea className="w-full rounded-xl border px-4 py-3 min-h-20" placeholder="Decisions" value={summaryForm.decisions} onChange={(e) => setSummaryForm({ ...summaryForm, decisions: e.target.value })} />
            <button className="inline-flex items-center gap-2 rounded-xl bg-violet-600 px-4 py-3 font-semibold text-white hover:bg-violet-700">
              <FiSave />
              Save Summary
            </button>
          </form>
          {summary && (
            <div className="mt-4 rounded-2xl bg-slate-50 p-4 text-sm text-slate-700">
              <p className="font-semibold mb-2">Current Summary</p>
              <p className="whitespace-pre-line">{summary.summary}</p>
            </div>
          )}
        </section>
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-2">
        <section className="rounded-3xl border bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold">Attendees</h2>
            <FiUserPlus className="text-violet-600" />
          </div>
          <form className="mb-4 flex gap-3" onSubmit={addAttendee}>
            <input className="flex-1 rounded-xl border px-4 py-3" placeholder="User ID" value={attendeeForm.user_id} onChange={(e) => setAttendeeForm({ user_id: e.target.value })} />
            <button className="rounded-xl bg-violet-600 px-4 py-3 font-semibold text-white">Add</button>
          </form>
          <div className="space-y-3">
            {attendees.map((attendee) => (
              <div key={attendee.id} className="rounded-2xl border px-4 py-3">
                <div className="font-semibold">User #{attendee.user_id}</div>
                <div className="text-sm text-slate-500">{attendee.attendance_status}</div>
              </div>
            ))}
            {attendees.length === 0 && <div className="text-slate-500">No attendees yet.</div>}
          </div>
        </section>

        <section className="rounded-3xl border bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold">Meeting Notes</h2>
            <FiMessageSquare className="text-violet-600" />
          </div>
          <form className="mb-4 space-y-3" onSubmit={addNote}>
            <textarea className="w-full rounded-xl border px-4 py-3 min-h-28" placeholder="Capture notes, decisions, and follow-ups" value={noteForm} onChange={(e) => setNoteForm(e.target.value)} />
            <button className="inline-flex items-center gap-2 rounded-xl bg-slate-900 px-4 py-3 font-semibold text-white">
              <FiSave />
              Save Note
            </button>
          </form>
          <div className="space-y-3">
            {notes.map((note) => (
              <div key={note.id} className="rounded-2xl border px-4 py-3">
                <div className="text-sm text-slate-500 mb-2">{new Date(note.created_at).toLocaleString()}</div>
                <div className="whitespace-pre-line">{note.notes}</div>
              </div>
            ))}
            {notes.length === 0 && <div className="text-slate-500">No notes yet.</div>}
          </div>
        </section>
      </div>
    </PageLayout>
  );
}
