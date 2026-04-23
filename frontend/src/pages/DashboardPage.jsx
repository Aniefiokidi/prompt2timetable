import React from "react";
import { Link } from "react-router-dom";
import AppShell from "../components/AppShell";

const stats = [
  { label: "Courses", value: 58, color: "bg-indigo-50 text-indigo-700" },
  { label: "Lecturers", value: 32, color: "bg-cyan-50 text-cyan-700" },
  { label: "Rooms", value: 45, color: "bg-blue-50 text-blue-700" },
  { label: "Programs", value: 12, color: "bg-emerald-50 text-emerald-700" },
];

export default function DashboardPage() {
  return (
    <AppShell title="Welcome back, Admin 👋" subtitle="AI-Powered University Timetabling System">
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
        {stats.map((item) => (
          <div key={item.label} className="rounded-xl border border-slate-200 bg-white p-4">
            <div className={`inline-flex rounded-lg px-3 py-1 text-xs font-semibold ${item.color}`}>{item.label}</div>
            <p className="text-3xl font-bold text-slate-800 mt-2">{item.value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Link to="/upload" className="rounded-lg bg-emerald-600 text-white px-4 py-3 text-center font-semibold hover:bg-emerald-700">
          Upload Data
        </Link>
        <Link to="/assistant" className="rounded-lg bg-cu-purple text-cu-gold px-4 py-3 text-center font-semibold hover:bg-purple-900">
          Generate Timetable
        </Link>
        <Link to="/timetable" className="rounded-lg bg-blue-600 text-white px-4 py-3 text-center font-semibold hover:bg-blue-700">
          View Timetable
        </Link>
      </div>
    </AppShell>
  );
}
