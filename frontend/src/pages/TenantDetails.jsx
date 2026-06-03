import React, {
  useEffect,
  useState
} from "react";

import {
  useParams,
  Link
} from "react-router-dom";

import axios from "../api/axios";

export default function TenantDetails() {

  const { id } = useParams();

  const [tenant, setTenant] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  useEffect(() => {

    const loadTenant = async () => {

      try {

        const res =
          await axios.get(
            `/tenants/${id}`
          );

        setTenant(
          res.data
        );

      } catch (err) {

        console.error(err);

        setError(
          "Failed to load tenant"
        );

      } finally {

        setLoading(false);

      }

    };

    loadTenant();

  }, [id]);

  if (loading) {

    return (
      <div className="p-6">
        Loading...
      </div>
    );

  }

  if (error) {

    return (
      <div className="p-6">
        <div className="bg-red-100 text-red-700 p-4 rounded">
          {error}
        </div>
      </div>
    );

  }

  if (!tenant) {

    return (
      <div className="p-6">
        Tenant not found
      </div>
    );

  }

  return (

    <div className="p-6">

      <div className="bg-white shadow rounded-xl p-6">

        <div className="flex justify-between items-center">

          <div>

            <h1 className="text-3xl font-bold">
              {tenant.name}
            </h1>

            <p className="text-gray-500">
              Tenant ID: {tenant.id}
            </p>

          </div>

          <Link
            to="/tenant-onboarding"
            className="bg-green-600 text-white px-4 py-2 rounded"
          >
            Onboard
          </Link>

        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">

          <div>
            <p className="font-semibold">
              Email
            </p>

            <p>
              {tenant.contact_email}
            </p>
          </div>

          <div>
            <p className="font-semibold">
              Phone
            </p>

            <p>
              {tenant.phone || "-"}
            </p>
          </div>

          <div>
            <p className="font-semibold">
              Industry
            </p>

            <p>
              {tenant.industry || "-"}
            </p>
          </div>

          <div>
            <p className="font-semibold">
              Status
            </p>

            <p>
              {tenant.status}
            </p>
          </div>

          <div>
            <p className="font-semibold">
              Address
            </p>

            <p>
              {tenant.address || "-"}
            </p>
          </div>

          <div>
            <p className="font-semibold">
              Slug
            </p>

            <p>
              {tenant.slug}
            </p>
          </div>

        </div>

        <div className="flex flex-wrap gap-4 mt-8">

          <Link
            to={`/tenants/${tenant.id}/settings`}
            className="bg-indigo-600 text-white px-5 py-2 rounded"
          >
            Collaboration Settings
          </Link>

          <Link
            to={`/tenants/${tenant.id}/usage`}
            className="bg-blue-600 text-white px-5 py-2 rounded"
          >
            Collaboration Usage
          </Link>

        </div>

      </div>

    </div>

  );

}