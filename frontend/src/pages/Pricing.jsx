import React, {
  useState,
  useEffect
} from "react";

import axios from "axios";

import {
  ArrowLeft,
  CreditCard,
  Crown,
  Zap,
  CheckCircle
} from "lucide-react";


function Pricing() {

  // =====================================================
  // SUBSCRIPTION STATE
  // =====================================================

  const [credits, setCredits] =
    useState(0);

  const [currentPlan, setCurrentPlan] =
    useState("No Plan");

  const [loading, setLoading] =
    useState(false);

  // =====================================================
  // FETCH SUBSCRIPTION
  // =====================================================

  useEffect(() => {

    fetchSubscription();

    // =========================================
    // AUTO REFRESH EVERY 3 SECONDS
    // =========================================

    const interval = setInterval(() => {

      fetchSubscription();

    }, 3000);

    return () => clearInterval(interval);

  }, []);


  // =====================================================
  // FETCH CURRENT SUBSCRIPTION
  // =====================================================

  const fetchSubscription = async () => {

    try {

      const response = await axios.get(

        "http://127.0.0.1:8000/subscriptions/current"
      );

      setCurrentPlan(

        response.data.plan || "No Plan"
      );

      setCredits(

        response.data.credits || 0
      );

    } catch (error) {

      console.error(error);
    }
  };


  // =====================================================
  // STRIPE CHECKOUT
  // =====================================================

  const handleCheckout = async (plan) => {

    try {

      setLoading(true);

      const response = await axios.get(

        `http://127.0.0.1:8000/billing/checkout/${plan}`
      );

      // =====================================
      // REDIRECT TO STRIPE
      // =====================================

      window.location.href =
        response.data.checkout_url;

    } catch (error) {

      console.error(error);

      alert("Checkout failed");

    } finally {

      setLoading(false);
    }
  };


  // =====================================================
  // BACK BUTTON
  // =====================================================

  const goBack = () => {

    window.history.back();
  };


  // =====================================================
  // PLAN CARD COMPONENT
  // =====================================================

  const PlanCard = ({
    title,
    price,
    creditsIncluded,
    features,
    buttonText,
    planKey,
    popular,
    icon
  }) => (

    <div
      style={{
        background: "#fff",
        borderRadius: "24px",
        padding: "32px",
        width: "320px",
        boxShadow:
          "0px 10px 30px rgba(0,0,0,0.08)",
        border: popular
          ? "2px solid #6366F1"
          : "1px solid #E5E7EB",
        position: "relative",
        transition: "0.3s"
      }}
    >

      {/* ================================= */}
      {/* POPULAR BADGE */}
      {/* ================================= */}

      {popular && (

        <div
          style={{
            position: "absolute",
            top: "-12px",
            right: "20px",
            background: "#6366F1",
            color: "#fff",
            padding: "6px 14px",
            borderRadius: "20px",
            fontSize: "12px",
            fontWeight: "bold"
          }}
        >
          MOST POPULAR
        </div>
      )}

      {/* ================================= */}
      {/* TITLE */}
      {/* ================================= */}

      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "10px"
        }}
      >

        {icon}

        <h2>{title}</h2>
      </div>

      {/* ================================= */}
      {/* PRICE */}
      {/* ================================= */}

      <h1
        style={{
          marginTop: "20px",
          fontSize: "42px"
        }}
      >
        ₹{price}
      </h1>

      <p
        style={{
          color: "#6B7280"
        }}
      >
        / month
      </p>

      {/* ================================= */}
      {/* CREDITS */}
      {/* ================================= */}

      <div
        style={{
          marginTop: "20px",
          background: "#F3F4F6",
          padding: "14px",
          borderRadius: "14px"
        }}
      >
        <strong>
          Credits Included
        </strong>

        <p
          style={{
            marginTop: "8px"
          }}
        >
          {creditsIncluded} Credits
        </p>
      </div>

      {/* ================================= */}
      {/* FEATURES */}
      {/* ================================= */}

      <div
        style={{
          marginTop: "24px"
        }}
      >

        {features.map((feature, index) => (

          <div
            key={index}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "10px",
              marginBottom: "14px"
            }}
          >

            <CheckCircle
              size={18}
              color="#10B981"
            />

            <span>{feature}</span>
          </div>
        ))}
      </div>

      {/* ================================= */}
      {/* BUTTON */}
      {/* ================================= */}

      <button

        onClick={() =>
          handleCheckout(planKey)
        }

        disabled={loading}

        style={{
          marginTop: "30px",
          width: "100%",
          padding: "14px",
          borderRadius: "14px",
          border: "none",
          background: "#111827",
          color: "#fff",
          fontSize: "16px",
          cursor: "pointer",
          fontWeight: "bold"
        }}
      >

        {loading
          ? "Redirecting..."
          : buttonText}

      </button>
    </div>
  );


  // =====================================================
  // UI
  // =====================================================

  return (

    <div
      style={{
        minHeight: "100vh",
        background: "#F9FAFB",
        padding: "40px"
      }}
    >

      {/* ========================================= */}
      {/* TOP BAR */}
      {/* ========================================= */}

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "40px"
        }}
      >

        <button

          onClick={goBack}

          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            background: "#fff",
            border: "1px solid #E5E7EB",
            padding: "10px 18px",
            borderRadius: "12px",
            cursor: "pointer"
          }}
        >

          <ArrowLeft size={18} />

          Back
        </button>

        <h1
          style={{
            fontSize: "38px"
          }}
        >
          Pricing & Subscription
        </h1>

        <div />
      </div>


      {/* ========================================= */}
      {/* CURRENT SUBSCRIPTION */}
      {/* ========================================= */}

      <div
        style={{
          display: "flex",
          gap: "20px",
          marginBottom: "40px"
        }}
      >

        {/* CURRENT PLAN */}

        <div
          style={{
            flex: 1,
            background: "#fff",
            borderRadius: "24px",
            padding: "25px",
            boxShadow:
              "0px 10px 20px rgba(0,0,0,0.05)"
          }}
        >

          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "10px"
            }}
          >

            <Crown color="#F59E0B" />

            <h2>Current Subscription</h2>
          </div>

          <h1
            style={{
              marginTop: "20px",
              color: "#6366F1"
            }}
          >
            {currentPlan}
          </h1>

          <p
            style={{
              color: "#6B7280"
            }}
          >
            Active Subscription Plan
          </p>
        </div>


        {/* CREDIT WALLET */}

        <div
          style={{
            flex: 1,
            background: "#fff",
            borderRadius: "24px",
            padding: "25px",
            boxShadow:
              "0px 10px 20px rgba(0,0,0,0.05)"
          }}
        >

          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "10px"
            }}
          >

            <CreditCard color="#10B981" />

            <h2>Credit Wallet</h2>
          </div>

          <h1
            style={{
              marginTop: "20px",
              color: "#10B981"
            }}
          >
            {credits} Credits
          </h1>

          <p
            style={{
              color: "#6B7280"
            }}
          >
            Credits are used for AI tasks,
            analytics, reports, and premium
            features.
          </p>
        </div>
      </div>


      {/* ========================================= */}
      {/* PLANS */}
      {/* ========================================= */}

      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: "30px",
          flexWrap: "wrap"
        }}
      >

        <PlanCard
          title="Basic"
          price="499"
          creditsIncluded="100"
          planKey="basic"
          buttonText="Choose Basic"
          icon={<Zap color="#6366F1" />}
          features={[
            "100 Monthly Credits",
            "Task Management",
            "Email Support",
            "Basic Analytics"
          ]}
        />

        <PlanCard
          title="Silver"
          price="1499"
          creditsIncluded="500"
          planKey="silver"
          popular={true}
          buttonText="Choose Silver"
          icon={<Crown color="#6366F1" />}
          features={[
            "500 Monthly Credits",
            "Advanced Analytics",
            "AI Task Insights",
            "Priority Support",
            "Kanban Board"
          ]}
        />

        <PlanCard
          title="Gold"
          price="3999"
          creditsIncluded="2000"
          planKey="gold"
          buttonText="Choose Gold"
          icon={<CreditCard color="#6366F1" />}
          features={[
            "2000 Monthly Credits",
            "Unlimited AI Features",
            "Team Management",
            "Audit Logs",
            "Enterprise Security",
            "24/7 Support"
          ]}
        />
      </div>
    </div>
  );
}

export default Pricing;