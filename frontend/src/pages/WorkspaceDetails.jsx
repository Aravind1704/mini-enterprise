import React, {
  useEffect,
  useState
} from "react";

import {
  useParams,
  Link
} from "react-router-dom";

import axios from "../api/axios";

export default function WorkspaceDetails() {

  const { id } = useParams();

  const [workspace, setWorkspace] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  useEffect(() => {

    const fetchWorkspace = async () => {

      try {

        const res =
          await axios.get(
            `/workspaces/${id}`
          );

        setWorkspace(
          res.data
        );

      } catch (err) {

        console.error(err);

        setError(
          err.response?.data?.detail ||
          "Failed to load workspace"
        );

      } finally {

        setLoading(false);

      }

    };

    if (id) {

      fetchWorkspace();

    }

  }, [id]);

  if (loading) {

    return (

      <div className="p-6">

        <div className="bg-white rounded-xl shadow p-6">

          Loading Workspace...

        </div>

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

  if (!workspace) {

    return (

      <div className="p-6">

        <div className="bg-yellow-100 text-yellow-700 p-4 rounded">

          Workspace Not Found

        </div>

      </div>

    );

  }

  return (

    <div className="p-6">

      <div className="bg-white rounded-xl shadow-lg p-8">

        <div className="flex justify-between items-center mb-8">

          <div>

            <h1 className="text-3xl font-bold">

              {workspace.name}

            </h1>

            <p className="text-gray-500 mt-1">

              Workspace ID: {workspace.id}

            </p>

          </div>

          <Link
            to={`/workspace-members/${workspace.id}`}
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2 rounded-lg"
          >
            View Members
          </Link>

        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

          <div>

            <h3 className="font-semibold text-gray-600">
              Tenant ID
            </h3>

            <p>
              {workspace.tenant_id}
            </p>

          </div>

          <div>

            <h3 className="font-semibold text-gray-600">
              Visibility
            </h3>

            <p>
              {workspace.visibility}
            </p>

          </div>

          <div>

            <h3 className="font-semibold text-gray-600">
              Description
            </h3>

            <p>
              {workspace.description || "-"}
            </p>

          </div>

          <div>

            <h3 className="font-semibold text-gray-600">
              Slug
            </h3>

            <p>
              {workspace.slug || "-"}
            </p>

          </div>

          <div>

            <h3 className="font-semibold text-gray-600">
              Created By
            </h3>

            <p>
              {workspace.created_by}
            </p>

          </div>

          <div>

            <h3 className="font-semibold text-gray-600">
              Archived
            </h3>

            <p>
              {workspace.is_archived
                ? "Yes"
                : "No"}
            </p>

          </div>

          <div>

            <h3 className="font-semibold text-gray-600">
              Created At
            </h3>

            <p>
              {workspace.created_at}
            </p>

          </div>

          <div>

            <h3 className="font-semibold text-gray-600">
              Updated At
            </h3>

            <p>
              {workspace.updated_at}
            </p>

          </div>

        </div>

      </div>

    </div>

  );

}