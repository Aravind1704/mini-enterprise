import { useEffect, useState } from "react";

import { Link } from "react-router-dom";

import api from "../api/axios";

export default function Documents() {

  const [documents, setDocuments] = useState([]);

  const [file, setFile] = useState(null);

  const [taskId, setTaskId] = useState("");

  const [loading, setLoading] = useState(false);


  // ----------------------------
  // FETCH DOCUMENTS
  // ----------------------------

  const fetchDocuments = async () => {

    try {

      const res = await api.get(
        "/documents/"
      );

      setDocuments(res.data);

    } catch (err) {

      console.error(err);

    }
  };


  // ----------------------------
  // LOAD DATA
  // ----------------------------

  useEffect(() => {

    fetchDocuments();

  }, []);


  // ----------------------------
  // UPLOAD DOCUMENT
  // ----------------------------

  const handleUpload = async (e) => {

    e.preventDefault();

    if (!file) {

      alert("Please select file");

      return;
    }

    try {

      setLoading(true);

      const formData = new FormData();

      formData.append("file", file);

      formData.append("task_id", taskId);

      await api.post(
        "/documents/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        }
      );

      alert("Document uploaded successfully");

      setFile(null);

      setTaskId("");

      fetchDocuments();

    } catch (err) {

      console.error(err);

      alert("Upload failed");

    } finally {

      setLoading(false);
    }
  };


  // ----------------------------
  // DOWNLOAD DOCUMENT
  // ----------------------------

  const handleDownload = (id) => {
    window.open(
      `http://127.0.0.1:8000/documents/download/${id}`,
      "_blank"
    );
  };


  // ----------------------------
  // DELETE DOCUMENT
  // ----------------------------

  const handleDelete = async (id) => {

    const confirmDelete = window.confirm(
      "Delete this document?"
    );

    if (!confirmDelete) return;

    try {

      await api.delete(
        `/documents/${id}`
      );

      alert("Document deleted");

      fetchDocuments();

    } catch (err) {

      console.error(err);

      alert("Delete failed");
    }
  };


  // ----------------------------
  // UI
  // ----------------------------

  return (

    <div style={styles.container}>


      {/* HEADER */}

      <div style={styles.header}>

        <div>

          <h1 style={styles.title}>
            📄 Documents
          </h1>

          <p style={styles.subtitle}>
            Upload documents with version control
          </p>

        </div>

        <Link
          to="/dashboard"
          style={styles.backBtn}
        >
          ← Dashboard
        </Link>

      </div>


      {/* UPLOAD BOX */}

      <form
        onSubmit={handleUpload}
        style={styles.uploadBox}
      >

        <h3 style={styles.uploadTitle}>
          Upload New Document
        </h3>

        <input
          type="number"
          placeholder="Task ID"
          value={taskId}
          onChange={(e) =>
            setTaskId(e.target.value)
          }
          style={styles.input}
        />

        <input
          type="file"
          onChange={(e) =>
            setFile(e.target.files[0])
          }
          style={styles.fileInput}
        />

        <button
          type="submit"
          style={styles.uploadBtn}
        >
          {
            loading
              ? "Uploading..."
              : "Upload Document"
          }
        </button>

      </form>


      {/* DOCUMENT LIST */}

      <div style={styles.grid}>

        {
          documents.length === 0 ? (

            <div style={styles.empty}>
              No documents uploaded
            </div>

          ) : (

            documents.map((doc) => (

              <div
                key={doc.id}
                style={styles.card}
              >

                <div style={styles.icon}>
                  📄
                </div>

                <h3 style={styles.fileName}>
                  {doc.file_name}
                </h3>

                <p style={styles.version}>
                  Version: v{doc.version}
                </p>

                <p style={styles.task}>
                  Task ID: {doc.task_id}
                </p>

                <p style={styles.date}>
                  {
                    new Date(
                      doc.created_at
                    ).toLocaleString()
                  }
                </p>


                <div style={styles.buttonGroup}>

                  <button
                    style={styles.downloadBtn}
                    onClick={() =>
                      handleDownload(doc.id)
                    }
                  >
                    Download
                  </button>

                  <button
                    style={styles.deleteBtn}
                    onClick={() =>
                      handleDelete(doc.id)
                    }
                  >
                    Delete
                  </button>

                </div>

              </div>

            ))
          )
        }

      </div>

    </div>
  );
}


const styles = {

  container: {
    minHeight: "100vh",
    background: "#f3f4f6",
    padding: "30px",
    fontFamily: "Arial"
  },

  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "30px"
  },

  title: {
    fontSize: "42px",
    margin: 0,
    color: "#111827"
  },

  subtitle: {
    color: "#6b7280",
    marginTop: "10px"
  },

  backBtn: {
    background: "#4f46e5",
    color: "#fff",
    padding: "12px 20px",
    borderRadius: "10px",
    textDecoration: "none",
    fontWeight: "bold"
  },

  uploadBox: {
    background: "#fff",
    padding: "25px",
    borderRadius: "16px",
    marginBottom: "30px",
    boxShadow: "0 2px 10px rgba(0,0,0,0.08)"
  },

  uploadTitle: {
    marginBottom: "20px"
  },

  input: {
    width: "100%",
    padding: "14px",
    marginBottom: "15px",
    border: "1px solid #ddd",
    borderRadius: "10px"
  },

  fileInput: {
    marginBottom: "20px"
  },

  uploadBtn: {
    background: "#4f46e5",
    color: "#fff",
    border: "none",
    padding: "14px 20px",
    borderRadius: "10px",
    cursor: "pointer",
    fontWeight: "bold"
  },

  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
    gap: "20px"
  },

  card: {
    background: "#fff",
    padding: "24px",
    borderRadius: "16px",
    boxShadow: "0 2px 10px rgba(0,0,0,0.08)"
  },

  icon: {
    fontSize: "40px",
    marginBottom: "15px"
  },

  fileName: {
    margin: 0,
    marginBottom: "12px",
    color: "#111827"
  },

  version: {
    color: "#4f46e5",
    fontWeight: "bold",
    marginBottom: "8px"
  },

  task: {
    color: "#374151",
    marginBottom: "8px"
  },

  date: {
    color: "#6b7280",
    fontSize: "14px",
    marginBottom: "20px"
  },

  buttonGroup: {
    display: "flex",
    gap: "10px"
  },

  downloadBtn: {
    background: "#4f46e5",
    color: "#fff",
    border: "none",
    padding: "12px 16px",
    borderRadius: "10px",
    cursor: "pointer",
    fontWeight: "bold"
  },

  deleteBtn: {
    background: "#dc2626",
    color: "#fff",
    border: "none",
    padding: "12px 16px",
    borderRadius: "10px",
    cursor: "pointer",
    fontWeight: "bold"
  },

  empty: {
    background: "#fff",
    padding: "40px",
    borderRadius: "16px",
    textAlign: "center",
    color: "#6b7280"
  }

};
