
import {
  useEffect,
  useState
} from "react";

import {
  Link,
  useNavigate
} from "react-router-dom";

import api from "../api/axios";

import { useAuth }
from "../context/AuthContext";

import WebSocketClient
from "../services/WebSocketClient";


const STATUS_COLORS = {

  todo: {
    bg: "#fff3cd",
    color: "#856404"
  },

  in_progress: {
    bg: "#cce5ff",
    color: "#004085"
  },

  review: {
    bg: "#efe3ff",
    color: "#6f42c1"
  },

  done: {
    bg: "#d4edda",
    color: "#155724"
  },
};


const PRIORITY_COLORS = {

  low: {
    bg: "#e2f0d9",
    color: "#3a7d44"
  },

  medium: {
    bg: "#fff3cd",
    color: "#856404"
  },

  high: {
    bg: "#fde8e8",
    color: "#c0392b"
  },
};


export default function Dashboard() {

  const {
    user,
    logout
  } = useAuth();

  const navigate =
    useNavigate();

  const [tasks, setTasks] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [stats, setStats] =
    useState(null);

    const [currentPlan, setCurrentPlan] =
        useState("No Plan");

      const [credits, setCredits] =
        useState(0);


  // =====================================================
  // FETCH DASHBOARD
  // =====================================================

  const fetchDashboard =
    async () => {

      try {

        const [
          tasksResponse,
          statsResponse,
          subscriptionResponse
        ] = await Promise.all([

          api.get("/tasks/"),

          api.get("/role-dashboard"),

          api.get("/subscriptions/current")
        ]);

        setTasks(
          tasksResponse.data
        );

        setStats(
          statsResponse.data
        );
        setCurrentPlan(
          subscriptionResponse.data.plan
        );

        setCredits(
          subscriptionResponse.data.credits
        );
      } catch (error) {

        console.log(error);

      } finally {

        setLoading(false);
      }
    };


  // =====================================================
  // INITIAL LOAD
  // =====================================================

  useEffect(() => {

    fetchDashboard();

  }, []);


  // =====================================================
  // LIVE WEBSOCKET
  // =====================================================

  useEffect(() => {

    WebSocketClient.connect(

      (data) => {

        if (

          data.type ===
          "TASK_UPDATED"

        ) {

          fetchDashboard();
        }
      }
    );

  }, []);


  // =====================================================
  // LOGOUT
  // =====================================================

  const handleLogout =
    () => {

      logout();

      navigate("/login");
    };


  // =====================================================
  // DELETE TASK
  // =====================================================

  const handleDelete =
    async (id) => {

      if (
        !window.confirm(
          "Delete this task?"
        )
      ) return;

      await api.delete(
        `/tasks/${id}`
      );

      setTasks(

        tasks.filter(
          (t) => t.id !== id
        )
      );
    };


  // =====================================================
  // LOADING
  // =====================================================

  if (loading) {

    return (

      <div style={styles.loading}>

        Loading Dashboard...

      </div>
    );
  }


  return (

    <div style={styles.container}>


      {/* =====================================================
          NAVBAR
      ===================================================== */}

      <div style={styles.navbar}>


        {/* LEFT */}

        <div style={styles.navLeft}>

          <span style={styles.logo}>

            ⚡ EnterpriseFlow

          </span>

          <span style={styles.roleBadge}>

            {user?.role?.toUpperCase()}

          </span>

        </div>


        {/* CENTER */}

        <div style={styles.navCenter}>

          <Link
            to="/kanban"
            style={styles.navLink}
          >
            ⚡ Kanban
          </Link>

          <Link
            to="/approvals"
            style={styles.navLink}
          >
            ✅ Approvals
          </Link>

          <Link
            to="/documents"
            style={styles.navLink}
          >
            📄 Documents
          </Link>

          <Link
            to="/notifications"
            style={styles.navLink}
          >
            🔔 Notifications
          </Link>

          <Link
            to="/ai-insights"
            style={styles.navLink}
          >
            🤖 AI Insights
          </Link>

          <Link
            to="/analytics"
            style={styles.navLink}
          >
            📊 Analytics
          </Link>

          {user?.role === "admin" && (

            <Link
              to="/audit-logs"
              style={styles.navLink}
            >
              🔍 Audit Logs
            </Link>
          )}

        </div>


        {/* RIGHT */}

        <div style={styles.navRight}>
          
          <button
            onClick={() => navigate("/pricing")}
            style={styles.upgradeBtn}
          >
            🚀 Upgrade
          </button>
          <span style={styles.userName}>

            {user?.name}

          </span>

          {(

            user?.role === "admin" ||

            user?.role === "manager"

          ) && (

            <Link
              to="/tasks/create"
              style={styles.createBtn}
            >
              + New Task
            </Link>
          )}

          <button
            onClick={handleLogout}
            style={styles.logoutBtn}
          >
            Logout
          </button>

        </div>

      </div>



      {/* =====================================================
          MAIN
      ===================================================== */}

      <div style={styles.main}>


        {/* =====================================================
            ROLE BASED STATS
        ===================================================== */}

        <div style={styles.statsGrid}>

        {/* CURRENT PLAN */}

<div style={styles.smallCard}>

  <p style={styles.smallTitle}>
    Current Plan
  </p>

  <h2 style={styles.planValue}>
    {currentPlan}
  </h2>

</div>


{/* CURRENT CREDITS */}

<div style={styles.smallCard}>

  <p style={styles.smallTitle}>
    Credits
  </p>

  <h2 style={styles.creditValue}>
    {credits}
  </h2>

</div>
          {/* EMPLOYEE */}

          {stats?.role ===
            "employee" && (

            <>

              <div style={styles.statCard}>

                <h3>
                  My Tasks
                </h3>

                <p style={styles.statValue}>
                  {stats.my_tasks}
                </p>

              </div>

              <div style={styles.statCard}>

                <h3>
                  Pending
                </h3>

                <p style={styles.statValue}>
                  {stats.pending_tasks}
                </p>

              </div>

            </>
          )}


          {/* MANAGER */}

          {stats?.role ===
            "manager" && (

            <>

              <div style={styles.statCard}>

                <h3>
                  Team Tasks
                </h3>

                <p style={styles.statValue}>
                  {stats.team_tasks}
                </p>

              </div>

              <div style={styles.statCard}>

                <h3>
                  Pending Approvals
                </h3>

                <p style={styles.statValue}>
                  {stats.pending_approvals}
                </p>

              </div>

            </>
          )}


          {/* ADMIN */}

          {stats?.role ===
            "admin" && (

            <>

              <div style={styles.statCard}>

                <h3>
                  Total Users
                </h3>

                <p style={styles.statValue}>
                  {stats.total_users}
                </p>

              </div>

              <div style={styles.statCard}>

                <h3>
                  Total Tasks
                </h3>

                <p style={styles.statValue}>
                  {stats.total_tasks}
                </p>

              </div>

              <div style={styles.statCard}>

                <h3>
                  Approvals
                </h3>

                <p style={styles.statValue}>
                  {stats.total_approvals}
                </p>

              </div>

            </>
          )}

        </div>



        {/* =====================================================
            TASK LIST
        ===================================================== */}

        <div style={styles.headerSection}>

          <div>

            <h1 style={styles.pageTitle}>

              Task Dashboard

            </h1>

            <p style={styles.pageSubtitle}>

              {tasks.length}
              {" "}tasks available

            </p>

          </div>

        </div>



        {/* =====================================================
            TASK GRID
        ===================================================== */}

        <div style={styles.grid}>


          {tasks.map((task) => (

            <div
              key={task.id}
              style={styles.card}
            >


              {/* BADGES */}

              <div style={styles.cardHeader}>


                <span
                  style={{
                    ...styles.badge,
                    ...PRIORITY_COLORS[
                      task.priority
                    ]
                  }}
                >

                  {task.priority}

                </span>


                <span
                  style={{
                    ...styles.badge,
                    ...STATUS_COLORS[
                      task.status
                    ]
                  }}
                >

                  {task.status.replace(
                    "_",
                    " "
                  )}

                </span>

              </div>



              {/* TITLE */}

              <h3 style={styles.cardTitle}>

                {task.title}

              </h3>



              {/* DESCRIPTION */}

              <p style={styles.cardDesc}>

                {task.description ||
                  "No description"}

              </p>



              {/* DUE DATE */}

              {task.due_date && (

                <p style={styles.dueDate}>

                  📅 Due:
                  {" "}

                  {
                    new Date(
                      task.due_date
                    ).toLocaleDateString()
                  }

                </p>
              )}



              {/* ASSIGNED */}

              {task.assigned_to_id && (

                <p style={styles.assignedTo}>

                  👤 Assigned:
                  {" "}
                  User #
                  {task.assigned_to_id}

                </p>
              )}



              {/* ACTIONS */}

              <div style={styles.cardActions}>


                <Link
                  to={`/tasks/edit/${task.id}`}
                  style={styles.editBtn}
                >

                  Edit

                </Link>


                <Link
                  to={`/tasks/${task.id}/comments`}
                  style={styles.commentBtn}
                >

                  💬 Comments

                </Link>


                {(

                  user?.role === "admin" ||

                  user?.role === "manager"

                ) && (

                  <button
                    onClick={() =>
                      handleDelete(task.id)
                    }
                    style={styles.deleteBtn}
                  >

                    Delete

                  </button>
                )}

              </div>

            </div>
          ))}

        </div>

      </div>

    </div>
  );
}



const styles = {

  container: {
    minHeight: "100vh",
    background: "#f0f2f5",
    fontFamily: "sans-serif"
  },

  navbar: {
    background: "#fff",
    padding: "0 32px",
    height: "72px",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    boxShadow:
      "0 1px 4px rgba(0,0,0,0.08)"
  },

  navLeft: {
    display: "flex",
    alignItems: "center",
    gap: "12px"
  },

  logo: {
    fontSize: "18px",
    fontWeight: "700",
    color: "#4f46e5"
  },

  roleBadge: {
    background: "#eef2ff",
    color: "#4f46e5",
    padding: "4px 12px",
    borderRadius: "20px",
    fontSize: "11px",
    fontWeight: "700"
  },

  navCenter: {
    display: "flex",
    gap: "22px",
    flex: 1,
    justifyContent: "center"
  },

  navLink: {
    color: "#555",
    textDecoration: "none",
    fontSize: "13px",
    fontWeight: "600"
  },

  navRight: {
    display: "flex",
    alignItems: "center",
    gap: "12px"
  },

  userName: {
    fontSize: "14px",
    color: "#555"
  },

  createBtn: {
    background: "#4f46e5",
    color: "#fff",
    padding: "8px 16px",
    borderRadius: "8px",
    textDecoration: "none",
    fontSize: "13px",
    fontWeight: "600"
  },

  logoutBtn: {
    background: "transparent",
    border: "1px solid #ddd",
    padding: "7px 14px",
    borderRadius: "8px",
    cursor: "pointer"
  },

  main: {
    maxWidth: "1300px",
    margin: "0 auto",
    padding: "32px 20px"
  },

  statsGrid: {
    display: "grid",
    gridTemplateColumns:
      "repeat(auto-fit,minmax(220px,1fr))",
    gap: "20px",
    marginBottom: "32px"
  },

  statCard: {
    background: "#fff",
    borderRadius: "14px",
    padding: "24px",
    boxShadow:
      "0 2px 12px rgba(0,0,0,0.07)"
  },

  statValue: {
    fontSize: "30px",
    fontWeight: "700",
    color: "#4f46e5",
    marginTop: "10px"
  },

  headerSection: {
    marginBottom: "20px"
  },

  pageTitle: {
    fontSize: "28px",
    fontWeight: "700",
    color: "#1a1a2e",
    margin: 0
  },

  pageSubtitle: {
    color: "#888",
    marginTop: "6px"
  },

  grid: {
    display: "grid",
    gridTemplateColumns:
      "repeat(auto-fill,minmax(320px,1fr))",
    gap: "20px"
  },

  card: {
    background: "#fff",
    borderRadius: "14px",
    padding: "22px",
    boxShadow:
      "0 2px 12px rgba(0,0,0,0.07)"
  },

  cardHeader: {
    display: "flex",
    gap: "8px",
    marginBottom: "14px"
  },

  badge: {
    padding: "3px 10px",
    borderRadius: "20px",
    fontSize: "11px",
    fontWeight: "700",
    textTransform: "uppercase"
  },

  cardTitle: {
    margin: "0 0 10px",
    fontSize: "17px",
    fontWeight: "700",
    color: "#1a1a2e"
  },

  cardDesc: {
    color: "#666",
    fontSize: "13px",
    lineHeight: "1.5"
  },

  dueDate: {
    fontSize: "12px",
    color: "#777",
    marginTop: "12px"
  },

  assignedTo: {
    fontSize: "12px",
    color: "#777",
    marginTop: "6px"
  },

  cardActions: {
    display: "flex",
    gap: "8px",
    marginTop: "18px",
    flexWrap: "wrap"
  },

  editBtn: {
    background: "#eef2ff",
    color: "#4f46e5",
    padding: "7px 16px",
    borderRadius: "8px",
    textDecoration: "none",
    fontSize: "13px",
    fontWeight: "600"
  },

  commentBtn: {
    background: "#f0fdf4",
    color: "#059669",
    padding: "7px 16px",
    borderRadius: "8px",
    textDecoration: "none",
    fontSize: "13px",
    fontWeight: "600"
  },

  deleteBtn: {
    background: "#fde8e8",
    color: "#c0392b",
    padding: "7px 16px",
    borderRadius: "8px",
    border: "none",
    cursor: "pointer",
    fontSize: "13px",
    fontWeight: "600"
  },

  loading: {
    textAlign: "center",
    padding: "80px",
    fontSize: "18px"
  },
  smallCard:{

  background: "#fff",

  borderRadius: "14px",

  padding: "20px",

  boxShadow:
    "0 2px 12px rgba(0,0,0,0.07)"
},

smallTitle: {

  fontSize: "14px",

  color: "#666",

  marginBottom: "10px"
},

planValue: {

  fontSize: "28px",

  fontWeight: "700",

  color: "#4f46e5",

  margin: 0
},

creditValue: {

  fontSize: "28px",

  fontWeight: "700",

  color: "#10b981",

  margin: 0
},

upgradeBtn: {

  background: "#10b981",

  color: "#fff",

  border: "none",

  padding: "10px 18px",

  borderRadius: "10px",

  cursor: "pointer",

  fontSize: "14px",

  fontWeight: "700"
},
};