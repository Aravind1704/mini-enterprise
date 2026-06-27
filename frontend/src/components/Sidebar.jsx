import { Link, useLocation } from "react-router-dom";

export default function Sidebar() {
  const location = useLocation();
  const channelId =
  localStorage.getItem("channelId");
  const projectId =
    localStorage.getItem("projectId");
  const teamId =
    localStorage.getItem("teamId");
  
  const user = JSON.parse(
    localStorage.getItem("user")
  );

  const tenantId =
    localStorage.getItem("selectedTenantId");

  const workspaceId =
    localStorage.getItem("workspaceId");

  const isSuperAdmin =
    user?.role === "super_admin";

  const currentTeamId =
    teamId ||
    location.pathname.match(/^\/teams\/(\d+)/)?.[1] ||
    "";

  const currentProjectId =
    projectId ||
    location.pathname.match(/^\/projects\/(\d+)/)?.[1] ||
    "";

  const menuClass = (path) => {
    const active =
      location.pathname === path;

    return `block p-3 rounded-lg transition ${
      active
        ? "bg-indigo-100 text-indigo-700 font-semibold"
        : "hover:bg-indigo-50 text-gray-700"
      }`;
  };

  const subMenuClass = (pathname, hash = "") => {
    const active =
      location.pathname === pathname &&
      (hash ? location.hash === hash : true);

    return `block rounded-lg px-3 py-2 text-sm transition ${
      active
        ? "bg-indigo-100 text-indigo-700 font-semibold"
        : "hover:bg-indigo-50 text-gray-700"
    }`;
  };

  return (
    <aside className="w-72 bg-white border-r min-h-screen">
      {/* Logo */}
      <div className="p-6 border-b">
        <h2 className="font-bold text-2xl text-indigo-600">
          Collab Platform
        </h2>

        <p className="text-sm text-gray-500 mt-1">
          Enterprise SaaS
        </p>
      </div>

      <nav className="px-4 py-4 space-y-4">
        {/* Dashboard */}
        <Link
          to={
            isSuperAdmin
              ? "/tenant-dashboard"
              : "/dashboard"
          }
          className={menuClass(
            isSuperAdmin
              ? "/tenant-dashboard"
              : "/dashboard"
          )}
        >
          📊 Dashboard
        </Link>

        {/* ================= SUPER ADMIN ================= */}

        {isSuperAdmin && (
          <>
            <div>
              <h3 className="text-xs font-bold text-gray-400 uppercase mb-2">
                Tenant Management
              </h3>

              <div className="space-y-1">
                <Link
                  to="/tenants"
                  className={menuClass("/tenants")}
                >
                  🏢 Tenant List
                </Link>

                <Link
                  to="/tenant-create"
                  className={menuClass(
                    "/tenant-create"
                  )}
                >
                  ➕ Create Tenant
                </Link>

                <Link
                  to="/tenant-onboarding"
                  className={menuClass(
                    "/tenant-onboarding"
                  )}
                >
                  🚀 Tenant Onboarding
                </Link>
              </div>
            </div>

            <div>
              <h3 className="text-xs font-bold text-gray-400 uppercase mb-2">
                Collaboration
              </h3>

              <div className="space-y-1">
                <Link
                  to={
                    tenantId
                      ? `/tenants/${tenantId}/settings`
                      : "/tenants"
                  }
                  className={menuClass(
                    "/settings"
                  )}
                >
                  ⚙️ Settings
                </Link>

                <Link
                  to={
                    tenantId
                      ? `/tenants/${tenantId}/usage`
                      : "/tenants"
                  }
                  className={menuClass(
                    "/usage"
                  )}
                >
                  📈 Usage
                </Link>
              </div>
            </div>
          </>
        )}

        {/* ================= NORMAL USER ================= */}

        {!isSuperAdmin && (
          <>
            {/* Workspace Management */}
            <div>
              <h3 className="text-xs font-bold text-gray-400 uppercase mb-2">
                Tenant > Workspace
              </h3>

              <div className="space-y-1">
                <Link
                  to="/workspaces"
                  className={menuClass(
                    "/workspaces"
                  )}
                >
                  📂 Workspace List
                </Link>

                <Link
                  to="/workspace-create"
                  className={menuClass(
                    "/workspace-create"
                  )}
                >
                  ➕ Create Workspace
                </Link>

                <Link
                  to={
                    workspaceId
                      ? `/workspaces/${workspaceId}`
                      : "/workspaces"
                  }
                  className={
                    workspaceId &&
                    location.pathname ===
                      `/workspaces/${workspaceId}`
                      ? "block p-3 rounded-lg bg-indigo-100 text-indigo-700 font-semibold"
                      : "block p-3 rounded-lg hover:bg-indigo-50 text-gray-700"
                  }
                >
                  🔍 Workspace Details
                </Link>

                <Link
                  to={
                    workspaceId
                      ? `/workspaces/${workspaceId}/members`
                      : "/workspaces"
                  }
                  className={
                    workspaceId &&
                    location.pathname ===
                      `/workspaces/${workspaceId}/members`
                      ? "block p-3 rounded-lg bg-indigo-100 text-indigo-700 font-semibold"
                      : "block p-3 rounded-lg hover:bg-indigo-50 text-gray-700"
                  }
                >
                  👥 Workspace Members
                </Link>
              </div>
            </div>

            {/* Channel Management */}
            <div>
              <h3 className="text-xs font-bold text-gray-400 uppercase mb-2">
                Channel Management
              </h3>

              <div className="space-y-1">
                <Link
                to={
                  workspaceId
                    ? `/workspaces/${workspaceId}/channels`
                    : "/workspaces"
                }
                className={
                  location.pathname.includes(
                    "/channels"
                  ) &&
                  !location.pathname.includes(
                    "/channel-details"
                  ) &&
                  !location.pathname.includes(
                    "/channel-members"
                  )
                    ? "block p-3 rounded-lg bg-indigo-100 text-indigo-700 font-semibold"
                    : "block p-3 rounded-lg hover:bg-indigo-50 text-gray-700"
                }
              >
                💬 Channel List
              </Link>
                <Link
                  to="/channel-create"
                  className={menuClass(
                    "/channel-create"
                  )}
                >
                  ➕ Create Channel
                </Link>

               <Link
                to={
                  channelId
                    ? `/channel-details/${channelId}`
                    : "/channels"
                }
                className={
                  location.pathname.includes(
                    "/channel-details"
                  )
                    ? "block p-3 rounded-lg bg-indigo-100 text-indigo-700 font-semibold"
                    : "block p-3 rounded-lg hover:bg-indigo-50 text-gray-700"
                }
              >
                🔍 Channel Details
              </Link>

           <Link
              to={
                channelId
                  ? `/channel-members/${channelId}`
                  : "/channels"
              }
              className={
                location.pathname.includes(
                  "/channel-members"
                )
                  ? "block p-3 rounded-lg bg-indigo-100 text-indigo-700 font-semibold"
                  : "block p-3 rounded-lg hover:bg-indigo-50 text-gray-700"
              }
            >
              👥 Channel Members
            </Link>
              </div>
            </div>

            {/* Task Management */}
            <div>
              <h3 className="text-xs font-bold text-gray-400 uppercase mb-2">
                Task Management
              </h3>

              <div className="space-y-1">
                <Link
                  to="/kanban"
                  className={menuClass("/kanban")}
                >
                  📋 Kanban Board
                </Link>

                <Link
                  to="/tasks/create"
                  className={menuClass("/tasks/create")}
                >
                  ➕ Create Task
                </Link>
              </div>
            </div>

            {/* Enterprise Planning */}
            <div>
              <h3 className="text-xs font-bold text-gray-400 uppercase mb-2">
                Teams > Projects
              </h3>

              <div className="space-y-2">
                <Link
                  to="/teams"
                  className={menuClass("/teams")}
                >
                  Teams
                </Link>

                <Link
                  to={
                    currentTeamId
                      ? `/teams/${currentTeamId}`
                      : "/teams"
                  }
                  className={
                    location.pathname === `/teams/${currentTeamId}`
                      ? "block p-3 rounded-lg bg-indigo-100 text-indigo-700 font-semibold"
                      : "block p-3 rounded-lg hover:bg-indigo-50 text-gray-700"
                  }
                >
                  Team Details
                </Link>

                <Link
                  to="/projects"
                  className={menuClass("/projects")}
                >
                  Projects
                </Link>

                <div className="ml-3 space-y-1 border-l border-slate-200 pl-3">
                  <Link
                    to={
                      currentProjectId
                        ? { pathname: `/projects/${currentProjectId}`, hash: "#project-teams" }
                        : "/projects"
                    }
                    className={subMenuClass(`/projects/${currentProjectId}`, "#project-teams")}
                  >
                    Project Teams
                  </Link>

                  <Link
                    to={
                      currentProjectId
                        ? { pathname: `/projects/${currentProjectId}`, hash: "#project-channels" }
                        : "/projects"
                    }
                    className={subMenuClass(`/projects/${currentProjectId}`, "#project-channels")}
                  >
                    Project Channels
                  </Link>

                  <Link
                    to={
                      currentProjectId
                        ? { pathname: `/projects/${currentProjectId}`, hash: "#project-tasks" }
                        : "/projects"
                    }
                    className={subMenuClass(`/projects/${currentProjectId}`, "#project-tasks")}
                  >
                    Project Tasks
                  </Link>

                  <Link
                    to={
                      currentProjectId
                        ? { pathname: `/projects/${currentProjectId}`, hash: "#project-documents" }
                        : "/projects"
                    }
                    className={subMenuClass(`/projects/${currentProjectId}`, "#project-documents")}
                  >
                    Project Documents
                  </Link>

                  <Link
                    to={
                      currentProjectId
                        ? { pathname: `/projects/${currentProjectId}`, hash: "#project-meetings" }
                        : "/projects"
                    }
                    className={subMenuClass(`/projects/${currentProjectId}`, "#project-meetings")}
                  >
                    Project Meetings
                  </Link>
                </div>

                <Link
                  to="/meetings"
                  className={menuClass("/meetings")}
                >
                  Meetings
                </Link>

                <Link
                  to={
                    teamId
                      ? `/teams/${teamId}/workload`
                      : "/teams"
                  }
                  className={
                    location.pathname.includes(
                      "/teams/"
                    ) &&
                    location.pathname.includes(
                      "/workload"
                    )
                      ? "block p-3 rounded-lg bg-indigo-100 text-indigo-700 font-semibold"
                      : "block p-3 rounded-lg hover:bg-indigo-50 text-gray-700"
                  }
                >
                  Team Workload
                </Link>

                <Link
                  to={
                    projectId
                      ? `/projects/${projectId}/calendar`
                      : "/projects"
                  }
                  className={
                    location.pathname.includes(
                      "/calendar"
                    )
                      ? "block p-3 rounded-lg bg-indigo-100 text-indigo-700 font-semibold"
                      : "block p-3 rounded-lg hover:bg-indigo-50 text-gray-700"
                  }
                >
                  Project Calendar
                </Link>

                <Link
                  to={
                    projectId
                      ? `/projects/${projectId}/workload`
                      : "/projects"
                  }
                  className={
                    location.pathname.includes(
                      "/projects/"
                    ) &&
                    location.pathname.includes(
                      "/workload"
                    )
                      ? "block p-3 rounded-lg bg-indigo-100 text-indigo-700 font-semibold"
                      : "block p-3 rounded-lg hover:bg-indigo-50 text-gray-700"
                  }
                >
                  Project Workload
                </Link>
              </div>
            </div>

            {/* Documents & Approvals */}
            <div>
              <h3 className="text-xs font-bold text-gray-400 uppercase mb-2">
                Documents & Approvals
              </h3>

              <div className="space-y-1">
                <Link
                  to="/documents"
                  className={menuClass("/documents")}
                >
                  📄 Documents
                </Link>

                <Link
                  to="/approvals"
                  className={menuClass("/approvals")}
                >
                  ✓ Approvals
                </Link>
              </div>
            </div>

            {/* Notifications & Settings */}
            <div>
              <h3 className="text-xs font-bold text-gray-400 uppercase mb-2">
                Settings
              </h3>

              <div className="space-y-1">
                <Link
                  to="/notifications"
                  className={menuClass("/notifications")}
                >
                  🔔 Notifications
                </Link>

                <Link
                  to="/audit-logs"
                  className={menuClass("/audit-logs")}
                >
                  📝 Audit Logs
                </Link>
              </div>
            </div>
          </>
        )}
      </nav>
    </aside>
  );
}
