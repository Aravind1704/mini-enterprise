import React, {
  useEffect,
  useState,
  useCallback
} from "react";

import {
  Link,
  useNavigate,
  useParams
} from "react-router-dom";

import {
  FiSearch,
  FiEye,
  FiPlus,
  FiUsers
} from "react-icons/fi";

import axios from "../api/axios";
import PageLayout from "../components/PageLayout";

export default function ChannelList() {
  const navigate = useNavigate();
  const { id } = useParams();

  const [channels, setChannels] =
    useState([]);

  const [search, setSearch] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const workspaceId = Number(
    id || localStorage.getItem("workspaceId")
  );

  useEffect(() => {
    if (workspaceId) {
      localStorage.setItem("workspaceId", String(workspaceId));
    }
  }, [workspaceId]);

  const loadChannels =
    useCallback(async () => {
      if (!workspaceId) return;

      try {
        setLoading(true);

        const res =
          await axios.get(
            `/workspaces/${workspaceId}/channels`
          );

        setChannels(
          res.data || []
        );
      } catch (err) {
        console.error(
          "Failed to load channels:",
          err
        );
        setChannels([]);
      } finally {
        setLoading(false);
      }
    }, [workspaceId]);

  useEffect(() => {
    loadChannels();
  }, [loadChannels]);

  const filtered =
    channels.filter((channel) =>
      channel.name
        ?.toLowerCase()
        .includes(
          search.toLowerCase()
        )
    );

  if (!workspaceId) {
    return (
      <PageLayout>
        <div className="bg-white border rounded-2xl p-8">
          <h2 className="text-xl font-bold mb-2">
            No Workspace Selected
          </h2>

          <p className="text-gray-500">
            Please select a
            workspace from the
            Workspace List.
          </p>
        </div>
      </PageLayout>
    );
  }

  return (
    <PageLayout>
      {/* Header */}

      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold">
            Channel List
          </h1>

          <p className="text-gray-500">
            Workspace ID:
            {" "}
            {workspaceId}
          </p>
        </div>

        <Link
          to="/channel-create"
          className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-3 rounded-xl flex items-center gap-2"
        >
          <FiPlus />
          Create Channel
        </Link>
      </div>

      {/* Search */}

      <div className="bg-white border rounded-2xl p-5 mb-6">
        <div className="relative">
          <FiSearch
            className="absolute left-4 top-4 text-gray-400"
          />

          <input
            type="text"
            placeholder="Search channels..."
            className="w-full border rounded-xl pl-12 pr-4 py-3"
            value={search}
            onChange={(e) =>
              setSearch(
                e.target.value
              )
            }
          />
        </div>
      </div>

      {/* Table */}

      <div className="bg-white border rounded-2xl overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="p-4 text-left">
                ID
              </th>

              <th className="p-4 text-left">
                Name
              </th>

              <th className="p-4 text-left">
                Description
              </th>

              <th className="p-4 text-left">
                Type
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
                  colSpan="6"
                  className="text-center py-10"
                >
                  Loading
                  Channels...
                </td>
              </tr>
            )}

            {!loading &&
              filtered.length >
                0 &&
              filtered.map(
                (channel) => (
                  <tr
                    key={
                      channel.id
                    }
                    className="border-t hover:bg-gray-50"
                  >
                    <td className="p-4">
                      {
                        channel.id
                      }
                    </td>

                    <td className="p-4 font-medium">
                      {
                        channel.name
                      }
                    </td>

                    <td className="p-4">
                      {channel.description ||
                        "-"}
                    </td>

                    <td className="p-4">
                      {
                        channel.channel_type
                      }
                    </td>

                    <td className="p-4">
                      <span
                        className={`px-3 py-1 rounded-full text-xs ${
                          channel.is_archived
                            ? "bg-red-100 text-red-700"
                            : "bg-green-100 text-green-700"
                        }`}
                      >
                        {channel.is_archived
                          ? "ARCHIVED"
                          : "ACTIVE"}
                      </span>
                    </td>

                    <td className="p-4">
                      <div className="flex gap-4">
                        {/* Details */}

                        <button
                          onClick={() => {
                            localStorage.setItem(
                              "channelId",
                              channel.id
                            );

                            navigate(
                              `/channel-details/${channel.id}`
                            );
                          }}
                          className="text-blue-600 hover:text-blue-800"
                          title="Channel Details"
                        >
                          <FiEye />
                        </button>

                        {/* Members */}

                        <button
                          onClick={() => {
                            localStorage.setItem(
                              "channelId",
                              channel.id
                            );

                            navigate(
                              `/channel-members/${channel.id}`
                            );
                          }}
                          className="text-purple-600 hover:text-purple-800"
                          title="Channel Members"
                        >
                          <FiUsers />
                        </button>
                      </div>
                    </td>
                  </tr>
                )
              )}

            {!loading &&
              filtered.length ===
                0 && (
                <tr>
                  <td
                    colSpan="6"
                    className="text-center py-10 text-gray-500"
                  >
                    No channels
                    found for this
                    workspace.
                  </td>
                </tr>
              )}
          </tbody>
        </table>
      </div>
    </PageLayout>
  );
}
