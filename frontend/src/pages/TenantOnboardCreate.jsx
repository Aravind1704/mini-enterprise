import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

export default function TenantOnboardCreate() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);

  const [tenant, setTenant] = useState({
    name: "",
    contact_email: "",
    phone: "",
    address: "",
    industry: "",
  });

  const [admin, setAdmin] = useState({
    name: "",
    email: "",
    password: "",
    role: "admin",
  });

  const submit = async (e) => {
    e.preventDefault();

    setLoading(true);

    try {
      const payload = {
        ...tenant,
      };

      const adminPayload = {
        ...admin,
      };

      const res = await api.post("/tenants/onboard/create", {
        tenant: payload,
        admin: adminPayload,
      });

      alert("Tenant and admin created successfully");
      console.log(res.data);
      navigate("/tenants");
    } catch (err) {
      alert(err.response?.data?.detail || "Onboarding failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <div className="bg-white shadow rounded p-6 max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold mb-4">Create Tenant & First Admin</h1>

        <form onSubmit={submit} className="space-y-4">
          <h2 className="font-semibold">Tenant Details</h2>
          <input required placeholder="Organization name" className="border p-3 rounded w-full" value={tenant.name} onChange={(e) => setTenant({ ...tenant, name: e.target.value })} />
          <input required type="email" placeholder="Contact email" className="border p-3 rounded w-full" value={tenant.contact_email} onChange={(e) => setTenant({ ...tenant, contact_email: e.target.value })} />
          <input placeholder="Phone" className="border p-3 rounded w-full" value={tenant.phone} onChange={(e) => setTenant({ ...tenant, phone: e.target.value })} />
          <input placeholder="Address" className="border p-3 rounded w-full" value={tenant.address} onChange={(e) => setTenant({ ...tenant, address: e.target.value })} />
          <input placeholder="Industry" className="border p-3 rounded w-full" value={tenant.industry} onChange={(e) => setTenant({ ...tenant, industry: e.target.value })} />

          <h2 className="font-semibold mt-4">Admin User</h2>
          <input required placeholder="Full name" className="border p-3 rounded w-full" value={admin.name} onChange={(e) => setAdmin({ ...admin, name: e.target.value })} />
          <input required type="email" placeholder="Email" className="border p-3 rounded w-full" value={admin.email} onChange={(e) => setAdmin({ ...admin, email: e.target.value })} />
          <input required type="password" placeholder="Password" className="border p-3 rounded w-full" value={admin.password} onChange={(e) => setAdmin({ ...admin, password: e.target.value })} />

          <div className="flex gap-3">
            <button className="bg-indigo-600 text-white px-4 py-2 rounded" disabled={loading}>{loading ? "Creating..." : "Create & Onboard"}</button>
            <button type="button" onClick={() => navigate('/tenant-create')} className="bg-gray-200 px-4 py-2 rounded">Create Tenant Only</button>
          </div>
        </form>
      </div>
    </div>
  );
}
