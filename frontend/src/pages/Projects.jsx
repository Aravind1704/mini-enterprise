import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FiPlus, FiFolder, FiEye, FiRefreshCw } from "react-icons/fi";

import axios from "../api/axios";
import PageLayout from "../components/PageLayout";

const statusOptions = ["PLANNED", "ACTIVE", "ON_HOLD", "COMPLETED", "CANCELLED"];
const priorityOptions = ["LOW", "MEDIUM", "HIGH", "CRITICAL"];

export default function Projects() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user"));
  const tenantId = Number(localStorage.getItem("selectedTenantId") || user?.tenant_id || 0);
  const workspaceId = Number(localStorage.getItem("workspaceId") || 0);

  const [projects, setProjects] = useState([]);
  const [saving, setSaving] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    tenant_id: tenantId || "",
    workspace_id: workspaceId || "",
    name: "",
    description: "",
    owner_id: user?.id || "",
    status: "PLANNED",
    priority: "MEDIUM",
    start_date: "",
    end_date: "",
  });

  const loadProjects = useCallback(async () => {
    try {
      setLoading(true);
      setError("");
      const res = await axios.get("/projects/", {
        params: {
          tenant_id: tenantId || undefined,
          workspace_id: workspaceId || undefined,
        },
      });
      setProjects(res.data || []);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Failed to load projects");
      setProjects([]);
    } finally {
      setLoading(false);
    }
  }, [tenantId, workspaceId]);

  useEffect(() => {
    loadProjects();
  }, [loadProjects]);

  const createProject = async (e) => {
    e.preventDefault();
    try {
      setSaving(true);
      setError("");
      await axios.post("/projects/", {
        tenant_id: Number(form.tenant_id || tenantId),
        workspace_id: Number(form.workspace_id || workspaceId),
        owner_id: Number(form.owner_id || user?.id),
        name: form.name,
        description: form.description,
        status: form.status,
        priority: form.priority,
        start_date: form.start_date || null,
        end_date: form.end_date || null,
      });
      setForm({
        tenant_id: tenantId || "",
        workspace_id: workspaceId || "",
        name: "",
        description: "",
        owner_id: user?.id || "",
        status: "PLANNED",
        priority: "MEDIUM",
        start_date: "",
        end_date: "",
      });
      await loadProjects();
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Failed to create project");
    } finally {
      setSaving(false);
    }
  };

  const archiveProject = async (projectId) => {
    await axios.delete(`/projects/${projectId}`);
    await loadProjects();
  };

  return (
    <PageLayout>
      <div className="mb-8 rounded-3xl bg-gradient-to-r from-slate-950 via-cyan-950 to-indigo-950 p-8 text-white shadow-xl">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p className="text-cyan-300 uppercase tracking-[0.3em] text-xs mb-2">Portfolio Control</p>
            <h1 className="text-4xl font-black">Projects</h1>
            <p className="text-slate-300 mt-2 max-w-2xl">
              Manage project ownership, lifecycle, teams, documents, meetings, and execution load.
            </p>
          </div>
          <button
            onClick={loadProjects}
            className="inline-flex items-center gap-2 rounded-xl border border-white/20 bg-white/10 px-4 py-3 text-sm font-semibold hover:bg-white/15"
          >
            <FiRefreshCw />
            Refresh
          </button>
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.1fr_1.5fr]">
        <section className="rounded-3xl border bg-white p-6 shadow-sm">
          <h2 className="text-xl font-bold mb-4">Create Project</h2>
          {error && (
            <div className="mb-4 rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
              {error}
            </div>
          )}
          <form className="grid gap-4" onSubmit={createProject}>
            <div className="grid gap-4 md:grid-cols-2">
              <input
                className="rounded-xl border px-4 py-3 bg-slate-50"
                placeholder="Tenant ID"
                value={form.tenant_id}
                onChange={(e) => setForm({ ...form, tenant_id: e.target.value })}
                required
              />
              <input
                className="rounded-xl border px-4 py-3 bg-slate-50"
                placeholder="Workspace ID"
                value={form.workspace_id}
                onChange={(e) => setForm({ ...form, workspace_id: e.target.value })}
                required
              />
            </div>
            <input className="rounded-xl border px-4 py-3" placeholder="Project name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
            <textarea className="rounded-xl border px-4 py-3 min-h-28" placeholder="Description" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
            <div className="grid gap-4 md:grid-cols-2">
              <input className="rounded-xl border px-4 py-3" placeholder="Owner ID" value={form.owner_id} onChange={(e) => setForm({ ...form, owner_id: e.target.value })} />
              <select className="rounded-xl border px-4 py-3" value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                {statusOptions.map((status) => <option key={status} value={status}>{status}</option>)}
              </select>
            </div>
            <div className="grid gap-4 md:grid-cols-2">
              <select className="rounded-xl border px-4 py-3" value={form.priority} onChange={(e) => setForm({ ...form, priority: e.target.value })}>
                {priorityOptions.map((priority) => <option key={priority} value={priority}>{priority}</option>)}
              </select>
              <input className="rounded-xl border px-4 py-3" type="date" value={form.start_date} onChange={(e) => setForm({ ...form, start_date: e.target.value })} />
            </div>
            <input className="rounded-xl border px-4 py-3" type="date" value={form.end_date} onChange={(e) => setForm({ ...form, end_date: e.target.value })} />
            <button disabled={saving} className="inline-flex items-center gap-2 rounded-xl bg-cyan-600 px-5 py-3 font-semibold text-white hover:bg-cyan-700 disabled:opacity-60">
              <FiPlus />
              {saving ? "Creating..." : "Create Project"}
            </button>
          </form>
        </section>

        <section className="rounded-3xl border bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-xl font-bold">Project List</h2>
              <p className="text-sm text-slate-500">{projects.length} projects loaded</p>
            </div>
            <FiFolder className="text-2xl text-cyan-600" />
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            {loading && <div className="text-slate-500">Loading projects...</div>}
            {!loading && projects.map((project) => (
              <article key={project.id} className="rounded-2xl border p-4 hover:border-cyan-200 hover:bg-cyan-50/40">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h3 className="font-semibold text-lg">{project.name}</h3>
                    <p className="text-sm text-slate-500 mt-1 line-clamp-3">{project.description || "No description"}</p>
                  </div>
                  <span className={`rounded-full px-3 py-1 text-xs font-semibold ${project.status === "ACTIVE" ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-slate-600"}`}>
                    {project.status}
                  </span>
                </div>
                <div className="mt-4 flex items-center gap-2 flex-wrap">
                  <button
                    onClick={() => {
                      localStorage.setItem("projectId", project.id);
                      navigate(`/projects/${project.id}`);
                    }}
                    className="inline-flex items-center gap-2 rounded-xl bg-slate-900 px-4 py-2 text-sm font-medium text-white"
                  >
                    <FiEye />
                    Details
                  </button>
                  <button
                    onClick={() => archiveProject(project.id)}
                    className="rounded-xl border px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
                  >
                    Archive
                  </button>
                </div>
              </article>
            ))}
            {!loading && projects.length === 0 && <div className="text-slate-500">No projects found in this workspace.</div>}
          </div>
        </section>
      </div>
    </PageLayout>
  );
}
