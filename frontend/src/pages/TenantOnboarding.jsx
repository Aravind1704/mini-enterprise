import React, {
  useState
} from "react";

import axios from "../api/axios";

export default function TenantOnboarding() {

  const [tenantId, setTenantId] =
    useState("");

  const [adminUserId,
    setAdminUserId] =
    useState("");

  const [status, setStatus] =
    useState(null);

  const onboard = async () => {

    try {

      const res =
        await axios.post(
          `/tenants/onboard?tenant_id=${tenantId}&admin_user_id=${adminUserId}`
        );

      alert(
        "Tenant Onboarded"
      );

      console.log(res.data);

    } catch (err) {

      alert(
        err.response?.data?.detail
      );

    }

  };

  const getStatus = async () => {

    try {

      const res =
        await axios.get(
          `/tenants/${tenantId}/onboarding-status`
        );

      setStatus(
        res.data
      );

    } catch (err) {

      console.log(err);

    }

  };

  return (
    <div className="p-6">

      <div className="bg-white shadow rounded p-6">

        <h1 className="text-2xl font-bold mb-5">
          Tenant Onboarding
        </h1>

        <input
          placeholder="Tenant ID"
          className="border p-3 rounded w-full mb-4"
          value={tenantId}
          onChange={(e) =>
            setTenantId(
              e.target.value
            )
          }
        />

        <input
          placeholder="Admin User ID"
          className="border p-3 rounded w-full mb-4"
          value={adminUserId}
          onChange={(e) =>
            setAdminUserId(
              e.target.value
            )
          }
        />

        <div className="flex gap-3">

          <button
            onClick={onboard}
            className="bg-green-600 text-white px-4 py-2 rounded"
          >
            Onboard
          </button>

          <button
            onClick={getStatus}
            className="bg-indigo-600 text-white px-4 py-2 rounded"
          >
            Check Status
          </button>

        </div>

        {status && (

          <div className="mt-5 bg-gray-100 p-4 rounded">

            <pre>
              {JSON.stringify(
                status,
                null,
                2
              )}
            </pre>

          </div>

        )}

      </div>

    </div>
  );
}