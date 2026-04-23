import React from "react";

export default function CourseCard({ course, timetable, onClose }) {
  if (!course) return null;
  const clean = (v) => {
    const t = String(v || "").trim();
    return !t || t.toUpperCase() === "TBA" ? "-" : t;
  };
  const allSessions = timetable.filter(c => c.course_code === course.course_code);
  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 z-50 flex justify-end">
      <div className="w-full max-w-md bg-white h-full shadow-xl p-6 overflow-y-auto relative animate-slidein border-l-8 border-cu-purple">
        <button className="absolute top-4 right-4 text-2xl" onClick={onClose}>&times;</button>
        <h2 className="text-2xl font-bold mb-2 text-cu-purple">{course.course_code}</h2>
        <div className="mb-2 text-lg font-semibold">{course.course_title || ""}</div>
        <div className="mb-2">Lecturer: <span className="font-medium">{clean(course.lecturer)}</span></div>
        <div className="mb-2">Room: <span className="font-medium">{clean(course.room)}</span></div>
        <div className="mb-2">Level: <span className="font-medium">{course.level}</span></div>
        <div className="mb-2">Department: <span className="font-medium">{course.department}</span></div>
        <div className="mb-2">Total Course Hours: <span className="font-medium">{course.duration || course["COURSE LOAD(HOURS)"] || "-"}</span></div>
        <div className="mb-2">Sessions:</div>
        <ul className="mb-4 list-disc ml-6">
          {allSessions.map((s, idx) => (
            <li key={idx}>
              {s.day}, {clean(s.start_time)} - {clean(s.end_time)} ({clean(s.room)})
            </li>
          ))}
        </ul>
      </div>
      <style>{`
        .animate-slidein {
          animation: slidein 0.3s cubic-bezier(.4,0,.2,1);
        }
        @keyframes slidein {
          from { transform: translateX(100%); }
          to { transform: translateX(0); }
        }
      `}</style>
    </div>
  );
}
