import React, {
  useState,
  useEffect,
  useCallback,
  useMemo
} from "react";

import { useParams } from "react-router-dom";

import {
  FiUsers,
  FiUserPlus,
  FiTrash2,
  FiRefreshCw,
  FiSearch
} from "react-icons/fi";

import PageLayout from "../components/PageLayout";
import axios from "../api/axios";

export default function WorkspaceMembers() {
  const { id } = useParams();

  const [userId, setUserId] = useState("");
  const [role, setRole] = useState("MEMBER");
  const [members, setMembers] = useState([]);
  const [search, setSearch] = useState("");

  const [loading, setLoading] =
    useState(false);

  const [adding, setAdding] =
    useState(false);

  const loadMembers = useCallback(async () => {
    if (!id) return;

    try {
      setLoading(true);

      const res = await axios.get(
        `/workspaces/${id}/members`
      );

      setMembers(res.data);
    } catch (err) {
      console.error(err);

      alert(
        err.response?.data?.detail ||
          "Failed to load members"
      );
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    loadMembers();
  }, [loadMembers]);

  const addMember = async () => {
    if (!id) {
      alert("Workspace ID missing");
      return;
    }

    if (!userId) {
      alert("Please enter User ID");
      return;
    }

    try {
      setAdding(true);

      const payload = {
        user_id: Number(userId),
        role
      };

      await axios.post(
        `/workspaces/${id}/members`,
        payload
      );

      alert(
        "Member Added Successfully"
      );

      setUserId("");
      setRole("MEMBER");

      loadMembers();
    } catch (err) {
      console.error(err);

      alert(
        err.response?.data?.detail ||
          JSON.stringify(
            err.response?.data,
            null,
            2
          )
      );
    } finally {
      setAdding(false);
    }
  };

  const removeMember = async (
    memberUserId
  ) => {
    if (
      !window.confirm(
        "Remove this member?"
      )
    )
      return;

    try {
      await axios.delete(
        `/workspaces/${id}/members/${memberUserId}`
      );

      alert(
        "Member Removed Successfully"
      );

      loadMembers();
    } catch (err) {
      alert(
        err.response?.data?.detail ||
          "Failed to remove member"
      );
    }
  };

  const filteredMembers =
    useMemo(() => {
      return members.filter(
        (member) =>
          member.user_id
            ?.toString()
            .includes(search) ||
          member.role
            ?.toLowerCase()
            .includes(
              search.toLowerCase()
            )
      );
    }, [members, search]);

  const roleBadge = (role) => {
    switch (role) {
      case "WORKSPACE_ADMIN":
        return "bg-purple-100 text-purple-700";

      case "MODERATOR":
        return "bg-blue-100 text-blue-700";

      case "VIEWER":
        return "bg-gray-100 text-gray-700";

      default:
        return "bg-green-100 text-green-700";
    }
  };

  return (
    <PageLayout>
      <div className="space-y-6">

        {/* Header */}

        <div className="bg-white rounded-2xl border p-6">

          <div className="flex flex-col md:flex-row justify-between gap-4">

            <div>

              <h1 className="text-3xl font-bold flex items-center gap-3">
                <FiUsers />
                Workspace Members
              </h1>

              <p className="text-gray-500 mt-2">
                Manage members and roles
                inside this workspace.
              </p>

              <p className="text-sm text-gray-400 mt-1">
                Workspace ID : {id}
              </p>

            </div>

            <button
              onClick={loadMembers}
              className="flex items-center gap-2 bg-indigo-600 text-white px-5 py-3 rounded-xl"
            >
              <FiRefreshCw />
              Refresh
            </button>

          </div>

        </div>

        {/* Stats */}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

          <div className="bg-white border rounded-2xl p-6">

            <p className="text-gray-500">
              Total Members
            </p>

            <h2 className="text-4xl font-bold mt-2">
              {members.length}
            </h2>

          </div>

          <div className="bg-white border rounded-2xl p-6">

            <p className="text-gray-500">
              Workspace ID
            </p>

            <h2 className="text-4xl font-bold mt-2">
              {id}
            </h2>

          </div>

          <div className="bg-white border rounded-2xl p-6">

            <p className="text-gray-500">
              Active Members
            </p>

            <h2 className="text-4xl font-bold mt-2">
              {
                members.filter(
                  (m) =>
                    m.is_active
                ).length
              }
            </h2>

          </div>

        </div>

        {/* Add Member */}

        <div className="bg-white border rounded-2xl p-6">

          <h2 className="text-xl font-bold mb-6">
            Add Workspace Member
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

            <input
              type="number"
              placeholder="User ID"
              value={userId}
              onChange={(e) =>
                setUserId(
                  e.target.value
                )
              }
              className="border rounded-xl p-3"
            />

            <select
              value={role}
              onChange={(e) =>
                setRole(
                  e.target.value
                )
              }
              className="border rounded-xl p-3"
            >
              <option value="WORKSPACE_ADMIN">
                Workspace Admin
              </option>

              <option value="MODERATOR">
                Moderator
              </option>

              <option value="MEMBER">
                Member
              </option>

              <option value="VIEWER">
                Viewer
              </option>
            </select>

            <button
              onClick={addMember}
              disabled={adding}
              className="bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl px-6 py-3 flex items-center justify-center gap-2"
            >
              <FiUserPlus />

              {adding
                ? "Adding..."
                : "Add Member"}
            </button>

          </div>

        </div>

        {/* Search */}

        <div className="bg-white border rounded-2xl p-6">

          <div className="relative">

            <FiSearch className="absolute top-4 left-4 text-gray-400" />

            <input
              type="text"
              placeholder="Search by User ID or Role"
              value={search}
              onChange={(e) =>
                setSearch(
                  e.target.value
                )
              }
              className="w-full border rounded-xl p-3 pl-12"
            />

          </div>

        </div>

        {/* Members Table */}

        <div className="bg-white border rounded-2xl overflow-hidden">

          <div className="p-6 border-b">

            <h2 className="text-xl font-bold">
              Members List
            </h2>

          </div>

          <div className="overflow-x-auto">

            <table className="w-full">

              <thead className="bg-slate-50">

                <tr>

                  <th className="p-4 text-left">
                    User ID
                  </th>

                  <th className="p-4 text-left">
                    Role
                  </th>

                  <th className="p-4 text-left">
                    Joined At
                  </th>

                  <th className="p-4 text-left">
                    Status
                  </th>

                  <th className="p-4 text-left">
                    Actions
                  </th>

                </tr>

              </thead>

              <tbody>

                {loading && (
                  <tr>
                    <td
                      colSpan="5"
                      className="p-10 text-center"
                    >
                      Loading Members...
                    </td>
                  </tr>
                )}

                {!loading &&
                  filteredMembers.map(
                    (member) => (
                      <tr
                        key={
                          member.id
                        }
                        className="border-t hover:bg-slate-50"
                      >

                        <td className="p-4 font-medium">
                          {
                            member.user_id
                          }
                        </td>

                        <td className="p-4">

                          <span
                            className={`px-3 py-1 rounded-full text-xs font-semibold ${roleBadge(
                              member.role
                            )}`}
                          >
                            {
                              member.role
                            }
                          </span>

                        </td>

                        <td className="p-4 text-gray-600">
                          {member.joined_at
                            ? new Date(
                                member.joined_at
                              ).toLocaleString()
                            : "-"}
                        </td>

                        <td className="p-4">

                          {member.is_active ? (
                            <span className="text-green-600 font-medium">
                              Active
                            </span>
                          ) : (
                            <span className="text-red-600 font-medium">
                              Inactive
                            </span>
                          )}

                        </td>

                        <td className="p-4">

                          <button
                            onClick={() =>
                              removeMember(
                                member.user_id
                              )
                            }
                            className="flex items-center gap-2 text-red-600 hover:text-red-800"
                          >
                            <FiTrash2 />
                            Remove
                          </button>

                        </td>

                      </tr>
                    )
                  )}

                {!loading &&
                  filteredMembers.length ===
                    0 && (
                    <tr>

                      <td
                        colSpan="5"
                        className="p-12 text-center text-gray-500"
                      >
                        No members found.
                      </td>

                    </tr>
                  )}

              </tbody>

            </table>

          </div>

        </div>

      </div>
    </PageLayout>
  );
}