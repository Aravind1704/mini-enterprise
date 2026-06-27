import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { FiArrowLeft, FiUsers } from "react-icons/fi";

import axios from "../api/axios";
import PageLayout from "../components/PageLayout";

export default function ProjectWorkload() {
  const { id } = useParams();
  const projectId = Number(id);
  const [payload, setPayload] = useState(null);

  useEffect(() => {
    localStorage.setItem("projectId", String(projectId));
    axios.get(`/projects/${projectId}/workload`).then((res) => setPayload(res.data)).catch(console.error);
  }, [projectId]);

  return (
    <PageLayout>
      <div className="mb-6 flex items-center gap-3">
        <Link to={`/projects/${projectId}`} className="inline-flex items-center gap-2 rounded-xl border bg-white px-4 py-2 text-sm font-medium">
          <FiArrowLeft />
          Back to Project
        </Link>
      </div>

      <div className="rounded-3xl bg-gradient-to-r from-slate-950 via-cyan-950 to-indigo-950 p-8 text-white shadow-xl">
        <p className="text-cyan-300 uppercase tracking-[0.3em] text-xs mb-2">Project Workload</p>
        <h1 className="text-4xl font-black">{payload?.project_name || `Project ${projectId}`}</h1>
        <p className="text-slate-300 mt-2">Break down execution load by team and user.</p>
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-2">
        <section className="rounded-3xl border bg-white p-6 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <FiUsers className="text-cyan-600" />
            <h2 className="text-xl font-bold">By Team</h2>
          </div>
          <div className="space-y-3">
            {(payload?.by_team || []).map((row) => (
              <div key={row.team_id || row.team_name} className="rounded-2xl border px-4 py-3">
                <div className="font-semibold">{row.team_name}</div>
                <div className="text-sm text-slate-500">{row.total_tasks} total · {row.completed_tasks} done · {row.pending_tasks} pending · {row.overdue_tasks} overdue</div>
              </div>
            ))}
            {(payload?.by_team || []).length === 0 && <div className="text-slate-500">No team workload data.</div>}
          </div>
        </section>

        <section className="rounded-3xl border bg-white p-6 shadow-sm">
          <h2 className="text-xl font-bold mb-4">By User</h2>
          <div className="space-y-3">
            {(payload?.by_user || []).map((row) => (
              <div key={row.user_id || row.user_name} className="rounded-2xl border px-4 py-3">
                <div className="font-semibold">{row.user_name}</div>
                <div className="text-sm text-slate-500">{row.total_tasks} total · {row.completed_tasks} done · {row.pending_tasks} pending · {row.overdue_tasks} overdue</div>
              </div>
            ))}
            {(payload?.by_user || []).length === 0 && <div className="text-slate-500">No user workload data.</div>}
          </div>
        </section>
      </div>
    </PageLayout>
  );
}
