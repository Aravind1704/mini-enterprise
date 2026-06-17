import React, {
  useState
} from "react";

import axios from "../api/axios";
import PageLayout from "../components/PageLayout";

export default function WorkspaceCreate() {

  const [form, setForm] =
    useState({

      tenant_id: "",
      name: "",
      description: "",
      visibility: "PUBLIC",
      created_by: 1

    });

  const submit = async (e) => {

    e.preventDefault();

    try {

      await axios.post(
        "/workspaces",
        form
      );

      alert(
        "Workspace Created"
      );

    } catch (err) {

      alert(
        err.response?.data?.detail
      );

    }

  };

  return (

    <PageLayout>

      <div className="bg-white rounded-2xl border p-8">

        <h1 className="text-3xl font-bold mb-8">
          Create Workspace
        </h1>

        <form
          onSubmit={submit}
          className="space-y-4"
        >

          <input
            className="w-full border p-3 rounded-xl"
            placeholder="Tenant ID"
            value={form.tenant_id}
            onChange={(e)=>
              setForm({
                ...form,
                tenant_id:
                  Number(
                    e.target.value
                  )
              })
            }
          />

          <input
            className="w-full border p-3 rounded-xl"
            placeholder="Workspace Name"
            value={form.name}
            onChange={(e)=>
              setForm({
                ...form,
                name:e.target.value
              })
            }
          />

          <textarea
            className="w-full border p-3 rounded-xl"
            placeholder="Description"
            value={form.description}
            onChange={(e)=>
              setForm({
                ...form,
                description:e.target.value
              })
            }
          />

          <select
            className="w-full border p-3 rounded-xl"
            value={form.visibility}
            onChange={(e)=>
              setForm({
                ...form,
                visibility:e.target.value
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
            className="bg-blue-600 text-white px-6 py-3 rounded-xl"
          >
            Create Workspace
          </button>

        </form>

      </div>

    </PageLayout>

  );

}