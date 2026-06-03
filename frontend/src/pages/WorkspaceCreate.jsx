import React, { useState } from "react";
import axios from "../api/axios";
import { useNavigate } from "react-router-dom";

export default function WorkspaceCreate() {

  const navigate = useNavigate();

  const [form, setForm] = useState({
    tenant_id: 1,
    name: "",
    description: "",
    avatar_url: "",
    visibility: "PUBLIC",
    created_by: 1
  });

  const submit = async (e) => {

    e.preventDefault();

    try {

      await axios.post(
        "/workspaces/",
        form
      );

      alert(
        "Workspace Created"
      );

      navigate(
        "/workspaces"
      );

    } catch (err) {

      console.error(err);

      alert(
        err.response?.data?.detail
      );

    }
  };

  return (
    <div className="p-6">

      <div className="bg-white p-6 rounded shadow max-w-3xl">

        <h1 className="text-3xl font-bold mb-6">
          Create Workspace
        </h1>

        <form
          onSubmit={submit}
          className="space-y-4"
        >

          <input
            className="w-full border p-3 rounded"
            placeholder="Workspace Name"
            onChange={(e) =>
              setForm({
                ...form,
                name: e.target.value
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
                visibility:
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

          </select>

          <button
            className="bg-indigo-600 text-white px-6 py-3 rounded"
          >
            Create Workspace
          </button>

        </form>

      </div>

    </div>
  );
}