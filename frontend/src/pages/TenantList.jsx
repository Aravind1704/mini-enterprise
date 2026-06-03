import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "../api/axios";

export default function TenantList() {

  const [tenants, setTenants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetchTenants();
  }, []);

  const fetchTenants = async () => {
    try {

      const res = await axios.get("/tenants/");

      setTenants(res.data);

    } catch (err) {

      console.log(err);

    } finally {

      setLoading(false);

    }
  };

  const filtered = tenants.filter(
    (tenant) =>
      tenant.name
        ?.toLowerCase()
        .includes(search.toLowerCase())
  );

  return (
    <div className="p-6">

      <div className="flex justify-between mb-6">

        <h1 className="text-3xl font-bold">
          Tenants
        </h1>

        <Link
          to="/tenants/create"
          className="bg-indigo-600 text-white px-4 py-2 rounded"
        >
          Create Tenant
        </Link>

      </div>

      <input
        type="text"
        placeholder="Search Tenant"
        className="border p-2 rounded w-full mb-4"
        value={search}
        onChange={(e) =>
          setSearch(e.target.value)
        }
      />

      <div className="bg-white shadow rounded">

        {loading ? (
          <p className="p-5">
            Loading...
          </p>
        ) : (
          <table className="w-full">

            <thead className="bg-gray-100">

              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Status</th>
                <th>Action</th>
              </tr>

            </thead>

            <tbody>

              {filtered.map((tenant) => (

                <tr
                  key={tenant.id}
                  className="border-b"
                >
                  <td>{tenant.id}</td>

                  <td>{tenant.name}</td>

                  <td>
                    {tenant.contact_email}
                  </td>

                  <td>
                    {tenant.status}
                  </td>

                  <td>

                    <Link
                      to={`/tenants/${tenant.id}`}
                      className="text-blue-600"
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

    </div>
  );
}