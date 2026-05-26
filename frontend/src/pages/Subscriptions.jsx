import axios from "axios";

export default function Subscriptions() {

  const handleUpgrade =
    async () => {

    const res =
      await axios.get(
        "http://127.0.0.1:8000/billing/checkout"
      );

    window.location.href =
      res.data.checkout_url;
  };


  return (

    <div className="
      min-h-screen
      bg-black
      text-white
      flex
      items-center
      justify-center
    ">

      <button

        onClick={handleUpgrade}

        className="
          bg-yellow-400
          text-black
          px-10
          py-5
          rounded-2xl
          text-2xl
          font-black
        "
      >

        Upgrade to Gold

      </button>

    </div>
  );
}