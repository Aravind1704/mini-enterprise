import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function PrivateRoute({ children }) {
  const { user, loading } = useAuth();

  // Show loading while auth state is being resolved
  if (loading) {
    return (
      <div style={{ textAlign: "center", padding: "60px" }}>
        Loading...
      </div>
    );
  }

  // Not logged in
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // Redirect super_admin to tenant dashboard
  if (user.role === "super_admin") {
    return <Navigate to="/tenant-dashboard" replace />;
  }

  // Allow authenticated non-super-admin users
  return children;
}