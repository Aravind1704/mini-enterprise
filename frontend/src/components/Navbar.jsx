import { Link, useNavigate } from "react-router-dom";

import {
  Bell,
  Crown,
  Sparkles
} from "lucide-react";
export default function Navbar({

  user,

  aiData,

  currentPlan = "Silver",

  credits = 600,

  showSummary = true

}) {

  const navigate = useNavigate();

  const handleLogout = () => {

    localStorage.removeItem("token");

    localStorage.removeItem("access_token");

    navigate("/login");

  };

  if (!user) return null;

  return (

    <>

      {/* TOP NAVBAR */}

      <nav className="bg-indigo-600 shadow-lg px-8 py-4 flex justify-between items-center text-white">

        {/* LEFT */}

        <div>

          <h1 className="text-3xl font-extrabold">
            EnterpriseFlow
          </h1>

          <p className="text-xs text-indigo-200 mt-1">
            {user.name} • {user.role}
          </p>

        </div>
         

        {/* MENU */}
        
              

        <div className="flex items-center gap-6 font-semibold">

          <Link to="/dashboard" className="hover:text-indigo-200">
            Dashboard
          </Link>

          <Link to="/kanban" className="hover:text-indigo-200">
            Kanban
          </Link>

          <Link to="/approvals" className="hover:text-indigo-200">
            Approvals
          </Link>

          <Link to="/analytics" className="hover:text-indigo-200">
            Analytics
          </Link>

          <Link to="/documents" className="hover:text-indigo-200">
            Documents
          </Link>

          <Link to="/ai-insights" className="hover:text-indigo-200">
            AI
          </Link>
           {/* SLA Links - Only for Admin/Manager */}
            {(user?.role === "admin" || user?.role === "manager") && (
            <>
              <Link 
                to="/sla-dashboard" 
                className="hover:text-indigo-200"
              >
                SLA Dashboard
              </Link>

              <Link 
                to="/sla-rules" 
                className="hover:text-indigo-200"
              >
                SLA Rules
              </Link>
            </>
          )}
            
            <Link

            to="/pricing"

            className="
                bg-yellow-400
                hover:bg-yellow-500
                text-black
                px-4
                py-2
                rounded-xl
                font-bold
                transition
            "
            >
          
            Upgrade

            </Link>
          {/* BELL */}
          
          <Link
            to="/notifications"
            className="relative"
          >

            <Bell size={22} />

            {aiData?.unread_notifications > 0 && (

              <span
                className="
                  absolute
                  -top-2
                  -right-2
                  bg-red-500
                  text-white
                  text-[10px]
                  w-5
                  h-5
                  rounded-full
                  flex
                  items-center
                  justify-center
                "
              >
                {aiData.unread_notifications}
              </span>

            )}

          </Link>

          {/* LOGOUT */}

          <button
            onClick={handleLogout}
            className="
              bg-red-500
              hover:bg-red-600
              px-4
              py-2
              rounded-lg
            "
          >
            Logout
          </button>

        </div>

      </nav>



      {/* PLAN + AI */}

      {showSummary && (
        <div className="max-w-7xl mx-auto px-8 mt-6 grid grid-cols-1 lg:grid-cols-2 gap-6">

          {/* PLAN */}

          <div className="bg-white rounded-2xl shadow-md p-6 flex items-center gap-4">

          <div className="bg-yellow-100 p-4 rounded-xl">

            <Crown className="text-yellow-500" size={28} />

          </div>

          <div>

            <h3 className="font-bold text-lg">
              {currentPlan} Plan
            </h3>

            <p className="text-indigo-600 font-semibold">
              {credits} AI Credits Remaining
            </p>

          </div>

        </div>


        {/* AI SUMMARY */}

        <div
          className="
            bg-gradient-to-r
            from-indigo-600
            via-purple-600
            to-pink-600
            rounded-2xl
            shadow-xl
            p-6
            text-white
            flex
            items-center
            gap-5
          "
        >

          <div className="bg-white/20 p-4 rounded-xl">

            <Sparkles size={32} />

          </div>

          <div>

            <h3 className="font-bold text-lg">
              AI ASSISTANT SUMMARY
            </h3>

            <p className="text-sm mt-2 leading-relaxed">
              Your workflow efficiency improved by 18%.
              No critical tasks are overdue.
              AI recommends prioritizing approval reviews today.
            </p>

          </div>

          </div>

        </div>
      )}

    </>

  );

}