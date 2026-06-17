import React from "react";
import { Link } from "react-router-dom";

export default function BackToDashboard({ className = "" }) {
  return (
    <Link
      to="/dashboard"
      className={`inline-flex items-center gap-2 text-indigo-600 hover:text-indigo-800 ${className}`}
    >
      ← Dashboard
    </Link>
  );
}
