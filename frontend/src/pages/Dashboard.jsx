import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import api from "../api/axios";

const STATUS_COLORS = {
  todo: { bg: "#fff3cd", color: "#856404" },
  in_progress: { bg: "#cce5ff", color: "#004085" },
  done: { bg: "#d4edda", color: "#155724" },
};

const PRIORITY_COLORS = {
  low: { bg: "#e2f0d9", color: "#3a7d44" },
  medium: { bg: "#fff3cd", color: "#856404" },
  high: { bg: "#fde8e8", color: "#c0392b" },
};

export default function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/tasks/")
      .then((res) => setTasks(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleLogout = () => { logout(); navigate("/login"); };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this task?")) return;
    await api.delete(`/tasks/${id}`);
    setTasks(tasks.filter((t) => t.id !== id));
  };

  return (
    <div style={styles.container}>
      {/* Navbar */}
      <div style={styles.navbar}>
        <div style={styles.navLeft}>
          <span style={styles.logo}>⚡ TaskManager</span>
          <span style={styles.roleBadge}>{user?.role?.toUpperCase()}</span>
        </div>

        {/* Navigation Links - CENTER */}
        <div style={styles.navCenter}>
          <Link to="/stats" style={styles.navLink}>📊 Analytics</Link>
          <Link to="/kanban" style={styles.navLink}>⚡ Kanban</Link>
          <Link to="/approvals" style={styles.navLink}>✅ Approvals</Link>
        </div>

        <div style={styles.navRight}>
          <span style={styles.userName}>{user?.name}</span>
          {(user?.role === "admin" || user?.role === "manager") && (
            <Link to="/tasks/create" style={styles.createBtn}>+ New Task</Link>
          )}
          <button onClick={handleLogout} style={styles.logoutBtn}>Logout</button>
        </div>
      </div>

      {/* Main Content */}
      <div style={styles.main}>
        <h1 style={styles.pageTitle}>
          {user?.role === "admin" ? "All Tasks" : user?.role === "manager" ? "My Tasks" : "Assigned Tasks"}
        </h1>
        <p style={styles.pageSubtitle}>{tasks.length} task{tasks.length !== 1 ? "s" : ""} found</p>

        {loading ? (
          <div style={styles.loading}>Loading tasks...</div>
        ) : tasks.length === 0 ? (
          <div style={styles.empty}>No tasks found.</div>
        ) : (
          <div style={styles.grid}>
            {tasks.map((task) => (
              <div key={task.id} style={styles.card}>
                <div style={styles.cardHeader}>
                  <span style={{ ...styles.badge, ...PRIORITY_COLORS[task.priority] }}>
                    {task.priority}
                  </span>
                  <span style={{ ...styles.badge, ...STATUS_COLORS[task.status] }}>
                    {task.status.replace("_", " ")}
                  </span>
                </div>

                <h3 style={styles.cardTitle}>{task.title}</h3>
                <p style={styles.cardDesc}>{task.description || "No description"}</p>

                {task.due_date && (
                  <p style={styles.dueDate}>
                    📅 Due: {new Date(task.due_date).toLocaleDateString()}
                  </p>
                )}

                {task.assigned_to_id && (
                  <p style={styles.assignedTo}>👤 Assigned to: User #{task.assigned_to_id}</p>
                )}

                <div style={styles.cardActions}>
                  <Link to={`/tasks/edit/${task.id}`} style={styles.editBtn}>Edit</Link>
                  <Link to={`/tasks/${task.id}/comments`} style={styles.commentBtn}>💬 Comments</Link>
                  {(user?.role === "admin" || user?.role === "manager") && (
                    <button onClick={() => handleDelete(task.id)} style={styles.deleteBtn}>Delete</button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: { minHeight: "100vh", background: "#f0f2f5", fontFamily: "sans-serif" },
  navbar: { background: "#fff", padding: "0 32px", height: "70px", display: "flex", alignItems: "center", justifyContent: "space-between", boxShadow: "0 1px 4px rgba(0,0,0,0.08)" },
  navLeft: { display: "flex", alignItems: "center", gap: "12px" },
  logo: { fontSize: "18px", fontWeight: "700", color: "#4f46e5" },
  roleBadge: { background: "#eef2ff", color: "#4f46e5", padding: "2px 10px", borderRadius: "20px", fontSize: "11px", fontWeight: "700" },
  navCenter: { display: "flex", gap: "24px", flex: 1, justifyContent: "center" },
  navLink: { color: "#555", textDecoration: "none", fontSize: "13px", fontWeight: "600" },
  navRight: { display: "flex", alignItems: "center", gap: "12px" },
  userName: { fontSize: "14px", color: "#555" },
  createBtn: { background: "#4f46e5", color: "#fff", padding: "8px 16px", borderRadius: "8px", textDecoration: "none", fontSize: "13px", fontWeight: "600" },
  logoutBtn: { background: "transparent", border: "1px solid #ddd", padding: "7px 14px", borderRadius: "8px", cursor: "pointer", fontSize: "13px", color: "#555" },
  main: { maxWidth: "1100px", margin: "0 auto", padding: "32px 16px" },
  pageTitle: { fontSize: "26px", fontWeight: "700", color: "#1a1a2e", margin: "0 0 4px" },
  pageSubtitle: { color: "#888", fontSize: "14px", margin: "0 0 24px" },
  loading: { textAlign: "center", color: "#888", padding: "60px" },
  empty: { textAlign: "center", color: "#aaa", padding: "60px", fontSize: "16px" },
  grid: { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: "20px" },
  card: { background: "#fff", borderRadius: "12px", padding: "20px", boxShadow: "0 2px 12px rgba(0,0,0,0.07)" },
  cardHeader: { display: "flex", gap: "8px", marginBottom: "12px" },
  badge: { padding: "3px 10px", borderRadius: "20px", fontSize: "11px", fontWeight: "700", textTransform: "uppercase" },
  cardTitle: { margin: "0 0 8px", fontSize: "16px", fontWeight: "700", color: "#1a1a2e" },
  cardDesc: { margin: "0 0 12px", fontSize: "13px", color: "#666", lineHeight: "1.5" },
  dueDate: { fontSize: "12px", color: "#888", margin: "0 0 4px" },
  assignedTo: { fontSize: "12px", color: "#888", margin: "0 0 16px" },
  cardActions: { display: "flex", gap: "8px", marginTop: "16px", flexWrap: "wrap" },
  editBtn: { background: "#eef2ff", color: "#4f46e5", padding: "7px 16px", borderRadius: "8px", textDecoration: "none", fontSize: "13px", fontWeight: "600" },
  commentBtn: { background: "#f0fdf4", color: "#059669", padding: "7px 16px", borderRadius: "8px", textDecoration: "none", fontSize: "13px", fontWeight: "600" },
  deleteBtn: { background: "#fde8e8", color: "#c0392b", padding: "7px 16px", borderRadius: "8px", border: "none", cursor: "pointer", fontSize: "13px", fontWeight: "600" },
};