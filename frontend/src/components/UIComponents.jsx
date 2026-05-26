import React from "react";

/* STATUS BADGE */
export function StatusBadge({ status }) {
  const colors = {
    active: "bg-green-100 text-green-700",
    pending: "bg-yellow-100 text-yellow-700",
    cancelled: "bg-red-100 text-red-700",
    resolved: "bg-blue-100 text-blue-700",
  };

  return (
    <span
      className={`px-3 py-1 rounded-full text-xs font-semibold ${
        colors[status?.toLowerCase()] ||
        "bg-slate-100 text-slate-700"
      }`}
    >
      {status}
    </span>
  );
}

/* PAGE HEADER */
export function PageHeader({
  title,
  subtitle,
  action,
}) {
  return (
    <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 mb-8">
      <div>
        <h1 className="text-4xl font-bold text-slate-800">
          {title}
        </h1>

        <p className="text-slate-500 mt-2">
          {subtitle}
        </p>
      </div>

      <div>{action}</div>
    </div>
  );
}

/* ERROR MESSAGE */
export function ErrorMessage({
  message,
  onClose,
}) {
  return (
    <div className="bg-red-100 border border-red-300 text-red-700 px-5 py-4 rounded-2xl mb-6 flex justify-between items-center">
      <span>{message}</span>

      <button
        onClick={onClose}
        className="font-bold"
      >
        ✕
      </button>
    </div>
  );
}

/* LOADING SPINNER */
export function LoadingSpinner() {
  return (
    <div className="flex justify-center items-center py-20">
      <div className="h-14 w-14 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
    </div>
  );
}

/* EMPTY STATE */
export function EmptyState({
  icon,
  title,
  description,
}) {
  return (
    <div className="text-center py-20 bg-white rounded-3xl shadow-sm border border-slate-200">
      <div className="text-6xl mb-4">{icon}</div>

      <h3 className="text-2xl font-bold text-slate-700">
        {title}
      </h3>

      <p className="text-slate-500 mt-2">
        {description}
      </p>
    </div>
  );
}

/* FILTER BAR */
export function FilterBar({
  filters,
  onFilterChange,
  onReset,
}) {
  return (
    <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm mb-6 flex flex-wrap gap-4 items-end">
      {filters.map((filter) => (
        <div key={filter.key}>
          <label className="block text-sm font-semibold text-slate-700 mb-2">
            {filter.label}
          </label>

          <select
            value={filter.value}
            onChange={(e) =>
              onFilterChange(
                filter.key,
                e.target.value
              )
            }
            className="p-3 rounded-2xl border border-slate-200 bg-slate-50 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="">
              All
            </option>

            {filter.options.map((opt) => (
              <option
                key={opt.value}
                value={opt.value}
              >
                {opt.label}
              </option>
            ))}
          </select>
        </div>
      ))}

      <button
        onClick={onReset}
        className="px-5 py-3 bg-slate-200 rounded-2xl font-semibold hover:bg-slate-300 transition"
      >
        Reset
      </button>
    </div>
  );
}

/* DATA TABLE */
export function DataTable({
  columns,
  rows,
  actions,
}) {
  return (
    <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-slate-100">
            <tr>
              {columns.map((col) => (
                <th
                  key={col.key}
                  className="px-6 py-4 text-left text-sm font-bold text-slate-700 uppercase"
                >
                  {col.label}
                </th>
              ))}

              {actions && (
                <th className="px-6 py-4 text-center text-sm font-bold text-slate-700 uppercase">
                  Actions
                </th>
              )}
            </tr>
          </thead>

          <tbody>
            {rows.map((row, idx) => (
              <tr
                key={idx}
                className="border-b border-slate-100 hover:bg-slate-50 transition"
              >
                {columns.map((col) => (
                  <td
                    key={col.key}
                    className="px-6 py-4 text-slate-700"
                  >
                    {row[col.key]}
                  </td>
                ))}

                {actions && (
                  <td className="px-6 py-4 text-center">
                    {actions(row)}
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

/* CONFIRM MODAL */
export function ConfirmModal({
  title,
  message,
  onConfirm,
  onCancel,
  danger,
}) {
  return (
    <div className="fixed inset-0 bg-black/40 flex justify-center items-center z-50">
      <div className="bg-white rounded-3xl p-8 w-full max-w-md shadow-2xl">
        <h2 className="text-2xl font-bold text-slate-800 mb-3">
          {title}
        </h2>

        <p className="text-slate-600 mb-6">
          {message}
        </p>

        <div className="flex justify-end gap-3">
          <button
            onClick={onCancel}
            className="px-5 py-3 rounded-2xl bg-slate-200 font-semibold hover:bg-slate-300 transition"
          >
            Cancel
          </button>

          <button
            onClick={onConfirm}
            className={`px-5 py-3 rounded-2xl text-white font-semibold transition ${
              danger
                ? "bg-red-600 hover:bg-red-700"
                : "bg-indigo-600 hover:bg-indigo-700"
            }`}
          >
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
}