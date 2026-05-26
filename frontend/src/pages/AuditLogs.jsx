import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

export default function AuditLogs() {

  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  // FETCH LOGS
  const fetchLogs = async () => {

    try {

      const res = await api.get("/audit-logs/");

      setLogs(res.data);

    } catch (err) {

      console.error(err);

    } finally {

      setLoading(false);

    }
  };

  useEffect(() => {

    fetchLogs();

  }, []);

  return (

    <div className="
      min-h-screen
      bg-gradient-to-br
      from-slate-100
      via-blue-50
      to-indigo-100
      p-6
      md:p-10
    ">

      {/* CONTAINER */}
      <div className="
        max-w-7xl
        mx-auto
      ">

        {/* HEADER */}
        <div className="
          bg-white/80
          backdrop-blur-xl
          rounded-3xl
          shadow-xl
          border
          border-white/40
          p-8
          mb-8
        ">

          <div className="
            flex
            flex-col
            lg:flex-row
            lg:items-center
            lg:justify-between
            gap-6
          ">

            {/* LEFT */}
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
                🔍
              </div>

              <div>

                <h1 className="
                  text-4xl
                  md:text-5xl
                  font-bold
                  text-gray-900
                ">
                  Audit Logs
                </h1>

                <p className="
                  text-gray-500
                  mt-3
                  text-lg
                ">
                  Track all activities, actions and user operations
                </p>

              </div>

            </div>

            {/* RIGHT */}
            <Link
              to="/dashboard"
              className="
                bg-indigo-600
                hover:bg-indigo-700
                text-white
                px-6
                py-3
                rounded-2xl
                font-semibold
                shadow-lg
                hover:shadow-xl
                transition-all
                duration-300
                text-center
              "
            >
              ← Dashboard
            </Link>

          </div>

        </div>

        {/* TABLE CARD */}
        <div className="
          bg-white/80
          backdrop-blur-xl
          rounded-[32px]
          shadow-xl
          border
          border-white/40
          overflow-hidden
        ">

          {/* TABLE HEADER */}
          <div className="
            px-8
            py-6
            border-b
            border-gray-100
            bg-gradient-to-r
            from-indigo-50
            to-white
          ">

            <div className="
              flex
              items-center
              justify-between
            ">

              <div>

                <h2 className="
                  text-3xl
                  font-bold
                  text-gray-900
                ">
                  📜 Activity Timeline
                </h2>

                <p className="
                  text-gray-500
                  mt-2
                ">
                  Monitor all audit events happening in the system
                </p>

              </div>

              <div className="
                bg-indigo-100
                text-indigo-700
                px-5
                py-2
                rounded-xl
                font-bold
              ">
                {logs.length} Logs
              </div>

            </div>

          </div>

          {/* TABLE */}
          <div className="overflow-x-auto">

            <table className="w-full">

              <thead className="bg-gray-50">

                <tr>

                  <th className={thStyle}>ID</th>

                  <th className={thStyle}>User</th>

                  <th className={thStyle}>Module</th>

                  <th className={thStyle}>Action</th>

                  <th className={thStyle}>Record</th>

                  <th className={thStyle}>Details</th>

                  <th className={thStyle}>Timestamp</th>

                </tr>

              </thead>

              <tbody>

                {/* LOADING */}
                {loading ? (

                  <tr>

                    <td
                      colSpan="7"
                      className="
                        text-center
                        py-20
                        text-indigo-600
                        font-bold
                        text-xl
                      "
                    >
                      Loading Audit Logs...
                    </td>

                  </tr>

                ) : logs.length === 0 ? (

                  <tr>

                    <td
                      colSpan="7"
                      className="
                        text-center
                        py-20
                        text-gray-500
                        text-lg
                      "
                    >
                      No audit logs found
                    </td>

                  </tr>

                ) : (

                  logs.map((log) => (

                    <tr
                      key={log.id}
                      className="
                        border-t
                        hover:bg-indigo-50
                        transition-all
                        duration-200
                      "
                    >

                      <td className={tdStyle}>
                        #{log.id}
                      </td>

                      <td className={tdStyle}>
                        User #{log.user_id || "-"}
                      </td>

                      <td className={tdStyle}>
                        {log.module_name || "-"}
                      </td>

                      <td className={tdStyle}>

                        <span className="
                          bg-indigo-100
                          text-indigo-700
                          px-4
                          py-2
                          rounded-xl
                          text-sm
                          font-bold
                          uppercase
                        ">
                          {log.action_type || "-"}
                        </span>

                      </td>

                      <td className={tdStyle}>
                        #{log.record_id || "-"}
                      </td>

                      <td className={tdStyle}>
                        {log.details || "-"}
                      </td>

                      <td className={tdStyle}>
                        {
                          log.timestamp
                            ? new Date(log.timestamp).toLocaleString()
                            : "-"
                        }
                      </td>

                    </tr>

                  ))

                )}

              </tbody>

            </table>

          </div>

        </div>

      </div>

    </div>
  );
}

/* TABLE HEADER STYLE */
const thStyle = `
  px-8
  py-5
  text-left
  text-sm
  font-bold
  text-gray-600
  uppercase
`;

/* TABLE DATA STYLE */
const tdStyle = `
  px-8
  py-6
  text-gray-700
  font-medium
`;