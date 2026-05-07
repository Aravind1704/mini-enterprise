import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

export default function NotificationCenter() {
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(true);

  const fetchNotifications = () => {
    api.get("/notifications/")
      .then((res) => {
        setNotifications(res.data || []);
        const unread = res.data.filter((n) => !n.is_read).length;
        setUnreadCount(unread);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchNotifications();
    const interval = setInterval(fetchNotifications, 10000); // Refresh every 10s
    return () => clearInterval(interval);
  }, []);

  const handleMarkRead = async (id) => {
    await api.patch(`/notifications/${id}/read`);
    fetchNotifications();
  };

  const getIcon = (type) => {
    switch (type) {
      case "task_assigned":
        return "📋";
      case "comment_added":
        return "💬";
      case "approval_requested":
        return "✅";
      default:
        return "🔔";
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>🔔 Notifications</h1>
          {unreadCount > 0 && (
            <p style={styles.unreadBadge}>{unreadCount} unread</p>
          )}
        </div>
        <Link to="/dashboard" style={styles.backBtn}>← Dashboard</Link>
      </div>

      {loading ? (
        <div style={styles.loading}>Loading notifications...</div>
      ) : notifications.length === 0 ? (
        <div style={styles.empty}>No notifications yet. You're all caught up! ✨</div>
      ) : (
        <div style={styles.list}>
          {notifications.map((notif) => (
            <div
              key={notif.id}
              style={{
                ...styles.item,
                background: notif.is_read ? "#f8f9fa" : "#fffbf0",
                borderLeft: notif.is_read ? "4px solid #ddd" : "4px solid #f59e0b",
              }}
            >
              <div style={styles.itemContent}>
                <p style={styles.icon}>{getIcon(notif.action_type)}</p>
                <div style={{ flex: 1 }}>
                  <p style={styles.message}>{notif.message}</p>
                  <p style={styles.timestamp}>
                    {new Date(notif.created_at).toLocaleString()}
                  </p>
                </div>
              </div>

              {!notif.is_read && (
                <button
                  onClick={() => handleMarkRead(notif.id)}
                  style={styles.markBtn}
                >
                  Mark as read
                </button>
              )}
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
  unreadBadge: { fontSize: "13px", color: "#f59e0b", fontWeight: "600", margin: "4px 0 0" },
  backBtn: { background: "#fff", color: "#4f46e5", padding: "8px 16px", borderRadius: "8px", textDecoration: "none", fontSize: "13px", fontWeight: "600" },
  loading: { textAlign: "center", padding: "60px", color: "#888" },
  empty: { textAlign: "center", padding: "60px", color: "#aaa" },
  list: { display: "flex", flexDirection: "column", gap: "12px" },
  item: { background: "#fff", padding: "16px", borderRadius: "12px", boxShadow: "0 2px 8px rgba(0,0,0,0.05)" },
  itemContent: { display: "flex", gap: "12px", alignItems: "flex-start" },
  icon: { fontSize: "24px", margin: 0 },
  message: { margin: "0 0 4px", fontSize: "14px", fontWeight: "600", color: "#1a1a2e" },
  timestamp: { margin: 0, fontSize: "12px", color: "#aaa" },
  markBtn: { background: "#eef2ff", color: "#4f46e5", border: "none", padding: "6px 12px", borderRadius: "6px", fontSize: "12px", fontWeight: "600", cursor: "pointer" },
};