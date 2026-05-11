import { useEffect, useState } from "react";

import { Link } from "react-router-dom";

import api from "../api/axios";

export default function AuditLogs() {

  const [logs, setLogs] = useState([]);

  const [loading, setLoading] = useState(true);


  const fetchLogs = async () => {

    try {

      const res = await api.get(
        "/audit-logs/"
      );

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

    <div style={styles.container}>

      {/* HEADER */}

      <div style={styles.header}>

        <div>

          <h1 style={styles.title}>
            🔍 Audit Logs
          </h1>

          <p style={styles.subtitle}>
            Track all task activities with user, action and timestamp
          </p>

        </div>


        <Link
          to="/dashboard"
          style={styles.backBtn}
        >
          ← Dashboard
        </Link>

      </div>


      {/* TABLE */}

      <div style={styles.tableWrapper}>

        <table style={styles.table}>

          <thead>

            <tr>

              <th style={styles.th}>ID</th>

              <th style={styles.th}>User</th>

              <th style={styles.th}>Action</th>

              <th style={styles.th}>Entity Type</th>

              <th style={styles.th}>Entity ID</th>

              <th style={styles.th}>Details</th>

              <th style={styles.th}>Created At</th>

            </tr>

          </thead>


          <tbody>

            {
              loading ? (

                <tr>

                  <td
                    colSpan="7"
                    style={styles.empty}
                  >
                    Loading...
                  </td>

                </tr>

              ) : logs.length === 0 ? (

                <tr>

                  <td
                    colSpan="7"
                    style={styles.empty}
                  >
                    No audit logs found
                  </td>

                </tr>

              ) : (

                logs.map((log) => (

                  <tr
                    key={log.id}
                    style={styles.row}
                  >

                    <td style={styles.td}>
                      {log.id}
                    </td>

                    <td style={styles.td}>
                      User #{log.user_id}
                    </td>

                    <td style={styles.td}>

                      <span style={styles.badge}>
                        {log.action}
                      </span>

                    </td>

                    <td style={styles.td}>
                      {log.entity || log.entity_type}
                    </td>

                    <td style={styles.td}>
                      #{log.entity_id}
                    </td>

                    <td style={styles.td}>
                      {log.details}
                    </td>

                    <td style={styles.td}>

                      {
                        new Date(
                          log.timestamp || log.created_at
                        ).toLocaleString()
                      }

                    </td>

                  </tr>

                ))

              )
            }

          </tbody>

        </table>

      </div>

    </div>
  );
}



const styles = {

  container: {
    padding: "30px",
    background: "#f4f7fb",
    minHeight: "100vh"
  },

  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "25px"
  },

  title: {
    fontSize: "40px",
    fontWeight: "bold",
    color: "#111827",
    marginBottom: "10px"
  },

  subtitle: {
    color: "#6b7280",
    fontSize: "16px"
  },

  backBtn: {
    background: "#4f46e5",
    color: "#fff",
    textDecoration: "none",
    padding: "12px 22px",
    borderRadius: "10px",
    fontWeight: "bold",
    transition: "0.2s"
  },

  tableWrapper: {
    background: "#fff",
    borderRadius: "16px",
    overflow: "hidden",
    boxShadow: "0 4px 15px rgba(0,0,0,0.08)"
  },

  table: {
    width: "100%",
    borderCollapse: "collapse"
  },

  th: {
    background: "#eef2ff",
    padding: "18px",
    textAlign: "left",
    color: "#111827",
    fontWeight: "bold",
    fontSize: "15px"
  },

  td: {
    padding: "18px",
    borderBottom: "1px solid #f1f1f1",
    color: "#374151",
    fontSize: "15px"
  },

  row: {
    transition: "0.2s"
  },

  badge: {
    background: "#4f46e5",
    color: "#fff",
    padding: "6px 14px",
    borderRadius: "20px",
    fontSize: "12px",
    fontWeight: "bold",
    textTransform: "uppercase"
  },

  empty: {
    textAlign: "center",
    padding: "30px",
    color: "#6b7280",
    fontSize: "16px"
  }

};