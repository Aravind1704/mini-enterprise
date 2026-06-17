import React, {
  useEffect,
  useState,
  useCallback
} from "react";

import axios from "../api/axios";
import PageLayout from "../components/PageLayout";

export default function CollaborationUsage() {

  const [tenants, setTenants] =
    useState([]);

  const [tenantId, setTenantId] =
    useState("");

  const [usage, setUsage] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  useEffect(() => {

    loadTenants();

  }, []);

  const loadTenants = async () => {

    try {

      const res =
        await axios.get("/tenants");

      setTenants(res.data);

    } catch (err) {

      console.error(err);

      setError(
        "Failed to load tenants"
      );

    }

  };

  const loadUsage =
    useCallback(async () => {

      if (!tenantId) {

        setUsage(null);

        return;

      }

      try {

        setLoading(true);

        const res =
          await axios.get(
            `/tenants/${tenantId}/collaboration/usage`
          );

        setUsage(res.data);

        setError("");

      } catch (err) {

        console.error(err);

        setError(
          err.response?.data?.detail ||
          "Failed to load usage"
        );

      } finally {

        setLoading(false);

      }

    }, [tenantId]);

  useEffect(() => {

    loadUsage();

  }, [loadUsage]);

  const recalculateUsage =
    async () => {

      if (!tenantId) {

        alert(
          "Please select a tenant first"
        );

        return;

      }

      try {

        await axios.post(
          `/tenants/${tenantId}/collaboration/recalculate-usage`
        );

        await loadUsage();

        alert(
          "Usage Recalculated"
        );

      } catch (err) {

        alert(
          err.response?.data?.detail ||
          "Failed to recalculate usage"
        );

      }

    };

  return (

    <PageLayout>

      <div className="flex justify-between items-center mb-8">

        <div>

          <h1 className="text-3xl font-bold">
            Collaboration Usage
          </h1>

          <p className="text-gray-500">
            Current tenant usage statistics
          </p>

        </div>

        <button
          onClick={recalculateUsage}
          className="bg-blue-600 text-white px-5 py-3 rounded-xl"
        >
          Recalculate Usage
        </button>

      </div>

      <div className="bg-white p-6 rounded-2xl border mb-8">

        <label className="block font-medium mb-2">
          Select Tenant
        </label>

        <select
          value={tenantId}
          onChange={(e) =>
            setTenantId(
              e.target.value
            )
          }
          className="w-full border p-3 rounded-xl"
        >

          <option value="">
            Select Tenant
          </option>

          {tenants.map((tenant) => (

            <option
              key={tenant.id}
              value={tenant.id}
            >
              {tenant.name}
            </option>

          ))}

        </select>

      </div>

      {loading && (

        <div className="mb-6">
          Loading...
        </div>

      )}

      {error && (

        <div className="bg-red-100 text-red-700 p-4 rounded-xl mb-6">

          {error}

        </div>

      )}

      {usage && (

        <>

          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-8">

            <div className="bg-white p-6 rounded-2xl border">

              <h3 className="text-gray-500">
                Workspaces
              </h3>

              <p className="text-4xl font-bold mt-2">
                {usage.workspace_count}
              </p>

            </div>

            <div className="bg-white p-6 rounded-2xl border">

              <h3 className="text-gray-500">
                Channels
              </h3>

              <p className="text-4xl font-bold mt-2">
                {usage.channel_count}
              </p>

            </div>

            <div className="bg-white p-6 rounded-2xl border">

              <h3 className="text-gray-500">
                Members
              </h3>

              <p className="text-4xl font-bold mt-2">
                {usage.member_count}
              </p>

            </div>

            <div className="bg-white p-6 rounded-2xl border">

              <h3 className="text-gray-500">
                Storage Used
              </h3>

              <p className="text-4xl font-bold mt-2">
                {usage.storage_used_mb}
              </p>

              <p className="text-gray-400 text-sm">
                MB
              </p>

            </div>

          </div>

          <div className="bg-white rounded-2xl border p-6">

            <h2 className="text-xl font-semibold mb-4">
              Usage Details
            </h2>

            <table className="w-full">

              <tbody>

                <tr className="border-b">
                  <td className="py-3">
                    Workspace Count
                  </td>
                  <td>
                    {usage.workspace_count}
                  </td>
                </tr>

                <tr className="border-b">
                  <td className="py-3">
                    Channel Count
                  </td>
                  <td>
                    {usage.channel_count}
                  </td>
                </tr>

                <tr className="border-b">
                  <td className="py-3">
                    Member Count
                  </td>
                  <td>
                    {usage.member_count}
                  </td>
                </tr>

                <tr>
                  <td className="py-3">
                    Storage Used
                  </td>
                  <td>
                    {usage.storage_used_mb} MB
                  </td>
                </tr>

              </tbody>

            </table>

          </div>

        </>

      )}

    </PageLayout>

  );

}