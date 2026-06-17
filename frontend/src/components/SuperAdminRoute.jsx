import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function SuperAdminRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div style={{ textAlign: "center", padding: "60px" }}>
        Loading...
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (user.role !== "super_admin") {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}