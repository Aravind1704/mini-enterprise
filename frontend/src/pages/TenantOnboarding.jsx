import React, {
  useState,
  useEffect
} from "react";

import axios from "../api/axios";
import PageLayout from "../components/PageLayout";

export default function TenantOnboarding() {
  const [form, setForm] = useState({
    tenant_id: "",
    admin_user_id: ""
  });

  const [tenants, setTenants] = useState([]);
  const [admins, setAdmins] = useState([]);

  useEffect(() => {
    loadTenants();
    loadAdmins();
  }, []);

  const loadTenants = async () => {

    try {

      const res = await axios.get(
        "/super-admin/tenants"
      );

      setTenants(res.data);

    } catch (err) {

      console.error(
        "Failed to load tenants",
        err
      );

    }
  };

  const loadAdmins = async () => {

    try {

      const res = await axios.get(
        "/super-admin/tenant-admins"
      );

      setAdmins(res.data);

    } catch (err) {

      console.error(
        "Failed to load tenant admins",
        err
      );

    }
  };

  const submit = async (e) => {

    e.preventDefault();

    try {

      await axios.post(
        "/tenants/onboard",
        null,
        {
          params: {
            tenant_id: form.tenant_id,
            admin_user_id: form.admin_user_id
          }
        }
      );

      alert(
        "Tenant Onboarding Completed"
      );

      setForm({
        tenant_id: "",
        admin_user_id: ""
      });

    } catch (err) {

      alert(
        err.response?.data?.detail ||
        "Onboarding Failed"
      );

    }
  };

  return (

    <PageLayout>

      <div className="space-y-6">

        {/* Onboarding Form */}

        <div className="bg-white p-8 rounded-2xl border shadow">

          <h1 className="text-3xl font-bold mb-8">
            Tenant Onboarding
          </h1>

          <form
            onSubmit={submit}
            className="space-y-4"
          >

            <input
              className="w-full border p-3 rounded-xl"
              placeholder="Tenant ID"
              value={form.tenant_id}
              onChange={(e) =>
                setForm({
                  ...form,
                  tenant_id: e.target.value
                })
              }
              required
            />

            <input
              className="w-full border p-3 rounded-xl"
              placeholder="Admin User ID"
              value={form.admin_user_id}
              onChange={(e) =>
                setForm({
                  ...form,
                  admin_user_id: e.target.value
                })
              }
              required
            />

            <button
              className="bg-blue-600 text-white px-6 py-3 rounded-xl"
            >
              Complete Onboarding
            </button>

          </form>

        </div>

        {/* Tenant List */}

        <div className="bg-white p-6 rounded-2xl border shadow">

          <h2 className="text-2xl font-bold mb-4">
            Existing Tenants
          </h2>

          <table className="w-full border">

            <thead>

              <tr className="bg-gray-100">

                <th className="border p-2">ID</th>
                <th className="border p-2">Name</th>
                <th className="border p-2">Slug</th>
                <th className="border p-2">Email</th>
                <th className="border p-2">Industry</th>

              </tr>

            </thead>

            <tbody>

              {tenants.map((tenant) => (

                <tr key={tenant.id}>

                  <td className="border p-2">
                    {tenant.id}
                  </td>

                  <td className="border p-2">
                    {tenant.name}
                  </td>

                  <td className="border p-2">
                    {tenant.slug}
                  </td>

                  <td className="border p-2">
                    {tenant.contact_email}
                  </td>

                  <td className="border p-2">
                    {tenant.industry}
                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

        {/* Tenant Admin List */}

        <div className="bg-white p-6 rounded-2xl border shadow">

          <h2 className="text-2xl font-bold mb-4">
            Existing Tenant Admins
          </h2>

          <table className="w-full border">

            <thead>

              <tr className="bg-gray-100">

                <th className="border p-2">ID</th>
                <th className="border p-2">Name</th>
                <th className="border p-2">Email</th>
                <th className="border p-2">Tenant ID</th>
                <th className="border p-2">Role</th>

              </tr>

            </thead>

            <tbody>

              {admins.map((admin) => (

                <tr key={admin.id}>

                  <td className="border p-2">
                    {admin.id}
                  </td>

                  <td className="border p-2">
                    {admin.name}
                  </td>

                  <td className="border p-2">
                    {admin.email}
                  </td>

                  <td className="border p-2">
                    {admin.tenant_id}
                  </td>

                  <td className="border p-2">
                    {admin.role}
                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      </div>

    </PageLayout>

  );
}
