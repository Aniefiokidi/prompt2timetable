import React, { useState } from "react";
import AppShell from "../components/AppShell";

export default function UploadDataPage() {
  const [message, setMessage] = useState("");

  const triggerPreprocess = async () => {
    setMessage("Processing...");
    try {
      const res = await fetch("http://localhost:8000/api/preprocess", { method: "POST" });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Preprocess failed");
      setMessage(`Success: ${data.count} timetable entries processed.`);
    } catch (e) {
      setMessage(e.message || "Failed.");
    }
  };

  return (
    <AppShell title="Upload Data" subtitle="Admin data ingestion and preprocessing trigger.">
      <div className="rounded-xl border border-dashed border-slate-300 p-6 bg-slate-50">
        <p className="text-sm text-slate-600 mb-4">
          Place/update timetable Excel files in the <code>TIMETABLE/</code> folder, then trigger preprocessing.
        </p>
        <button
          onClick={triggerPreprocess}
          className="bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg px-4 py-2 font-medium"
        >
          Run Preprocess
        </button>
        {message && <p className="mt-3 text-sm text-slate-700">{message}</p>}
      </div>
    </AppShell>
  );
}
