
import React, { useEffect, useState } from "react";

export default function EvaluationPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/api/compare")
      .then(res => res.json())
      .then(data => {
        if (!data.real) throw new Error("No stats");
        // Calculate stats
        const timetable = data.real_sample.concat(data.real_sample.length < 10 ? [] : []); // just to use the real timetable
        setStats({
          totalCourses: data.real_sample.length,
          rooms: Array.from(new Set(data.real_sample.map(e => e.venue || e.room))).filter(Boolean),
          busiestDay: (() => {
            const dayCount = {};
            data.real_sample.forEach(e => { dayCount[e.day] = (dayCount[e.day] || 0) + 1; });
            return Object.entries(dayCount).sort((a, b) => b[1] - a[1])[0]?.[0] || "-";
          })(),
          mostLoadedLevel: (() => {
            const levelCount = {};
            data.real_sample.forEach(e => { levelCount[e.level] = (levelCount[e.level] || 0) + 1; });
            return Object.entries(levelCount).sort((a, b) => b[1] - a[1])[0]?.[0] || "-";
          })(),
        });
      })
      .catch(e => setError("Failed to load stats."))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8 text-center">Loading timetable stats...</div>;
  if (error) return <div className="p-8 text-center text-red-600">{error}</div>;
  if (!stats) return null;

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4 text-cu-purple">Timetable Stats</h1>
      <ul className="mb-6 space-y-2">
        <li><b>Total Courses Loaded:</b> {stats.totalCourses}</li>
        <li><b>Rooms in Use:</b> {stats.rooms.join(", ")}</li>
        <li><b>Busiest Day:</b> {stats.busiestDay}</li>
        <li><b>Most Loaded Level:</b> {stats.mostLoadedLevel}</li>
      </ul>
    </div>
  );
}
