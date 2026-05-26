import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();

  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const [error, setError] = useState("");

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);

    setError("");

    try {
      await login(
        form.email,
        form.password
      );

      navigate("/dashboard");

    } catch (err) {

      setError(
        err.response?.data?.detail ||
        "Invalid email or password"
      );

    } finally {

      setLoading(false);
    }
  };

  const handleGoogleLogin = () => {

    window.location.href =
      "http://127.0.0.1:8000/auth/google/login";
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>

        <h1 style={styles.title}>
          Welcome Back
        </h1>

        <p style={styles.subtitle}>
          Sign in to your account
        </p>

        {error && (
          <div style={styles.error}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>

          <div style={styles.field}>
            <label style={styles.label}>
              Email
            </label>

            <input
              style={styles.input}
              type="email"
              name="email"
              placeholder="admin@example.com"
              value={form.email}
              onChange={handleChange}
              required
            />
          </div>

          <div style={styles.field}>
            <label style={styles.label}>
              Password
            </label>

            <input
              style={styles.input}
              type="password"
              name="password"
              placeholder="••••••••"
              value={form.password}
              onChange={handleChange}
              required
            />
          </div>
<Link to="/forgot-password">Forgot password?</Link>

          <button
            type="submit"
            style={styles.button}
            disabled={loading}
          >
            {loading
              ? "Signing in..."
              : "Sign In"}
          </button>
        </form>

        <div style={styles.divider}>
          <span>OR</span>
        </div>

        <button
          style={styles.googleBtn}
          onClick={handleGoogleLogin}
        >
          Continue with Google
        </button>

        <p style={styles.link}>
          Don't have an account?{" "}

          <Link
            to="/register"
            style={styles.anchor}
          >
            Register
          </Link>
        </p>

      </div>
    </div>
  );
}

const styles = {

  container: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "#f3f4f6",
    padding: "20px",
    fontFamily: "Arial",
  },

  card: {
    width: "100%",
    maxWidth: "420px",
    background: "#ffffff",
    borderRadius: "14px",
    padding: "40px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.08)",
  },

  title: {
    margin: 0,
    fontSize: "30px",
    fontWeight: "700",
    color: "#111827",
  },

  subtitle: {
    marginTop: "8px",
    marginBottom: "28px",
    color: "#6b7280",
    fontSize: "14px",
  },

  error: {
    background: "#fef2f2",
    border: "1px solid #fecaca",
    color: "#dc2626",
    padding: "12px",
    borderRadius: "8px",
    marginBottom: "18px",
    fontSize: "14px",
  },

  field: {
    marginBottom: "18px",
  },

  label: {
    display: "block",
    marginBottom: "8px",
    fontSize: "14px",
    fontWeight: "600",
    color: "#374151",
  },

  input: {
    width: "100%",
    padding: "12px 14px",
    borderRadius: "8px",
    border: "1px solid #d1d5db",
    fontSize: "14px",
    outline: "none",
    boxSizing: "border-box",
  },

  button: {
    width: "100%",
    padding: "12px",
    borderRadius: "8px",
    border: "none",
    background: "#4f46e5",
    color: "#ffffff",
    fontSize: "15px",
    fontWeight: "600",
    cursor: "pointer",
    marginTop: "10px",
  },

  divider: {
    textAlign: "center",
    margin: "24px 0",
    color: "#9ca3af",
    fontSize: "13px",
    position: "relative",
  },

  googleBtn: {
    width: "100%",
    padding: "12px",
    background: "#ffffff",
    color: "#111827",
    border: "1px solid #d1d5db",
    borderRadius: "8px",
    fontSize: "15px",
    fontWeight: "600",
    cursor: "pointer",
  },

  link: {
    textAlign: "center",
    marginTop: "22px",
    fontSize: "14px",
    color: "#6b7280",
  },

  anchor: {
    color: "#4f46e5",
    textDecoration: "none",
    fontWeight: "600",
  },
};
