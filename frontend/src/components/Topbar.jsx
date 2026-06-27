import {
  FiBell,
  FiLogOut,
  FiUser
} from "react-icons/fi";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Topbar() {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const user = JSON.parse(
    localStorage.getItem("user")
  );

  const handleLogout = () => {
    logout();
    localStorage.removeItem("workspaceId");
    localStorage.removeItem("selectedTenantId");
    localStorage.removeItem("projectId");
    localStorage.removeItem("channelId");
    localStorage.removeItem("teamId");
    navigate("/login");
  };

  return (
    <header className="bg-white border-b h-16 px-8 flex items-center justify-between">

      {/* Left Side */}
      <div>
        <h2 className="text-lg font-semibold text-gray-800">
          Welcome,
          {" "}
          {user?.name || "User"}
        </h2>
      </div>

      {/* Right Side */}
      <div className="flex items-center gap-6">

        {/* Notifications */}
        <button className="relative text-gray-600 hover:text-indigo-600">
          <FiBell size={22} />

          <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full px-1.5 py-0.5">
            3
          </span>
        </button>

        {/* User Details */}
        <div className="flex items-center gap-3">

          <div className="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600">
            <FiUser size={20} />
          </div>

          <div className="flex flex-col">
            <span className="font-medium text-gray-800">
              {user?.name || "Guest"}
            </span>

            <span className="text-xs text-gray-500 uppercase">
              {user?.role || "User"}
            </span>
          </div>
        </div>

        {/* Logout */}
        <button
          onClick={handleLogout}
          className="flex items-center gap-2 bg-red-50 text-red-600 px-4 py-2 rounded-lg hover:bg-red-100"
        >
          <FiLogOut />
          Logout
        </button>

      </div>
    </header>
  );
}
