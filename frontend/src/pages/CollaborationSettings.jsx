import React, {
  useEffect,
  useState
} from "react";

import { useParams } from "react-router-dom";

import axios from "../api/axios";

export default function CollaborationSettings() {

  const { id } = useParams();

  const [loading, setLoading] =
    useState(true);

  const [saving, setSaving] =
    useState(false);

  const [form, setForm] =
    useState({
      max_workspaces: 0,
      max_channels_per_workspace: 0,
      max_workspace_members: 0,
      max_storage_mb: 0,
      workspace_enabled: true,
      channel_enabled: true
    });

  useEffect(() => {

    const fetchSettings = async () => {

      try {

        const res =
          await axios.get(
            `/tenants/${id}/collaboration/settings`
          );

        setForm(res.data);

      } catch (err) {

        console.error(err);

      } finally {

        setLoading(false);

      }

    };

    fetchSettings();

  }, [id]);

  const updateSettings = async () => {

    try {

      setSaving(true);

      await axios.put(
        `/tenants/${id}/collaboration/settings`,
        form
      );

      alert(
        "Settings Updated Successfully"
      );

    } catch (err) {

      console.error(err);

      alert(
        err.response?.data?.detail ||
        "Failed to update settings"
      );

    } finally {

      setSaving(false);

    }

  };

  if (loading) {

    return (
      <div className="p-6">
        Loading...
      </div>
    );

  }

  return (

    <div className="p-6">

      <div className="bg-white shadow rounded-xl p-6">

        <h1 className="text-2xl font-bold mb-6">
          Collaboration Settings
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">

          <div>

            <label className="block mb-2">
              Max Workspaces
            </label>

            <input
              type="number"
              value={form.max_workspaces}
              className="w-full border rounded p-3"
              onChange={(e) =>
                setForm({
                  ...form,
                  max_workspaces:
                    Number(e.target.value)
                })
              }
            />

          </div>

          <div>

            <label className="block mb-2">
              Max Channels Per Workspace
            </label>

            <input
              type="number"
              value={form.max_channels_per_workspace}
              className="w-full border rounded p-3"
              onChange={(e) =>
                setForm({
                  ...form,
                  max_channels_per_workspace:
                    Number(e.target.value)
                })
              }
            />

          </div>

          <div>

            <label className="block mb-2">
              Max Workspace Members
            </label>

            <input
              type="number"
              value={form.max_workspace_members}
              className="w-full border rounded p-3"
              onChange={(e) =>
                setForm({
                  ...form,
                  max_workspace_members:
                    Number(e.target.value)
                })
              }
            />

          </div>

          <div>

            <label className="block mb-2">
              Max Storage (MB)
            </label>

            <input
              type="number"
              value={form.max_storage_mb}
              className="w-full border rounded p-3"
              onChange={(e) =>
                setForm({
                  ...form,
                  max_storage_mb:
                    Number(e.target.value)
                })
              }
            />

          </div>

        </div>

        <div className="mt-6 space-y-4">

          <label className="flex items-center gap-2">

            <input
              type="checkbox"
              checked={form.workspace_enabled}
              onChange={(e) =>
                setForm({
                  ...form,
                  workspace_enabled:
                    e.target.checked
                })
              }
            />

            Workspace Enabled

          </label>

          <label className="flex items-center gap-2">

            <input
              type="checkbox"
              checked={form.channel_enabled}
              onChange={(e) =>
                setForm({
                  ...form,
                  channel_enabled:
                    e.target.checked
                })
              }
            />

            Channel Enabled

          </label>

        </div>

        <button
          onClick={updateSettings}
          disabled={saving}
          className="mt-6 bg-indigo-600 text-white px-5 py-3 rounded"
        >
          {saving
            ? "Saving..."
            : "Update Settings"}
        </button>

      </div>

    </div>

  );

}