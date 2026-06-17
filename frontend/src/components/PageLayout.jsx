import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

export default function PageLayout({ children }) {
  return (
    <div className="min-h-screen bg-slate-50">
      <Topbar />

      <div className="flex">
        <Sidebar />

        <main className="flex-1 p-8">
          {children}
        </main>
      </div>
    </div>
  );
}