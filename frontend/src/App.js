import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import CreateTask from "./pages/CreateTask";
import EditTask from "./pages/EditTask";
import KanbanBoard from "./pages/KanbanBoard";
import Approvals from "./pages/Approvals";
import TaskComments from "./pages/TaskComments";
import DashboardStats from "./pages/DashboardStats";
import PrivateRoute from "./components/PrivateRoute";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          <Route path="/tasks/create" element={<PrivateRoute><CreateTask /></PrivateRoute>} />
          <Route path="/tasks/edit/:id" element={<PrivateRoute><EditTask /></PrivateRoute>} />
          <Route path="/kanban" element={<PrivateRoute><KanbanBoard /></PrivateRoute>} />
          <Route path="/approvals" element={<PrivateRoute><Approvals /></PrivateRoute>} />
          <Route path="/tasks/:id/comments" element={<PrivateRoute><TaskComments /></PrivateRoute>} />
          <Route path="/stats" element={<PrivateRoute><DashboardStats /></PrivateRoute>} />
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}