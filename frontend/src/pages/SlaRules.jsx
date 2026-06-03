import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import { useAuth } from "../context/AuthContext";
import api from "../api/axios";

export default function SlaRules() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [rules, setRules] = useState([]);

  const [form, setForm] = useState({
    module_name: "task",
    priority: "high",
    allowed_hours: 24,
    escalation_enabled: false,
    escalation_after_hours: 1,
  });

  const [editing, setEditing] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {

  fetchRules();

  const interval = setInterval(() => {
    fetchRules();
  }, 5000);

  return () => clearInterval(interval);

}, []);

  async function fetchRules() {
    try {
      setLoading(true);

      const res = await api.get("/sla-rules");

      setRules(res.data || []);
    } catch (err) {
      console.error(err);
      setError("Failed to load SLA rules");
    } finally {
      setLoading(false);
    }
  }

  async function save(e) {
    e.preventDefault();

    try {
      if (editing) {
        await api.put(`/sla-rules/${editing.id}`, form);
      } else {
        await api.post("/sla-rules", form);
      }

      setEditing(null);

      setForm({
        module_name: "task",
        priority: "high",
        allowed_hours: 24,
        escalation_enabled: false,
        escalation_after_hours: 1,
      });

      fetchRules();
    } catch (err) {
      setError("Failed to save SLA rule");
    }
  }

  async function disableRule(id) {
    if (!window.confirm("Disable this SLA Rule?")) return;

    try {
      await api.delete(`/sla-rules/${id}`);
      fetchRules();
    } catch (err) {
      setError("Failed to disable rule");
    }
  }

  function edit(rule) {
    setEditing(rule);

    setForm({
      module_name: rule.module_name,
      priority: rule.priority,
      allowed_hours: rule.allowed_hours,
      escalation_enabled: rule.escalation_enabled,
      escalation_after_hours: rule.escalation_after_hours,
    });

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  }

  if (!user) return null;

  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-gradient-to-br from-slate-100 via-white to-slate-200 p-6">

        <div className="max-w-7xl mx-auto space-y-8">

          {/* HEADER */}
          <div className="bg-white rounded-3xl shadow-2xl border border-slate-200 p-8 flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6">

            <div>
              <h1 className="text-4xl font-bold text-slate-800 flex items-center gap-3">
                ⚙️ SLA Rules 
              </h1>

              <p className="text-slate-500 mt-3 text-sm md:text-base">
                Manage escalation policies, approval rules, and SLA tracking
                with enterprise-grade controls.
              </p>
            </div>

            {/* RIGHT SIDE BUTTONS */}
            <div className="flex flex-wrap gap-4 w-full lg:w-auto justify-end">

              {/* BACK BUTTON */}
              <button
                onClick={() => navigate(-1)}
                className="
                  px-6
                  py-3
                  rounded-2xl
                  bg-slate-900
                  text-white
                  font-semibold
                  shadow-lg
                  hover:bg-slate-800
                  hover:scale-105
                  transition-all
                  duration-300
                "
              >
                ← Back
              </button>

              {/* NEW RULE BUTTON */}
              <button
                onClick={() => {
                  setEditing(null);

                  setForm({
                    module_name: "task",
                    priority: "high",
                    allowed_hours: 24,
                    escalation_enabled: false,
                    escalation_after_hours: 1,
                  });
                }}
                className="
                  px-6
                  py-3
                  rounded-2xl
                  bg-blue-600
                  text-white
                  font-semibold
                  shadow-lg
                  hover:bg-blue-700
                  hover:scale-105
                  transition-all
                  duration-300
                "
              >
                + New Rule
              </button>
            </div>
          </div>

          {/* ERROR */}
          {error && (
            <div className="bg-red-100 border border-red-300 text-red-700 rounded-2xl shadow-md p-4">
              {error}
            </div>
          )}

          {/* FORM CARD */}
          <div className="bg-white rounded-3xl shadow-2xl border border-slate-200 p-8">

            <div className="flex items-center justify-between mb-8">
              <h2 className="text-2xl font-bold text-slate-800">
                {editing ? "✏️ Edit SLA Rule" : "➕ Create SLA Rule"}
              </h2>
            </div>

            <form onSubmit={save} className="space-y-6">

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                {/* MODULE */}
                <div>
                  <label className="block mb-2 text-sm font-semibold text-slate-700">
                    Module
                  </label>

                  <select
                    value={form.module_name}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        module_name: e.target.value,
                      })
                    }
                    className="
                      w-full
                      p-4
                      rounded-2xl
                      border
                      border-slate-300
                      bg-slate-50
                      focus:ring-4
                      focus:ring-blue-200
                      outline-none
                      transition
                    "
                  >
                    <option value="task">Task</option>
                    <option value="approval">Approval</option>
                  </select>
                </div>

                {/* PRIORITY */}
                <div>
                  <label className="block mb-2 text-sm font-semibold text-slate-700">
                    Priority
                  </label>

                  <select
                    value={form.priority}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        priority: e.target.value,
                      })
                    }
                    className="
                      w-full
                      p-4
                      rounded-2xl
                      border
                      border-slate-300
                      bg-slate-50
                      focus:ring-4
                      focus:ring-blue-200
                      outline-none
                      transition
                    "
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>

                {/* HOURS */}
                <div>
                  <label className="block mb-2 text-sm font-semibold text-slate-700">
                    Allowed Hours
                  </label>

                  <input
                    type="number"
                    min="1"
                    value={form.allowed_hours}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        allowed_hours: Number(e.target.value),
                      })
                    }
                    className="
                      w-full
                      p-4
                      rounded-2xl
                      border
                      border-slate-300
                      bg-slate-50
                      focus:ring-4
                      focus:ring-blue-200
                      outline-none
                      transition
                    "
                  />
                </div>

                {/* ESCALATION */}
                <div className="flex items-center pt-10">
                  <label className="flex items-center gap-3 text-slate-700 font-semibold">

                    <input
                      type="checkbox"
                      checked={form.escalation_enabled}
                      onChange={(e) =>
                        setForm({
                          ...form,
                          escalation_enabled: e.target.checked,
                        })
                      }
                      className="w-5 h-5"
                    />

                    Escalation Enabled
                  </label>
                </div>

                {/* ESCALATION HOURS */}
                {form.escalation_enabled && (
                  <div className="md:col-span-2">

                    <label className="block mb-2 text-sm font-semibold text-slate-700">
                      Escalation After Hours
                    </label>

                    <input
                      type="number"
                      min="1"
                      value={form.escalation_after_hours}
                      onChange={(e) =>
                        setForm({
                          ...form,
                          escalation_after_hours: Number(e.target.value),
                        })
                      }
                      className="
                        w-full
                        p-4
                        rounded-2xl
                        border
                        border-slate-300
                        bg-slate-50
                        focus:ring-4
                        focus:ring-blue-200
                        outline-none
                        transition
                      "
                    />
                  </div>
                )}
              </div>

              {/* BUTTONS */}
              <div className="flex flex-wrap gap-4 pt-2">

                <button
                  type="submit"
                  className="
                    px-8
                    py-3
                    rounded-2xl
                    bg-green-600
                    text-white
                    font-semibold
                    shadow-lg
                    hover:bg-green-700
                    hover:scale-105
                    transition-all
                    duration-300
                  "
                >
                  {editing ? "Update Rule" : "Create Rule"}
                </button>

                {editing && (
                  <button
                    type="button"
                    onClick={() => {
                      setEditing(null);

                      setForm({
                        module_name: "task",
                        priority: "high",
                        allowed_hours: 24,
                        escalation_enabled: false,
                        escalation_after_hours: 1,
                      });
                    }}
                    className="
                      px-8
                      py-3
                      rounded-2xl
                      bg-slate-500
                      text-white
                      font-semibold
                      shadow-lg
                      hover:bg-slate-600
                      hover:scale-105
                      transition-all
                      duration-300
                    "
                  >
                    Cancel
                  </button>
                )}
              </div>
            </form>
          </div>

          {/* TABLE */}
          <div className="bg-white rounded-3xl shadow-2xl border border-slate-200 overflow-hidden">

            <div className="p-6 border-b bg-slate-50">
              <h2 className="text-2xl font-bold text-slate-800">
                📋 SLA Rules List
              </h2>
            </div>

            {loading ? (
              <div className="p-10 text-center text-slate-500 text-lg">
                Loading SLA Rules...
              </div>
            ) : rules.length === 0 ? (
              <div className="p-10 text-center text-slate-500 text-lg">
                No SLA Rules Found
              </div>
            ) : (
              <div className="overflow-x-auto">

                <table className="w-full text-sm">

                  <thead className="bg-slate-100 text-slate-700">
                    <tr>
                      <th className="p-5 text-left font-bold">ID</th>
                      <th className="p-5 text-left font-bold">Module</th>
                      <th className="p-5 text-left font-bold">Priority</th>
                      <th className="p-5 text-left font-bold">Hours</th>
                      <th className="p-5 text-left font-bold">Escalation</th>
                      <th className="p-5 text-left font-bold">Status</th>
                      <th className="p-5 text-left font-bold">Actions</th>
                    </tr>
                  </thead>

                  <tbody>
                    {rules.map((r) => (
                      <tr
                        key={r.id}
                        className="
                          border-t
                          hover:bg-slate-50
                          hover:shadow-md
                          transition-all
                          duration-200
                        "
                      >
                        <td className="p-5 font-medium">{r.id}</td>

                        <td className="p-5 capitalize">
                          {r.module_name}
                        </td>

                        <td className="p-5 capitalize">
                          {r.priority}
                        </td>

                        <td className="p-5">
                          {r.allowed_hours}h
                        </td>

                        <td className="p-5">
                          {r.escalation_enabled
                            ? `Yes (${r.escalation_after_hours}h)`
                            : "No"}
                        </td>

                        <td className="p-5">
                          {r.is_active ? (
                            <span className="px-3 py-1 rounded-full bg-green-100 text-green-700 font-semibold">
                              Active
                            </span>
                          ) : (
                            <span className="px-3 py-1 rounded-full bg-red-100 text-red-700 font-semibold">
                              Disabled
                            </span>
                          )}
                        </td>

                        <td className="p-5 flex gap-4">

                          <button
                            onClick={() => edit(r)}
                            className="
                              text-blue-600
                              font-semibold
                              hover:text-blue-800
                              hover:underline
                              transition
                            "
                          >
                            Edit
                          </button>

                          {r.is_active && (
                            <button
                              onClick={() => disableRule(r.id)}
                              className="
                                text-red-600
                                font-semibold
                                hover:text-red-800
                                hover:underline
                                transition
                              "
                            >
                              Disable
                            </button>
                          )}

                        </td>
                      </tr>
                    ))}
                  </tbody>

                </table>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}