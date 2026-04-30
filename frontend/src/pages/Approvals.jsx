import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import api from "../api/axios";

const STATUS_STYLE = {
  pending:  { bg: "#fff3cd", color: "#856404" },
  approved: { bg: "#d4edda", color: "#155724" },
  rejected: { bg: "#fde8e8", color: "#c0392b" },
  hold:     { bg: "#e2e3e5", color: "#383d41" },
};

export default function Approvals() {
  const { user } = useAuth();
  const [approvals, setApprovals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionModal, setActionModal] = useState(null);
  const [comment, setComment] = useState("");
  const [newForm, setNewForm] = useState({ title: "", description: "" });
  const [showForm, setShowForm] = useState(false);
  const [error, setError] = useState("");

  const fetchApprovals = () => {
    api.get("/approvals/")
      .then((res) => setApprovals(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchApprovals(); }, []);

  const handleSubmitApproval = async (e) => {
    e.preventDefault();
    try {
      await api.post("/approvals/", newForm);
      setShowForm(false);
      setNewForm({ title: "", description: "" });
      fetchApprovals();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to submit");
    }
  };

  const handleAction = async () => {
    if (actionModal.action === "rejected" && !comment) {
      setError("Comment is required for rejection");
      return;
    }
    try {
      await api.patch(`/approvals/${actionModal.id}/action`, {
        action: actionModal.action,
        comment,
      });
      setActionModal(null);
      setComment("");
      fetchApprovals();
    } catch (err) {
      setError(err.response?.data?.detail || "Action failed");
    }
  };

  return (
    <div style={styles.container}>
      {/* Header */}
      <div style={styles.header}>
        <div>
          <h1 style={styles.title}> Approvals</h1>
          <p style={styles.subtitle}>Manage approval requests</p>
        </div>
        <div style={{ display: "flex", gap: "10px" }}>
          <button onClick={() => setShowForm(!showForm)} style={styles.newBtn}>
            + New Request
          </button>
          <Link to="/dashboard" style={styles.backBtn}>← Dashboard</Link>
        </div>
      </div>

      {error && (
        <div style={styles.error}>
          {error}
          <button onClick={() => setError("")} style={styles.closeErr}>✕</button>
        </div>
      )}

      {/* New Approval Form */}
      {showForm && (
        <div style={styles.formCard}>
          <h3 style={styles.formTitle}>Submit New Approval Request</h3>
          <form onSubmit={handleSubmitApproval}>
            <div style={styles.field}>
              <label style={styles.label}>Title *</label>
              <input
                style={styles.input}
                placeholder="Approval title"
                value={newForm.title}
                onChange={(e) => setNewForm({ ...newForm, title: e.target.value })}
                required
              />
            </div>
            <div style={styles.field}>
              <label style={styles.label}>Description</label>
              <textarea
                style={{ ...styles.input, height: "80px" }}
                placeholder="Details..."
                value={newForm.description}
                onChange={(e) => setNewForm({ ...newForm, description: e.target.value })}
              />
            </div>
            <button style={styles.submitBtn} type="submit">Submit Request</button>
          </form>
        </div>
      )}

      {/* Approvals List */}
      {loading ? (
        <div style={styles.loading}>Loading...</div>
      ) : approvals.length === 0 ? (
        <div style={styles.empty}>No approvals found.</div>
      ) : (
        <div style={styles.list}>
          {approvals.map((a) => (
            <div key={a.id} style={styles.card}>
              <div style={styles.cardTop}>
                <div>
                  <h3 style={styles.cardTitle}>{a.title}</h3>
                  <p style={styles.cardDesc}>{a.description || "No description"}</p>
                </div>
                <div style={styles.badges}>
                  <span style={{ ...styles.badge, ...STATUS_STYLE[a.status] }}>
                    {a.status}
                  </span>
                  <span style={styles.levelBadge}>
                    Level: {a.current_level}
                  </span>
                </div>
              </div>

              <div style={styles.cardFooter}>
                <span style={styles.meta}>
                  📅 {new Date(a.created_at).toLocaleDateString()} &nbsp;|&nbsp;
                  👤 Requested by: User #{a.requested_by}
                </span>

                {/* Action Buttons for Manager/Admin */}
                {(user?.role === "admin" || user?.role === "manager") &&
                  a.status === "pending" && (
                    <div style={{ display: "flex", gap: "8px" }}>
                      <button
                        onClick={() => setActionModal({ id: a.id, action: "approved" })}
                        style={styles.approveBtn}
                      >
                        ✓ Approve
                      </button>
                      <button
                        onClick={() => setActionModal({ id: a.id, action: "hold" })}
                        style={styles.holdBtn}
                      >
                        ⏸ Hold
                      </button>
                      <button
                        onClick={() => setActionModal({ id: a.id, action: "rejected" })}
                        style={styles.rejectBtn}
                      >
                        ✕ Reject
                      </button>
                    </div>
                  )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Action Modal */}
      {actionModal && (
        <div style={styles.overlay}>
          <div style={styles.modal}>
            <h3 style={styles.modalTitle}>
              {actionModal.action === "approved" ? "✓ Approve" :
               actionModal.action === "rejected" ? "✕ Reject" : "⏸ Hold"} Request
            </h3>
            <div style={styles.field}>
              <label style={styles.label}>
                Comment {actionModal.action === "rejected" ? "(Required)" : "(Optional)"}
              </label>
              <textarea
                style={{ ...styles.input, height: "80px" }}
                placeholder="Add a comment..."
                value={comment}
                onChange={(e) => setComment(e.target.value)}
              />
            </div>
            {error && <p style={{ color: "#c0392b", fontSize: "13px" }}>{error}</p>}
            <div style={{ display: "flex", gap: "10px", marginTop: "16px" }}>
              <button onClick={handleAction} style={styles.submitBtn}>Confirm</button>
              <button
                onClick={() => { setActionModal(null); setComment(""); setError(""); }}
                style={styles.cancelBtn}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: { minHeight: "100vh", background: "#f0f2f5", padding: "24px", fontFamily: "sans-serif" },
  header: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "24px" },
  title: { margin: "0 0 4px", fontSize: "24px", fontWeight: "700", color: "#1a1a2e" },
  subtitle: { margin: 0, color: "#888", fontSize: "13px" },
  newBtn: { background: "#4f46e5", color: "#fff", padding: "8px 16px", borderRadius: "8px", border: "none", cursor: "pointer", fontSize: "13px", fontWeight: "600" },
  backBtn: { background: "#fff", color: "#4f46e5", padding: "8px 16px", borderRadius: "8px", textDecoration: "none", fontSize: "13px", fontWeight: "600" },
  error: { background: "#fff0f0", border: "1px solid #ffcccc", color: "#cc0000", padding: "10px 16px", borderRadius: "8px", marginBottom: "16px", display: "flex", justifyContent: "space-between" },
  closeErr: { background: "none", border: "none", cursor: "pointer", color: "#cc0000" },
  loading: { textAlign: "center", padding: "60px", color: "#888" },
  empty: { textAlign: "center", padding: "60px", color: "#aaa", fontSize: "16px" },
  formCard: { background: "#fff", padding: "24px", borderRadius: "12px", marginBottom: "24px", boxShadow: "0 2px 12px rgba(0,0,0,0.07)" },
  formTitle: { margin: "0 0 16px", fontSize: "16px", fontWeight: "700", color: "#1a1a2e" },
  list: { display: "flex", flexDirection: "column", gap: "16px" },
  card: { background: "#fff", padding: "20px", borderRadius: "12px", boxShadow: "0 2px 12px rgba(0,0,0,0.07)" },
  cardTop: { display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "12px" },
  cardTitle: { margin: "0 0 6px", fontSize: "16px", fontWeight: "700", color: "#1a1a2e" },
  cardDesc: { margin: 0, fontSize: "13px", color: "#666" },
  badges: { display: "flex", flexDirection: "column", gap: "6px", alignItems: "flex-end" },
  badge: { padding: "3px 12px", borderRadius: "20px", fontSize: "12px", fontWeight: "700", textTransform: "uppercase" },
  levelBadge: { background: "#eef2ff", color: "#4f46e5", padding: "3px 10px", borderRadius: "20px", fontSize: "11px", fontWeight: "600" },
  cardFooter: { display: "flex", justifyContent: "space-between", alignItems: "center" },
  meta: { fontSize: "12px", color: "#aaa" },
  approveBtn: { background: "#d4edda", color: "#155724", border: "none", padding: "6px 14px", borderRadius: "8px", cursor: "pointer", fontSize: "13px", fontWeight: "600" },
  holdBtn: { background: "#e2e3e5", color: "#383d41", border: "none", padding: "6px 14px", borderRadius: "8px", cursor: "pointer", fontSize: "13px", fontWeight: "600" },
  rejectBtn: { background: "#fde8e8", color: "#c0392b", border: "none", padding: "6px 14px", borderRadius: "8px", cursor: "pointer", fontSize: "13px", fontWeight: "600" },
  field: { marginBottom: "14px" },
  label: { display: "block", marginBottom: "6px", fontSize: "13px", fontWeight: "600", color: "#333" },
  input: { width: "100%", padding: "10px 14px", border: "1px solid #ddd", borderRadius: "8px", fontSize: "14px", boxSizing: "border-box", fontFamily: "sans-serif" },
  submitBtn: { background: "#4f46e5", color: "#fff", border: "none", padding: "10px 20px", borderRadius: "8px", cursor: "pointer", fontSize: "14px", fontWeight: "600" },
  cancelBtn: { background: "#f0f2f5", color: "#555", border: "none", padding: "10px 20px", borderRadius: "8px", cursor: "pointer", fontSize: "14px" },
  overlay: { position: "fixed", inset: 0, background: "rgba(0,0,0,0.4)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000 },
  modal: { background: "#fff", padding: "32px", borderRadius: "12px", width: "100%", maxWidth: "440px" },
  modalTitle: { margin: "0 0 20px", fontSize: "18px", fontWeight: "700", color: "#1a1a2e" },
};