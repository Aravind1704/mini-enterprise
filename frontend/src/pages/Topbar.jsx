export default function Topbar() {

  return (

    <header className="bg-white border-b h-16 flex items-center justify-between px-8">

      <div />

      <div className="flex items-center gap-4">

        <button>
          🔔
        </button>

        <div className="w-10 h-10 rounded-full bg-indigo-700 text-white flex items-center justify-center">
          SA
        </div>

        <span className="font-semibold">
          Super Admin
        </span>

      </div>

    </header>

  );
}