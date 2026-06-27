import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FiPlus, FiUsers, FiEye, FiRefreshCw } from "react-icons/fi";

import axios from "../api/axios";
import PageLayout from "../components/PageLayout";

export default function Teams() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user"));
  const tenantId = Number(localStorage.getItem("selectedTenantId") || user?.tenant_id || 0);
  const workspaceId = Number(localStorage.getItem("workspaceId") || 0);

  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    tenant_id: tenantId || "",
    workspace_id: workspaceId || "",
    name: "",
    description: "",
    is_active: true,
    created_by: user?.id || "",
  });

  const loadTeams = useCallback(async () => {
    try {
      setLoading(true);
      setError("");
      const res = await axios.get("/teams/", {
        params: {
          tenant_id: tenantId || undefined,
          workspace_id: workspaceId || undefined,
        },
      });
      setTeams(res.data || []);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Failed to load teams");
      setTeams([]);
    } finally {
      setLoading(false);
    }
  }, [tenantId, workspaceId]);

  useEffect(() => {
    loadTeams();
  }, [loadTeams]);

  const createTeam = async (e) => {
    e.preventDefault();
    try {
      setSaving(true);
      setError("");
      await axios.post("/teams/", {
        tenant_id: Number(form.tenant_id || tenantId),
        workspace_id: Number(form.workspace_id || workspaceId),
        name: form.name,
        description: form.description,
        is_active: form.is_active,
        created_by: Number(form.created_by || user?.id),
      });
      setForm({
        tenant_id: tenantId || "",
        workspace_id: workspaceId || "",
        name: "",
        description: "",
        is_active: true,
        created_by: user?.id || "",
      });
      await loadTeams();
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Failed to create team");
    } finally {
      setSaving(false);
    }
  };

  const archiveTeam = async (teamId) => {
    await axios.delete(`/teams/${teamId}`);
    await loadTeams();
  };

  return (
    <PageLayout>
      <div className="mb-8 rounded-3xl bg-gradient-to-r from-slate-950 via-slate-900 to-emerald-950 text-white p-8 shadow-xl">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p className="text-emerald-300 uppercase tracking-[0.3em] text-xs mb-2">Enterprise Collaboration</p>
            <h1 className="text-4xl font-black">Teams</h1>
            <p className="text-slate-300 mt-2 max-w-2xl">
              Group execution responsibility across your workspace and project structure.
            </p>
          </div>
          <button
            onClick={loadTeams}
            className="inline-flex items-center gap-2 rounded-xl border border-white/20 bg-white/10 px-4 py-3 text-sm font-semibold hover:bg-white/15"
          >
            <FiRefreshCw />
            Refresh
          </button>
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.1fr_1.4fr]">
        <section className="rounded-3xl border bg-white p-6 shadow-sm">
          <h2 className="text-xl font-bold mb-4">Create Team</h2>
          {error && (
            <div className="mb-4 rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
              {error}
            </div>
          )}
          <form className="space-y-4" onSubmit={createTeam}>
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <label className="block text-sm font-medium mb-2">Tenant ID</label>
                <input
                  className="w-full rounded-xl border px-4 py-3 bg-slate-50"
                  value={form.tenant_id}
                  onChange={(e) => setForm({ ...form, tenant_id: e.target.value })}
                  placeholder="Tenant ID"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Workspace ID</label>
                <input
                  className="w-full rounded-xl border px-4 py-3 bg-slate-50"
                  value={form.workspace_id}
                  onChange={(e) => setForm({ ...form, workspace_id: e.target.value })}
                  placeholder="Workspace ID"
                  required
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Name</label>
              <input
                className="w-full rounded-xl border px-4 py-3"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                placeholder="Backend Team"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Description</label>
              <textarea
                className="w-full rounded-xl border px-4 py-3 min-h-28"
                value={form.description}
                onChange={(e) => setForm({ ...form, description: e.target.value })}
                placeholder="Responsible for APIs, services, and integrations"
              />
            </div>
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <label className="block text-sm font-medium mb-2">Created By</label>
                <input
                  className="w-full rounded-xl border px-4 py-3 bg-slate-50"
                  value={form.created_by}
                  readOnly
                  placeholder="Current user ID"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Status</label>
                <select
                  className="w-full rounded-xl border px-4 py-3"
                  value={form.is_active ? "active" : "archived"}
                  onChange={(e) => setForm({ ...form, is_active: e.target.value === "active" })}
                >
                  <option value="active">Active</option>
                  <option value="archived">Archived</option>
                </select>
              </div>
            </div>
            <button
              disabled={saving || !form.created_by}
              className="inline-flex items-center gap-2 rounded-xl bg-emerald-600 px-5 py-3 font-semibold text-white hover:bg-emerald-700 disabled:opacity-60"
            >
              <FiPlus />
              {saving ? "Creating..." : "Create Team"}
            </button>
          </form>
        </section>

        <section className="rounded-3xl border bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-xl font-bold">Team Directory</h2>
              <p className="text-sm text-slate-500">{teams.length} teams loaded</p>
            </div>
            <FiUsers className="text-2xl text-emerald-600" />
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            {loading && <div className="text-slate-500">Loading teams...</div>}
            {!loading &&
              teams.map((team) => (
                <article key={team.id} className="rounded-2xl border p-4 hover:border-emerald-200 hover:bg-emerald-50/40">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <h3 className="font-semibold text-lg">{team.name}</h3>
                      <p className="text-sm text-slate-500 mt-1">{team.description || "No description"}</p>
                    </div>
                    <span className={`rounded-full px-3 py-1 text-xs font-semibold ${team.is_active ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-slate-500"}`}>
                      {team.is_active ? "ACTIVE" : "ARCHIVED"}
                    </span>
                  </div>
                  <div className="mt-4 flex items-center gap-2">
                    <button
                      onClick={() => {
                        localStorage.setItem("teamId", team.id);
                        navigate(`/teams/${team.id}`);
                      }}
                      className="inline-flex items-center gap-2 rounded-xl bg-slate-900 px-4 py-2 text-sm font-medium text-white"
                    >
                      <FiEye />
                      Details
                    </button>
                    <button
                      onClick={() => archiveTeam(team.id)}
                      className="rounded-xl border px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
                    >
                      Archive
                    </button>
                  </div>
                </article>
              ))}
            {!loading && teams.length === 0 && <div className="text-slate-500">No teams found in this workspace.</div>}
          </div>
        </section>
      </div>
    </PageLayout>
  );
}
