import React, {
  useState
} from "react";

import axios from "../api/axios";

import {
  useNavigate
} from "react-router-dom";

export default function ChannelCreate() {

  const navigate =
    useNavigate();

  const [form, setForm] =
    useState({
      tenant_id: 1,
      workspace_id: 1,
      name: "",
      description: "",
      channel_type: "PUBLIC",
      created_by: 1
    });

  const submit = async (e) => {

    e.preventDefault();

    try {

      await axios.post(
        "/channels",
        form
      );

      alert(
        "Channel Created"
      );

      navigate(
        "/channels"
      );

    } catch (err) {

      alert(
        err.response?.data?.detail
      );

    }
  };

  return (
    <div className="p-6">

      <div className="bg-white p-6 rounded shadow max-w-3xl">
  <button
    onClick={() => navigate("/dashboard")}
    className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700  display-inline left-0 mb-4"
  >
    ← Back
  </button>
        <h1 className="text-3xl font-bold mb-6">
          Create Channel
        </h1>

        <form
          onSubmit={submit}
          className="space-y-4"
        >

          <input
            className="w-full border p-3 rounded"
            placeholder="Channel Name"
            onChange={(e) =>
              setForm({
                ...form,
                name:
                  e.target.value
              })
            }
          />

          <textarea
            className="w-full border p-3 rounded"
            placeholder="Description"
            onChange={(e) =>
              setForm({
                ...form,
                description:
                  e.target.value
              })
            }
          />

          <select
            className="w-full border p-3 rounded"
            onChange={(e) =>
              setForm({
                ...form,
                channel_type:
                  e.target.value
              })
            }
          >

            <option value="PUBLIC">
              PUBLIC
            </option>

            <option value="PRIVATE">
              PRIVATE
            </option>

            <option value="ANNOUNCEMENT">
              ANNOUNCEMENT
            </option>

            <option value="PROJECT">
              PROJECT
            </option>

          </select>

          <button
            className="bg-indigo-600 text-white px-6 py-3 rounded"
          >
            Create Channel
          </button>

        </form>

      </div>

    </div>
  );
}