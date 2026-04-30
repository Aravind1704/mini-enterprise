import { useEffect, useState } from "react";
import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd";
import { Link } from "react-router-dom";
import api from "../api/axios";

const COLUMNS = [
  { id: "todo",        label: "📋 Todo",        color: "#f59e0b" },
  { id: "in_progress", label: "🔵 In Progress",  color: "#3b82f6" },
  { id: "review",      label: "🟣 Review",       color: "#8b5cf6" },
  { id: "done",        label: "✅ Done",          color: "#10b981" },
];

export default function KanbanBoard() {
  const [board, setBoard] = useState({ todo: [], in_progress: [], review: [], done: [] });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/tasks/kanban")
      .then((res) => setBoard(res.data))
      .catch(() => setError("Failed to load Kanban board"))
      .finally(() => setLoading(false));
  }, []);

  const onDragEnd = async (result) => {
    const { source, destination, draggableId } = result;
    if (!destination) return;
    if (source.droppableId === destination.droppableId) return;

    const taskId = parseInt(draggableId);
    const newStatus = destination.droppableId;
    const oldStatus = source.droppableId;

    // Optimistic UI update
    const task = board[oldStatus].find((t) => t.id === taskId);
    const newBoard = { ...board };
    newBoard[oldStatus] = newBoard[oldStatus].filter((t) => t.id !== taskId);
    newBoard[newStatus] = [...newBoard[newStatus], { ...task, status: newStatus }];
    setBoard(newBoard);

    try {
      await api.patch(`/tasks/${taskId}/status`, { status: newStatus });
    } catch (err) {
      setError(err.response?.data?.detail || "Invalid status transition");
      // Revert on error
      setBoard(board);
    }
  };

  if (loading) return <div style={styles.loading}>Loading Kanban Board...</div>;

  return (
    <div style={styles.container}>
      {/* Header */}
      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>⚡ Kanban Board</h1>
          <p style={styles.subtitle}>Drag tasks to update their status</p>
        </div>
        <Link to="/dashboard" style={styles.backBtn}>← Dashboard</Link>
      </div>

      {error && (
        <div style={styles.error}>
          ⚠️ {error}
          <button onClick={() => setError("")} style={styles.closeErr}>✕</button>
        </div>
      )}

      {/* Board */}
      <DragDropContext onDragEnd={onDragEnd}>
        <div style={styles.board}>
          {COLUMNS.map((col) => (
            <div key={col.id} style={styles.column}>
              {/* Column Header */}
              <div style={{ ...styles.colHeader, borderTop: `4px solid ${col.color}` }}>
                <span style={styles.colTitle}>{col.label}</span>
                <span style={{ ...styles.colCount, background: col.color }}>
                  {board[col.id]?.length || 0}
                </span>
              </div>

              {/* Droppable */}
              <Droppable droppableId={col.id}>
                {(provided, snapshot) => (
                  <div
                    ref={provided.innerRef}
                    {...provided.droppableProps}
                    style={{
                      ...styles.colBody,
                      background: snapshot.isDraggingOver ? "#f0f4ff" : "#f8f9fa",
                    }}
                  >
                    {board[col.id]?.map((task, index) => (
                      <Draggable key={task.id} draggableId={String(task.id)} index={index}>
                        {(provided, snapshot) => (
                          <div
                            ref={provided.innerRef}
                            {...provided.draggableProps}
                            {...provided.dragHandleProps}
                            style={{
                              ...styles.card,
                              boxShadow: snapshot.isDragging
                                ? "0 8px 24px rgba(0,0,0,0.15)"
                                : "0 2px 8px rgba(0,0,0,0.07)",
                              ...provided.draggableProps.style,
                            }}
                          >
                            <p style={styles.cardTitle}>{task.title}</p>
                            {task.description && (
                              <p style={styles.cardDesc}>{task.description.slice(0, 60)}...</p>
                            )}
                            <div style={styles.cardFooter}>
                              <span style={{
                                ...styles.priority,
                                background: task.priority === "high" ? "#fde8e8" :
                                            task.priority === "medium" ? "#fff3cd" : "#d4edda",
                                color: task.priority === "high" ? "#c0392b" :
                                       task.priority === "medium" ? "#856404" : "#155724",
                              }}>
                                {task.priority}
                              </span>
                              {task.due_date && (
                                <span style={styles.due}>
                                  📅 {new Date(task.due_date).toLocaleDateString()}
                                </span>
                              )}
                            </div>
                          </div>
                        )}
                      </Draggable>
                    ))}
                    {provided.placeholder}
                    {board[col.id]?.length === 0 && (
                      <div style={styles.empty}>Drop tasks here</div>
                    )}
                  </div>
                )}
              </Droppable>
            </div>
          ))}
        </div>
      </DragDropContext>
    </div>
  );
}

const styles = {
  container: { minHeight: "100vh", background: "#f0f2f5", padding: "24px", fontFamily: "sans-serif" },
  header: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "24px" },
  title: { margin: "0 0 4px", fontSize: "24px", fontWeight: "700", color: "#1a1a2e" },
  subtitle: { margin: 0, color: "#888", fontSize: "13px" },
  backBtn: { background: "#fff", color: "#4f46e5", padding: "8px 16px", borderRadius: "8px", textDecoration: "none", fontSize: "13px", fontWeight: "600", boxShadow: "0 2px 8px rgba(0,0,0,0.07)" },
  error: { background: "#fff0f0", border: "1px solid #ffcccc", color: "#cc0000", padding: "10px 16px", borderRadius: "8px", marginBottom: "16px", display: "flex", justifyContent: "space-between" },
  closeErr: { background: "none", border: "none", cursor: "pointer", color: "#cc0000", fontWeight: "700" },
  loading: { textAlign: "center", padding: "80px", color: "#888", fontSize: "16px" },
  board: { display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "16px" },
  column: { background: "#fff", borderRadius: "12px", overflow: "hidden", boxShadow: "0 2px 12px rgba(0,0,0,0.07)" },
  colHeader: { padding: "16px", display: "flex", justifyContent: "space-between", alignItems: "center", background: "#fff" },
  colTitle: { fontWeight: "700", fontSize: "14px", color: "#1a1a2e" },
  colCount: { color: "#fff", borderRadius: "20px", padding: "2px 10px", fontSize: "12px", fontWeight: "700" },
  colBody: { padding: "12px", minHeight: "400px", transition: "background 0.2s" },
  card: { background: "#fff", borderRadius: "10px", padding: "14px", marginBottom: "10px", cursor: "grab", border: "1px solid #eee" },
  cardTitle: { margin: "0 0 6px", fontWeight: "600", fontSize: "14px", color: "#1a1a2e" },
  cardDesc: { margin: "0 0 10px", fontSize: "12px", color: "#888", lineHeight: "1.4" },
  cardFooter: { display: "flex", justifyContent: "space-between", alignItems: "center" },
  priority: { padding: "2px 8px", borderRadius: "20px", fontSize: "11px", fontWeight: "700", textTransform: "uppercase" },
  due: { fontSize: "11px", color: "#aaa" },
  empty: { textAlign: "center", color: "#ccc", padding: "30px 0", fontSize: "13px" },
};