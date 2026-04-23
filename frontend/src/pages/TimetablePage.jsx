import React, { useEffect, useState } from "react";
import TimetableGrid from "../components/TimetableGrid";
import ExportBar from "../components/ExportBar";
import AppShell from "../components/AppShell";
import BackButton from "../components/BackButton";

function safeHours(value) {
  const n = Number(value);
  if (!Number.isFinite(n) || n <= 0) return 1;
  return Math.max(1, Math.round(n));
}

function assignClientSlots(rows) {
  const byDay = rows.reduce((acc, row) => {
    const day = row.day || "Unknown";
    if (!acc[day]) acc[day] = [];
    acc[day].push({ ...row });
    return acc;
  }, {});

  Object.keys(byDay).forEach((day) => {
    const used = new Set();
    const dayRows = byDay[day].sort((a, b) => String(a.course_code || "").localeCompare(String(b.course_code || "")));
    let nextHour = 7;

    for (const row of dayRows) {
      const duration = safeHours(row.hours);
      while ([...Array(duration).keys()].some((d) => used.has(nextHour + d))) {
        nextHour += 1;
      }
      const start = nextHour;
      const end = Math.min(start + duration, 23);
      row.start_time = `${String(start).padStart(2, "0")}:00`;
      row.end_time = `${String(end).padStart(2, "0")}:00`;
      for (let h = start; h < end; h += 1) used.add(h);
      nextHour += 1;
    }
  });

  return Object.values(byDay).flat();
}

export default function TimetablePage() {
  const [timetable, setTimetable] = useState([]);
  const [dept, setDept] = useState("");
  const [level, setLevel] = useState("");

  useEffect(() => {
    const data = JSON.parse(window.localStorage.getItem("timetable"));
    if (data && data.timetable) {
      const hasTba = data.timetable.some(
        (r) => !r.start_time || !r.end_time || String(r.start_time).toUpperCase() === "TBA" || String(r.end_time).toUpperCase() === "TBA"
      );
      setTimetable(hasTba ? assignClientSlots(data.timetable) : data.timetable);
      setDept(data.department || data.department_code || "");
      setLevel(data.level || "");
    }
  }, []);

  return (
    <AppShell title={`${dept || "Department"} ${level || ""} Timetable`.trim()} subtitle="Review in grid or list view and export as needed.">
      <div className="w-full">
        <div className="mb-3">
          <BackButton label="Back to Lookup" />
        </div>
        <h1 className="text-2xl font-bold mb-2 text-cu-purple">{dept} {level} Timetable</h1>
        <ExportBar timetable={timetable} department={dept} level={level} />
        <TimetableGrid timetable={timetable} />
      </div>
    </AppShell>
  );
}
