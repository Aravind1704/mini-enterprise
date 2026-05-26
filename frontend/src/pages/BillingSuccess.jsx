import { Link } from "react-router-dom";


export default function BillingSuccess() {

  return (

    <div className="
      min-h-screen
      flex
      items-center
      justify-center
      bg-gray-100
    ">

      <div className="
        bg-white
        p-12
        rounded-3xl
        shadow-xl
        text-center
      ">

        <h1 className="
          text-5xl
          font-black
          text-green-600
          mb-6
        ">

          ✅ Payment Successful

        </h1>


        <p className="
          text-gray-500
          text-xl
          mb-8
        ">

          Your plan has been upgraded.

        </p>


        <Link

          to="/dashboard"

          className="
            bg-indigo-600
            hover:bg-indigo-700
            text-white
            px-8
            py-4
            rounded-2xl
            font-bold
          "
        >

          Back to Dashboard

        </Link>

      </div>

    </div>
  );
}