
import React, { useEffect, useState } from "react";
import AppShell from "../components/AppShell";
import BackButton from "../components/BackButton";

export default function EvaluationPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/api/compare")
      .then(res => res.json())
      .then(data => {
        if (!data.real || !data.greedy || !data.random) throw new Error("No stats");
        const models = [
          { key: "real", label: "Current Timetable", ...data.real },
          { key: "greedy", label: "Greedy Baseline", ...data.greedy },
          { key: "random", label: "Random Baseline", ...data.random },
        ].map((m) => ({
          ...m,
          violationCount: Object.values(m.hard_violations || {}).reduce((a, b) => a + b, 0),
          roomUtilPct: Math.round((m.room_utilization || 0) * 100),
        }));
        setStats({ models, raw: data });
      })
      .catch(e => setError("Failed to load stats."))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <AppShell title="Timetable Stats"><div className="p-8 text-center">Loading timetable stats...</div></AppShell>;
  if (error) return <AppShell title="Timetable Stats"><div className="p-8 text-center text-red-600">{error}</div></AppShell>;
  if (!stats) return <AppShell title="Timetable Stats"><div className="p-8 text-center">No stats available.</div></AppShell>;

  return (
    <AppShell title="Timetable Evaluation" subtitle="Compare timetable quality against baseline generators.">
      <BackButton label="Back" />
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
        {stats.models.map((m) => (
          <div key={m.key} className="rounded-xl border border-slate-200 bg-white p-4">
            <h3 className="font-semibold text-cu-purple">{m.label}</h3>
            <p className="text-sm text-slate-600 mt-1">Hard Violations</p>
            <p className="text-2xl font-bold text-slate-800">{m.violationCount}</p>
            <p className="text-sm text-slate-600 mt-2">Soft Score: <span className="font-semibold">{m.soft_score}</span></p>
            <p className="text-sm text-slate-600">Room Utilization: <span className="font-semibold">{m.roomUtilPct}%</span></p>
            <p className="text-sm text-slate-600">Runtime: <span className="font-semibold">{(m.runtime_sec || 0).toFixed(3)}s</span></p>
            <div className="mt-3 h-2 bg-slate-100 rounded">
              <div className="h-2 rounded bg-cu-purple" style={{ width: `${Math.max(2, m.roomUtilPct)}%` }} />
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 rounded-xl border border-slate-200 bg-white p-4 overflow-x-auto">
        <h4 className="font-semibold text-slate-800 mb-3">Hard Constraint Breakdown</h4>
        <table className="min-w-full text-sm">
          <thead>
            <tr className="text-left border-b">
              <th className="py-2 pr-6">Constraint</th>
              <th className="py-2 pr-6">Current</th>
              <th className="py-2 pr-6">Greedy</th>
              <th className="py-2">Random</th>
            </tr>
          </thead>
          <tbody>
            {["lecturer_overlap", "room_overlap", "student_group_overlap", "session_too_long"].map((k) => (
              <tr key={k} className="border-b last:border-0">
                <td className="py-2 pr-6 font-medium">{k.replaceAll("_", " ")}</td>
                <td className="py-2 pr-6">{stats.raw.real.hard_violations?.[k] || 0}</td>
                <td className="py-2 pr-6">{stats.raw.greedy.hard_violations?.[k] || 0}</td>
                <td className="py-2">{stats.raw.random.hard_violations?.[k] || 0}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </AppShell>
  );
}
