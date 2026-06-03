import React, {
  useEffect,
  useState
} from "react";

import { useParams } from "react-router-dom";

import axios from "../api/axios";

export default function CollaborationUsage() {

  const { id } = useParams();

  const [loading, setLoading] =
    useState(true);

  const [usage, setUsage] =
    useState(null);

  useEffect(() => {

    const fetchUsage = async () => {

      try {

        const res =
          await axios.get(
            `/tenants/${id}/collaboration/usage`
          );

        setUsage(
          res.data
        );

      } catch (err) {

        console.error(err);

      } finally {

        setLoading(false);

      }

    };

    fetchUsage();

  }, [id]);

  const recalculate = async () => {

    try {

      await axios.post(
        `/tenants/${id}/collaboration/recalculate-usage`
      );

      const res =
        await axios.get(
          `/tenants/${id}/collaboration/usage`
        );

      setUsage(
        res.data
      );

      alert(
        "Usage Recalculated Successfully"
      );

    } catch (err) {

      console.error(err);

      alert(
        err.response?.data?.detail ||
        "Failed to recalculate usage"
      );

    }

  };

  if (loading) {

    return (
      <div className="p-6">
        Loading...
      </div>
    );

  }

  if (!usage) {

    return (
      <div className="p-6">

        <div className="bg-white p-6 rounded-xl shadow">

          <h2 className="text-xl font-bold">
            No Usage Record Found
          </h2>

          <button
            onClick={recalculate}
            className="mt-4 bg-indigo-600 text-white px-4 py-2 rounded"
          >
            Create Usage Record
          </button>

        </div>

      </div>
    );

  }

  return (

    <div className="p-6">

      <div className="flex justify-between items-center mb-6">

        <h1 className="text-3xl font-bold">
          Collaboration Usage
        </h1>

        <button
          onClick={recalculate}
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          Recalculate Usage
        </button>

      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">

        <div className="bg-white shadow rounded-xl p-6">

          <p className="text-gray-500">
            Workspaces
          </p>

          <h2 className="text-4xl font-bold">
            {usage.workspace_count}
          </h2>

        </div>

        <div className="bg-white shadow rounded-xl p-6">

          <p className="text-gray-500">
            Channels
          </p>

          <h2 className="text-4xl font-bold">
            {usage.channel_count}
          </h2>

        </div>

        <div className="bg-white shadow rounded-xl p-6">

          <p className="text-gray-500">
            Members
          </p>

          <h2 className="text-4xl font-bold">
            {usage.member_count}
          </h2>

        </div>

        <div className="bg-white shadow rounded-xl p-6">

          <p className="text-gray-500">
            Storage Used
          </p>

          <h2 className="text-4xl font-bold">
            {usage.storage_used_mb} MB
          </h2>

        </div>

      </div>

      <div className="bg-white shadow rounded-xl p-6 mt-6">

        <h3 className="font-semibold mb-2">
          Last Calculated
        </h3>

        <p>
          {usage.last_calculated_at ||
            "Not Available"}
        </p>

      </div>

    </div>

  );

}