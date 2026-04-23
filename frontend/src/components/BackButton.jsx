import React from "react";
import { useNavigate } from "react-router-dom";

export default function BackButton({ label = "Back" }) {
  const navigate = useNavigate();
  return (
    <button
      type="button"
      onClick={() => navigate(-1)}
      className="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
    >
      <span aria-hidden>←</span>
      {label}
    </button>
  );
}
