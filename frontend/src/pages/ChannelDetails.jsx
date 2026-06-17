import React, {
  useCallback,
  useEffect,
  useState,
} from "react";

import { useParams } from "react-router-dom";
import axios from "../api/axios";
import PageLayout from "../components/PageLayout";
import { useAuth } from "../context/AuthContext";

const tabs = [
  "Messages",
  "Tasks",
  "Documents",
];

const documentTypes = [
  "REQUIREMENT",
  "SPECIFICATION",
  "REFERENCE",
  "DELIVERABLE",
  "OTHER",
];

export default function ChannelDetails() {
  const { id } = useParams();
  const { user } = useAuth();

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [activeTab, setActiveTab] =
    useState("Messages");

  const [channel, setChannel] =
    useState(null);

  const [members, setMembers] =
    useState([]);

  const [messages, setMessages] =
    useState([]);

  const [tasks, setTasks] =
    useState([]);

  const [documents, setDocuments] =
    useState({});

  const [messageText, setMessageText] =
    useState("");

  const [editingMessage, setEditingMessage] =
    useState(null);

  const [taskForm, setTaskForm] =
    useState({
      title: "",
      description: "",
      priority: "medium",
      due_date: "",
      assigned_to_id: "",
    });

  const [uploadState, setUploadState] =
    useState({});

  const canCreateTask = [
    "admin",
    "manager",
    "WORKSPACE_ADMIN",
    "MODERATOR",
  ].includes(user?.role);

  /*
  ====================================
  LOAD DOCUMENTS
  ====================================
  */

  const loadDocuments =
    useCallback(async (taskList) => {
      if (!taskList || taskList.length === 0) {
        setDocuments({});
        return;
      }

      const pairs =
        await Promise.all(
          taskList.map(async (task) => {
            try {
              const res =
                await axios.get(
                  `/tasks/${task.id}/documents`
                );

              return [
                task.id,
                res.data,
              ];
            } catch {
              return [
                task.id,
                [],
              ];
            }
          })
        );

      setDocuments(
        Object.fromEntries(pairs)
      );
    }, []);

  /*
  ====================================
  LOAD CHANNEL
  ====================================
  */

  const loadChannel =
    useCallback(async () => {
      try {
        setLoading(true);
        setError("");

        const [
          channelRes,
          memberRes,
          messageRes,
          taskRes,
        ] = await Promise.all([
          axios.get(
            `/channels/${id}`
          ),
          axios.get(
            `/channels/${id}/members`
          ).catch(() => ({ data: [] })),
          axios.get(
            `/channels/${id}/messages`
          ).catch(() => ({ data: [] })),
          axios.get(
            `/channels/${id}/tasks`
          ).catch(() => ({ data: [] })),
        ]);

        setChannel(
          channelRes.data
        );

        setMembers(
          memberRes.data
        );

        setMessages(
          messageRes.data
        );

        setTasks(
          taskRes.data
        );

        await loadDocuments(
          taskRes.data
        );
      } catch (err) {
        setError(
          err.response?.data
            ?.detail ||
            "Failed to load channel"
        );
      } finally {
        setLoading(false);
      }
    }, [id, loadDocuments]);

  useEffect(() => {
    if (id) {
      loadChannel();
    }
  }, [id, loadChannel]);

  /*
  ====================================
  SEND MESSAGE
  ====================================
  */

  const sendMessage =
    async (e) => {
      e.preventDefault();

      if (
        !messageText.trim()
      )
        return;

      try {
        await axios.post(
          `/channels/${id}/messages`,
          {
            content:
              messageText,
            message_type:
              "TEXT",
          }
        );

        setMessageText("");

        const res =
          await axios.get(
            `/channels/${id}/messages`
          );

        setMessages(
          res.data
        );
      } catch (err) {
        alert(
          err.response?.data
            ?.detail ||
            "Failed to send message"
        );
      }
    };

  /*
  ====================================
  DELETE MESSAGE
  ====================================
  */

  const deleteMessage =
    async (
      messageId
    ) => {
      try {
        await axios.delete(
          `/channel-messages/${messageId}`
        );

        const res =
          await axios.get(
            `/channels/${id}/messages`
          );

        setMessages(
          res.data
        );
      } catch (err) {
        alert(
          err.response?.data
            ?.detail ||
            "Delete failed"
        );
      }
    };

  /*
  ====================================
  UPDATE MESSAGE
  ====================================
  */

  const updateMessage =
    async () => {
      try {
        if (
          !editingMessage?.content.trim()
        )
          return;

        await axios.put(
          `/channel-messages/${editingMessage.id}`,
          {
            content:
              editingMessage.content,
          }
        );

        setEditingMessage(
          null
        );

        const res =
          await axios.get(
            `/channels/${id}/messages`
          );

        setMessages(
          res.data
        );
      } catch (err) {
        alert(
          err.response?.data
            ?.detail ||
            "Update failed"
        );
      }
    };

  /*
  ====================================
  CREATE TASK
  ====================================
  */

  const createTask =
    async (e) => {
      e.preventDefault();

      const payload =
        {
          ...taskForm,
          assigned_to_id:
            taskForm.assigned_to_id
              ? Number(
                  taskForm.assigned_to_id
                )
              : null,
          due_date:
            taskForm.due_date ||
            null,
        };

      try {
        await axios.post(
          `/channels/${id}/tasks`,
          payload
        );

        setTaskForm({
          title: "",
          description:
            "",
          priority:
            "medium",
          due_date: "",
          assigned_to_id:
            "",
        });

        const res =
          await axios.get(
            `/channels/${id}/tasks`
          );

        setTasks(
          res.data
        );

        loadDocuments(
          res.data
        );
      } catch (err) {
        alert(
          err.response?.data
            ?.detail ||
            "Failed to create task"
        );
      }
    };

  /*
  ====================================
  DELETE TASK
  ====================================
  */

  const deleteTask =
    async (taskId) => {
      try {
        await axios.delete(
          `/tasks/${taskId}`
        );

        const res =
          await axios.get(
            `/channels/${id}/tasks`
          );

        setTasks(
          res.data
        );
      } catch (err) {
        alert(
          err.response?.data
            ?.detail ||
            "Delete failed"
        );
      }
    };

  /*
  ====================================
  UPLOAD DOCUMENT
  ====================================
  */

  const uploadDocument =
    async (taskId) => {
      const state =
        uploadState[taskId];

      if (
        !state?.file
      )
        return;

      const formData =
        new FormData();

      formData.append(
        "document_type",
        state.document_type ||
          "OTHER"
      );

      formData.append(
        "file",
        state.file
      );

      try {
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

        const res =
          await axios.get(
            `/tasks/${taskId}/documents`
          );

        setDocuments({
          ...documents,
          [taskId]:
            res.data,
        });
      } catch (err) {
        alert(
          err.response?.data
            ?.detail ||
            "Upload failed"
        );
      }
    };

  /*
  ====================================
  DOWNLOAD DOCUMENT
  ====================================
  */

  const downloadDocument =
    async (
      documentId,
      fileName
    ) => {
      try {
        const res =
          await axios.get(
            `/task-documents/${documentId}/download`,
            {
              responseType:
                "blob",
            }
          );

        const url =
          window.URL.createObjectURL(
            new Blob([
              res.data,
            ])
          );

        const link =
          document.createElement(
            "a"
          );

        link.href = url;
        link.download =
          fileName;

        document.body.appendChild(
          link
        );

        link.click();

        link.remove();

        window.URL.revokeObjectURL(
          url
        );
      } catch (err) {
        alert("Failed to download document");
      }
    };

  if (loading) {
    return (
      <PageLayout>
        <div className="p-6">
          Loading Channel...
        </div>
      </PageLayout>
    );
  }

  if (!channel) {
    return (
      <PageLayout>
        <div className="p-6 text-red-600">
          {error}
        </div>
      </PageLayout>
    );
  }

  return (
    <PageLayout>
      <div className="space-y-6">
        <h1 className="text-3xl font-bold">
          #{channel.name}
        </h1>

        <div className="flex gap-3 border-b pb-3">
          {tabs.map(
            (tab) => (
              <button
                key={tab}
                onClick={() =>
                  setActiveTab(
                    tab
                  )
                }
                className={`px-4 py-2 rounded ${
                  activeTab ===
                  tab
                    ? "bg-blue-600 text-white"
                    : "bg-gray-100"
                }`}
              >
                {tab}
              </button>
            )
          )}
        </div>

        {/* Messages */}

{activeTab === "Messages" && (
  <div className="bg-white rounded-2xl border p-6">

    <form
      onSubmit={sendMessage}
      className="flex gap-3 mb-6"
    >
      <input
        className="flex-1 border rounded-xl p-3"
        placeholder="Type message..."
        value={messageText}
        onChange={(e) =>
          setMessageText(
            e.target.value
          )
        }
      />

      <button
        type="submit"
        className="bg-indigo-600 text-white px-6 rounded-xl"
      >
        Send
      </button>
    </form>

    <div className="space-y-3">

      {messages.length === 0 && (
        <p className="text-gray-500">
          No messages yet
        </p>
      )}

      {messages.map((msg) => (
        <div
          key={msg.id}
          className="border rounded-xl p-4"
        >
          {editingMessage?.id ===
          msg.id ? (
            <div className="space-y-3">

              <textarea
                className="w-full border rounded p-3"
                value={
                  editingMessage.content
                }
                onChange={(e) =>
                  setEditingMessage({
                    ...editingMessage,
                    content:
                      e.target.value,
                  })
                }
              />

              <div className="flex gap-3">

                <button
                  onClick={
                    updateMessage
                  }
                  className="bg-green-600 text-white px-4 py-2 rounded"
                >
                  Save
                </button>

                <button
                  onClick={() =>
                    setEditingMessage(
                      null
                    )
                  }
                  className="bg-gray-500 text-white px-4 py-2 rounded"
                >
                  Cancel
                </button>

              </div>

            </div>
          ) : (
            <>
              <p>{msg.content}</p>

              <div className="flex gap-3 mt-4">

                <button
                  onClick={() =>
                    setEditingMessage(
                      msg
                    )
                  }
                  className="bg-yellow-500 text-white px-4 py-2 rounded"
                >
                  Edit
                </button>

                <button
                  onClick={() =>
                    deleteMessage(
                      msg.id
                    )
                  }
                  className="bg-red-600 text-white px-4 py-2 rounded"
                >
                  Delete
                </button>

              </div>
            </>
          )}
        </div>
      ))}

    </div>

  </div>
)}

        {/* Tasks */}

{activeTab === "Tasks" && (
  <div className="space-y-6">

    {canCreateTask && (
      <div className="bg-white rounded-2xl border p-6">

        <h2 className="text-xl font-bold mb-4">
          Create Task
        </h2>

        <form
          onSubmit={createTask}
          className="space-y-4"
        >
          <input
            className="w-full border rounded p-3"
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
            className="w-full border rounded p-3"
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
            className="w-full border rounded p-3"
            value={
              taskForm.priority
            }
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
            type="date"
            className="w-full border rounded p-3"
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

          <select
            className="w-full border rounded p-3"
            value={
              taskForm.assigned_to_id
            }
            onChange={(e) =>
              setTaskForm({
                ...taskForm,
                assigned_to_id:
                  e.target.value,
              })
            }
          >
            <option value="">
              Assign User
            </option>

            {members.map((m) => (
              <option
                key={m.user_id}   
              value={m.user_id}     
>                {m.user_name} ({m.user_id})
              </option>
            ))}

          </select>

          <button
            type="submit"
            className="bg-indigo-600 text-white px-6 py-2 rounded"
          >
            Create Task
          </button>

        </form>

      </div>
    )}

    <div className="bg-white rounded-2xl border p-6">

      <h2 className="text-xl font-bold mb-4">
        Tasks
      </h2>

      {tasks.length === 0 ? (
        <p className="text-gray-500">
          No tasks yet
        </p>
      ) : (
        <div className="space-y-4">       

          {tasks.map((task) => (        
            <div  
              key={task.id}
              className="border rounded-xl p-4"
            >
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-bold">
                  {task.title}
                </h3>

                <button
                  onClick={() =>
                    deleteTask(
                      task.id
                    )
                  }
                  className="bg-red-600 text-white px-4 py-2 rounded"
                >
                  Delete
                </button>
              </div>

              <p className="text-gray-700 mt-2">
                {task.description}
              </p>

              <p className="text-gray-500 mt-1">
                Priority: {task.priority}
              </p>

              <p className="text-gray-500 mt-1">
                Due Date: {task.due_date || "N/A"}
              </p>

              <p className="text-gray-500 mt-1">
                Assigned To: {task.assigned_to_name || "Unassigned"}
              </p>

              <div className="mt-4">

                <h4 className="font-semibold mb-2">
                  Documents
                </h4>

                {documents[task.id]?.length === 0 ? (
                  <p className="text-gray-500">
                    No documents uploaded
                  </p>
                ) : (
                  <ul className="space-y-2">
                    {documents[task.id]?.map((doc) => (
                      <li key={doc.id} className="flex justify-between items-center">
                        <span>{doc.file_name} ({doc.document_type})</span>
                        <button
                          onClick={() =>
                            downloadDocument(
                              doc.id,
                              doc.file_name
                            )
                          }
                          className="bg-blue-600 text-white px-3 py-1 rounded"      
                      >
                          Download
                        </button>
                      </li>
                    ))}
                  </ul>
                )}

                <div className="mt-4 space-y-2">
                  <input
                    type="file"
                    onChange={(e) =>
                      setUploadState({
                        ...uploadState,
                        [task.id]: {
                          ...uploadState[task.id],
                          file: e.target.files[0],
                        },
                      })
                    }
                  />

                  <select
                    value={
                      uploadState[task.id]?.document_type || "OTHER"
                    }
                    onChange={(e) =>
                      setUploadState({
                        ...uploadState,
                        [task.id]: {
                          ...uploadState[task.id],
                          document_type: e.target.value,
                        },
                      })
                    }
                  >
                    {documentTypes.map((type) => (
                      <option key={type} value={type}>
                        {type}
                      </option>
                    ))}
                  </select>

                  <button
                    onClick={() =>
                      uploadDocument(
                        task.id
                      )
                    }
                    className="bg-green-600 text-white px-4 py-2 rounded"
                  >
                    Upload Document
                  </button>
                </div>

              </div>

            </div>
          ))}

        </div>
      )}

    </div>

  </div>
)}
      </div>
    </PageLayout>
  );
} 