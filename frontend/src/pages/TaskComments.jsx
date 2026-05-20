import { useEffect, useState } from "react";

import {
  useParams,
  Link
} from "react-router-dom";

import {
  useAuth
} from "../context/AuthContext";

import api from "../api/axios";


export default function TaskComments() {

  const { id } = useParams();

  const { user } = useAuth();

  const [comments, setComments] =
    useState([]);

  const [form, setForm] =
    useState({
      content: "",
      is_internal: false
    });

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");


  // =========================================
  // FETCH COMMENTS
  // =========================================

  useEffect(() => {

    const fetchCommentsData =
      async () => {

      try {

        const res =
          await api.get(
            `/tasks/${id}/comments`
          );

        setComments(
          res.data
        );

      } catch (err) {

        console.log(err);

      } finally {

        setLoading(false);

      }

    };

    fetchCommentsData();

  }, [id]);


  // =========================================
  // ADD COMMENT
  // =========================================

  const handleSubmit =
    async (e) => {

    e.preventDefault();

    if (
      !form.content.trim()
    ) return;

    try {

      await api.post(

        `/tasks/${id}/comments`,

        form
      );

      setForm({
        content: "",
        is_internal: false
      });


      // REFRESH COMMENTS

      const res =
        await api.get(
          `/tasks/${id}/comments`
        );

      setComments(
        res.data
      );

    } catch (err) {

      setError(

        err.response?.data?.detail ||

        "Failed to add comment"
      );

    }

  };


  // =========================================
  // LOADING
  // =========================================

  if (loading) {

    return (

      <div style={styles.loading}>

        Loading comments...

      </div>

    );

  }


  // =========================================
  // UI
  // =========================================

  return (

    <div style={styles.container}>

      <div style={styles.card}>


        {/* HEADER */}

        <div style={styles.header}>

          <Link
            to="/dashboard"
            style={styles.back}
          >
            ← Back
          </Link>

          <h2 style={styles.title}>

            💬 Task #{id} Comments

          </h2>

        </div>


        {/* ERROR */}

        {error && (

          <div style={styles.error}>

            {error}

          </div>

        )}


        {/* FORM */}

        <form
          onSubmit={handleSubmit}
          style={styles.form}
        >

          <textarea

            style={styles.textarea}

            placeholder="Write a comment..."

            value={form.content}

            onChange={(e) =>

              setForm({

                ...form,

                content: e.target.value

              })

            }

            rows={4}

            required
          />


          {(

            user?.role === "admin" ||

            user?.role === "manager"

          ) && (

            <label style={styles.checkLabel}>

              <input

                type="checkbox"

                checked={form.is_internal}

                onChange={(e) =>

                  setForm({

                    ...form,

                    is_internal:
                    e.target.checked

                  })

                }
              />

              &nbsp;

              Internal Note
              (Hidden from employees)

            </label>

          )}


          <button
            type="submit"
            style={styles.submitBtn}
          >

            Post Comment

          </button>

        </form>


        <hr style={styles.divider} />


        {/* COMMENTS */}

        {

          comments.length === 0 ? (

            <div style={styles.empty}>

              No comments yet

            </div>

          ) : (

            <div style={styles.commentList}>

              {

                comments.map((c) => (

                  <div

                    key={c.id}

                    style={{

                      ...styles.comment,

                      background:
                      c.is_internal

                      ? "#fffbeb"

                      : "#f9fafb",

                      borderLeft:
                      c.is_internal

                      ? "5px solid #f59e0b"

                      : "5px solid #4f46e5"
                    }}
                  >

                    <div
                      style={styles.commentHeader}
                    >

                      <div
                        style={styles.avatar}
                      >

                        {

                          c.user_id === user?.id

                          ? "👤 You"

                          : `👤 User #${c.user_id}`
                        }

                      </div>


                      <div
                        style={styles.rightHeader}
                      >

                        {c.is_internal && (

                          <span
                            style={styles.internalBadge}
                          >

                            🔒 Internal

                          </span>

                        )}


                        <span
                          style={styles.timestamp}
                        >

                          {

                            new Date(

                              c.created_at

                            ).toLocaleString()

                          }

                        </span>

                      </div>

                    </div>


                    <p style={styles.commentText}>

                      {c.content}

                    </p>

                  </div>

                ))

              }

            </div>

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

    display: "flex",

    justifyContent: "center",

    padding: "40px 20px"
  },

  card: {

    background: "#fff",

    width: "100%",

    maxWidth: "800px",

    borderRadius: "20px",

    padding: "35px",

    boxShadow:
    "0 4px 20px rgba(0,0,0,0.06)"
  },

  loading: {

    minHeight: "100vh",

    display: "flex",

    justifyContent: "center",

    alignItems: "center",

    fontSize: "26px",

    fontWeight: "bold",

    color: "#4f46e5"
  },

  header: {

    marginBottom: "25px"
  },

  back: {

    color: "#4f46e5",

    textDecoration: "none",

    fontWeight: "600",

    fontSize: "14px"
  },

  title: {

    marginTop: "10px",

    fontSize: "32px",

    fontWeight: "bold",

    color: "#111827"
  },

  error: {

    background: "#fee2e2",

    color: "#b91c1c",

    padding: "14px",

    borderRadius: "10px",

    marginBottom: "20px"
  },

  form: {

    marginBottom: "30px"
  },

  textarea: {

    width: "100%",

    padding: "15px",

    border: "1px solid #d1d5db",

    borderRadius: "12px",

    fontSize: "15px",

    resize: "vertical",

    outline: "none",

    marginBottom: "15px"
  },

  checkLabel: {

    display: "flex",

    alignItems: "center",

    marginBottom: "15px",

    fontSize: "14px",

    color: "#374151"
  },

  submitBtn: {

    background: "#4f46e5",

    color: "#fff",

    border: "none",

    padding: "12px 24px",

    borderRadius: "12px",

    fontWeight: "bold",

    cursor: "pointer"
  },

  divider: {

    border: "none",

    borderTop: "1px solid #e5e7eb",

    marginBottom: "30px"
  },

  empty: {

    textAlign: "center",

    color: "#6b7280",

    padding: "40px"
  },

  commentList: {

    display: "flex",

    flexDirection: "column",

    gap: "20px"
  },

  comment: {

    padding: "20px",

    borderRadius: "14px"
  },

  commentHeader: {

    display: "flex",

    justifyContent: "space-between",

    alignItems: "center",

    marginBottom: "10px"
  },

  avatar: {

    fontWeight: "bold",

    color: "#4f46e5"
  },

  rightHeader: {

    display: "flex",

    alignItems: "center",

    gap: "10px"
  },

  internalBadge: {

    background: "#fef3c7",

    color: "#92400e",

    padding: "4px 10px",

    borderRadius: "999px",

    fontSize: "11px",

    fontWeight: "bold"
  },

  timestamp: {

    fontSize: "12px",

    color: "#6b7280"
  },

  commentText: {

    color: "#374151",

    lineHeight: "1.7"
  }

};