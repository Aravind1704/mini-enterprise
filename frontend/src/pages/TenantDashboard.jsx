import React, {
  useEffect,
  useState
} from "react";

import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import axios from "../api/axios";

export default function Dashboard() {

  const [stats, setStats] =
    useState({
      tenants: 0,
      workspaces: 0,
      channels: 0,
      users: 0
    });

  useEffect(() => {

    loadStats();

  }, []);

  const loadStats = async () => {

    try {

      const res =
        await axios.get(
          "/dashboard/stats"
        );

      setStats(res.data);

    } catch (err) {

      console.error(err);

    }

  };

  return (

    <div className="min-h-screen bg-slate-50">

      <Topbar />

      <div className="flex">

        <Sidebar />

        <main className="flex-1 p-8">

          <h1 className="text-4xl font-bold mb-2">
            Dashboard
          </h1>

          <p className="text-gray-500 mb-8">
            SaaS Tenant Management Platform
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">

            <div className="bg-white p-6 rounded-xl border shadow-sm">
              <h3 className="text-gray-500">
                Tenants
              </h3>

              <p className="text-4xl font-bold mt-2">
                {stats.tenants}
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl border shadow-sm">
              <h3 className="text-gray-500">
                Workspaces
              </h3>

              <p className="text-4xl font-bold mt-2">
                {stats.workspaces}
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl border shadow-sm">
              <h3 className="text-gray-500">
                Channels
              </h3>

              <p className="text-4xl font-bold mt-2">
                {stats.channels}
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl border shadow-sm">
              <h3 className="text-gray-500">
                Users
              </h3>

              <p className="text-4xl font-bold mt-2">
                {stats.users}
              </p>
            </div>

          </div>

        </main>

      </div>

    </div>

  );

}