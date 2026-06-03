import React, {
  useEffect,
  useState
} from "react";

import {
  useParams
} from "react-router-dom";

import axios from "../api/axios";

export default function WorkspaceMembers() {

  const { workspaceId } =
    useParams();

  const [members, setMembers] =
    useState([]);

  const [userId, setUserId] =
    useState("");

  const [role, setRole] =
    useState("MEMBER");

  useEffect(() => {

  const loadMembers = async () => {

    try {

      const res = await axios.get(
        `/workspaces/${workspaceId}/members`
      );

      setMembers(res.data);

    } catch (err) {

      console.error(err);

    }

  };

  loadMembers();

}, [workspaceId]);

  const loadMembers = async () => {

    try {

      const res =
        await axios.get(
          `/workspaces/${workspaceId}/members`
        );

      setMembers(
        res.data
      );

    } catch (err) {

      console.error(err);

    }
  };

  const addMember = async () => {

    try {

      await axios.post(
        `/workspaces/${workspaceId}/members`,
        {
          user_id:
            Number(userId),
          role
        }
      );

      loadMembers();

      setUserId("");

    } catch (err) {

      alert(
        err.response?.data?.detail
      );

    }
  };

  const removeMember =
    async (userId) => {

      if (
        !window.confirm(
          "Remove member?"
        )
      )
        return;

      await axios.delete(
        `/workspaces/${workspaceId}/members/${userId}`
      );

      loadMembers();
    };

  return (
    <div className="p-6">

      <h1 className="text-3xl font-bold mb-6">
        Workspace Members
      </h1>

      <div className="bg-white p-6 rounded shadow mb-6">

        <div className="flex gap-3">

          <input
            className="border p-2 rounded"
            placeholder="User ID"
            value={userId}
            onChange={(e) =>
              setUserId(
                e.target.value
              )
            }
          />

          <select
            className="border p-2 rounded"
            value={role}
            onChange={(e) =>
              setRole(
                e.target.value
              )
            }
          >

            <option>
              MEMBER
            </option>

            <option>
              MODERATOR
            </option>

            <option>
              VIEWER
            </option>

            <option>
              WORKSPACE_ADMIN
            </option>

          </select>

          <button
            onClick={addMember}
            className="bg-indigo-600 text-white px-4 rounded"
          >
            Add Member
          </button>

        </div>

      </div>

      <div className="bg-white rounded shadow">

        <table className="w-full">

          <thead className="bg-gray-100">

            <tr>

              <th className="p-3">
                User ID
              </th>

              <th>
                Role
              </th>

              <th>
                Joined
              </th>

              <th>
              </th>

            </tr>

          </thead>

          <tbody>

            {members.map(
              (member) => (
                <tr
                  key={member.id}
                  className="border-t"
                >
                  <td className="p-3">
                    {member.user_id}
                  </td>

                  <td>
                    {member.role}
                  </td>

                  <td>
                    {member.joined_at}
                  </td>

                  <td>

                    <button
                      onClick={() =>
                        removeMember(
                          member.user_id
                        )
                      }
                      className="text-red-600"
                    >
                      Remove
                    </button>

                  </td>
                </tr>
              )
            )}

          </tbody>

        </table>

      </div>

    </div>
  );
}