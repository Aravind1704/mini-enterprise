import React, {
  useEffect,
  useState
} from "react";

import {
  useParams,
  Link,
  useNavigate
} from "react-router-dom";

import axios from "../api/axios";

export default function ChannelDetails() {

  const { id } = useParams();
  const navigate = useNavigate();

  const [channel, setChannel] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  useEffect(() => {

    const loadChannel = async () => {

      try {

        const res = await axios.get(
          `/channels/${id}`
        );

        setChannel(res.data);

      } catch (err) {

        console.error(err);

        setError(
          err.response?.data?.detail ||
          "Failed to load channel"
        );

      } finally {

        setLoading(false);

      }

    };

    loadChannel();

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

  if (!channel) {

    return (
      <div className="p-6">
        Channel Not Found
      </div>
    );

  }

  return (

    <div className="p-6">

      <div className="bg-white p-6 rounded shadow">

        {/* Header */}

        <div className="flex justify-between items-center mb-6">

          <h1 className="text-3xl font-bold">

            {channel.name}

          </h1>

          <div className="flex gap-3">

            <button
              onClick={() => navigate("/dashboard")}
              className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
            >
              ← dashboard
            </button>

            <Link
              to={`/channel-members/${channel.id}`}
              className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700"
            >
              Members
            </Link>

          </div>

        </div>

        {/* Details */}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

          <div>

            <p className="font-semibold">
              Channel ID
            </p>

            <p>
              {channel.id}
            </p>

          </div>

          <div>

            <p className="font-semibold">
              Channel Type
            </p>

            <p>
              {channel.channel_type}
            </p>

          </div>

          <div>

            <p className="font-semibold">
              Workspace ID
            </p>

            <p>
              {channel.workspace_id}
            </p>

          </div>

          <div>

            <p className="font-semibold">
              Tenant ID
            </p>

            <p>
              {channel.tenant_id}
            </p>

          </div>

          <div>

            <p className="font-semibold">
              Description
            </p>

            <p>
              {channel.description || "-"}
            </p>

          </div>

          <div>

            <p className="font-semibold">
              Archived
            </p>

            <p>
              {channel.is_archived
                ? "Yes"
                : "No"}
            </p>

          </div>

        </div>

      </div>

    </div>

  );

}