import React, { useState } from "react";
import axios from "../api/axios";
import PageLayout from "../components/PageLayout";
import { useNavigate } from "react-router-dom";

export default function TenantCreate() {

  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    slug: "",
    contact_email: "",
    phone: "",
    address: "",
    industry: ""
  });

  const [loading, setLoading] = useState(false);

  const submit = async (e) => {

    e.preventDefault();

    try {

      setLoading(true);

      await axios.post(
        "/tenants",
        form
      );

      alert(
        "Tenant Created Successfully"
      );

      navigate("/tenants");

    } catch (err) {

      alert(
        err.response?.data?.detail ||
        "Failed to create tenant"
      );

    } finally {

      setLoading(false);
    }
  };

  return (

    <PageLayout>

      <div className="bg-white p-8 rounded-2xl border">

        <h1 className="text-3xl font-bold mb-8">
          Create Tenant
        </h1>

        <form
          onSubmit={submit}
          className="space-y-4"
        >

          <input
            className="w-full border p-3 rounded-xl"
            placeholder="Tenant Name"
            value={form.name}
            onChange={(e) =>
              setForm({
                ...form,
                name: e.target.value
              })
            }
            required
          />

          <input
            className="w-full border p-3 rounded-xl"
            placeholder="Tenant Slug"
            value={form.slug}
            onChange={(e) =>
              setForm({
                ...form,
                slug: e.target.value
              })
            }
            required
          />

          <input
            className="w-full border p-3 rounded-xl"
            placeholder="Contact Email"
            value={form.contact_email}
            onChange={(e) =>
              setForm({
                ...form,
                contact_email: e.target.value
              })
            }
            required
          />

          <input
            className="w-full border p-3 rounded-xl"
            placeholder="Phone"
            value={form.phone}
            onChange={(e) =>
              setForm({
                ...form,
                phone: e.target.value
              })
            }
          />

          <input
            className="w-full border p-3 rounded-xl"
            placeholder="Address"
            value={form.address}
            onChange={(e) =>
              setForm({
                ...form,
                address: e.target.value
              })
            }
          />

          <input
            className="w-full border p-3 rounded-xl"
            placeholder="Industry"
            value={form.industry}
            onChange={(e) =>
              setForm({
                ...form,
                industry: e.target.value
              })
            }
          />

          <button
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-3 rounded-xl"
          >
            {loading
              ? "Creating..."
              : "Create Tenant"}
          </button>

        </form>

      </div>

    </PageLayout>

  );
}