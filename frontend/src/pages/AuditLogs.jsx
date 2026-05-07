import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

export default function AuditLogs() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    api.get("/audit-logs/")
      .then((res) => setLogs(res.data || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const filteredLogs = filter === "all" 
    ? logs 
    : logs.filter((log) => log.action === filter);

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>🔍 Audit Logs</h1>
        <Link to="/dashboard" style={styles.backBtn}>← Dashboard</Link>
      </div>

      {/* Filter */}
      <div style={styles.filterBar}>
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          style={styles.select}
        >
          <option value="all">All Actions</option>
          <option value="created">Created</option>
          <option value="updated">Updated</option>
          <option value="deleted">Deleted</option>
          <option value="uploaded">Uploaded</option>
          <option value="assigned">Assigned</option>
        </select>
        <p style={styles.count}>{filteredLogs.length} entries</p>
      </div>

      {/* Logs Table */}
      {loading ? (
        <div style={styles.loading}>Loading audit logs...</div>
      ) : filteredLogs.length === 0 ? (
        <div style={styles.empty}>No audit logs found.</div>
      ) : (
        <div style={styles.table}>
          <div style={styles.tableHeader}>
            <div style={styles.col1}>Timestamp</div>
            <div style={styles.col2}>User</div>
            <div style={styles.col3}>Action</div>
            <div style={styles.col4}>Entity</div>
            <div style={styles.col5}>Details</div>
          </div>

          {filteredLogs.map((log) => (
            <div key={log.id} style={styles.tableRow}>
              <div style={styles.col1}>
                {new Date(log.timestamp).toLocaleString()}
              </div>
              <div style={styles.col2}>User #{log.user_id}</div>
              <div style={styles.col3}>
                <span style={{
                  ...styles.badge,
                  background: log.action === "created" ? "#d4edda" :
                              log.action === "updated" ? "#cce5ff" :
                              log.action === "deleted" ? "#fde8e8" : "#f0f0f0",
                  color: log.action === "created" ? "#155724" :
                         log.action === "updated" ? "#004085" :
                         log.action === "deleted" ? "#c0392b" : "#555",
                }}>
                  {log.action}
                </span>
              </div>
              <div style={styles.col4}>{log.entity}</div>
              <div style={styles.col5}>{log.details || "—"}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

const styles = {
  container: { minHeight: "100vh", background: "#f0f2f5", padding: "24px", fontFamily: "sans-serif" },
  header: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "24px" },
  title: { fontSize: "24px", fontWeight: "700", color: "#1a1a2e", margin: 0 },
  backBtn: { background: "#fff", color: "#4f46e5", padding: "8px 16px", borderRadius: "8px", textDecoration: "none", fontSize: "13px", fontWeight: "600" },
  filterBar: { background: "#fff", padding: "16px", borderRadius: "12px", marginBottom: "20px", display: "flex", gap: "12px", alignItems: "center" },
  select: { padding: "8px 12px", border: "1px solid #ddd", borderRadius: "8px", fontSize: "13px" },
  count: { fontSize: "13px", color: "#888", margin: 0 },
  loading: { textAlign: "center", padding: "60px", color: "#888" },
  empty: { textAlign: "center", padding: "60px", color: "#aaa" },
  table: { background: "#fff", borderRadius: "12px", overflow: "hidden", boxShadow: "0 2px 12px rgba(0,0,0,0.07)" },
  tableHeader: { display: "grid", gridTemplateColumns: "180px 120px 100px 100px 1fr", padding: "16px", background: "#f8f9fa", fontWeight: "700", fontSize: "13px", color: "#555", borderBottom: "1px solid #eee" },
  tableRow: { display: "grid", gridTemplateColumns: "180px 120px 100px 100px 1fr", padding: "14px 16px", borderBottom: "1px solid #eee", alignItems: "center", fontSize: "13px" },
  col1: { color: "#888" },
  col2: { color: "#555" },
  col3: { color: "#555" },
  col4: { color: "#4f46e5", fontWeight: "600" },
  col5: { color: "#666" },
  badge: { padding: "4px 10px", borderRadius: "20px", fontSize: "11px", fontWeight: "700", textTransform: "uppercase", display: "inline-block" },
};