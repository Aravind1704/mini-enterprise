import React, {
  useEffect,
  useState,
  useCallback
} from "react";

import axios from "../api/axios";
import PageLayout from "../components/PageLayout";

export default function CollaborationSettings() {

  const tenantId =
    localStorage.getItem("tenantId") || "1";

  const [loading, setLoading] =
    useState(true);

  const [form, setForm] =
    useState({
      max_workspaces: 10,
      max_channels_per_workspace: 50,
      max_workspace_members: 500,
      max_storage_mb: 1024,
      workspace_enabled: true,
      channel_enabled: true
    });

  const loadSettings = useCallback(async () => {

    try {

      const res =
        await axios.get(
          `/tenants/${tenantId}/collaboration/settings`
        );

      setForm({
        max_workspaces:
          res.data.max_workspaces ?? 10,

        max_channels_per_workspace:
          res.data.max_channels_per_workspace ?? 50,

        max_workspace_members:
          res.data.max_workspace_members ?? 500,

        max_storage_mb:
          res.data.max_storage_mb ?? 1024,

        workspace_enabled:
          res.data.workspace_enabled ?? true,

        channel_enabled:
          res.data.channel_enabled ?? true
      });

    } catch (err) {

      console.error(
        "Load Settings Error:",
        err.response?.data
      );

      alert(
        err.response?.data?.detail ||
        "Failed to load settings"
      );

    } finally {

      setLoading(false);

    }

  }, [tenantId]);

  useEffect(() => {

    loadSettings();

  }, [loadSettings]);

  const saveSettings = async () => {

    try {

      const payload = {
        max_workspaces:
          Number(form.max_workspaces),

        max_channels_per_workspace:
          Number(
            form.max_channels_per_workspace
          ),

        max_workspace_members:
          Number(
            form.max_workspace_members
          ),

        max_storage_mb:
          Number(form.max_storage_mb),

        workspace_enabled:
          Boolean(
            form.workspace_enabled
          ),

        channel_enabled:
          Boolean(
            form.channel_enabled
          )
      };

      await axios.put(
        `/tenants/${tenantId}/collaboration/settings`,
        payload
      );

      alert(
        "Settings Saved Successfully"
      );

    } catch (err) {

      console.error(
        "Save Settings Error:",
        err.response?.data
      );

      alert(
        JSON.stringify(
          err.response?.data,
          null,
          2
        )
      );

    }

  };

  if (loading) {

    return (
      <PageLayout>
        Loading...
      </PageLayout>
    );

  }

  return (

    <PageLayout>

      <div className="bg-white rounded-2xl border p-8">

        <h1 className="text-3xl font-bold mb-2">
          Collaboration Settings
        </h1>

        <p className="text-gray-500 mb-8">
          Configure collaboration limits and controls
        </p>

        <div className="grid grid-cols-2 gap-6">

          <div>

            <label className="block mb-2">
              Max Workspaces
            </label>

            <input
              type="number"
              className="w-full border p-3 rounded-xl"
              value={form.max_workspaces}
              onChange={(e) =>
                setForm({
                  ...form,
                  max_workspaces:
                    e.target.value
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
              className="w-full border p-3 rounded-xl"
              value={form.max_channels_per_workspace}
              onChange={(e) =>
                setForm({
                  ...form,
                  max_channels_per_workspace:
                    e.target.value
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
              className="w-full border p-3 rounded-xl"
              value={form.max_workspace_members}
              onChange={(e) =>
                setForm({
                  ...form,
                  max_workspace_members:
                    e.target.value
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
              className="w-full border p-3 rounded-xl"
              value={form.max_storage_mb}
              onChange={(e) =>
                setForm({
                  ...form,
                  max_storage_mb:
                    e.target.value
                })
              }
            />

          </div>

        </div>

        <div className="mt-8">

          <h2 className="font-semibold mb-4">
            Feature Controls
          </h2>

          <div className="space-y-4">

            <label className="flex justify-between border p-4 rounded-xl">

              <span>
                Workspace Module
              </span>

              <input
                type="checkbox"
                checked={
                  form.workspace_enabled
                }
                onChange={(e) =>
                  setForm({
                    ...form,
                    workspace_enabled:
                      e.target.checked
                  })
                }
              />

            </label>

            <label className="flex justify-between border p-4 rounded-xl">

              <span>
                Channel Module
              </span>

              <input
                type="checkbox"
                checked={
                  form.channel_enabled
                }
                onChange={(e) =>
                  setForm({
                    ...form,
                    channel_enabled:
                      e.target.checked
                  })
                }
              />

            </label>

          </div>

        </div>

        <div className="mt-8 flex justify-end">

          <button
            onClick={saveSettings}
            className="bg-blue-600 text-white px-6 py-3 rounded-xl"
          >
            Save Settings
          </button>

        </div>

      </div>

    </PageLayout>

  );

}