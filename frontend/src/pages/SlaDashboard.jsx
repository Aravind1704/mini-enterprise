import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function SlaDashboard() {
  const navigate = useNavigate();

  const [active, setActive] = useState([]);
  const [breached, setBreached] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {

  fetchData();

  const interval = setInterval(() => {
    fetchData();
  }, 5000);

  return () => clearInterval(interval);

}, []);

  const fetchData = async () => {
    try {
      const token = localStorage.getItem("access_token");

      const headers = {
        Authorization: `Bearer ${token}`,
      };

      const [activeRes, breachedRes] = await Promise.all([
        fetch("http://127.0.0.1:8000/sla-tracking/active", {
          headers,
        }),
        fetch("http://127.0.0.1:8000/sla-tracking/breached", {
          headers,
        }),
      ]);

      const activeData = await activeRes.json();
      const breachedData = await breachedRes.json();

      setActive(activeData || []);
      setBreached(breachedData || []);
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#eef2ff] via-[#f8fafc] to-[#e0e7ff]">

      {/* TOP NAVBAR */}
      <div className="w-full bg-white/80 backdrop-blur-xl border-b border-gray-200 sticky top-0 z-50 shadow-sm">

        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">

          {/* LOGO */}
          <div className="flex items-center gap-3">

            <div className="
              w-11
              h-11
              rounded-2xl
              bg-indigo-600
              text-white
              flex
              items-center
              justify-center
              text-xl
              shadow-lg
            ">
              📊
            </div>

            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                EnterpriseFlow
              </h1>

              <p className="text-xs text-gray-500">
                SLA Monitoring Dashboard
              </p>
            </div>

          </div>

          {/* ACTIONS */}
          <div className="flex items-center gap-4">

            <button
              onClick={fetchData}
              className="
                bg-white
                border
                border-gray-200
                hover:border-indigo-400
                px-5
                py-2.5
                rounded-xl
                text-gray-700
                font-semibold
                hover:shadow-md
                transition-all
              "
            >
              🔄 Refresh
            </button>

            <button
              onClick={() => navigate("/dashboard")}
              className="
                bg-indigo-600
                hover:bg-indigo-700
                text-white
                px-6
                py-2.5
                rounded-xl
                font-semibold
                shadow-lg
                hover:shadow-xl
                transition-all
              "
            >
              ← Back
            </button>

          </div>

        </div>

      </div>

      {/* MAIN */}
      <div className="max-w-7xl mx-auto px-6 py-10">

        {/* HEADER */}
        <div className="
          bg-white/70
          backdrop-blur-xl
          rounded-[32px]
          shadow-xl
          border
          border-white/40
          p-8
          md:p-10
          mb-10
        ">

          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-8">

            <div className="flex items-center gap-5">

              <div className="
                w-20
                h-20
                rounded-3xl
                bg-indigo-100
                flex
                items-center
                justify-center
                text-4xl
                shadow-md
              ">
                📈
              </div>

              <div>

                <h2 className="text-5xl font-bold text-gray-900">
                  SLA Dashboard
                </h2>

                <p className="text-gray-500 mt-3 text-lg">
                  Monitor SLA performance, breached timelines and operational efficiency
                </p>

              </div>

            </div>

          </div>

        </div>

        {/* LOADING */}
        {loading ? (
          <div className="
            bg-white
            rounded-3xl
            shadow-xl
            p-20
            text-center
          ">

            <div className="animate-pulse">

              <div className="
                w-20
                h-20
                bg-indigo-100
                rounded-full
                mx-auto
                mb-8
              "></div>

              <h2 className="text-3xl font-bold text-gray-700">
                Loading Dashboard...
              </h2>

            </div>

          </div>
        ) : (
          <>
            {/* STATS */}
            <div className="
              grid
              grid-cols-1
              md:grid-cols-2
              xl:grid-cols-4
              gap-8
              mb-12
            ">

              {/* CARD */}
              <div className="
                bg-white/80
                backdrop-blur-xl
                rounded-3xl
                p-8
                shadow-lg
                hover:shadow-2xl
                border
                border-white
                transition-all
                hover:-translate-y-2
              ">

                <div className="flex items-start justify-between">

                  <div>

                    <p className="text-gray-500 text-sm font-bold uppercase">
                      Active SLAs
                    </p>

                    <h2 className="text-6xl font-bold text-green-500 mt-4">
                      {active.length}
                    </h2>

                  </div>

                  <div className="
                    w-16
                    h-16
                    rounded-2xl
                    bg-green-100
                    flex
                    items-center
                    justify-center
                    text-3xl
                  ">
                    ✅
                  </div>

                </div>

              </div>

              {/* CARD */}
              <div className="
                bg-white/80
                backdrop-blur-xl
                rounded-3xl
                p-8
                shadow-lg
                hover:shadow-2xl
                border
                border-white
                transition-all
                hover:-translate-y-2
              ">

                <div className="flex items-start justify-between">

                  <div>

                    <p className="text-gray-500 text-sm font-bold uppercase">
                      Breached
                    </p>

                    <h2 className="text-6xl font-bold text-red-500 mt-4">
                      {breached.length}
                    </h2>

                  </div>

                  <div className="
                    w-16
                    h-16
                    rounded-2xl
                    bg-red-100
                    flex
                    items-center
                    justify-center
                    text-3xl
                  ">
                    ⚠️
                  </div>

                </div>

              </div>

              {/* CARD */}
              <div className="
                bg-white/80
                backdrop-blur-xl
                rounded-3xl
                p-8
                shadow-lg
                hover:shadow-2xl
                border
                border-white
                transition-all
                hover:-translate-y-2
              ">

                <div className="flex items-start justify-between">

                  <div>

                    <p className="text-gray-500 text-sm font-bold uppercase">
                      Total Records
                    </p>

                    <h2 className="text-6xl font-bold text-indigo-600 mt-4">
                      {active.length + breached.length}
                    </h2>

                  </div>

                  <div className="
                    w-16
                    h-16
                    rounded-2xl
                    bg-indigo-100
                    flex
                    items-center
                    justify-center
                    text-3xl
                  ">
                    📊
                  </div>

                </div>

              </div>

              {/* CARD */}
              <div className="
                bg-white/80
                backdrop-blur-xl
                rounded-3xl
                p-8
                shadow-lg
                hover:shadow-2xl
                border
                border-white
                transition-all
                hover:-translate-y-2
              ">

                <div className="flex items-start justify-between">

                  <div>

                    <p className="text-gray-500 text-sm font-bold uppercase">
                      SLA Health
                    </p>

                    <h2 className="text-5xl font-bold text-purple-600 mt-4">
                      Excellent
                    </h2>

                  </div>

                  <div className="
                    w-16
                    h-16
                    rounded-2xl
                    bg-purple-100
                    flex
                    items-center
                    justify-center
                    text-3xl
                  ">
                    🚀
                  </div>

                </div>

              </div>

            </div>

            {/* ACTIVE TABLE */}
            <div className="
              bg-white/80
              backdrop-blur-xl
              rounded-[32px]
              shadow-xl
              border
              border-white
              overflow-hidden
              mb-10
            ">

              <div className="
                px-8
                py-6
                border-b
                border-gray-100
                flex
                items-center
                justify-between
              ">

                <div>

                  <h2 className="text-3xl font-bold text-gray-900">
                    ✅ Active SLA Records
                  </h2>

                  <p className="text-gray-500 mt-2">
                    Records currently within SLA timeline
                  </p>

                </div>

                <div className="
                  bg-green-100
                  text-green-700
                  px-4
                  py-2
                  rounded-xl
                  font-bold
                ">
                  {active.length} Active
                </div>

              </div>

              <div className="overflow-x-auto">

                <table className="w-full">

                  <thead className="bg-gray-50">

                    <tr>

                      <th className="px-8 py-5 text-left text-sm font-bold text-gray-600 uppercase">
                        ID
                      </th>

                      <th className="px-8 py-5 text-left text-sm font-bold text-gray-600 uppercase">
                        Module
                      </th>

                      <th className="px-8 py-5 text-left text-sm font-bold text-gray-600 uppercase">
                        Record ID
                      </th>

                      <th className="px-8 py-5 text-left text-sm font-bold text-gray-600 uppercase">
                        Due Time
                      </th>

                    </tr>

                  </thead>

                  <tbody>

                    {active.map((item) => (

                      <tr
                        key={item.id}
                        className="
                          border-t
                          hover:bg-indigo-50
                          transition-all
                        "
                      >

                        <td className="px-8 py-6 font-bold">
                          #{item.id}
                        </td>

                        <td className="px-8 py-6 font-semibold text-gray-800">
                          {item.module_name}
                        </td>

                        <td className="px-8 py-6 text-gray-600">
                          {item.record_id}
                        </td>

                        <td className="px-8 py-6 text-gray-600">
                          {new Date(item.due_time).toLocaleString()}
                        </td>

                      </tr>

                    ))}

                  </tbody>

                </table>

              </div>

            </div>

            {/* BREACHED TABLE */}
            <div className="
              bg-white/80
              backdrop-blur-xl
              rounded-[32px]
              shadow-xl
              border
              border-white
              overflow-hidden
            ">

              <div className="
                px-8
                py-6
                border-b
                border-gray-100
                flex
                items-center
                justify-between
              ">

                <div>

                  <h2 className="text-3xl font-bold text-gray-900">
                    ⚠️ Breached SLA Records
                  </h2>

                  <p className="text-gray-500 mt-2">
                    Records that exceeded SLA timelines
                  </p>

                </div>

                <div className="
                  bg-red-100
                  text-red-700
                  px-4
                  py-2
                  rounded-xl
                  font-bold
                ">
                  {breached.length} Breached
                </div>

              </div>

              <div className="overflow-x-auto">

                <table className="w-full">

                  <thead className="bg-gray-50">

                    <tr>

                      <th className="px-8 py-5 text-left text-sm font-bold text-gray-600 uppercase">
                        ID
                      </th>

                      <th className="px-8 py-5 text-left text-sm font-bold text-gray-600 uppercase">
                        Module
                      </th>

                      <th className="px-8 py-5 text-left text-sm font-bold text-gray-600 uppercase">
                        Record ID
                      </th>

                      <th className="px-8 py-5 text-left text-sm font-bold text-gray-600 uppercase">
                        Due Time
                      </th>

                      <th className="px-8 py-5 text-left text-sm font-bold text-gray-600 uppercase">
                        Reason
                      </th>

                    </tr>

                  </thead>

                  <tbody>

                    {breached.map((item) => (

                      <tr
                        key={item.id}
                        className="
                          border-t
                          hover:bg-red-50
                          transition-all
                        "
                      >

                        <td className="px-8 py-6 font-bold">
                          #{item.id}
                        </td>

                        <td className="px-8 py-6 font-semibold text-gray-800">
                          {item.module_name}
                        </td>

                        <td className="px-8 py-6 text-gray-600">
                          {item.record_id}
                        </td>

                        <td className="px-8 py-6 text-gray-600">
                          {new Date(item.due_time).toLocaleString()}
                        </td>

                        <td className="px-8 py-6">

                          <span className="
                            bg-red-100
                            text-red-600
                            px-4
                            py-2
                            rounded-xl
                            text-sm
                            font-bold
                          ">
                            {item.breach_reason || "Breached"}
                          </span>

                        </td>

                      </tr>

                    ))}

                  </tbody>

                </table>

              </div>

            </div>

          </>
        )}

      </div>

    </div>
  );
}