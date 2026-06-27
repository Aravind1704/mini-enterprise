import { useCallback, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { FiPlus, FiCalendar, FiEye, FiRefreshCw, FiAlertCircle } from "react-icons/fi";

import axios from "../api/axios";
import PageLayout from "../components/PageLayout";

export default function Meetings() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user"));
  const tenantId = Number(localStorage.getItem("selectedTenantId") || user?.tenant_id || 0);
  const workspaceId = Number(localStorage.getItem("workspaceId") || 0);

  const [projects, setProjects] = useState([]);
  const [meetings, setMeetings] = useState([]);
  const [saving, setSaving] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    project_id: "",
    project_id_manual: "",
    title: "",
    description: "",
    start_time: "",
    end_time: "",
    status: "SCHEDULED",
  });

  const loadProjects = useCallback(async () => {
    const attempts = [
      { tenant_id: tenantId || undefined, workspace_id: workspaceId || undefined },
      { tenant_id: tenantId || undefined },
      {},
    ];

    for (const params of attempts) {
      try {
        const res = await axios.get("/projects/", { params });
        if ((res.data || []).length > 0) {
          return res.data;
        }
      } catch (err) {
        if (params === attempts[attempts.length - 1]) {
          console.error(err);
        }
      }
    }

    return [];
  }, [tenantId, workspaceId]);

  const load = useCallback(async () => {
    setError("");
    const [projectsRes, meetingsRes] = await Promise.all([
      loadProjects(),
      axios.get("/meetings/", { params: { tenant_id: tenantId || undefined } }),
    ]);
    setProjects(projectsRes || []);
    setMeetings(meetingsRes.data || []);
  }, [tenantId, loadProjects]);

  useEffect(() => {
    setLoading(true);
    load().catch(console.error).finally(() => setLoading(false));
  }, [load]);

  const createMeeting = async (e) => {
    e.preventDefault();
    try {
      setSaving(true);
      setError("");
      await axios.post("/meetings/", {
        tenant_id: tenantId,
        project_id: Number(form.project_id || form.project_id_manual),
        title: form.title,
        description: form.description,
        start_time: form.start_time,
        end_time: form.end_time,
        created_by: user?.id,
        status: form.status,
      });
      setForm({ project_id: "", project_id_manual: "", title: "", description: "", start_time: "", end_time: "", status: "SCHEDULED" });
      await load();
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Failed to schedule meeting");
    } finally {
      setSaving(false);
    }
  };

  const cancelMeeting = async (meetingId) => {
    await axios.delete(`/meetings/${meetingId}`);
    await load();
  };

  return (
    <PageLayout>
      <div className="mb-8 rounded-3xl bg-gradient-to-r from-slate-950 via-violet-950 to-cyan-950 p-8 text-white shadow-xl">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p className="text-cyan-300 uppercase tracking-[0.3em] text-xs mb-2">Collaboration Rhythm</p>
            <h1 className="text-4xl font-black">Meetings</h1>
            <p className="text-slate-300 mt-2 max-w-2xl">
              Schedule project meetings, invite attendees, and keep notes and AI summaries in one place.
            </p>
          </div>
          <button
            onClick={load}
            className="inline-flex items-center gap-2 rounded-xl border border-white/20 bg-white/10 px-4 py-3 text-sm font-semibold hover:bg-white/15"
          >
            <FiRefreshCw />
            Refresh
          </button>
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.1fr_1.5fr]">
        <section className="rounded-3xl border bg-white p-6 shadow-sm">
          <div className="mb-4 flex items-center justify-between gap-3">
            <div>
              <h2 className="text-xl font-bold">Schedule Meeting</h2>
              <p className="text-sm text-slate-500">Choose a project and add the schedule to the collaboration timeline.</p>
            </div>
            <FiCalendar className="text-violet-600" />
          </div>
          <div className="mb-4 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600">
            Context: <span className="font-semibold">Tenant {tenantId || "N/A"}</span>
            {workspaceId ? <span> · Workspace {workspaceId}</span> : null}
            <div className="mt-2">
              <Link to="/projects" className="font-semibold text-violet-700 hover:underline">
                Open Projects
              </Link>
              <span className="mx-2 text-slate-400">or add a project ID manually if the dropdown is empty.</span>
            </div>
          </div>
          {error && (
            <div className="mb-4 rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700 flex items-center gap-2">
              <FiAlertCircle />
              {error}
            </div>
          )}
          <form className="grid gap-4" onSubmit={createMeeting}>
            <select className="rounded-xl border px-4 py-3" value={form.project_id} onChange={(e) => setForm({ ...form, project_id: e.target.value, project_id_manual: "" })} required={projects.length > 0}>
              <option value="">Select project</option>
              {projects.map((project) => <option key={project.id} value={project.id}>{project.name}</option>)}
            </select>
            {projects.length === 0 && (
              <input
                className="rounded-xl border px-4 py-3"
                type="number"
                min="1"
                placeholder="Manual Project ID"
                value={form.project_id_manual}
                onChange={(e) => setForm({ ...form, project_id_manual: e.target.value })}
                required
              />
            )}
            <input className="rounded-xl border px-4 py-3" placeholder="Title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required />
            <textarea className="rounded-xl border px-4 py-3 min-h-28" placeholder="Description" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
            <select
              className="rounded-xl border px-4 py-3"
              value={form.status}
              onChange={(e) => setForm({ ...form, status: e.target.value })}
            >
              <option value="SCHEDULED">SCHEDULED</option>
              <option value="COMPLETED">COMPLETED</option>
              <option value="CANCELLED">CANCELLED</option>
            </select>
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <label className="mb-2 block text-sm font-medium">Start</label>
                <input className="w-full rounded-xl border px-4 py-3" type="datetime-local" value={form.start_time} onChange={(e) => setForm({ ...form, start_time: e.target.value })} required />
              </div>
              <div>
                <label className="mb-2 block text-sm font-medium">End</label>
                <input className="w-full rounded-xl border px-4 py-3" type="datetime-local" value={form.end_time} onChange={(e) => setForm({ ...form, end_time: e.target.value })} required />
              </div>
            </div>
            <button disabled={saving} className="inline-flex items-center gap-2 rounded-xl bg-violet-600 px-5 py-3 font-semibold text-white hover:bg-violet-700 disabled:opacity-60">
              <FiPlus />
              {saving ? "Scheduling..." : "Schedule Meeting"}
            </button>
          </form>
          {projects.length === 0 && (
            <div className="mt-4 rounded-2xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">
              No projects were loaded from the current context. Use the manual project ID field above, or create/select a project first.
            </div>
          )}
          {projects.length > 0 && (
            <div className="mt-4 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600">
              {projects.length} project{projects.length === 1 ? "" : "s"} available for scheduling.
            </div>
          )}
        </section>

        <section className="rounded-3xl border bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-xl font-bold">Meeting Schedule</h2>
              <p className="text-sm text-slate-500">{meetings.length} meetings loaded</p>
            </div>
            <FiCalendar className="text-2xl text-violet-600" />
          </div>

          <div className="space-y-4">
            {loading && <div className="text-slate-500">Loading meetings...</div>}
            {!loading && meetings.map((meeting) => (
              <article key={meeting.id} className="rounded-2xl border p-4 hover:border-violet-200 hover:bg-violet-50/40">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h3 className="font-semibold text-lg">{meeting.title}</h3>
                    <p className="text-sm text-slate-500 mt-1">{meeting.description || "No description"}</p>
                    <div className="mt-2 text-xs text-slate-500">
                      {new Date(meeting.start_time).toLocaleString()} - {new Date(meeting.end_time).toLocaleString()}
                    </div>
                  </div>
                  <span className={`rounded-full px-3 py-1 text-xs font-semibold ${meeting.status === "SCHEDULED" ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-slate-600"}`}>
                    {meeting.status}
                  </span>
                </div>
                <div className="mt-4 flex items-center gap-2 flex-wrap">
                  <button
                    onClick={() => navigate(`/meetings/${meeting.id}`)}
                    className="inline-flex items-center gap-2 rounded-xl bg-slate-900 px-4 py-2 text-sm font-medium text-white"
                  >
                    <FiEye />
                    Details
                  </button>
                  <button
                    onClick={() => cancelMeeting(meeting.id)}
                    className="rounded-xl border px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
                  >
                    Cancel
                  </button>
                </div>
              </article>
            ))}
            {!loading && meetings.length === 0 && (
              <div className="rounded-2xl border border-dashed bg-slate-50 p-6 text-slate-500">
                No meetings scheduled yet. Create a meeting above to start filling the collaboration rhythm.
              </div>
            )}
          </div>
        </section>
      </div>
    </PageLayout>
  );
}
