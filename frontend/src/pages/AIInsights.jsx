import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

export default function AIInsights() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/dashboard/ai-summary")
      .then((res) => setSummary(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading)
    return <div style={styles.loading}>Loading AI insights...</div>;

  if (!summary)
    return <div style={styles.error}>No insights available</div>;

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>🤖 AI Insights</h1>
        <Link to="/dashboard" style={styles.backBtn}>← Dashboard</Link>
      </div>

      {/* AI Summary */}
      <div style={styles.summaryCard}>
        <h2 style={styles.summaryTitle}>📊 System Summary</h2>
        <p style={styles.summaryText}>{summary.summary}</p>
      </div>

      {/* Key Metrics */}
      <div style={styles.grid}>
        <div style={styles.metricCard}>
          <div style={styles.metricIcon}>📋</div>
          <div style={styles.metricValue}>{summary.total_tasks}</div>
          <div style={styles.metricLabel}>Total Tasks</div>
        </div>

        <div style={styles.metricCard}>
          <div style={styles.metricIcon}>🔴</div>
          <div style={styles.metricValue}>{summary.high_priority_tasks}</div>
          <div style={styles.metricLabel}>High Priority</div>
        </div>

        <div style={styles.metricCard}>
          <div style={styles.metricIcon}>⏳</div>
          <div style={styles.metricValue}>{summary.pending_tasks}</div>
          <div style={styles.metricLabel}>Pending</div>
        </div>

        <div style={styles.metricCard}>
          <div style={styles.metricIcon}>⏰</div>
          <div style={styles.metricValue}>{summary.overdue_tasks}</div>
          <div style={styles.metricLabel}>Overdue</div>
        </div>

        <div style={styles.metricCard}>
          <div style={styles.metricIcon}>✅</div>
          <div style={styles.metricValue}>{summary.pending_approvals}</div>
          <div style={styles.metricLabel}>Approvals Pending</div>
        </div>
      </div>

      {/* Recommendations */}
      <div style={styles.card}>
        <h3 style={styles.cardTitle}>💡 AI Recommendations</h3>
        <div style={styles.recommendations}>
          {summary.high_priority_tasks > 0 && (
            <div style={styles.rec}>
              🎯 Focus on {summary.high_priority_tasks} high priority task
              {summary.high_priority_tasks > 1 ? "s" : ""}
            </div>
          )}
          {summary.overdue_tasks > 0 && (
            <div style={styles.rec}>
              🚨 {summary.overdue_tasks} task{summary.overdue_tasks > 1 ? "s" : ""} {summary.overdue_tasks > 1 ? "are" : "is"} overdue
            </div>
          )}
          {summary.pending_approvals > 0 && (
            <div style={styles.rec}>
              ⚡ {summary.pending_approvals} approval{summary.pending_approvals > 1 ? "s" : ""} waiting
            </div>
          )}
          {summary.pending_tasks > 5 && (
            <div style={styles.rec}>
              📌 Consider delegating some of the {summary.pending_tasks} pending tasks
            </div>
          )}
          {summary.high_priority_tasks === 0 &&
            summary.overdue_tasks === 0 &&
            summary.pending_approvals === 0 && (
              <div style={styles.rec}>✨ All systems optimal! Keep up the good work</div>
            )}
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: { minHeight: "100vh", background: "#f0f2f5", padding: "24px", fontFamily: "sans-serif" },
  header: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "24px" },
  title: { fontSize: "24px", fontWeight: "700", color: "#1a1a2e", margin: 0 },
  backBtn: { background: "#fff", color: "#4f46e5", padding: "8px 16px", borderRadius: "8px", textDecoration: "none", fontSize: "13px", fontWeight: "600" },
  loading: { textAlign: "center", padding: "80px", color: "#888", fontSize: "16px" },
  error: { textAlign: "center", padding: "80px", color: "#c0392b", fontSize: "16px" },
  summaryCard: { background: "#fff", padding: "24px", borderRadius: "12px", marginBottom: "24px", boxShadow: "0 2px 12px rgba(0,0,0,0.07)", borderLeft: "4px solid #4f46e5" },
  summaryTitle: { margin: "0 0 12px", fontSize: "16px", fontWeight: "700", color: "#1a1a2e" },
  summaryText: { margin: 0, fontSize: "16px", color: "#555", lineHeight: "1.6" },
  grid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))", gap: "16px", marginBottom: "24px" },
  metricCard: { background: "#fff", padding: "20px", borderRadius: "12px", textAlign: "center", boxShadow: "0 2px 12px rgba(0,0,0,0.07)" },
  metricIcon: { fontSize: "28px", marginBottom: "8px" },
  metricValue: { fontSize: "28px", fontWeight: "700", color: "#4f46e5", margin: "0 0 4px" },
  metricLabel: { fontSize: "12px", color: "#888", margin: 0 },
  card: { background: "#fff", padding: "24px", borderRadius: "12px", boxShadow: "0 2px 12px rgba(0,0,0,0.07)" },
  cardTitle: { margin: "0 0 16px", fontSize: "16px", fontWeight: "700", color: "#1a1a2e" },
  recommendations: { display: "flex", flexDirection: "column", gap: "12px" },
  rec: { padding: "12px 16px", background: "#f8f9fa", borderRadius: "8px", fontSize: "14px", color: "#555", borderLeft: "3px solid #4f46e5" },
};