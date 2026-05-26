import { Link } from "react-router-dom";


export default function BillingCancel() {

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
          text-red-600
          mb-6
        ">

          ❌ Payment Cancelled

        </h1>


        <p className="
          text-gray-500
          text-xl
          mb-8
        ">

          Your payment was cancelled.

        </p>


        <Link

          to="/pricing"

          className="
            bg-red-500
            hover:bg-red-600
            text-white
            px-8
            py-4
            rounded-2xl
            font-bold
          "
        >

          Try Again

        </Link>

      </div>

    </div>
  );
}