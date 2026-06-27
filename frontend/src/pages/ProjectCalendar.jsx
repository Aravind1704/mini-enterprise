import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { FiArrowLeft, FiCalendar, FiClock, FiTarget, FiFlag } from "react-icons/fi";

import axios from "../api/axios";
import PageLayout from "../components/PageLayout";

export default function ProjectCalendar() {
  const { id } = useParams();
  const projectId = Number(id);
  const [calendar, setCalendar] = useState(null);

  useEffect(() => {
    localStorage.setItem("projectId", String(projectId));
    axios.get(`/projects/${projectId}/calendar`).then((res) => setCalendar(res.data)).catch(console.error);
  }, [projectId]);

  const meetings = calendar?.meetings || [];
  const tasks = calendar?.tasks || [];
  const milestones = calendar?.milestones || [];
  const releaseDates = calendar?.release_dates || [];

  return (
    <PageLayout>
      <div className="mb-6 flex items-center gap-3">
        <Link to={`/projects/${projectId}`} className="inline-flex items-center gap-2 rounded-xl border bg-white px-4 py-2 text-sm font-medium shadow-sm">
          <FiArrowLeft />
          Back to Project
        </Link>
      </div>

      <div className="rounded-3xl bg-gradient-to-r from-slate-950 via-cyan-950 to-emerald-950 p-8 text-white shadow-xl">
        <p className="text-cyan-300 uppercase tracking-[0.3em] text-xs mb-2">Project Calendar</p>
        <h1 className="text-4xl font-black">{calendar?.project_name || `Project ${projectId}`}</h1>
        <p className="mt-2 max-w-2xl text-slate-300">Meetings, task due dates, milestones, and release dates in one timeline.</p>

        <div className="mt-6 grid gap-4 md:grid-cols-4">
          {[
            ["Meetings", meetings.length, FiCalendar],
            ["Tasks", tasks.length, FiClock],
            ["Milestones", milestones.length, FiTarget],
            ["Releases", releaseDates.length, FiFlag],
          ].map(([label, value, Icon]) => {
            const IconComponent = Icon;
            return (
              <div key={label} className="rounded-2xl bg-white/10 p-4 backdrop-blur">
                <div className="flex items-center justify-between">
                  <p className="text-xs uppercase tracking-wide text-slate-200">{label}</p>
                  <IconComponent className="text-cyan-200" />
                </div>
                <p className="mt-2 text-3xl font-black">{value}</p>
              </div>
            );
          })}
        </div>
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-2">
        <section className="rounded-3xl border bg-white p-6 shadow-sm">
          <div className="mb-4 flex items-center gap-2">
            <FiCalendar className="text-cyan-600" />
            <h2 className="text-xl font-bold">Meetings</h2>
          </div>
          <div className="space-y-3">
            {meetings.map((meeting) => (
              <div key={meeting.id} className="rounded-2xl border bg-slate-50 px-4 py-3">
                <div className="font-semibold">{meeting.title}</div>
                <div className="text-sm text-slate-500">{new Date(meeting.start_time).toLocaleString()} - {new Date(meeting.end_time).toLocaleString()}</div>
              </div>
            ))}
            {meetings.length === 0 && <div className="rounded-2xl border border-dashed bg-slate-50 px-4 py-5 text-slate-500">No meetings scheduled.</div>}
          </div>
        </section>

        <section className="rounded-3xl border bg-white p-6 shadow-sm">
          <div className="mb-4 flex items-center gap-2">
            <FiClock className="text-cyan-600" />
            <h2 className="text-xl font-bold">Task Due Dates</h2>
          </div>
          <div className="space-y-3">
            {tasks.map((task) => (
              <div key={task.id} className="rounded-2xl border bg-slate-50 px-4 py-3">
                <div className="font-semibold">{task.title}</div>
                <div className="text-sm text-slate-500">{task.due_date ? new Date(task.due_date).toLocaleDateString() : "No due date"}</div>
              </div>
            ))}
            {tasks.length === 0 && <div className="rounded-2xl border border-dashed bg-slate-50 px-4 py-5 text-slate-500">No project tasks yet.</div>}
          </div>
        </section>

        <section className="rounded-3xl border bg-white p-6 shadow-sm">
          <div className="mb-4 flex items-center gap-2">
            <FiTarget className="text-emerald-600" />
            <h2 className="text-xl font-bold">Milestones</h2>
          </div>
          <div className="space-y-3">
            {milestones.map((item) => (
              <div key={item.id} className="rounded-2xl border bg-slate-50 px-4 py-3">
                <div className="font-semibold">{item.title}</div>
                <div className="text-sm text-slate-500">{item.date ? new Date(item.date).toLocaleDateString() : "No date"}</div>
              </div>
            ))}
            {milestones.length === 0 && <div className="rounded-2xl border border-dashed bg-slate-50 px-4 py-5 text-slate-500">No milestones defined yet.</div>}
          </div>
        </section>

        <section className="rounded-3xl border bg-white p-6 shadow-sm">
          <div className="mb-4 flex items-center gap-2">
            <FiFlag className="text-emerald-600" />
            <h2 className="text-xl font-bold">Release Dates</h2>
          </div>
          <div className="space-y-3">
            {releaseDates.map((item) => (
              <div key={item.id} className="rounded-2xl border bg-slate-50 px-4 py-3">
                <div className="font-semibold">{item.title}</div>
                <div className="text-sm text-slate-500">{item.date ? new Date(item.date).toLocaleDateString() : "No date"}</div>
              </div>
            ))}
            {releaseDates.length === 0 && <div className="rounded-2xl border border-dashed bg-slate-50 px-4 py-5 text-slate-500">No release dates defined yet.</div>}
          </div>
        </section>
      </div>
    </PageLayout>
  );
}
