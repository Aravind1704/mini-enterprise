import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "../api/axios";

export default function WorkspaceList() {
  const [workspaces, setWorkspaces] = useState([]);
  const [tenantId] = useState(1);
  const [loading, setLoading] = useState(false);
useEffect(() => {

  const fetchWorkspaces = async () => {

    try {

      setLoading(true);

      const res = await axios.get(
        `/workspaces?tenant_id=${tenantId}`
      );

      setWorkspaces(res.data);

    } catch (err) {

      console.error(err);

    } finally {

      setLoading(false);

    }

  };

  fetchWorkspaces();

}, [tenantId]);

  

  return (
    <div className="p-6">

      <div className="flex justify-between mb-6">

        <h1 className="text-3xl font-bold">
          Workspaces
        </h1>

        <Link
          to="/workspace-create"
          className="bg-indigo-600 text-white px-4 py-2 rounded"
        >
          Create Workspace
        </Link>

      </div>

      <div className="bg-white rounded shadow">

        {loading ? (
          <div className="p-6">
            Loading...
          </div>
        ) : (
          <table className="w-full">

            <thead className="bg-gray-100">
              <tr>
                <th className="p-3">ID</th>
                <th>Name</th>
                <th>Visibility</th>
                <th>Status</th>
                <th></th>
              </tr>
            </thead>

            <tbody>

              {workspaces.map((workspace) => (
                <tr
                  key={workspace.id}
                  className="border-t"
                >
                  <td className="p-3">
                    {workspace.id}
                  </td>

                  <td>{workspace.name}</td>

                  <td>
                    {workspace.visibility}
                  </td>

                  <td>
                    {workspace.is_archived
                      ? "Archived"
                      : "Active"}
                  </td>

                  <td>

                    <Link
                      to={`/workspace-details/${workspace.id}`}
                      className="text-indigo-600"
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