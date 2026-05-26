import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import {
  AuthProvider
} from "./context/AuthContext";

import PrivateRoute from "./components/PrivateRoute";
<<<<<<< HEAD
import ApprovalEscalations from "./pages/ApprovalEscalations";
import ApprovalDelegations from "./pages/ApprovalDelegations";
=======

>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
// ========================================
// PAGES
// ========================================

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import CreateTask from "./pages/CreateTask";
import EditTask from "./pages/EditTask";
import KanbanBoard from "./pages/KanbanBoard";
import Approvals from "./pages/Approvals";
import TaskComments from "./pages/TaskComments";
import DashboardStats from "./pages/DashboardStats";
import DocumentManager from "./pages/DocumentManager";
import AuditLogs from "./pages/AuditLogs";
import NotificationCenter from "./pages/NotificationCenter";
import AIInsights from "./pages/AIInsights";
import OAuthSuccess from "./pages/OAuthSuccess";
import Analytics from "./pages/Analytics";
import Subscriptions from "./pages/Subscriptions";
import Billing from "./pages/Billing";
import Pricing from "./pages/Pricing";
<<<<<<< HEAD
import SlaRules from './pages/SlaRules';
import SlaDashboard from './pages/SlaDashboard';

import BillingSuccess from "./pages/BillingSuccess";
=======


import BillingSuccess from "./pages/BillingSuccess";

import BillingCancel from "./pages/BillingCancel";

>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2

import BillingCancel from "./pages/BillingCancel";
import ForgotPassword from "./components/ForgotPassword";
import ResetPassword from "./components/ResetPassword";
import NotificationPreferences from "./pages/notification-preferences"; 
export default function App() {

  return (

    <AuthProvider>

      <BrowserRouter>

        <Routes>

          {/* =====================================
              PUBLIC ROUTES
          ===================================== */}

          <Route
            path="/login"
            element={<Login />}
          />

          <Route
            path="/register"
            element={<Register />}
          />

          <Route
            path="/oauth-success"
            element={<OAuthSuccess />}
          />
<<<<<<< HEAD
         
=======


>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
          {/* =====================================
              PROTECTED ROUTES
          ===================================== */}

          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />

          <Route
            path="/tasks/create"
            element={
              <PrivateRoute>
                <CreateTask />
              </PrivateRoute>
            }
          />

          <Route
            path="/tasks/edit/:id"
            element={
              <PrivateRoute>
                <EditTask />
              </PrivateRoute>
            }
          />

          <Route
            path="/tasks/:id/comments"
            element={
              <PrivateRoute>
                <TaskComments />
              </PrivateRoute>
            }
          />

          <Route
            path="/kanban"
            element={
              <PrivateRoute>
                <KanbanBoard />
              </PrivateRoute>
            }
          />

          <Route
            path="/approvals"
            element={
              <PrivateRoute>
                <Approvals />
              </PrivateRoute>
            }
          />

          <Route
            path="/stats"
            element={
              <PrivateRoute>
                <DashboardStats />
              </PrivateRoute>
            }
          />

          <Route
            path="/documents"
            element={
              <PrivateRoute>
                <DocumentManager />
              </PrivateRoute>
            }
          />

          <Route
            path="/audit-logs"
            element={
              <PrivateRoute>
                <AuditLogs />
              </PrivateRoute>
            }
          />

          <Route
            path="/notifications"
            element={
              <PrivateRoute>
                <NotificationCenter />
              </PrivateRoute>
            }
          />

          <Route
            path="/ai-insights"
            element={
              <PrivateRoute>
                <AIInsights />
              </PrivateRoute>
            }
          />

          <Route
            path="/analytics"
            element={
              <PrivateRoute>
                <Analytics />
              </PrivateRoute>
            }
          />
<<<<<<< HEAD
          
=======
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2

          <Route
            path="/subscriptions"
            element={
              <PrivateRoute>
                <Subscriptions />
              </PrivateRoute>
            }
          />

          <Route
            path="/billing"
            element={
              <PrivateRoute>
                <Billing />
              </PrivateRoute>
            }
          />
         <Route
          path="/pricing"
          element={
            <PrivateRoute>
              <Pricing />
            </PrivateRoute>
          }
        />
<<<<<<< HEAD
        <Route
          path="/notification-preferences"
          element={
            <PrivateRoute>
              <NotificationPreferences />
            </PrivateRoute>
          }
        />
        <Route path="/sla-rules" element={<PrivateRoute><SlaRules /></PrivateRoute>} />
        <Route path="/sla-dashboard" element={<PrivateRoute><SlaDashboard /></PrivateRoute>} />
=======

>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
        <Route
          path="/success"
          element={<BillingSuccess />}
        />
<<<<<<< HEAD
       <Route path="/approval-escalations" element={<ApprovalEscalations />} />
        <Route path="/approval-delegations" element={<ApprovalDelegations />} />
=======

>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
        <Route
          path="/cancel"
          element={<BillingCancel />}
        />
<<<<<<< HEAD
        <Route path="/login" element={<Login />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />
=======

>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
          {/* =====================================
              DEFAULT ROUTE
          ===================================== */}

          <Route
            path="*"
            element={
              <Navigate to="/login" />
            }
          />

        </Routes>

      </BrowserRouter>

    </AuthProvider>
  );
}