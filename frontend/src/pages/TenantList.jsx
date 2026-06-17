import React, {
  useEffect,
  useState
} from "react";

import { Link } from "react-router-dom";

import axios from "../api/axios";
import PageLayout from "../components/PageLayout";

export default function TenantList() {

  const [tenants, setTenants] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {

    loadTenants();

  }, []);

  const loadTenants = async () => {

    try {

      const res =
        await axios.get(
          "/tenants"
        );

      setTenants(
        res.data
      );

    } catch (err) {

      console.error(
        "Failed to load tenants",
        err
      );

    } finally {

      setLoading(false);

    }

  };

  return (

    <PageLayout>

      <div className="bg-white rounded-2xl border p-6">

        <div className="flex justify-between items-center mb-6">

          <h1 className="text-3xl font-bold">
            Tenant List
          </h1>

          <Link
            to="/tenant-create"
            className="bg-blue-600 text-white px-4 py-2 rounded-xl"
          >
            Create Tenant
          </Link>

        </div>

        {loading ? (

          <p className="text-gray-500">
            Loading tenants...
          </p>

        ) : (

          <table className="w-full">

            <thead>

              <tr className="border-b">

                <th className="text-left p-3">
                  ID
                </th>

                <th className="text-left p-3">
                  Name
                </th>

                <th className="text-left p-3">
                  Email
                </th>

                <th className="text-left p-3">
                  Status
                </th>

                <th className="text-left p-3">
                  Actions
                </th>

              </tr>

            </thead>

            <tbody>

              {tenants.map((tenant) => (

                <tr
                  key={tenant.id}
                  className="border-b"
                >

                  <td className="p-3">
                    {tenant.id}
                  </td>

                  <td className="p-3">
                    {tenant.name}
                  </td>

                  <td className="p-3">
                    {tenant.contact_email}
                  </td>

                  <td className="p-3">
                    {tenant.status}
                  </td>

                  <td className="p-3">

                    <Link
                      to={`/tenants/${tenant.id}`}
                      className="text-blue-600 font-medium"
                      onClick={() => {

                        localStorage.setItem(
                          "selectedTenantId",
                          tenant.id
                        );

                        localStorage.setItem(
                          "selectedTenantName",
                          tenant.name
                        );

                      }}
                    >
                      View
                    </Link>

                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        )}

      </div>

    </PageLayout>

  );

}