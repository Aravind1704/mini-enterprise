import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, Legend,
  PieChart, Pie, Cell, ResponsiveContainer
} from "recharts";
import api from "../api/axios";

const COLORS = ["#f59e0b", "#3b82f6", "#8b5cf6", "#10b981"];

export default function DashboardStats() {
  const [summary, setSummary] = useState(null);
  const [distribution, setDistribution] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      api.get("/dashboard/summary"),
      api.get("/dashboard/task-distribution"),
    ])
      .then(([s, d]) => {
        setSummary(s.data);
        setDistribution(d.data);
      })
      .catch((err) => {
        setError("Failed to load dashboard data");
        console.error(err);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={styles.loading}>Loading Dashboard...</div>;

  if (error) return <div style={styles.error}>{error}</div>;

  if (!summary) return <div style={styles.error}>No data available</div>;

  const statCards = [
    { label: "Total Tasks", value: summary.total_tasks, color: "#4f46e5", icon: "📋" },
    { label: "Todo", value: summary.todo, color: "#f59e0b", icon: "📌" },
    { label: "In Progress", value: summary.in_progress, color: "#3b82f6", icon: "🔵" },
    { label: "In Review", value: summary.review, color: "#8b5cf6", icon: "🟣" },
    { label: "Completed", value: summary.done, color: "#10b981", icon: "✅" },
    { label: "Pending Approvals", value: summary.pending_approvals, color: "#ef4444", icon: "⏳" },
  ];

  return (
    <div style={styles.container}>
      {/* Header */}
      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>📊 Dashboard Analytics</h1>
          <p style={styles.subtitle}>Overview of all tasks and approvals</p>
        </div>
        <div style={{ display: "flex", gap: "10px" }}>
          <Link to="/kanban" style={styles.navBtn}>⚡ Kanban</Link>
          <Link to="/approvals" style={styles.navBtn}>✅ Approvals</Link>
          <Link to="/dashboard" style={styles.backBtn}>← Tasks</Link>
        </div>
      </div>

      {/* Stat Cards */}
      <div style={styles.grid}>
        {statCards.map((s, i) => (
          <div key={i} style={{ ...styles.statCard, borderTop: `4px solid ${s.color}` }}>
            <div style={styles.statIcon}>{s.icon}</div>
            <div style={{ ...styles.statValue, color: s.color }}>{s.value ?? 0}</div>
            <div style={styles.statLabel}>{s.label}</div>
          </div>
        ))}
      </div>

      {/* Charts */}
      <div style={styles.charts}>
        {/* Bar Chart */}
        <div style={styles.chartCard}>
          <h3 style={styles.chartTitle}>📊 Tasks by Status</h3>
          {distribution.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={distribution}>
                <XAxis dataKey="status" tick={{ fontSize: 12 }} />
                <YAxis allowDecimals={false} tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="count" fill="#4f46e5" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div style={styles.noData}>No data available</div>
          )}
        </div>

        {/* Pie Chart */}
        <div style={styles.chartCard}>
          <h3 style={styles.chartTitle}>🍩 Task Distribution</h3>
          {distribution.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie
                  data={distribution}
                  dataKey="count"
                  nameKey="status"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label
                >
                  {distribution.map((_, index) => (
                    <Cell key={index} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div style={styles.noData}>No data available</div>
          )}
        </div>
      </div>

      {/* Quick Links */}
      <div style={styles.quickLinks}>
        <h3 style={styles.chartTitle}>⚡ Quick Actions</h3>
        <div style={styles.linkGrid}>
          <Link to="/kanban" style={styles.linkCard}>
            <span style={styles.linkIcon}>⚡</span>
            <span>Kanban Board</span>
          </Link>
          <Link to="/approvals" style={styles.linkCard}>
            <span style={styles.linkIcon}>✅</span>
            <span>Approvals</span>
          </Link>
          <Link to="/tasks/create" style={styles.linkCard}>
            <span style={styles.linkIcon}>➕</span>
            <span>Create Task</span>
          </Link>
          <Link to="/dashboard" style={styles.linkCard}>
            <span style={styles.linkIcon}>📋</span>
            <span>All Tasks</span>
          </Link>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: { minHeight: "100vh", background: "#f0f2f5", padding: "24px", fontFamily: "sans-serif" },
  header: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "28px" },
  title: { margin: "0 0 4px", fontSize: "24px", fontWeight: "700", color: "#1a1a2e" },
  subtitle: { margin: 0, color: "#888", fontSize: "13px" },
  navBtn: { background: "#eef2ff", color: "#4f46e5", padding: "8px 16px", borderRadius: "8px", textDecoration: "none", fontSize: "13px", fontWeight: "600" },
  backBtn: { background: "#fff", color: "#4f46e5", padding: "8px 16px", borderRadius: "8px", textDecoration: "none", fontSize: "13px", fontWeight: "600" },
  loading: { textAlign: "center", padding: "80px", color: "#888", fontSize: "16px" },
  error: { textAlign: "center", padding: "80px", color: "#c0392b", fontSize: "16px", background: "#fff", borderRadius: "12px" },
  grid: { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(160px, 1fr))", gap: "16px", marginBottom: "28px" },
  statCard: { background: "#fff", borderRadius: "12px", padding: "20px", textAlign: "center", boxShadow: "0 2px 12px rgba(0,0,0,0.07)" },
  statIcon: { fontSize: "24px", marginBottom: "8px" },
  statValue: { fontSize: "32px", fontWeight: "800", marginBottom: "4px" },
  statLabel: { fontSize: "12px", color: "#888", fontWeight: "600" },
  charts: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px", marginBottom: "28px" },
  chartCard: { background: "#fff", borderRadius: "12px", padding: "24px", boxShadow: "0 2px 12px rgba(0,0,0,0.07)" },
  chartTitle: { margin: "0 0 20px", fontSize: "15px", fontWeight: "700", color: "#1a1a2e" },
  noData: { textAlign: "center", color: "#aaa", padding: "40px" },
  quickLinks: { background: "#fff", borderRadius: "12px", padding: "24px", boxShadow: "0 2px 12px rgba(0,0,0,0.07)" },
  linkGrid: { display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "12px", marginTop: "4px" },
  linkCard: { background: "#f8f9fa", borderRadius: "10px", padding: "20px", textAlign: "center", textDecoration: "none", color: "#1a1a2e", fontWeight: "600", fontSize: "13px", display: "flex", flexDirection: "column", gap: "8px", alignItems: "center" },
  linkIcon: { fontSize: "24px" },
};