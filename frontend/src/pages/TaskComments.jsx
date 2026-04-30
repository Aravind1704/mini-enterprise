import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import api from "../api/axios";

export default function TaskComments() {
  const { id } = useParams();
  const { user } = useAuth();
  const [comments, setComments] = useState([]);
  const [form, setForm] = useState({ content: "", is_internal: false });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchComments = () => {
    api.get(`/tasks/${id}/comments`)
      .then((res) => setComments(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchComments(); }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.content.trim()) return;
    try {
      await api.post(`/tasks/${id}/comments`, form);
      setForm({ content: "", is_internal: false });
      fetchComments();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to add comment");
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        {/* Header */}
        <div style={styles.header}>
          <Link to="/dashboard" style={styles.back}>← Back</Link>
          <h2 style={styles.title}>💬 Task #{id} — Comments</h2>
        </div>

        {error && <div style={styles.error}>{error}</div>}

        {/* Add Comment Form */}
        <form onSubmit={handleSubmit} style={styles.form}>
          <textarea
            style={styles.textarea}
            placeholder="Write a comment..."
            value={form.content}
            onChange={(e) => setForm({ ...form, content: e.target.value })}
            rows={3}
            required
          />
          {(user?.role === "admin" || user?.role === "manager") && (
            <label style={styles.checkLabel}>
              <input
                type="checkbox"
                checked={form.is_internal}
                onChange={(e) => setForm({ ...form, is_internal: e.target.checked })}
              />
              &nbsp; Internal note (hidden from employees)
            </label>
          )}
          <button style={styles.submitBtn} type="submit">
            Post Comment
          </button>
        </form>

        <hr style={styles.divider} />

        {/* Comments List */}
        {loading ? (
          <div style={styles.loading}>Loading comments...</div>
        ) : comments.length === 0 ? (
          <div style={styles.empty}>No comments yet. Be the first to comment!</div>
        ) : (
          <div style={styles.commentList}>
            {comments.map((c) => (
              <div
                key={c.id}
                style={{
                  ...styles.comment,
                  background: c.is_internal ? "#fffbeb" : "#f8f9fa",
                  borderLeft: c.is_internal ? "4px solid #f59e0b" : "4px solid #4f46e5",
                }}
              >
                <div style={styles.commentHeader}>
                  <div style={styles.avatar}>
                    {c.user_id === user?.id ? "👤 You" : `👤 User #${c.user_id}`}
                  </div>
                  <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
                    {c.is_internal && (
                      <span style={styles.internalBadge}>🔒 Internal</span>
                    )}
                    <span style={styles.timestamp}>
                      {new Date(c.created_at).toLocaleString()}
                    </span>
                  </div>
                </div>
                <p style={styles.commentText}>{c.content}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: { minHeight: "100vh", background: "#f0f2f5", display: "flex", justifyContent: "center", padding: "32px 16px", fontFamily: "sans-serif" },
  card: { background: "#fff", borderRadius: "12px", padding: "32px", width: "100%", maxWidth: "680px", boxShadow: "0 4px 24px rgba(0,0,0,0.08)" },
  header: { marginBottom: "24px" },
  back: { color: "#4f46e5", textDecoration: "none", fontSize: "13px", fontWeight: "600" },
  title: { margin: "8px 0 0", fontSize: "20px", fontWeight: "700", color: "#1a1a2e" },
  error: { background: "#fff0f0", border: "1px solid #ffcccc", color: "#cc0000", padding: "10px 14px", borderRadius: "8px", marginBottom: "16px", fontSize: "14px" },
  form: { marginBottom: "24px" },
  textarea: { width: "100%", padding: "12px", border: "1px solid #ddd", borderRadius: "8px", fontSize: "14px", boxSizing: "border-box", fontFamily: "sans-serif", resize: "vertical" },
  checkLabel: { display: "flex", alignItems: "center", fontSize: "13px", color: "#555", margin: "10px 0" },
  submitBtn: { background: "#4f46e5", color: "#fff", border: "none", padding: "10px 24px", borderRadius: "8px", cursor: "pointer", fontSize: "14px", fontWeight: "600", marginTop: "8px" },
  divider: { border: "none", borderTop: "1px solid #eee", margin: "0 0 24px" },
  loading: { textAlign: "center", color: "#888", padding: "40px" },
  empty: { textAlign: "center", color: "#aaa", padding: "40px", fontSize: "14px" },
  commentList: { display: "flex", flexDirection: "column", gap: "14px" },
  comment: { padding: "14px 16px", borderRadius: "8px" },
  commentHeader: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" },
  avatar: { fontSize: "13px", fontWeight: "600", color: "#4f46e5" },
  internalBadge: { background: "#fff3cd", color: "#856404", padding: "2px 8px", borderRadius: "20px", fontSize: "11px", fontWeight: "700" },
  timestamp: { fontSize: "11px", color: "#aaa" },
  commentText: { margin: 0, fontSize: "14px", color: "#333", lineHeight: "1.6" },
};