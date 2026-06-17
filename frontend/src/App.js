import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import {
  AuthProvider
} from "./context/AuthContext";
import {
  TenantProvider
} from "./context/TenantContext";

import PrivateRoute from "./components/PrivateRoute";

import ApprovalEscalations from "./pages/ApprovalEscalations";
import ApprovalDelegations from "./pages/ApprovalDelegations";


import TenantList from "./pages/TenantList";
import TenantOnboarding from "./pages/TenantOnboarding";


import SuperAdminRoute from "./components/SuperAdminRoute";
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

import SlaRules from './pages/SlaRules';
import SlaDashboard from './pages/SlaDashboard';

import BillingSuccess from "./pages/BillingSuccess";


import BillingCancel from "./pages/BillingCancel";
import ForgotPassword from "./components/ForgotPassword";
import ResetPassword from "./components/ResetPassword";
import NotificationPreferences from "./pages/notification-preferences"; 


import TenantDashboard from "./pages/TenantDashboard";


import TenantCreate from "./pages/TenantCreate";
import TenantDetails from "./pages/TenantDetails";
import TenantOnboardCreate from "./pages/TenantOnboardCreate";

import CollaborationSettings from "./pages/CollaborationSettings";
import CollaborationUsage from "./pages/CollaborationUsage";

import WorkspaceList from "./pages/WorkspaceList";
import WorkspaceCreate from "./pages/WorkspaceCreate";
import WorkspaceDetails from "./pages/WorkspaceDetails";
import WorkspaceMembers from "./pages/WorkspaceMembers";

import ChannelList from "./pages/ChannelList";
import ChannelCreate from "./pages/ChannelCreate";
import ChannelDetails from "./pages/ChannelDetails";
import ChannelMembers from "./pages/ChannelMembers";
export default function App() {

  return (

    <AuthProvider>

      <TenantProvider>

        <BrowserRouter>

          <Routes>

                  {/* =====================================
                      PUBLIC ROUTES
                  ===================================== */}
        {/* ================================
            TENANT MANAGEMENT
        ================================ */}


        <Route
        path="/tenants"
        element={
          <SuperAdminRoute>
            <TenantList />
          </SuperAdminRoute>
        }
      />

      <Route
        path="/tenant-create"
        element={
          <SuperAdminRoute>
            <TenantCreate />
          </SuperAdminRoute>
        }
      />

      <Route
        path="/tenant-onboarding"
        element={
          <SuperAdminRoute>
            <TenantOnboarding />
          </SuperAdminRoute>
        }
      />

      <Route
        path="/tenants/:id"
        element={
          <SuperAdminRoute>
            <TenantDetails />
          </SuperAdminRoute>
        }
      />

      <Route
        path="/tenants/:id/settings"
        element={
          <SuperAdminRoute>
            <CollaborationSettings />
          </SuperAdminRoute>
        }
      />

      <Route
        path="/tenants/:id/usage"
        element={
          <SuperAdminRoute>
            <CollaborationUsage />
          </SuperAdminRoute>
        }
      />
          <Route
            path="/tenant-details"
            element={
              <SuperAdminRoute>
                <TenantDetails />
              </SuperAdminRoute>
            }
          />
        <Route
          path="/tenant-details"
          element={
            <SuperAdminRoute>
              <TenantDetails />
            </SuperAdminRoute>
          }
        />

        <Route
          path="/tenant-create"
          element={
            <SuperAdminRoute>
              <TenantCreate />
            </SuperAdminRoute>
          }
        />

        <Route
          path="/tenant-onboard-create"
          element={
            <SuperAdminRoute>
              <TenantOnboardCreate />
            </SuperAdminRoute>
          }
        />
        <Route
          path="/tenant-dashboard"
          element={
            <SuperAdminRoute>
              <TenantDashboard />
            </SuperAdminRoute>
          }
        />
        {/* ================================
            COLLABORATION
        ================================ */}

        <Route
          path="/tenants/:id/settings"
          element={<CollaborationSettings />}
        />

        <Route
          path="/tenants/:id/usage"
          element={<CollaborationUsage />}
        />

        {/* ================================
            WORKSPACE MANAGEMENT
        ================================ */}

       




<Route path="/workspaces" element={<WorkspaceList />} />
<Route path="/workspace-create" element={<WorkspaceCreate />} />
<Route
  path="/workspaces/:id"
  element={<WorkspaceDetails />}
/>
<Route
  path="/workspaces/:id/members"
  element={<WorkspaceMembers />}
/>


       
        {/* ================================
            CHANNEL MANAGEMENT
        ================================ */}


        
          <Route
            path="/channels"
            element={
              <PrivateRoute>
                <ChannelList />
              </PrivateRoute>
            }
          />

          <Route
            path="/channel-create"
            element={
              <PrivateRoute>
                <ChannelCreate />
              </PrivateRoute>
            }
          />

          <Route
            path="/channel-details/:id"
            element={
              <PrivateRoute>
                <ChannelDetails />
              </PrivateRoute>
            }
          />

          <Route
            path="/channel-members/:channelId"
            element={
              <PrivateRoute>
                <ChannelMembers />
              </PrivateRoute>
            }
          />
        
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

        <Route
          path="/success"
          element={<BillingSuccess />}
        />

       <Route path="/approval-escalations" element={<ApprovalEscalations />} />
        <Route path="/approval-delegations" element={<ApprovalDelegations />} />

        <Route
          path="/cancel"
          element={<BillingCancel />}
        />

        <Route path="/login" element={<Login />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />


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

    </TenantProvider>

    </AuthProvider>
  );
}