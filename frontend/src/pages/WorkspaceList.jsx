import React, { useEffect, useState } from "react";
import {
  Link,
  useNavigate
} from "react-router-dom";

import {
  FiSearch,
  FiEye,
  FiEdit,
  FiPlus,
  FiUsers,
  FiMessageSquare
} from "react-icons/fi";

import axios from "../api/axios";
import PageLayout from "../components/PageLayout";

export default function WorkspaceList() {
  const navigate = useNavigate();

  const [workspaces, setWorkspaces] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadWorkspaces();
  }, []);

  const loadWorkspaces = async () => {
    try {
      setLoading(true);

      const res = await axios.get("/workspaces");

      setWorkspaces(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filtered = workspaces.filter((workspace) =>
    workspace.name
      ?.toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <PageLayout>
      {/* Header */}

      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold">
            Workspace List
          </h1>

          <p className="text-gray-500">
            Manage all workspaces
          </p>
        </div>

        <Link
          to="/workspace-create"
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-3 rounded-xl flex items-center gap-2"
        >
          <FiPlus />
          Create Workspace
        </Link>
      </div>

      {/* Search */}

      <div className="bg-white rounded-2xl border p-5 mb-6">
        <div className="relative">
          <FiSearch
            className="absolute left-4 top-4 text-gray-400"
          />

          <input
            className="w-full border rounded-xl pl-12 pr-4 py-3"
            placeholder="Search workspace..."
            value={search}
            onChange={(e) =>
              setSearch(e.target.value)
            }
          />
        </div>
      </div>

      {/* Table */}

      <div className="bg-white rounded-2xl border overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-50">
            <tr>
              <th className="text-left p-4">
                ID
              </th>

              <th className="text-left p-4">
                Name
              </th>

              <th className="text-left p-4">
                Visibility
              </th>

              <th className="text-left p-4">
                Members
              </th>

              <th className="text-left p-4">
                Status
              </th>

              <th className="text-left p-4">
                Actions
              </th>
            </tr>
          </thead>

          <tbody>
            {loading && (
              <tr>
                <td
                  colSpan="6"
                  className="text-center p-8"
                >
                  Loading Workspaces...
                </td>
              </tr>
            )}

            {!loading &&
              filtered.map((workspace) => (
                <tr
                  key={workspace.id}
                  className="border-t hover:bg-slate-50"
                >
                  <td className="p-4">
                    {workspace.id}
                  </td>

                  <td className="p-4 font-medium">
                    {workspace.name}
                  </td>

                  <td className="p-4">
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        workspace.visibility ===
                        "PUBLIC"
                          ? "bg-green-100 text-green-700"
                          : "bg-red-100 text-red-700"
                      }`}
                    >
                      {workspace.visibility}
                    </span>
                  </td>

                  <td className="p-4">
                    {workspace.member_count || 0}
                  </td>

                  <td className="p-4">
                    <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs">
                      {workspace.is_archived
                        ? "ARCHIVED"
                        : "ACTIVE"}
                    </span>
                  </td>

                  <td className="p-4">
                    <div className="flex gap-2 flex-wrap">

                      {/* View Workspace */}

                      <button
                        onClick={() =>
                          navigate(
                            `/workspaces/${workspace.id}`
                          )
                        }
                        className="bg-sky-100 text-sky-700 p-2 rounded-lg hover:bg-sky-200"
                        title="Workspace Details"
                      >
                        <FiEye />
                      </button>

                      {/* Edit */}

                      <Link
                        to={`/workspaces/${workspace.id}/edit`}
                        className="bg-amber-100 text-amber-700 p-2 rounded-lg hover:bg-amber-200"
                        title="Edit Workspace"
                      >
                        <FiEdit />
                      </Link>

                      {/* Members */}

                      <button
                        onClick={() =>
                          navigate(
                            `/workspaces/${workspace.id}/members`
                          )
                        }
                        className="bg-purple-100 text-purple-700 p-2 rounded-lg hover:bg-purple-200"
                        title="Workspace Members"
                      >
                        <FiUsers />
                      </button>

                      {/* Channels */}

                      <button
                        onClick={() => {
                          localStorage.setItem(
                            "workspaceId",
                            workspace.id
                          );

                          navigate(
                            `/workspaces/${workspace.id}/channels`
                          );
                        }}
                        className="bg-blue-100 text-blue-700 p-2 rounded-lg hover:bg-blue-200"
                        title="Channels"
                      >
                        <FiMessageSquare />
                      </button>

                    </div>
                  </td>
                </tr>
              ))}

            {!loading &&
              filtered.length === 0 && (
                <tr>
                  <td
                    colSpan="6"
                    className="text-center p-8 text-gray-500"
                  >
                    No workspaces found.
                  </td>
                </tr>
              )}
          </tbody>
        </table>
      </div>
    </PageLayout>
  );
}