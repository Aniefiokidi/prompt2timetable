import React, { useEffect, useState } from "react";
import TimetableGrid from "../components/TimetableGrid";
import ExportBar from "../components/ExportBar";

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
    <div className="min-h-screen bg-white p-4">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-2xl font-bold mb-2 text-cu-purple">{dept} {level} Timetable</h1>
        <ExportBar timetable={timetable} department={dept} level={level} />
        <TimetableGrid timetable={timetable} />
      </div>
    </div>
  );
}
