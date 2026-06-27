import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { FiArrowLeft, FiBarChart2, FiUsers, FiCheckCircle, FiClock, FiAlertCircle } from "react-icons/fi";

import axios from "../api/axios";
import PageLayout from "../components/PageLayout";

export default function TeamWorkload() {
  const { id } = useParams();
  const teamId = Number(id);
  const [payload, setPayload] = useState(null);

  useEffect(() => {
    localStorage.setItem("teamId", String(teamId));
    axios.get(`/teams/${teamId}/workload`).then((res) => setPayload(res.data)).catch(console.error);
  }, [teamId]);

  const data = payload?.workload || payload;
  const byUser = payload?.by_user || [];
  const totalTasks = data?.total_tasks || 0;
  const completedTasks = data?.completed_tasks || 0;
  const pendingTasks = data?.pending_tasks || 0;
  const overdueTasks = data?.overdue_tasks || 0;
  const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  const cards = [
    { label: "Total Tasks", value: totalTasks, icon: FiBarChart2, tone: "from-slate-900 to-slate-700" },
    { label: "Completed", value: completedTasks, icon: FiCheckCircle, tone: "from-emerald-500 to-teal-600" },
    { label: "Pending", value: pendingTasks, icon: FiClock, tone: "from-cyan-500 to-blue-600" },
    { label: "Overdue", value: overdueTasks, icon: FiAlertCircle, tone: "from-rose-500 to-red-600" },
  ];

  return (
    <PageLayout>
      <div className="mb-6 flex items-center gap-3">
        <Link to={`/teams/${teamId}`} className="inline-flex items-center gap-2 rounded-xl border bg-white px-4 py-2 text-sm font-medium shadow-sm">
          <FiArrowLeft />
          Back to Team
        </Link>
      </div>

      <div className="rounded-3xl bg-gradient-to-r from-slate-950 via-emerald-950 to-teal-950 p-8 text-white shadow-xl">
        <p className="text-emerald-300 uppercase tracking-[0.3em] text-xs mb-2">Team Workload</p>
        <h1 className="text-4xl font-black">{payload?.team_name || `Team ${teamId}`}</h1>
        <p className="mt-2 max-w-2xl text-slate-300">Track assigned, completed, pending, and overdue tasks.</p>

        <div className="mt-6 grid gap-4 md:grid-cols-4">
          {cards.map((card) => {
            const Icon = card.icon;
            return (
              <div key={card.label} className="rounded-2xl bg-white/10 p-4 backdrop-blur">
                <div className="flex items-center justify-between">
                  <p className="text-xs uppercase tracking-wide text-slate-200">{card.label}</p>
                  <Icon className="text-white/80" />
                </div>
                <p className="mt-2 text-3xl font-black">{card.value}</p>
              </div>
            );
          })}
        </div>
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <section className="rounded-3xl border bg-white p-6 shadow-sm">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold">Workload Snapshot</h2>
              <p className="text-sm text-slate-500">Completion rate and task distribution at a glance.</p>
            </div>
            <FiUsers className="text-emerald-600" />
          </div>

          <div className="rounded-2xl bg-slate-50 p-4">
            <div className="flex items-center justify-between text-sm text-slate-600">
              <span>Completion rate</span>
              <span>{completionRate}%</span>
            </div>
            <div className="mt-3 h-3 rounded-full bg-slate-200">
              <div
                className="h-3 rounded-full bg-gradient-to-r from-emerald-500 to-teal-500"
                style={{ width: `${completionRate}%` }}
              />
            </div>
            <div className="mt-4 grid gap-3 sm:grid-cols-3">
              <div className="rounded-2xl bg-white p-4">
                <p className="text-xs uppercase tracking-wide text-slate-500">Assigned</p>
                <p className="mt-2 text-2xl font-black">{totalTasks}</p>
              </div>
              <div className="rounded-2xl bg-white p-4">
                <p className="text-xs uppercase tracking-wide text-slate-500">In Progress</p>
                <p className="mt-2 text-2xl font-black">{pendingTasks}</p>
              </div>
              <div className="rounded-2xl bg-white p-4">
                <p className="text-xs uppercase tracking-wide text-slate-500">At Risk</p>
                <p className="mt-2 text-2xl font-black">{overdueTasks}</p>
              </div>
            </div>
          </div>
        </section>

        <section className="rounded-3xl border bg-white p-6 shadow-sm">
          <div className="mb-4 flex items-center gap-2">
            <FiBarChart2 className="text-emerald-600" />
            <h2 className="text-xl font-bold">Data Snapshot</h2>
          </div>
          <pre className="max-h-[360px] overflow-auto rounded-2xl bg-slate-50 p-4 text-sm text-slate-700">
            {JSON.stringify(data, null, 2)}
          </pre>
        </section>
      </div>

      <div className="mt-6 rounded-3xl border bg-white p-6 shadow-sm">
        <h2 className="text-xl font-bold mb-4">Workload Per User</h2>
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {byUser.map((row) => {
            const userCompletion = row.total_tasks > 0 ? Math.round((row.completed_tasks / row.total_tasks) * 100) : 0;
            return (
              <div key={row.user_id || row.user_name} className="rounded-2xl border bg-slate-50 p-4">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <div className="font-semibold">{row.user_name}</div>
                    <div className="text-xs uppercase tracking-wide text-slate-500">User workload</div>
                  </div>
                  <span className="rounded-full bg-white px-3 py-1 text-xs font-semibold text-slate-600">{userCompletion}% done</span>
                </div>
                <div className="mt-4 h-2 rounded-full bg-slate-200">
                  <div className="h-2 rounded-full bg-gradient-to-r from-emerald-500 to-teal-500" style={{ width: `${userCompletion}%` }} />
                </div>
                <div className="mt-4 grid grid-cols-2 gap-3 text-sm text-slate-600">
                  <div className="rounded-xl bg-white p-3">
                    <span className="block text-xs uppercase tracking-wide text-slate-500">Total</span>
                    <span className="text-lg font-bold text-slate-900">{row.total_tasks}</span>
                  </div>
                  <div className="rounded-xl bg-white p-3">
                    <span className="block text-xs uppercase tracking-wide text-slate-500">Completed</span>
                    <span className="text-lg font-bold text-slate-900">{row.completed_tasks}</span>
                  </div>
                  <div className="rounded-xl bg-white p-3">
                    <span className="block text-xs uppercase tracking-wide text-slate-500">Pending</span>
                    <span className="text-lg font-bold text-slate-900">{row.pending_tasks}</span>
                  </div>
                  <div className="rounded-xl bg-white p-3">
                    <span className="block text-xs uppercase tracking-wide text-slate-500">Overdue</span>
                    <span className="text-lg font-bold text-slate-900">{row.overdue_tasks}</span>
                  </div>
                </div>
              </div>
            );
          })}
          {byUser.length === 0 && (
            <div className="rounded-2xl border border-dashed bg-slate-50 p-6 text-slate-500">
              No per-user workload data yet.
            </div>
          )}
        </div>
      </div>
    </PageLayout>
  );
}
