import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../api/axios";

export default function TenantCreate() {

  const navigate = useNavigate();

  const [loading, setLoading] =
    useState(false);

  const [form, setForm] = useState({
    name: "",
    contact_email: "",
    phone: "",
    address: "",
    industry: ""
  });

  const submit = async (e) => {

    e.preventDefault();

    try {

      setLoading(true);

      await axios.post(
        "/tenants/",
        form
      );

      navigate("/tenants");

    } catch (err) {

      alert(
        err.response?.data?.detail
      );

    } finally {

      setLoading(false);

    }

  };

  return (
    <div className="p-6">

      <div className="bg-white shadow rounded p-6">

        <h1 className="text-2xl font-bold mb-6">
          Create Tenant
        </h1>

        <form
          onSubmit={submit}
          className="space-y-4"
        >

          <input
            placeholder="Name"
            className="border p-3 rounded w-full"
            onChange={(e) =>
              setForm({
                ...form,
                name: e.target.value
              })
            }
          />

          <input
            placeholder="Email"
            className="border p-3 rounded w-full"
            onChange={(e) =>
              setForm({
                ...form,
                contact_email:
                  e.target.value
              })
            }
          />

          <input
            placeholder="Phone"
            className="border p-3 rounded w-full"
            onChange={(e) =>
              setForm({
                ...form,
                phone: e.target.value
              })
            }
          />

          <input
            placeholder="Address"
            className="border p-3 rounded w-full"
            onChange={(e) =>
              setForm({
                ...form,
                address: e.target.value
              })
            }
          />

          <input
            placeholder="Industry"
            className="border p-3 rounded w-full"
            onChange={(e) =>
              setForm({
                ...form,
                industry: e.target.value
              })
            }
          />

          <button
            className="bg-indigo-600 text-white px-5 py-3 rounded"
            disabled={loading}
          >
            {loading
              ? "Creating..."
              : "Create Tenant"}
          </button>

        </form>

      </div>

    </div>
  );
}