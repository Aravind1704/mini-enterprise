import React, {
  useState,
  useEffect,
  useCallback
} from "react";

import { useParams } from "react-router-dom";
import PageLayout from "../components/PageLayout";
import axios from "../api/axios";

export default function WorkspaceDetails() {

  const [taskForm, setTaskForm] = useState({
  title: "",
  description: "",
  priority: "medium",
  due_date: "",
});

const user = JSON.parse(
  localStorage.getItem("user")
);

const canCreateTask =
  ["admin", "manager"].includes(
    user?.role
  );


  const createTask = async () => {
  try {
    await axios.post(
      `/workspaces/${id}/tasks`,
      taskForm
    );

    setTaskForm({
      title: "",
      description: "",
      priority: "medium",
      due_date: "",
    });

    const res =
      await axios.get(
        `/workspaces/${id}/tasks`
      );

    setTasks(res.data);
  } catch (err) {
    alert(
      err.response?.data?.detail ||
        "Failed to create task"
    );
  }
};

const deleteTask = async (taskId) => {
  try {
    await axios.delete(
      `/workspaces/${id}/tasks/${taskId}`
    );

    setTasks(
      tasks.filter(
        (t) => t.id !== taskId
      )
    );

    if (
      selectedTask?.id === taskId
    ) {
      setSelectedTask(null);
    }
  } catch (err) {
    alert(
      err.response?.data?.detail ||
        "Failed to delete task"
    );
  }
};
const updateTask = async () => {
  try {
    await axios.put(
      `/workspaces/${id}/tasks/${editingTask.id}`,
      editingTask
    );

    const res =
      await axios.get(
        `/workspaces/${id}/tasks`
      );

    setTasks(res.data);

    setEditingTask(null);
  } catch (err) {
    alert(
      err.response?.data?.detail ||
        "Failed to update task"
    );
  }
};
const [editingTask, setEditingTask] =
  useState(null);
  const { id } = useParams();

  const [workspace, setWorkspace] =
    useState(null);

  const [members, setMembers] =
    useState([]);

  const [channels, setChannels] =
    useState([]);

  const [messages, setMessages] =
    useState([]);

  const [tasks, setTasks] =
    useState([]);

  const [message, setMessage] =
    useState("");
  const [activeTab, setActiveTab] =
    useState("Overview");

  const [selectedTask, setSelectedTask] =
    useState(null);

  const [documents, setDocuments] =
    useState({});
  const [selectedFile, setSelectedFile] =
    useState(null);

  const [uploading, setUploading] =
    useState(false);
  const [comments, setComments] =
    useState({});

  const [activities, setActivities] =
    useState({});
  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");
  const loadTaskDocuments =
    async (taskId) => {
      try {
        const res =
          await axios.get(
            `/tasks/${taskId}/documents`
          );

        setDocuments((prev) => ({
          ...prev,
          [taskId]: res.data
        }));
      } catch {
        setDocuments((prev) => ({
          ...prev,
          [taskId]: []
        }));
      }
    };
const uploadTaskDocument =
  async (taskId) => {
    if (!selectedFile) {
      alert("Select a file");
      return;
    }

    try {
      setUploading(true);

      const formData =
        new FormData();

      formData.append(
        "file",
        selectedFile
      );

      formData.append(
        "document_type",
        "OTHER"
      );

      await axios.post(
        `/tasks/${taskId}/documents`,
        formData,
        {
          headers: {
            "Content-Type":
              "multipart/form-data",
          },
        }
      );

      await loadTaskDocuments(
        taskId
      );

      setSelectedFile(null);

      alert(
        "Document Uploaded"
      );
    } catch (err) {
      alert(
        err.response?.data?.detail ||
          "Upload failed"
      );
    } finally {
      setUploading(false);
    }
  };

const downloadDocument =
  (documentId) => {
    window.open(
      `${axios.defaults.baseURL}/task-documents/${documentId}/download`,
      "_blank"
    );
  };

const deleteDocument =
  async (
    documentId,
    taskId
  ) => {
    try {
      await axios.delete(
        `/task-documents/${documentId}`
      );

      await loadTaskDocuments(
        taskId
      );
    } catch (err) {
      alert(
        err.response?.data?.detail ||
          "Delete failed"
      );
    }
  };
  const loadTaskComments =
    async (taskId) => {
      try {
        const res =
          await axios.get(
            `/tasks/${taskId}/comments`
          );

        setComments((prev) => ({
          ...prev,
          [taskId]: res.data
        }));
      } catch {
        setComments((prev) => ({
          ...prev,
          [taskId]: []
        }));
      }
    };

const loadTaskActivities =
  async (taskId) => {
    try {
      const res =
        await axios.get(
          `/tasks/${taskId}/activities`
        );

      setActivities((prev) => ({
        ...prev,
        [taskId]: res.data
      }));
    } catch {
      setActivities((prev) => ({
        ...prev,
        [taskId]: []
      }));
    }
  };
  const loadWorkspace =
    useCallback(async () => {
      if (!id) return;

      try {
        setLoading(true);
        setError("");

        /*
        =====================
        WORKSPACE
        =====================
        */

        const workspaceRes =
          await axios.get(
            `/workspaces/${id}`
          );

        setWorkspace(
          workspaceRes.data
        );

        /*
        =====================
        MEMBERS
        =====================
        */

        try {
          const res =
            await axios.get(
              `/workspaces/${id}/members`
            );

          setMembers(res.data);
        } catch {
          setMembers([]);
        }

        /*
        =====================
        CHANNELS
        =====================
        */

        try {
          const res =
            await axios.get(
              `/workspaces/${id}/channels`
            );

          setChannels(res.data);
        } catch {
          setChannels([]);
        }

        /*
        =====================
        MESSAGES
        =====================
        */

        try {
          const res =
            await axios.get(
              `/workspaces/${id}/messages`
            );

          setMessages(res.data);
        } catch {
          setMessages([]);
        }

        /*
        =====================
        TASKS
        =====================
        */

        try {
          const res =
            await axios.get(
              `/workspaces/${id}/tasks`
            );

          setTasks(res.data);
        } catch {
          setTasks([]);
        }
      } catch (err) {
        console.log(err);

        setError(
          err.response?.data?.detail ||
            "Failed to load workspace"
        );
      } finally {
        setLoading(false);
      }
    }, [id]);

  useEffect(() => {
    loadWorkspace();
  }, [loadWorkspace]);

  /*
  =====================
  SEND MESSAGE
  =====================
  */

  const sendMessage =
    async () => {
      if (!message.trim()) return;

      try {
        await axios.post(
          `/workspaces/${id}/messages`,
          {
            content: message,
            message_type: "TEXT"
          }
        );

        setMessage("");

        const res =
          await axios.get(
            `/workspaces/${id}/messages`
          );

        setMessages(res.data);
      } catch (err) {
        alert(
          err.response?.data?.detail ||
            "Failed to send message"
        );
      }
    };

  /*
  =====================
  LOADING
  =====================
  */

  if (loading) {
    return (
      <PageLayout>
        <div className="p-8">
          Loading Workspace...
        </div>
      </PageLayout>
    );
  }

  /*
  =====================
  ERROR
  =====================
  */

  if (!workspace) {
    return (
      <PageLayout>
        <div className="p-8 text-red-600">
          {error}
        </div>
      </PageLayout>
    );
  }

  return (
    <PageLayout>
      <div className="space-y-6">

        {/* HEADER */}

        <div className="bg-white rounded-2xl border p-6">

          <h1 className="text-3xl font-bold">
            {workspace.name}
          </h1>

          <p className="text-gray-500 mt-2">
            {workspace.description ||
              "No description"}
          </p>

          <div className="mt-4 flex gap-3">

            <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full">
              {workspace.visibility}
            </span>

            <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full">
              Tenant ID:
              {" "}
              {workspace.tenant_id}
            </span>

          </div>
        </div>
<div className="flex gap-3">

  {[
    "Overview",
    "Members",
    "Channels",
    "Messages",
    "Tasks"
  ].map((tab) => (
    <button
      key={tab}
      onClick={() =>
        setActiveTab(tab)
      }
      className={`px-5 py-2 rounded-xl ${
        activeTab === tab
          ? "bg-indigo-600 text-white"
          : "bg-white border"
      }`}
    >
      {tab}
    </button>
  ))}

</div>
        {/* STATS */}

       {activeTab === "Overview" && (
  <div className="grid grid-cols-1 md:grid-cols-4 gap-6">

    <div className="bg-white rounded-2xl border p-6">
      <h3 className="text-gray-500">
        Members
      </h3>

      <p className="text-3xl font-bold mt-2">
        {members.length}
      </p>
    </div>

    <div className="bg-white rounded-2xl border p-6">
      <h3 className="text-gray-500">
        Channels
      </h3>

      <p className="text-3xl font-bold mt-2">
        {channels.length}
      </p>
    </div>

    <div className="bg-white rounded-2xl border p-6">
      <h3 className="text-gray-500">
        Messages
      </h3>

      <p className="text-3xl font-bold mt-2">
        {messages.length}
      </p>
    </div>

    <div className="bg-white rounded-2xl border p-6">
      <h3 className="text-gray-500">
        Tasks
      </h3>

      <p className="text-3xl font-bold mt-2">
        {tasks.length}
      </p>
    </div>

  </div>
)}
        {/* MEMBERS */}

        {activeTab === "Members" && (
  <div className="bg-white rounded-2xl border p-6">

    <h2 className="text-xl font-bold mb-4">
      Workspace Members
    </h2>

    <div className="space-y-3">

      {members.map((m) => (
        <div
          key={m.id}
          className="border rounded-xl p-3 flex justify-between"
        >
          <div>
            User ID: {m.user_id}
          </div>

          <div>
            {m.role}
          </div>
        </div>
      ))}

      {members.length === 0 && (
        <p>No members found</p>
      )}

    </div>

  </div>
)}

        {/* CHANNELS */}

        {activeTab === "Channels" && (
  <div className="bg-white rounded-2xl border p-6">

    <h2 className="text-xl font-bold mb-4">
      Channels
    </h2>

    <div className="space-y-3">

      {channels.map((c) => (
        <div
          key={c.id}
          className="border rounded-xl p-3"
        >
          <h3 className="font-semibold">
            {c.name}
          </h3>

          <p>
            {c.channel_type}
          </p>
        </div>
      ))}

      {channels.length === 0 && (
        <p>No channels found</p>
      )}

    </div>

  </div>
)}

        {/* MESSAGES */}

       {activeTab === "Messages" && (
  <div className="bg-white rounded-2xl border p-6">

    <h2 className="text-xl font-bold mb-4">
      Workspace Messages
    </h2>

    <div className="flex gap-3 mb-6">

      <input
        className="flex-1 border rounded-xl p-3"
        value={message}
        onChange={(e) =>
          setMessage(e.target.value)
        }
        placeholder="Type message..."
      />

      <button
        onClick={sendMessage}
        className="bg-indigo-600 text-white px-6 rounded-xl"
      >
        Send
      </button>

    </div>

    <div className="space-y-3">

      {messages.map((m) => (
        <div
          key={m.id}
          className="border rounded-xl p-3"
        >
          {m.content}
        </div>
      ))}

      {messages.length === 0 && (
        <p>No messages</p>
      )}

    </div>

  </div>
)}

        {/* TASKS */}
        {selectedTask && (
  <div className="space-y-6">

    {/* DOCUMENTS */}

    <div className="bg-white border rounded-2xl p-6">

      <h2 className="font-bold text-xl mb-4">
        Documents
      </h2>

      <div className="bg-white border rounded-2xl p-6">

  <h2 className="font-bold text-xl mb-4">
    Documents
  </h2>

  <div className="flex gap-3 mb-6">

    <input
      type="file"
      onChange={(e) =>
        setSelectedFile(
          e.target.files[0]
        )
      }
      className="border p-2 rounded"
    />

    <button
      onClick={() =>
        uploadTaskDocument(
          selectedTask.id
        )
      }
      disabled={uploading}
      className="bg-indigo-600 text-white px-4 py-2 rounded"
    >
      {uploading
        ? "Uploading..."
        : "Upload"}
    </button>

  </div>

  {(documents[
    selectedTask.id
  ] || []).map((doc) => (

    <div
      key={doc.id}
      className="border rounded-xl p-3 flex justify-between items-center mb-3"
    >
      <div>
        {doc.file_name}
      </div>

      <div className="flex gap-3">

        <button
          onClick={() =>
            downloadDocument(
              doc.id
            )
          }
          className="text-blue-600"
        >
          Download
        </button>

        <button
          onClick={() =>
            deleteDocument(
              doc.id,
              selectedTask.id
            )
          }
          className="text-red-600"
        >
          Delete
        </button>

      </div>

    </div>

  ))}

  {(documents[
    selectedTask.id
  ] || []).length === 0 && (
    <p>
      No documents found
    </p>
  )}

</div>

    </div>

    {/* COMMENTS */}

    <div className="bg-white border rounded-2xl p-6">

      <h2 className="font-bold text-xl mb-4">
        Comments
      </h2>

      {(comments[
        selectedTask.id
      ] || []).map((c) => (
        <div
          key={c.id}
          className="border rounded p-3"
        >
          {c.content}
        </div>
      ))}

    </div>

    {/* ACTIVITIES */}

    <div className="bg-white border rounded-2xl p-6">

      <h2 className="font-bold text-xl mb-4">
        Activities
      </h2>

      {(activities[
        selectedTask.id
      ] || []).map((a) => (
        <div
          key={a.id}
          className="border rounded p-3"
        >
          {a.action}
        </div>
      ))}

    </div>

  </div>
)}

      {activeTab === "Tasks" && (
  <div className="space-y-4">
{canCreateTask && (
  <div className="bg-white rounded-2xl border p-6">

    <h2 className="text-xl font-bold mb-4">
      Create Task
    </h2>

    <div className="space-y-4">

      <input
        className="w-full border rounded-xl p-3"
        placeholder="Title"
        value={taskForm.title}
        onChange={(e) =>
          setTaskForm({
            ...taskForm,
            title:
              e.target.value,
          })
        }
      />

      <textarea
        className="w-full border rounded-xl p-3"
        placeholder="Description"
        value={
          taskForm.description
        }
        onChange={(e) =>
          setTaskForm({
            ...taskForm,
            description:
              e.target.value,
          })
        }
      />

      <select
        className="w-full border rounded-xl p-3"
        value={taskForm.priority}
        onChange={(e) =>
          setTaskForm({
            ...taskForm,
            priority:
              e.target.value,
          })
        }
      >
        <option value="low">
          Low
        </option>

        <option value="medium">
          Medium
        </option>

        <option value="high">
          High
        </option>
      </select>

      <input
        type="datetime-local"
        className="w-full border rounded-xl p-3"
        value={
          taskForm.due_date
        }
        onChange={(e) =>
          setTaskForm({
            ...taskForm,
            due_date:
              e.target.value,
          })
        }
      />

      <button
        onClick={createTask}
        className="bg-indigo-600 text-white px-6 py-3 rounded-xl"
      >
        Create Task
      </button>

    </div>
  </div>
)}
    {tasks.map((t) => (
      <div
  key={t.id}
  className="bg-white rounded-2xl border p-6"
>

  {editingTask?.id ===
  t.id ? (
    <div className="space-y-3">

      <input
        className="w-full border rounded-xl p-3"
        value={
          editingTask.title
        }
        onChange={(e) =>
          setEditingTask({
            ...editingTask,
            title:
              e.target.value,
          })
        }
      />

      <textarea
        className="w-full border rounded-xl p-3"
        value={
          editingTask.description
        }
        onChange={(e) =>
          setEditingTask({
            ...editingTask,
            description:
              e.target.value,
          })
        }
      />

      <div className="flex gap-3">

        <button
          onClick={
            updateTask
          }
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          Save
        </button>

        <button
          onClick={() =>
            setEditingTask(
              null
            )
          }
          className="bg-gray-300 px-4 py-2 rounded"
        >
          Cancel
        </button>

      </div>

    </div>
  ) : (
    <>
      <h3 className="font-bold">
        {t.title}
      </h3>

      <p>
        {t.description}
      </p>

      <div className="mt-2 text-sm text-gray-500">
        Status:
        {" "}
        {t.status}
        {" | "}
        Priority:
        {" "}
        {t.priority}
      </div>

      <div className="flex gap-3 mt-4">

        <button
          onClick={() =>
            setEditingTask(
              t
            )
          }
          className="text-blue-600"
        >
          Edit
        </button>

        <button
          onClick={() =>
            deleteTask(
              t.id
            )
          }
          className="text-red-600"
        >
          Delete
        </button>

        <button
          onClick={async () => {
            setSelectedTask(
              t
            );

            await loadTaskDocuments(
              t.id
            );

            await loadTaskComments(
              t.id
            );

            await loadTaskActivities(
              t.id
            );
          }}
          className="bg-indigo-600 text-white px-4 py-2 rounded-lg"
        >
          View Details
        </button>

      </div>
    </>
  )}

</div>

    ))}

    {tasks.length === 0 && (
      <p>No tasks found</p>
    )}
  </div>
)}

      </div>
    </PageLayout>
  );
}