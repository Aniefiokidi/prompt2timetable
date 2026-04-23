import React, { useEffect, useState } from "react";
import TimetableGrid from "../components/TimetableGrid";
import ExportBar from "../components/ExportBar";
import AppShell from "../components/AppShell";
import BackButton from "../components/BackButton";

export default function TimetablePage() {
  const [timetable, setTimetable] = useState([]);
  const [dept, setDept] = useState("");
  const [level, setLevel] = useState("");

  useEffect(() => {
    const data = JSON.parse(window.localStorage.getItem("timetable"));
    if (data && data.timetable) {
      setTimetable(data.timetable);
      setDept(data.department || data.department_code || "");
      setLevel(data.level || "");
    }
  }, []);

  return (
    <AppShell title={`${dept || "Department"} ${level || ""} Timetable`.trim()} subtitle="Review in grid or list view and export as needed.">
      <div className="max-w-5xl">
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
