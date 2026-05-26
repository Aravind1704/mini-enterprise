import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/axios";

export default function NotificationPreferences() {
  const navigate = useNavigate();

  const [prefs, setPrefs] = useState({
    in_app_enabled: true,
    email_enabled: true,
    task_notifications: true,
    approval_notifications: true,
    escalation_notifications: true,
    document_notifications: true,
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  // ✅ FETCH PREFERENCES
  const fetchPrefs = async () => {
    try {
      const res = await API.get("/notification-preferences/me");
      setPrefs(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPrefs();
  }, []);

  // ✅ HANDLE CHANGE
  const handleChange = (key) => {
    setPrefs({
      ...prefs,
      [key]: !prefs[key],
    });
  };

  // ✅ SAVE
  const handleSave = async () => {
    try {
      setSaving(true);

      await API.put("/notification-preferences/me", {
        in_app_enabled: prefs.in_app_enabled,
        email_enabled: prefs.email_enabled,
        task_notifications: prefs.task_notifications,
        approval_notifications: prefs.approval_notifications,
        escalation_notifications: prefs.escalation_notifications,
        document_notifications: prefs.document_notifications,
      });

      setMessage("Preferences updated successfully ✅");

      setTimeout(() => {
        setMessage("");
      }, 3000);

    } catch (err) {
      console.error(err);
      setMessage("Failed to update preferences ❌");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div style={{ padding: "40px", textAlign: "center" }}>
        Loading...
      </div>
    );
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#f4f6f9",
        padding: "30px",
      }}
    >
      {/* ✅ HEADER */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "30px",
          flexWrap: "wrap",
          gap: "15px",
        }}
      >
        <div>
          <h1
            style={{
              margin: 0,
              fontSize: "32px",
              fontWeight: "700",
              color: "#111827",
            }}
          >
            🔔 Notification Preferences
          </h1>

          <p
            style={{
              marginTop: "8px",
              color: "#6b7280",
              fontSize: "15px",
            }}
          >
            Manage your notification settings and alerts
          </p>
        </div>

        {/* ✅ BACK BUTTON RIGHT SIDE */}
        <button
          onClick={() => navigate(-1)}
          style={{
            background: "#111827",
            color: "#fff",
            border: "none",
            padding: "12px 20px",
            borderRadius: "8px",
            fontWeight: "600",
            cursor: "pointer",
            fontSize: "14px",
          }}
        >
          ← Back
        </button>
      </div>

      {/* ✅ CARD */}
      <div
        style={{
          maxWidth: "700px",
          background: "#fff",
          padding: "30px",
          borderRadius: "16px",
          boxShadow: "0 4px 16px rgba(0,0,0,0.08)",
        }}
      >
        {/* MESSAGE */}
        {message && (
          <div
            style={{
              marginBottom: "20px",
              padding: "12px",
              borderRadius: "8px",
              background: "#ecfdf5",
              color: "#065f46",
              fontWeight: "600",
            }}
          >
            {message}
          </div>
        )}

        {/* ✅ SWITCH ROW */}
        {[
          {
            key: "in_app_enabled",
            title: "In-App Notifications",
            desc: "Receive notifications inside the application",
          },
          {
            key: "email_enabled",
            title: "Email Notifications",
            desc: "Receive notifications through email",
          },
          {
            key: "task_notifications",
            title: "Task Notifications",
            desc: "Alerts related to tasks and assignments",
          },
          {
            key: "approval_notifications",
            title: "Approval Notifications",
            desc: "Notifications for approvals and requests",
          },
          {
            key: "escalation_notifications",
            title: "Escalation Notifications",
            desc: "Get notified about escalations",
          },
          {
            key: "document_notifications",
            title: "Document Notifications",
            desc: "Updates related to documents",
          },
        ].map((item) => (
          <div
            key={item.key}
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              padding: "18px 0",
              borderBottom: "1px solid #e5e7eb",
              gap: "20px",
            }}
          >
            <div>
              <h3
                style={{
                  margin: 0,
                  fontSize: "16px",
                  color: "#111827",
                }}
              >
                {item.title}
              </h3>

              <p
                style={{
                  marginTop: "5px",
                  color: "#6b7280",
                  fontSize: "14px",
                }}
              >
                {item.desc}
              </p>
            </div>

            {/* TOGGLE */}
            <label
              style={{
                position: "relative",
                display: "inline-block",
                width: "55px",
                height: "28px",
              }}
            >
              <input
                type="checkbox"
                checked={prefs[item.key]}
                onChange={() => handleChange(item.key)}
                style={{ display: "none" }}
              />

              <span
                style={{
                  position: "absolute",
                  cursor: "pointer",
                  top: 0,
                  left: 0,
                  right: 0,
                  bottom: 0,
                  background: prefs[item.key] ? "#4f46e5" : "#d1d5db",
                  transition: ".3s",
                  borderRadius: "30px",
                }}
              >
                <span
                  style={{
                    position: "absolute",
                    height: "22px",
                    width: "22px",
                    left: prefs[item.key] ? "30px" : "3px",
                    bottom: "3px",
                    backgroundColor: "white",
                    transition: ".3s",
                    borderRadius: "50%",
                  }}
                />
              </span>
            </label>
          </div>
        ))}

        {/* ✅ SAVE BUTTON */}
        <div
          style={{
            marginTop: "30px",
            display: "flex",
            justifyContent: "flex-end",
          }}
        >
          <button
            onClick={handleSave}
            disabled={saving}
            style={{
              background: "#4f46e5",
              color: "#fff",
              border: "none",
              padding: "12px 24px",
              borderRadius: "8px",
              fontWeight: "600",
              cursor: "pointer",
              fontSize: "15px",
            }}
          >
            {saving ? "Saving..." : "Save Preferences"}
          </button>
        </div>
      </div>
    </div>
  );
}