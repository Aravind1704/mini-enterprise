import { useEffect, useState } from "react";

import { Link } from "react-router-dom";

import axios from "axios";


export default function Analytics() {

  const [summary, setSummary] = useState(null);

  const [taskStatus, setTaskStatus] = useState([]);

  const [userTasks, setUserTasks] = useState([]);

  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem("access_token");


  // =========================================
  // FETCH ANALYTICS
  // =========================================

  useEffect(() => {

    const fetchAnalytics = async () => {

      try {

        const headers = {
          Authorization: `Bearer ${token}`
        };

        const [
          summaryRes,
          statusRes,
          userRes
        ] = await Promise.all([

          axios.get(
            "http://127.0.0.1:8000/analytics/summary",
            { headers }
          ),

          axios.get(
            "http://127.0.0.1:8000/analytics/task-status",
            { headers }
          ),

          axios.get(
            "http://127.0.0.1:8000/analytics/user-tasks",
            { headers }
          )

        ]);

        setSummary(summaryRes.data);

        setTaskStatus(statusRes.data);

        setUserTasks(userRes.data);

      } catch (err) {

        console.error(err);

      } finally {

        setLoading(false);

      }

    };

    fetchAnalytics();

  }, [token]);


  // =========================================
  // LOADING
  // =========================================

  if (loading) {

    return (

      <div style={styles.loading}>

        Loading Analytics...

      </div>

    );

  }


  // =========================================
  // UI
  // =========================================

  return (

    <div style={styles.container}>


      {/* HEADER */}

      <div style={styles.header}>

        <div>

          <h1 style={styles.title}>
            📊 Analytics Dashboard
          </h1>

          <p style={styles.subtitle}>
            Track tasks, approvals and team productivity
          </p>

        </div>


        <Link
          to="/dashboard"
          style={styles.backBtn}
        >
          ← Dashboard
        </Link>

      </div>



      {/* SUMMARY CARDS */}

      <div style={styles.cardGrid}>


        <div style={styles.card}>

          <h3 style={styles.cardTitle}>
            Total Tasks
          </h3>

          <p style={styles.blueNumber}>
            {summary.total_tasks}
          </p>

        </div>


        <div style={styles.card}>

          <h3 style={styles.cardTitle}>
            Completed Tasks
          </h3>

          <p style={styles.greenNumber}>
            {summary.completed_tasks}
          </p>

        </div>


        <div style={styles.card}>

          <h3 style={styles.cardTitle}>
            Pending Tasks
          </h3>

          <p style={styles.redNumber}>
            {summary.pending_tasks}
          </p>

        </div>

      </div>



      {/* TASK STATUS */}

      <div style={styles.section}>

        <h2 style={styles.sectionTitle}>
          📌 Task Status Analytics
        </h2>


        {
          taskStatus.map((item) => (

            <div
              key={item.status}
              style={styles.row}
            >

              <span style={styles.rowLabel}>

                {item.status.replace("_", " ")}

              </span>

              <span style={styles.rowCount}>

                {item.count}

              </span>

            </div>

          ))
        }

      </div>



      {/* USER TASK DISTRIBUTION */}

      <div style={styles.section}>

        <h2 style={styles.sectionTitle}>
          👨‍💻 User Task Distribution
        </h2>


        {
          userTasks.map((item) => (

            <div
              key={item.user_name}
              style={styles.row}
            >

              <span style={styles.rowLabel}>

                {item.user_name}

              </span>

              <span style={styles.rowCountGreen}>

                {item.task_count}

              </span>

            </div>

          ))
        }

      </div>

    </div>
  );

}



const styles = {

  container: {
    padding: "30px",
    background: "#f3f4f6",
    minHeight: "100vh"
  },

  loading: {
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    fontSize: "28px",
    fontWeight: "bold",
    color: "#4f46e5",
    background: "#f3f4f6"
  },

  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "35px"
  },

  title: {
    fontSize: "42px",
    fontWeight: "bold",
    color: "#111827",
    marginBottom: "8px"
  },

  subtitle: {
    fontSize: "16px",
    color: "#6b7280"
  },

  backBtn: {
    background: "#4f46e5",
    color: "#fff",
    textDecoration: "none",
    padding: "14px 24px",
    borderRadius: "12px",
    fontWeight: "bold",
    fontSize: "15px"
  },

  cardGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
    gap: "25px",
    marginBottom: "35px"
  },

  card: {
    background: "#fff",
    borderRadius: "22px",
    padding: "35px",
    boxShadow: "0 2px 10px rgba(0,0,0,0.05)"
  },

  cardTitle: {
    fontSize: "18px",
    fontWeight: "600",
    color: "#6b7280",
    marginBottom: "18px"
  },

  blueNumber: {
    fontSize: "58px",
    fontWeight: "bold",
    color: "#4f46e5"
  },

  greenNumber: {
    fontSize: "58px",
    fontWeight: "bold",
    color: "#16a34a"
  },

  redNumber: {
    fontSize: "58px",
    fontWeight: "bold",
    color: "#ef4444"
  },

  section: {
    background: "#fff",
    borderRadius: "22px",
    padding: "35px",
    marginBottom: "35px",
    boxShadow: "0 2px 10px rgba(0,0,0,0.05)"
  },

  sectionTitle: {
    fontSize: "28px",
    fontWeight: "bold",
    color: "#111827",
    marginBottom: "25px"
  },

  row: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    background: "#f9fafb",
    padding: "18px 22px",
    borderRadius: "14px",
    marginBottom: "15px"
  },

  rowLabel: {
    fontSize: "17px",
    fontWeight: "500",
    color: "#374151",
    textTransform: "capitalize"
  },

  rowCount: {
    fontSize: "22px",
    fontWeight: "bold",
    color: "#4f46e5"
  },

  rowCountGreen: {
    fontSize: "22px",
    fontWeight: "bold",
    color: "#16a34a"
  }

};