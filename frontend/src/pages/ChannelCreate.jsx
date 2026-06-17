import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../api/axios";
import PageLayout from "../components/PageLayout";

export default function ChannelCreate() {
  const navigate = useNavigate();

  const user = JSON.parse(
    localStorage.getItem("user")
  );

  const workspaceId = Number(
    localStorage.getItem("workspaceId")
  );

  const tenantId = Number(
    user?.tenant_id ||
    localStorage.getItem(
      "selectedTenantId"
    )
  );

  const [form, setForm] = useState({
    tenant_id: tenantId || "",
    workspace_id: workspaceId || "",
    name: "",
    description: "",
    channel_type: "PUBLIC",
    created_by: user?.id || "",
  });

  const submit = async (e) => {
    e.preventDefault();

    if (!form.tenant_id) {
      alert("Tenant ID not found.");
      return;
    }

    if (!form.workspace_id) {
      alert("Please select a workspace first.");
      return;
    }

    try {
      const payload = {
        tenant_id: Number(
          form.tenant_id
        ),
        workspace_id: Number(
          form.workspace_id
        ),
        name: form.name,
        description:
          form.description,
        channel_type:
          form.channel_type,
        created_by: Number(
          form.created_by
        ),
      };

      console.log(
        "Creating Channel:",
        payload
      );

      const res =
        await axios.post(
          "/channels",
          payload
        );

      const channel =
        res.data;

      localStorage.setItem(
        "channelId",
        channel.id
      );

      alert(
        "Channel Created Successfully"
      );

      navigate(
        `/channel-details/${channel.id}`
      );
    } catch (err) {
      console.error(err);

      alert(
        err.response?.data?.detail ||
        "Failed to create channel"
      );
    }
  };

  return (
    <PageLayout>
      <div className="bg-white p-8 rounded-2xl border max-w-3xl">

        <h1 className="text-3xl font-bold mb-8">
          Create Channel
        </h1>

        <form
          onSubmit={submit}
          className="space-y-5"
        >

          {/* Tenant ID */}
          <div>
            <label className="block mb-2 font-semibold">
              Tenant ID
            </label>

            <input
              type="number"
              value={form.tenant_id}
              readOnly
              className="w-full border p-3 rounded-xl bg-gray-100"
            />
          </div>

          {/* Workspace ID */}
          <div>
            <label className="block mb-2 font-semibold">
              Workspace ID
            </label>

            <input
              type="number"
              value={form.workspace_id}
              readOnly
              className="w-full border p-3 rounded-xl bg-gray-100"
            />
          </div>

          {/* Channel Name */}
          <div>
            <input
              type="text"
              placeholder="Channel Name"
              value={form.name}
              onChange={(e) =>
                setForm({
                  ...form,
                  name:
                    e.target.value,
                })
              }
              className="w-full border p-3 rounded-xl"
              required
            />
          </div>

          {/* Description */}
          <div>
            <textarea
              placeholder="Description"
              value={
                form.description
              }
              onChange={(e) =>
                setForm({
                  ...form,
                  description:
                    e.target.value,
                })
              }
              className="w-full border p-3 rounded-xl"
              rows="4"
            />
          </div>

          {/* Channel Type */}
          <div>
            <select
              value={
                form.channel_type
              }
              onChange={(e) =>
                setForm({
                  ...form,
                  channel_type:
                    e.target.value,
                })
              }
              className="w-full border p-3 rounded-xl"
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
          </div>

          {/* Submit */}
          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl"
          >
            Create Channel
          </button>

        </form>
      </div>
    </PageLayout>
  );
}