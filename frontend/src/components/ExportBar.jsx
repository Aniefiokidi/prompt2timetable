import React from "react";

export default function ExportBar({ timetable, department, level }) {
  function download(format) {
    let content = "";
    let filename = `${department}_${level}_timetable`;
    if (format === "csv") {
      const header = "Course Code,Day,Start Time,End Time,Room,Lecturer,Level,Department\n";
      content = header + timetable.map(c => [c.course_code, c.day, c.start_time, c.end_time, c.room, c.lecturer, c.level, c.department].join(",")).join("\n");
      filename += ".csv";
      const blob = new Blob([content], { type: "text/csv" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      a.click();
      URL.revokeObjectURL(url);
    } else if (format === "text") {
      content = `${department} ${level} Timetable\n`;
      const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
      for (const day of days) {
        content += `\n${day}:\n`;
        const dayCourses = timetable.filter(c => c.day === day);
        if (dayCourses.length === 0) {
          content += "  No classes\n";
        } else {
          for (const c of dayCourses) {
            content += `  ${c.start_time}-${c.end_time}: ${c.course_code} (${c.room}) ${c.lecturer}\n`;
          }
        }
      }
      filename += ".txt";
      const blob = new Blob([content], { type: "text/plain" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      a.click();
      URL.revokeObjectURL(url);
    } else if (format === "pdf") {
      window.print(); // Use browser print for PDF
    }
  }

  return (
    <div className="flex flex-wrap gap-3 mb-5">
      <button
        className="inline-flex items-center gap-2 bg-cu-purple hover:bg-purple-900 text-cu-gold px-4 py-2.5 rounded-lg shadow-sm transition"
        onClick={() => download("pdf")}
      >
        Download PDF
      </button>
      <button
        className="inline-flex items-center gap-2 bg-white border border-cu-purple/30 hover:bg-cu-purple/5 text-cu-purple px-4 py-2.5 rounded-lg shadow-sm transition"
        onClick={() => download("text")}
      >
        Download Text
      </button>
      <button
        className="inline-flex items-center gap-2 bg-white border border-cu-purple/30 hover:bg-cu-purple/5 text-cu-purple px-4 py-2.5 rounded-lg shadow-sm transition"
        onClick={() => download("csv")}
      >
        Download CSV
      </button>
    </div>
  );
}
