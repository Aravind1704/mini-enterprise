import React, {
  useEffect,
  useState
} from "react";

import {
  Link
} from "react-router-dom";

import axios from "../api/axios";

export default function ChannelList() {

  const [channels, setChannels] =
    useState([]);

  const [workspaceId] =
  useState(1);

  const [loading, setLoading] =
    useState(false);

 useEffect(() => {

  const loadChannels = async () => {

    try {

      setLoading(true);

      const res = await axios.get(
        `/workspaces/${workspaceId}/channels`
      );

      setChannels(res.data);

    } catch (err) {

      console.error(err);

    } finally {

      setLoading(false);

    }

  };

  loadChannels();

}, [workspaceId]);

  const loadChannels = async () => {

    try {

      setLoading(true);

      const res =
        await axios.get(
          `/workspaces/${workspaceId}/channels`
        );

      setChannels(
        res.data
      );

    } catch (err) {

      console.error(err);

      alert(
        "Failed to load channels"
      );

    } finally {

      setLoading(false);

    }
  };

  return (
    <div className="p-6">

      <div className="flex justify-between mb-6">

        <h1 className="text-3xl font-bold">
          Channels
        </h1>

        <Link
          to="/channel-create"
          className="bg-indigo-600 text-white px-4 py-2 rounded"
        >
          Create Channel
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

                <th className="p-3">
                  ID
                </th>

                <th>
                  Name
                </th>

                <th>
                  Type
                </th>

                <th>
                  Status
                </th>

                <th>
                </th>

              </tr>

            </thead>

            <tbody>

              {channels.map(
                (channel) => (

                  <tr
                    key={channel.id}
                    className="border-t"
                  >

                    <td className="p-3">
                      {channel.id}
                    </td>

                    <td>
                      {channel.name}
                    </td>

                    <td>
                      {channel.channel_type}
                    </td>

                    <td>
                      {channel.is_archived
                        ? "Archived"
                        : "Active"}
                    </td>

                    <td>

                      <Link
                        to={`/channel-details/${channel.id}`}
                        className="text-indigo-600"
                      >
                        View
                      </Link>

                    </td>

                  </tr>

                )
              )}

            </tbody>

          </table>

        )}

      </div>

    </div>
  );
}