import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FiLogOut, FiShield, FiGlobe, FiLayers, FiUsers } from "react-icons/fi";

import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import axios from "../api/axios";
import { useAuth } from "../context/AuthContext";

export default function Dashboard() {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const [stats, setStats] = useState({
    tenants: 0,
    workspaces: 0,
    channels: 0,
    users: 0,
  });

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const res = await axios.get("/dashboard/stats");
      setStats(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const cards = [
    { label: "Tenants", value: stats.tenants, icon: FiShield, tone: "from-cyan-500 to-blue-600" },
    { label: "Workspaces", value: stats.workspaces, icon: FiGlobe, tone: "from-emerald-500 to-teal-600" },
    { label: "Channels", value: stats.channels, icon: FiLayers, tone: "from-violet-500 to-fuchsia-600" },
    { label: "Users", value: stats.users, icon: FiUsers, tone: "from-amber-500 to-orange-600" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white">
      <Topbar />
      <div className="flex">
        <Sidebar />

        <main className="flex-1 p-8">
          <div className="mb-8 rounded-3xl bg-gradient-to-r from-slate-950 via-indigo-950 to-cyan-950 p-8 text-white shadow-xl">
            <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
              <div>
                <p className="text-cyan-300 uppercase tracking-[0.3em] text-xs mb-2">
                  Super Admin Console
                </p>
                <h1 className="text-4xl font-black">
                  Tenant Operations
                </h1>
                <p className="mt-2 max-w-2xl text-slate-300">
                  Oversee tenants, workspaces, channels, and user growth from one control panel.
                </p>
              </div>

              <button
                onClick={handleLogout}
                className="inline-flex items-center gap-2 rounded-2xl bg-white px-5 py-3 font-semibold text-slate-900 shadow-lg hover:bg-slate-100"
              >
                <FiLogOut />
                Logout
              </button>
            </div>
          </div>

          <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
            {cards.map((card) => {
              const Icon = card.icon;
              return (
                <article key={card.label} className="overflow-hidden rounded-3xl border bg-white shadow-sm">
                  <div className={`h-2 bg-gradient-to-r ${card.tone}`} />
                  <div className="p-6">
                    <div className="flex items-center justify-between gap-4">
                      <div>
                        <p className="text-sm font-medium text-slate-500">{card.label}</p>
                        <p className="mt-2 text-4xl font-black">{card.value}</p>
                      </div>
                      <div className={`rounded-2xl bg-gradient-to-r ${card.tone} p-3 text-white shadow-lg`}>
                        <Icon size={22} />
                      </div>
                    </div>
                  </div>
                </article>
              );
            })}
          </div>
        </main>
      </div>
    </div>
  );
}
