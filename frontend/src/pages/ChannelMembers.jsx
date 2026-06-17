import React, {
  useState,
  useEffect,
  useCallback
} from "react";

import { useParams } from "react-router-dom";

import {
  FiUsers,
  FiUserPlus,
  FiUserMinus,
  FiRefreshCw,
  FiMail,
  FiHash
} from "react-icons/fi";

import axios from "../api/axios";
import PageLayout from "../components/PageLayout";

export default function ChannelMembers() {
  const { channelId } = useParams();

  const user = JSON.parse(
    localStorage.getItem("user")
  );

  const [userId, setUserId] =
    useState(
      user?.id?.toString() || ""
    );

  const [members, setMembers] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  const [actionLoading, setActionLoading] =
    useState(false);

  const loadMembers =
    useCallback(async () => {
      if (!channelId) return;

      try {
        setLoading(true);

        const res =
          await axios.get(
            `/channels/${channelId}/members`
          );

        setMembers(
          res.data || []
        );
      } catch (err) {
        console.error(
          "Failed to load members",
          err
        );
        setMembers([]);
      } finally {
        setLoading(false);
      }
    }, [channelId]);

  useEffect(() => {
    loadMembers();
  }, [loadMembers]);

  const joinChannel =
    async () => {
      if (!userId) {
        alert(
          "Please enter User ID"
        );
        return;
      }

      try {
        setActionLoading(true);

        await axios.post(
          `/channels/${channelId}/join?user_id=${userId}`
        );

        alert(
          "Joined Channel Successfully"
        );

        await loadMembers();
      } catch (err) {
        alert(
          err.response?.data
            ?.detail ||
            "Failed to join channel"
        );
      } finally {
        setActionLoading(false);
      }
    };

  const leaveChannel =
    async () => {
      if (!userId) {
        alert(
          "Please enter User ID"
        );
        return;
      }

      try {
        setActionLoading(true);

        await axios.post(
          `/channels/${channelId}/leave?user_id=${userId}`
        );

        alert(
          "Left Channel Successfully"
        );

        await loadMembers();
      } catch (err) {
        alert(
          err.response?.data
            ?.detail ||
            "Failed to leave channel"
        );
      } finally {
        setActionLoading(false);
      }
    };

  return (
    <PageLayout>
      <div className="space-y-6">
        {/* Header */}

        <div className="bg-white border rounded-2xl p-6 shadow-sm">
          <div className="flex justify-between items-center flex-wrap gap-4">
            <div>
              <h1 className="text-3xl font-bold flex items-center gap-3">
                <FiUsers />
                Channel Members
              </h1>

              <p className="text-gray-500 mt-2">
                Channel ID:
                {" "}
                {channelId}
              </p>
            </div>

            <button
              onClick={
                loadMembers
              }
              className="bg-slate-100 hover:bg-slate-200 px-4 py-2 rounded-xl flex items-center gap-2"
            >
              <FiRefreshCw />
              Refresh
            </button>
          </div>
        </div>

        {/* Join / Leave */}

        <div className="bg-white border rounded-2xl p-6 shadow-sm">
          <h2 className="text-xl font-bold mb-6">
            Join / Leave Channel
          </h2>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block font-semibold mb-2">
                User ID
              </label>

              <input
                type="number"
                className="w-full border rounded-xl p-3"
                placeholder="Enter User ID"
                value={userId}
                onChange={(e) =>
                  setUserId(
                    e.target.value
                  )
                }
              />
            </div>

            <div className="flex items-end gap-3">
              <button
                onClick={
                  joinChannel
                }
                disabled={
                  actionLoading
                }
                className="bg-green-600 hover:bg-green-700 text-white px-5 py-3 rounded-xl flex items-center gap-2"
              >
                <FiUserPlus />
                Join Channel
              </button>

              <button
                onClick={
                  leaveChannel
                }
                disabled={
                  actionLoading
                }
                className="bg-red-600 hover:bg-red-700 text-white px-5 py-3 rounded-xl flex items-center gap-2"
              >
                <FiUserMinus />
                Leave Channel
              </button>
            </div>
          </div>
        </div>

        {/* Stats */}

        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-white border rounded-2xl p-6 shadow-sm">
            <h3 className="text-gray-500">
              Total Members
            </h3>

            <p className="text-3xl font-bold mt-2">
              {members.length}
            </p>
          </div>

          <div className="bg-white border rounded-2xl p-6 shadow-sm">
            <h3 className="text-gray-500">
              Channel ID
            </h3>

            <p className="text-3xl font-bold mt-2">
              {channelId}
            </p>
          </div>

          <div className="bg-white border rounded-2xl p-6 shadow-sm">
            <h3 className="text-gray-500">
              Current User
            </h3>

            <p className="text-3xl font-bold mt-2">
              {user?.id || "-"}
            </p>
          </div>
        </div>

        {/* Members Table */}

        <div className="bg-white border rounded-2xl overflow-hidden shadow-sm">
          <div className="p-6 border-b">
            <h2 className="text-xl font-bold">
              Members List
            </h2>
          </div>

          <table className="w-full">
            <thead className="bg-slate-50">
              <tr>
                <th className="text-left p-4">
                  User ID
                </th>

                <th className="text-left p-4">
                  Name
                </th>

                <th className="text-left p-4">
                  Email
                </th>

                <th className="text-left p-4">
                  Status
                </th>
              </tr>
            </thead>

            <tbody>
              {loading && (
                <tr>
                  <td
                    colSpan="4"
                    className="text-center p-8"
                  >
                    Loading Members...
                  </td>
                </tr>
              )}

              {!loading &&
                members.map(
                  (member) => (
                    <tr
                      key={
                        member.id
                      }
                      className="border-t hover:bg-slate-50"
                    >
                      <td className="p-4">
                        <div className="flex items-center gap-2">
                          <FiHash />
                          {
                            member.user_id
                          }
                        </div>
                      </td>

                      <td className="p-4 font-medium">
                        {
                          member.user_name
                        }
                      </td>

                      <td className="p-4">
                        <div className="flex items-center gap-2">
                          <FiMail />
                          {
                            member.email
                          }
                        </div>
                      </td>

                      <td className="p-4">
                        <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs">
                          ACTIVE
                        </span>
                      </td>
                    </tr>
                  )
                )}

              {!loading &&
                members.length ===
                  0 && (
                  <tr>
                    <td
                      colSpan="4"
                      className="text-center p-10 text-gray-500"
                    >
                      No members have joined this channel.
                    </td>
                  </tr>
                )}
            </tbody>
          </table>
        </div>
      </div>
    </PageLayout>
  );
}