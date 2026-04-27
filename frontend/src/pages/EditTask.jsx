import { useState, useEffect } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import api from "../api/axios";

export default function EditTask() {
  const { id } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({ title: "", description: "", status: "todo", priority: "medium", due_date: "", assigned_to_id: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(true);

  useEffect(() => {
    // Fetch task details
    api.get(`/tasks/${id}`)
      .then((res) => {
        const t = res.data;
        setForm({
          title: t.title || "",
          description: t.description || "",
          status: t.status || "todo",
          priority: t.priority || "medium",
          due_date: t.due_date ? t.due_date.slice(0, 16) : "",
          assigned_to_id: t.assigned_to_id || "",
        });
      })
      .catch(() => setError("Failed to load task"))
      .finally(() => setFetching(false));

    // Fetch users for assign dropdown (admin/manager only)
    if (user?.role !== "employee") {
      api.get("/users/").then((res) => setUsers(res.data)).catch(() => {});
    }
  }, [id, user]);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const payload = {
        ...form,
        due_date: form.due_date ? new Date(form.due_date).toISOString() : null,
        assigned_to_id: form.assigned_to_id ? parseInt(form.assigned_to_id) : null,
      };
      // Employee can only update status
      if (user?.role === "employee") {
        await api.put(`/tasks/${id}`, { status: form.status });
      } else {
        await api.put(`/tasks/${id}`, payload);
      }
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to update task");
    } finally {
      setLoading(false);
    }
  };

  if (fetching) return <div style={{ textAlign: "center", padding: "60px", color: "#888" }}>Loading task...</div>;

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.header}>
          <Link to="/dashboard" style={styles.back}>← Back</Link>
          <h2 style={styles.title}>Edit Task #{id}</h2>
        </div>

        {error && <div style={styles.error}>{error}</div>}

        <form onSubmit={handleSubmit}>
          {/* Employees only see status */}
          {user?.role === "employee" ? (
            <div style={styles.field}>
              <label style={styles.label}>Status</label>
              <select style={styles.input} name="status" value={form.status} onChange={handleChange}>
                <option value="todo">To Do</option>
                <option value="in_progress">In Progress</option>
                <option value="done">Done</option>
              </select>
            </div>
          ) : (
            <>
              <div style={styles.field}>
                <label style={styles.label}>Title *</label>
                <input style={styles.input} type="text" name="title" value={form.title} onChange={handleChange} required />
              </div>

              <div style={styles.field}>
                <label style={styles.label}>Description</label>
                <textarea style={{ ...styles.input, height: "90px", resize: "vertical" }} name="description" value={form.description} onChange={handleChange} />
              </div>

              <div style={styles.row}>
                <div style={{ ...styles.field, flex: 1 }}>
                  <label style={styles.label}>Status</label>
                  <select style={styles.input} name="status" value={form.status} onChange={handleChange}>
                    <option value="todo">To Do</option>
                    <option value="in_progress">In Progress</option>
                    <option value="done">Done</option>
                  </select>
                </div>

                <div style={{ ...styles.field, flex: 1 }}>
                  <label style={styles.label}>Priority</label>
                  <select style={styles.input} name="priority" value={form.priority} onChange={handleChange}>
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
              </div>

              <div style={styles.field}>
                <label style={styles.label}>Due Date</label>
                <input style={styles.input} type="datetime-local" name="due_date" value={form.due_date} onChange={handleChange} />
              </div>

              <div style={styles.field}>
                <label style={styles.label}>Assign To</label>
                <select style={styles.input} name="assigned_to_id" value={form.assigned_to_id} onChange={handleChange}>
                  <option value="">-- Select User --</option>
                  {users.map((u) => (
                    <option key={u.id} value={u.id}>{u.name} ({u.role})</option>
                  ))}
                </select>
              </div>
            </>
          )}

          <button style={styles.button} type="submit" disabled={loading}>
            {loading ? "Saving..." : "Save Changes"}
          </button>
        </form>
      </div>
    </div>
  );
}

const styles = {
  container: { minHeight: "100vh", background: "#f0f2f5", display: "flex", alignItems: "center", justifyContent: "center", padding: "24px" },
  card: { background: "#fff", padding: "40px", borderRadius: "12px", boxShadow: "0 4px 24px rgba(0,0,0,0.1)", width: "100%", maxWidth: "560px" },
  header: { marginBottom: "24px" },
  back: { color: "#4f46e5", textDecoration: "none", fontSize: "13px", fontWeight: "600" },
  title: { margin: "8px 0 0", fontSize: "22px", fontWeight: "700", color: "#1a1a2e" },
  error: { background: "#fff0f0", border: "1px solid #ffcccc", color: "#cc0000", padding: "10px 14px", borderRadius: "8px", marginBottom: "16px", fontSize: "14px" },
  field: { marginBottom: "16px" },
  label: { display: "block", marginBottom: "6px", fontSize: "13px", fontWeight: "600", color: "#333" },
  input: { width: "100%", padding: "10px 14px", border: "1px solid #ddd", borderRadius: "8px", fontSize: "14px", boxSizing: "border-box", outline: "none", fontFamily: "sans-serif" },
  row: { display: "flex", gap: "16px" },
  button: { width: "100%", padding: "12px", background: "#4f46e5", color: "#fff", border: "none", borderRadius: "8px", fontSize: "15px", fontWeight: "600", cursor: "pointer", marginTop: "8px" },
};