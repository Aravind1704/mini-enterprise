import Navbar from "../components/Navbar";

function Billing() {

  return (

    <div className="min-h-screen bg-gray-100">

      <Navbar />

      <div className="p-8">

        <h1 className="text-4xl font-bold mb-8">
          💰 Billing Dashboard
        </h1>

        <div className="bg-white rounded-2xl shadow-lg p-8">

          <h2 className="text-2xl font-bold mb-4">
            Current Plan
          </h2>

          <p className="text-lg mb-2">
            Gold Plan
          </p>

          <p className="text-gray-600 mb-6">
            Next billing date: June 15, 2026
          </p>

          <button
            className="bg-red-500 text-white px-6 py-3 rounded-xl hover:bg-red-600 transition"
          >
            Cancel Subscription
          </button>

        </div>

      </div>

    </div>
  );
}

export default Billing;