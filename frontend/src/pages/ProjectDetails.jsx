import { useCallback, useEffect, useState } from "react";
import { useParams, Link, useNavigate, useLocation } from "react-router-dom";
import {
  FiArrowLeft,
  FiUpload,
  FiCalendar,
  FiUsers,
  FiMessageSquare,
  FiDownload,
  FiTrash2,
  FiPlus,
  FiClock,
  FiHash,
} from "react-icons/fi";

import axios from "../api/axios";
import PageLayout from "../components/PageLayout";

export default function ProjectDetails() {
  const { id } = useParams();
  const projectId = Number(id);
  const navigate = useNavigate();
  const location = useLocation();
  const user = JSON.parse(localStorage.getItem("user"));
  const workspaceId = Number(localStorage.getItem("workspaceId") || 0);

  const [project, setProject] = useState(null);
  const [projectForm, setProjectForm] = useState({
    name: "",
    description: "",
    owner_id: "",
    status: "PLANNED",
    priority: "MEDIUM",
    start_date: "",
    end_date: "",
  });
  const [teams, setTeams] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [meetings, setMeetings] = useState([]);
  const [channels, setChannels] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [calendar, setCalendar] = useState(null);
  const [workload, setWorkload] = useState(null);
  const [teamId, setTeamId] = useState("");
  const [docFile, setDocFile] = useState(null);
  const [documentType, setDocumentType] = useState("OTHER");
  const [savingProject, setSavingProject] = useState(false);

  const toDateInput = (value) => {
    if (!value) return "";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return "";
    return date.toISOString().slice(0, 10);
  };

  const load = useCallback(async () => {
    const [projectRes, teamsRes, docsRes, meetingsRes, tasksRes, calendarRes, workloadRes] = await Promise.all([
      axios.get(`/projects/${projectId}`),
      axios.get(`/projects/${projectId}/teams`),
      axios.get(`/projects/${projectId}/documents`),
      axios.get("/meetings/", { params: { project_id: projectId } }),
      axios.get("/tasks"),
      axios.get(`/projects/${projectId}/calendar`),
      axios.get(`/projects/${projectId}/workload`),
    ]);

    setProject(projectRes.data);
    setProjectForm({
      name: projectRes.data?.name || "",
      description: projectRes.data?.description || "",
      owner_id: projectRes.data?.owner_id || "",
      status: projectRes.data?.status || "PLANNED",
      priority: projectRes.data?.priority || "MEDIUM",
      start_date: toDateInput(projectRes.data?.start_date),
      end_date: toDateInput(projectRes.data?.end_date),
    });
    setTeams(teamsRes.data || []);
    setDocuments(docsRes.data || []);
    setMeetings(meetingsRes.data || []);
    setTasks((tasksRes.data || []).filter((task) => task.project_id === projectId));
    setCalendar(calendarRes.data);
    setWorkload(workloadRes.data);

    const projectWorkspaceId = projectRes.data?.workspace_id || workspaceId;
    if (projectWorkspaceId) {
      const channelsRes = await axios.get(`/workspaces/${projectWorkspaceId}/channels`, {
        params: { project_id: projectId },
      });
      setChannels(channelsRes.data || []);
    } else {
      setChannels([]);
    }
  }, [projectId, workspaceId]);

  useEffect(() => {
    localStorage.setItem("projectId", String(projectId));
    load().catch(console.error);
  }, [load, projectId]);

  useEffect(() => {
    if (!location.hash) return;
    const target = document.getElementById(location.hash.replace("#", ""));
    if (!target) return;

    const timer = window.setTimeout(() => {
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 50);

    return () => window.clearTimeout(timer);
  }, [location.hash, projectId]);

  const assignTeam = async (e) => {
    e.preventDefault();
    await axios.post(`/projects/${projectId}/teams`, {
      project_id: projectId,
      team_id: Number(teamId),
    });
    setTeamId("");
    await load();
  };

  const removeTeam = async (assignedTeamId) => {
    await axios.delete(`/projects/${projectId}/teams/${assignedTeamId}`);
    await load();
  };

  const uploadDocument = async (e) => {
    e.preventDefault();
    if (!docFile) return;

    const formData = new FormData();
    formData.append("file", docFile);
    formData.append("uploaded_by", String(user?.id || ""));
    formData.append("document_type", documentType);

    await axios.post(`/projects/${projectId}/documents`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    setDocFile(null);
    await load();
  };

  const updateProject = async (e) => {
    e.preventDefault();
    setSavingProject(true);
    try {
      await axios.put(`/projects/${projectId}`, {
        name: projectForm.name,
        description: projectForm.description,
        owner_id: Number(projectForm.owner_id || project.owner_id),
        status: projectForm.status,
        priority: projectForm.priority,
        start_date: projectForm.start_date || null,
        end_date: projectForm.end_date || null,
      });
      await load();
    } finally {
      setSavingProject(false);
    }
  };

  const archiveProject = async () => {
    await axios.delete(`/projects/${projectId}`);
    await load();
  };

  const restoreProject = async () => {
    await axios.patch(`/projects/${projectId}/restore`);
    await load();
  };

  const deleteDocument = async (documentId) => {
    await axios.delete(`/project-documents/${documentId}`);
    await load();
  };

  const downloadDocument = async (documentId, fileName) => {
    const res = await axios.get(`/project-documents/${documentId}/download`, {
      responseType: "blob",
    });

    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", fileName);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  };

  if (!project) {
    return (
      <PageLayout>
        <div className="rounded-3xl border bg-white p-8 shadow-sm">Loading project...</div>
      </PageLayout>
    );
  }

  const quickLinks = [
    ["Overview", "#project-overview", FiArrowLeft],
    ["Calendar", "#project-calendar", FiCalendar],
    ["Teams", "#project-teams", FiUsers],
    ["Channels", "#project-channels", FiMessageSquare],
    ["Tasks", "#project-tasks", FiHash],
    ["Documents", "#project-documents", FiUpload],
    ["Meetings", "#project-meetings", FiClock],
  ];

  return (
    <PageLayout>
      <div className="mb-6 flex flex-wrap items-center gap-3">
        <Link to="/projects" className="inline-flex items-center gap-2 rounded-xl border bg-white px-4 py-2 text-sm font-medium shadow-sm">
          <FiArrowLeft />
          Back
        </Link>
        <Link to={`/projects/${projectId}/calendar`} className="inline-flex items-center gap-2 rounded-xl border bg-white px-4 py-2 text-sm font-medium shadow-sm">
          <FiCalendar />
          Calendar
        </Link>
        <button
          onClick={() => teams[0] && navigate(`/teams/${teams[0].team_id}/workload`)}
          disabled={teams.length === 0}
          className="inline-flex items-center gap-2 rounded-xl border bg-white px-4 py-2 text-sm font-medium shadow-sm disabled:cursor-not-allowed disabled:opacity-50"
        >
          <FiUsers />
          Workload
        </button>
        <button type="button" onClick={archiveProject} className="inline-flex items-center gap-2 rounded-xl border border-rose-200 bg-white px-4 py-2 text-sm font-medium text-rose-700 shadow-sm">
          Archive
        </button>
        <button type="button" onClick={restoreProject} className="inline-flex items-center gap-2 rounded-xl border border-emerald-200 bg-white px-4 py-2 text-sm font-medium text-emerald-700 shadow-sm">
          Restore
        </button>
      </div>

      <div className="mb-6 rounded-3xl border bg-white/90 p-4 shadow-sm backdrop-blur">
        <div className="flex flex-wrap gap-2">
          {quickLinks.map(([label, hash, Icon]) => (
            <Link
              key={label}
              to={`/projects/${projectId}${hash}`}
              className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-cyan-300 hover:bg-cyan-50 hover:text-cyan-900"
            >
              <Icon size={14} />
              {label}
            </Link>
          ))}
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <section id="project-overview" className="scroll-mt-28 lg:col-span-2 rounded-3xl border bg-white p-6 shadow-sm">
          <p className="text-xs uppercase tracking-[0.3em] text-cyan-600">Project Overview</p>
          <h1 className="mt-2 text-3xl font-black">{project.name}</h1>
          <p className="mt-3 text-slate-500">{project.description || "No description provided."}</p>

          <form className="mt-6 grid gap-4" onSubmit={updateProject}>
            <div className="grid gap-4 md:grid-cols-2">
              <input
                className="rounded-xl border px-4 py-3"
                value={projectForm.name}
                onChange={(e) => setProjectForm({ ...projectForm, name: e.target.value })}
                placeholder="Project name"
              />
              <input
                className="rounded-xl border px-4 py-3"
                value={projectForm.owner_id}
                onChange={(e) => setProjectForm({ ...projectForm, owner_id: e.target.value })}
                placeholder="Owner ID"
              />
            </div>
            <textarea
              className="min-h-28 rounded-xl border px-4 py-3"
              value={projectForm.description}
              onChange={(e) => setProjectForm({ ...projectForm, description: e.target.value })}
              placeholder="Description"
            />
            <div className="grid gap-4 md:grid-cols-4">
              <select className="rounded-xl border px-4 py-3" value={projectForm.status} onChange={(e) => setProjectForm({ ...projectForm, status: e.target.value })}>
                {["PLANNED", "ACTIVE", "ON_HOLD", "COMPLETED", "CANCELLED"].map((status) => (
                  <option key={status} value={status}>{status}</option>
                ))}
              </select>
              <select className="rounded-xl border px-4 py-3" value={projectForm.priority} onChange={(e) => setProjectForm({ ...projectForm, priority: e.target.value })}>
                {["LOW", "MEDIUM", "HIGH", "CRITICAL"].map((priority) => (
                  <option key={priority} value={priority}>{priority}</option>
                ))}
              </select>
              <input className="rounded-xl border px-4 py-3" type="date" value={projectForm.start_date} onChange={(e) => setProjectForm({ ...projectForm, start_date: e.target.value })} />
              <input className="rounded-xl border px-4 py-3" type="date" value={projectForm.end_date} onChange={(e) => setProjectForm({ ...projectForm, end_date: e.target.value })} />
            </div>
            <div>
              <button disabled={savingProject} className="rounded-xl bg-cyan-600 px-5 py-3 font-semibold text-white hover:bg-cyan-700 disabled:opacity-60">
                {savingProject ? "Saving..." : "Update Project"}
              </button>
            </div>
          </form>

          <div className="mt-6 grid gap-4 md:grid-cols-4">
            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="text-xs uppercase tracking-wide text-slate-500">Teams</p>
              <p className="text-2xl font-bold">{teams.length}</p>
            </div>
            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="text-xs uppercase tracking-wide text-slate-500">Docs</p>
              <p className="text-2xl font-bold">{documents.length}</p>
            </div>
            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="text-xs uppercase tracking-wide text-slate-500">Meetings</p>
              <p className="text-2xl font-bold">{meetings.length}</p>
            </div>
            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="text-xs uppercase tracking-wide text-slate-500">Tasks</p>
              <p className="text-2xl font-bold">{workload?.total_tasks ?? tasks.length}</p>
            </div>
          </div>
        </section>

        <section id="project-calendar" className="scroll-mt-28 rounded-3xl border bg-white p-6 shadow-sm">
          <h2 className="text-xl font-bold">Calendar Snapshot</h2>
          <p className="mt-1 text-sm text-slate-500">Meetings, task due dates, milestones, and release dates in one place.</p>
          <div className="mt-4 space-y-4">
            <div>
              <p className="mb-2 text-xs uppercase tracking-wide text-slate-500">Meetings</p>
              {(calendar?.meetings || []).slice(0, 3).map((meeting) => (
                <div key={meeting.id} className="mb-2 rounded-2xl border bg-slate-50 px-4 py-3">
                  <div className="font-semibold">{meeting.title}</div>
                  <div className="text-xs text-slate-500">{new Date(meeting.start_time).toLocaleString()}</div>
                </div>
              ))}
              {(calendar?.meetings || []).length === 0 && <div className="rounded-2xl border border-dashed bg-slate-50 px-4 py-3 text-slate-500">No meetings scheduled.</div>}
            </div>
            <div>
              <p className="mb-2 text-xs uppercase tracking-wide text-slate-500">Task Due Dates</p>
              {(calendar?.tasks || []).slice(0, 3).map((task) => (
                <div key={task.id} className="mb-2 rounded-2xl border bg-slate-50 px-4 py-3">
                  <div className="font-semibold">{task.title}</div>
                  <div className="text-xs text-slate-500">{task.due_date ? new Date(task.due_date).toLocaleDateString() : "No due date"}</div>
                </div>
              ))}
              {(calendar?.tasks || []).length === 0 && <div className="rounded-2xl border border-dashed bg-slate-50 px-4 py-3 text-slate-500">No project tasks yet.</div>}
            </div>
            <div>
              <p className="mb-2 text-xs uppercase tracking-wide text-slate-500">Milestones</p>
              {(calendar?.milestones || []).slice(0, 3).map((item) => (
                <div key={item.id} className="mb-2 rounded-2xl border bg-slate-50 px-4 py-3">
                  <div className="font-semibold">{item.title}</div>
                  <div className="text-xs text-slate-500">{item.date ? new Date(item.date).toLocaleDateString() : "No date"}</div>
                </div>
              ))}
              {(calendar?.milestones || []).length === 0 && <div className="rounded-2xl border border-dashed bg-slate-50 px-4 py-3 text-slate-500">No milestones defined yet.</div>}
            </div>
            <div>
              <p className="mb-2 text-xs uppercase tracking-wide text-slate-500">Release Dates</p>
              {(calendar?.release_dates || []).slice(0, 3).map((item) => (
                <div key={item.id} className="mb-2 rounded-2xl border bg-slate-50 px-4 py-3">
                  <div className="font-semibold">{item.title}</div>
                  <div className="text-xs text-slate-500">{item.date ? new Date(item.date).toLocaleDateString() : "No date"}</div>
                </div>
              ))}
              {(calendar?.release_dates || []).length === 0 && <div className="rounded-2xl border border-dashed bg-slate-50 px-4 py-3 text-slate-500">No release dates defined yet.</div>}
            </div>
          </div>
        </section>
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-2">
        <section id="project-teams" className="scroll-mt-28 rounded-3xl border bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold">Project Teams</h2>
              <p className="text-sm text-slate-500">Attach one or more execution teams to this project.</p>
            </div>
            <FiUsers className="text-cyan-600" />
          </div>
          <form className="mt-4 flex gap-3" onSubmit={assignTeam}>
            <input
              className="flex-1 rounded-xl border px-4 py-3"
              placeholder="Team ID"
              value={teamId}
              onChange={(e) => setTeamId(e.target.value)}
            />
            <button className="rounded-xl bg-cyan-600 px-4 py-3 font-semibold text-white hover:bg-cyan-700">
              <FiPlus />
            </button>
          </form>
          <div className="mt-4 space-y-3">
            {teams.map((assignment) => (
              <div key={assignment.id} className="flex items-center justify-between rounded-2xl border px-4 py-3">
                <div>
                  <div className="font-semibold">Team #{assignment.team_id}</div>
                  <div className="text-sm text-slate-500">Assigned {new Date(assignment.assigned_at).toLocaleString()}</div>
                </div>
                <button onClick={() => removeTeam(assignment.team_id)} className="rounded-xl border px-3 py-2 text-sm text-rose-600 hover:bg-rose-50">
                  <FiTrash2 />
                </button>
              </div>
            ))}
            {teams.length === 0 && <div className="rounded-2xl border border-dashed bg-slate-50 px-4 py-3 text-slate-500">No teams assigned yet.</div>}
          </div>
        </section>

        <section id="project-documents" className="scroll-mt-28 rounded-3xl border bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold">Project Documents</h2>
              <p className="text-sm text-slate-500">Store requirement, testing, and release artifacts here.</p>
            </div>
            <FiUpload className="text-cyan-600" />
          </div>
          <form className="mt-4 grid gap-3" onSubmit={uploadDocument}>
            <input type="file" onChange={(e) => setDocFile(e.target.files?.[0] || null)} />
            <div className="grid gap-3 md:grid-cols-2">
              <select className="rounded-xl border px-4 py-3" value={documentType} onChange={(e) => setDocumentType(e.target.value)}>
                <option value="REQUIREMENT">Requirement</option>
                <option value="DESIGN">Design</option>
                <option value="TEST">Test</option>
                <option value="RELEASE">Release</option>
                <option value="OTHER">Other</option>
              </select>
              <button className="rounded-xl bg-cyan-600 px-4 py-3 font-semibold text-white hover:bg-cyan-700">
                Upload
              </button>
            </div>
          </form>
          <div className="mt-4 space-y-3">
            {documents.map((document) => (
              <div key={document.id} className="flex items-center justify-between rounded-2xl border px-4 py-3">
                <div>
                  <div className="font-semibold">{document.file_name}</div>
                  <div className="text-sm text-slate-500">{document.document_type} | {document.mime_type || "unknown"}</div>
                </div>
                <div className="flex items-center gap-2">
                  <button onClick={() => downloadDocument(document.id, document.file_name)} className="rounded-xl border px-3 py-2 text-sm">
                    <FiDownload />
                  </button>
                  <button onClick={() => deleteDocument(document.id)} className="rounded-xl border px-3 py-2 text-sm text-rose-600 hover:bg-rose-50">
                    <FiTrash2 />
                  </button>
                </div>
              </div>
            ))}
            {documents.length === 0 && <div className="rounded-2xl border border-dashed bg-slate-50 px-4 py-3 text-slate-500">No documents uploaded yet.</div>}
          </div>
        </section>
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-2">
        <section id="project-channels" className="scroll-mt-28 rounded-3xl border bg-white p-6 shadow-sm">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold">Project Channels</h2>
              <p className="text-sm text-slate-500">Focused communication spaces for the project.</p>
            </div>
            <FiMessageSquare className="text-cyan-600" />
          </div>
          <div className="space-y-3">
            {channels.map((channel) => (
              <div key={channel.id} className="rounded-2xl border px-4 py-3">
                <div className="font-semibold">#{channel.name}</div>
                <div className="text-sm text-slate-500">{channel.description || "No description"}</div>
              </div>
            ))}
            {channels.length === 0 && <div className="rounded-2xl border border-dashed bg-slate-50 px-4 py-3 text-slate-500">No project channels yet.</div>}
          </div>
        </section>

        <section id="project-meetings" className="scroll-mt-28 rounded-3xl border bg-white p-6 shadow-sm">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold">Project Meetings</h2>
              <p className="text-sm text-slate-500">Jump into each meeting to review notes, actions, and summaries.</p>
            </div>
            <FiCalendar className="text-cyan-600" />
          </div>
          <div className="space-y-3">
            {meetings.map((meeting) => (
              <button
                key={meeting.id}
                onClick={() => navigate(`/meetings/${meeting.id}`)}
                className="block w-full rounded-2xl border px-4 py-3 text-left hover:bg-slate-50"
              >
                <div className="font-semibold">{meeting.title}</div>
                <div className="text-sm text-slate-500">{new Date(meeting.start_time).toLocaleString()}</div>
              </button>
            ))}
            {meetings.length === 0 && <div className="rounded-2xl border border-dashed bg-slate-50 px-4 py-3 text-slate-500">No meetings scheduled yet.</div>}
          </div>
        </section>
      </div>

      <div id="project-tasks" className="scroll-mt-28 mt-6 rounded-3xl border bg-white p-6 shadow-sm">
        <div className="mb-4 flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold">Project Task View</h2>
            <p className="text-sm text-slate-500">All work items linked to this project.</p>
          </div>
          <FiHash className="text-cyan-600" />
        </div>
        <div className="grid gap-3">
          {tasks.map((task) => (
            <div key={task.id} className="rounded-2xl border px-4 py-3">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <div className="font-semibold">{task.title}</div>
                  <div className="text-sm text-slate-500">
                    {task.status} | {task.priority} | {task.team_id ? `Team #${task.team_id}` : "No team"} | {task.assigned_to_id ? `User #${task.assigned_to_id}` : "Unassigned"}
                  </div>
                </div>
                <span className="text-xs text-slate-500">{task.due_date ? new Date(task.due_date).toLocaleDateString() : "No due date"}</span>
              </div>
            </div>
          ))}
          {tasks.length === 0 && <div className="rounded-2xl border border-dashed bg-slate-50 px-4 py-3 text-slate-500">No tasks linked to this project yet.</div>}
        </div>
      </div>
    </PageLayout>
  );
}
