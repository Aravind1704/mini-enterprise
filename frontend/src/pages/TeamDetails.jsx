import { useCallback, useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { FiArrowLeft, FiUserPlus, FiTrash2, FiActivity } from "react-icons/fi";

import axios from "../api/axios";
import PageLayout from "../components/PageLayout";

export default function TeamDetails() {
  const { id } = useParams();
  const teamId = Number(id);

  const [team, setTeam] = useState(null);
  const [teamForm, setTeamForm] = useState({
    name: "",
    description: "",
    is_active: true,
  });
  const [members, setMembers] = useState([]);
  const [workload, setWorkload] = useState(null);
  const [form, setForm] = useState({ user_id: "", role: "MEMBER" });

  const load = useCallback(async () => {
    const [teamRes, membersRes, workloadRes] = await Promise.all([
      axios.get(`/teams/${teamId}`),
      axios.get(`/teams/${teamId}/members`),
      axios.get(`/teams/${teamId}/workload`),
    ]);
    setTeam(teamRes.data);
    setTeamForm({
      name: teamRes.data?.name || "",
      description: teamRes.data?.description || "",
      is_active: teamRes.data?.is_active ?? true,
    });
    setMembers(membersRes.data || []);
    setWorkload(workloadRes.data?.workload || workloadRes.data);
  }, [teamId]);

  useEffect(() => {
    localStorage.setItem("teamId", String(teamId));
    load().catch(console.error);
  }, [load, teamId]);

  const addMember = async (e) => {
    e.preventDefault();
    await axios.post(`/teams/${teamId}/members`, {
      team_id: teamId,
      user_id: Number(form.user_id),
      role: form.role,
    });
    setForm({ user_id: "", role: "MEMBER" });
    await load();
  };

  const removeMember = async (userId) => {
    await axios.delete(`/teams/${teamId}/members/${userId}`);
    await load();
  };

  const updateTeam = async (e) => {
    e.preventDefault();
    await axios.put(`/teams/${teamId}`, {
      name: teamForm.name,
      description: teamForm.description,
      is_active: teamForm.is_active,
    });
    await load();
  };

  const archiveTeam = async () => {
    await axios.delete(`/teams/${teamId}`);
    await load();
  };

  const restoreTeam = async () => {
    await axios.patch(`/teams/${teamId}/restore`);
    await load();
  };

  if (!team) {
    return (
      <PageLayout>
        <div className="rounded-3xl border bg-white p-8">Loading team...</div>
      </PageLayout>
    );
  }

  return (
    <PageLayout>
      <div className="mb-6 flex items-center gap-3">
        <Link to="/teams" className="inline-flex items-center gap-2 rounded-xl border bg-white px-4 py-2 text-sm font-medium">
          <FiArrowLeft />
          Back
        </Link>
        <span className={`rounded-full px-3 py-1 text-xs font-semibold ${team.is_active ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-slate-500"}`}>
          {team.is_active ? "ACTIVE" : "ARCHIVED"}
        </span>
        <button type="button" onClick={archiveTeam} className="inline-flex items-center gap-2 rounded-xl border border-rose-200 bg-white px-4 py-2 text-sm font-medium text-rose-700">
          Archive
        </button>
        <button type="button" onClick={restoreTeam} className="inline-flex items-center gap-2 rounded-xl border border-emerald-200 bg-white px-4 py-2 text-sm font-medium text-emerald-700">
          Restore
        </button>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <section className="lg:col-span-2 rounded-3xl border bg-white p-6 shadow-sm">
          <h1 className="text-3xl font-black">{team.name}</h1>
          <p className="text-slate-500 mt-2">{team.description || "No description provided."}</p>

          <form className="mt-6 grid gap-4" onSubmit={updateTeam}>
            <div className="grid gap-4 md:grid-cols-2">
              <input
                className="rounded-xl border px-4 py-3"
                value={teamForm.name}
                onChange={(e) => setTeamForm({ ...teamForm, name: e.target.value })}
                placeholder="Team name"
              />
              <select
                className="rounded-xl border px-4 py-3"
                value={teamForm.is_active ? "active" : "archived"}
                onChange={(e) => setTeamForm({ ...teamForm, is_active: e.target.value === "active" })}
              >
                <option value="active">Active</option>
                <option value="archived">Archived</option>
              </select>
            </div>
            <textarea
              className="rounded-xl border px-4 py-3 min-h-28"
              value={teamForm.description}
              onChange={(e) => setTeamForm({ ...teamForm, description: e.target.value })}
              placeholder="Description"
            />
            <div>
              <button className="rounded-xl bg-emerald-600 px-5 py-3 font-semibold text-white hover:bg-emerald-700">
                Update Team
              </button>
            </div>
          </form>

          <div className="mt-8 grid gap-4 md:grid-cols-4">
            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="text-xs uppercase tracking-wide text-slate-500">Members</p>
              <p className="text-2xl font-bold">{members.length}</p>
            </div>
            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="text-xs uppercase tracking-wide text-slate-500">Tasks</p>
              <p className="text-2xl font-bold">{workload?.total_tasks ?? 0}</p>
            </div>
            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="text-xs uppercase tracking-wide text-slate-500">Pending</p>
              <p className="text-2xl font-bold">{workload?.pending_tasks ?? 0}</p>
            </div>
            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="text-xs uppercase tracking-wide text-slate-500">Overdue</p>
              <p className="text-2xl font-bold">{workload?.overdue_tasks ?? 0}</p>
            </div>
          </div>
        </section>

        <section className="rounded-3xl border bg-white p-6 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <FiActivity className="text-emerald-600" />
            <h2 className="text-xl font-bold">Workload</h2>
          </div>
          <p className="text-sm text-slate-500 mb-2">{workload?.team_name || team.name}</p>
          <div className="space-y-3 text-sm">
            <div className="flex justify-between"><span>Total</span><strong>{workload?.total_tasks ?? 0}</strong></div>
            <div className="flex justify-between"><span>Completed</span><strong>{workload?.completed_tasks ?? 0}</strong></div>
            <div className="flex justify-between"><span>Pending</span><strong>{workload?.pending_tasks ?? 0}</strong></div>
            <div className="flex justify-between"><span>Overdue</span><strong>{workload?.overdue_tasks ?? 0}</strong></div>
          </div>
        </section>
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-2">
        <section className="rounded-3xl border bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold">Add Member</h2>
            <FiUserPlus className="text-emerald-600" />
          </div>
          <form className="grid gap-4" onSubmit={addMember}>
            <input
              className="rounded-xl border px-4 py-3"
              placeholder="User ID"
              value={form.user_id}
              onChange={(e) => setForm({ ...form, user_id: e.target.value })}
            />
            <select
              className="rounded-xl border px-4 py-3"
              value={form.role}
              onChange={(e) => setForm({ ...form, role: e.target.value })}
            >
              <option value="LEAD">Lead</option>
              <option value="MEMBER">Member</option>
              <option value="VIEWER">Viewer</option>
            </select>
            <button className="rounded-xl bg-emerald-600 px-4 py-3 font-semibold text-white hover:bg-emerald-700">
              Add to Team
            </button>
          </form>
        </section>

        <section className="rounded-3xl border bg-white p-6 shadow-sm">
          <h2 className="text-xl font-bold mb-4">Members</h2>
          <div className="space-y-3">
            {members.map((member) => (
              <div key={member.id} className="flex items-center justify-between rounded-2xl border px-4 py-3">
                <div>
                  <div className="font-semibold">User #{member.user_id}</div>
                  <div className="text-sm text-slate-500">{member.role}</div>
                </div>
                <button
                  onClick={() => removeMember(member.user_id)}
                  className="inline-flex items-center gap-2 rounded-xl border px-3 py-2 text-sm text-rose-600 hover:bg-rose-50"
                >
                  <FiTrash2 />
                  Remove
                </button>
              </div>
            ))}
            {members.length === 0 && <div className="text-slate-500">No members yet.</div>}
          </div>
        </section>
      </div>
    </PageLayout>
  );
}
