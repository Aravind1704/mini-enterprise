import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import api from "../api/axios";

export default function DocumentManager() {
  const { user } = useAuth();
  const [documents, setDocuments] = useState([]);
  const [taskId, setTaskId] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a file");
      return;
    }

    setLoading(true);
    setError("");
    setSuccess("");

    const formData = new FormData();
    formData.append("file", file);
    if (taskId) formData.append("task_id", taskId);

    try {
      await api.post("/documents/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setSuccess("✅ Document uploaded successfully!");
      setFile(null);
      setTaskId("");
      fetchDocuments();
    } catch (err) {
      setError(err.response?.data?.detail || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  const fetchDocuments = async () => {
    if (!taskId) return;
    try {
      const res = await api.get(`/documents/task/${taskId}`);
      setDocuments(res.data || []);
    } catch (err) {
      setDocuments([]);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, [taskId]);

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>📄 Document Manager</h1>
        <Link to="/dashboard" style={styles.backBtn}>← Dashboard</Link>
      </div>

      {error && <div style={styles.error}>{error}</div>}
      {success && <div style={styles.success}>{success}</div>}

      {/* Upload Form */}
      <div style={styles.card}>
        <h2 style={styles.cardTitle}>📤 Upload Document</h2>
        <form onSubmit={handleUpload} style={styles.form}>
          <div style={styles.field}>
            <label style={styles.label}>Select File *</label>
            <input
              type="file"
              onChange={handleFileChange}
              style={styles.fileInput}
              required
            />
          </div>

          <div style={styles.field}>
            <label style={styles.label}>Task ID (Optional)</label>
            <input
              type="number"
              placeholder="Enter task ID"
              value={taskId}
              onChange={(e) => setTaskId(e.target.value)}
              style={styles.input}
            />
          </div>

          <button style={styles.submitBtn} type="submit" disabled={loading}>
            {loading ? "Uploading..." : "Upload File"}
          </button>
        </form>
      </div>

      {/* Documents List */}
      {taskId && (
        <div style={styles.card}>
          <h2 style={styles.cardTitle}>📋 Task #{taskId} Documents</h2>
          {documents.length === 0 ? (
            <p style={styles.empty}>No documents uploaded yet.</p>
          ) : (
            <div style={styles.docList}>
              {documents.map((doc) => (
                <div key={doc.id} style={styles.docItem}>
                  <div>
                    <p style={styles.docName}>📎 {doc.file_name}</p>
                    <p style={styles.docMeta}>
                      v{doc.version} • {new Date(doc.created_at).toLocaleDateString()}
                    </p>
                  </div>
                  <a
                    href={`/downloads/${doc.id}`}
                    style={styles.downloadBtn}
                    download
                  >
                    ⬇️ Download
                  </a>
                </div>
              ))}
            </div>
          )}
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
  error: { background: "#fff0f0", border: "1px solid #ffcccc", color: "#cc0000", padding: "12px", borderRadius: "8px", marginBottom: "16px" },
  success: { background: "#d4edda", border: "1px solid #c3e6cb", color: "#155724", padding: "12px", borderRadius: "8px", marginBottom: "16px" },
  card: { background: "#fff", padding: "24px", borderRadius: "12px", boxShadow: "0 2px 12px rgba(0,0,0,0.07)", marginBottom: "20px" },
  cardTitle: { margin: "0 0 16px", fontSize: "16px", fontWeight: "700", color: "#1a1a2e" },
  form: { maxWidth: "400px" },
  field: { marginBottom: "16px" },
  label: { display: "block", marginBottom: "6px", fontSize: "13px", fontWeight: "600", color: "#333" },
  input: { width: "100%", padding: "10px", border: "1px solid #ddd", borderRadius: "8px", fontSize: "14px", boxSizing: "border-box" },
  fileInput: { width: "100%", padding: "10px", border: "1px solid #ddd", borderRadius: "8px", fontSize: "14px", boxSizing: "border-box" },
  submitBtn: { width: "100%", padding: "10px", background: "#4f46e5", color: "#fff", border: "none", borderRadius: "8px", fontSize: "14px", fontWeight: "600", cursor: "pointer" },
  empty: { color: "#aaa", textAlign: "center", padding: "24px" },
  docList: { display: "flex", flexDirection: "column", gap: "12px" },
  docItem: { display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px", background: "#f8f9fa", borderRadius: "8px" },
  docName: { margin: "0 0 4px", fontSize: "14px", fontWeight: "600", color: "#1a1a2e" },
  docMeta: { margin: 0, fontSize: "12px", color: "#888" },
  downloadBtn: { background: "#eef2ff", color: "#4f46e5", padding: "6px 12px", borderRadius: "6px", textDecoration: "none", fontSize: "12px", fontWeight: "600" },
};