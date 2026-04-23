import React, { useState, useEffect } from "react";
import CourseCard from "./CourseCard";

const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
const HOURS = Array.from({ length: 12 }, (_, i) => 7 + i); // 7am to 6pm

function getColor(courseCode) {
  // Consistent pastel color per course
  let hash = 0;
  for (let i = 0; i < courseCode.length; i++) hash = courseCode.charCodeAt(i) + ((hash << 5) - hash);
  const h = hash % 360;
  return `hsl(${h}, 70%, 85%)`;
}



function detectClashes(timetable) {
  const slots = {};
  for (const c of timetable) {
    const key = `${c.day}-${c.start_time}`;
    if (!slots[key]) slots[key] = [];
    slots[key].push(c);
  }
  return Object.values(slots).filter(arr => arr.length > 1);
}


export default function TimetableGrid({ timetable }) {
  const [selected, setSelected] = useState(null);
  const [view, setView] = useState(window.innerWidth < 640 ? "list" : "grid");
  const clashes = detectClashes(timetable);

  useEffect(() => {
    const handler = () => setView(window.innerWidth < 640 ? "list" : "grid");
    window.addEventListener("resize", handler);
    return () => window.removeEventListener("resize", handler);
  }, []);

  if (!timetable || timetable.length === 0) return <div>No timetable data.</div>;

  return (
    <div className="w-full max-w-5xl mx-auto mt-6">
      {clashes.length > 0 && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded mb-4">
          Warning: {clashes.length} slot{clashes.length > 1 ? "s" : ""} have course clashes!
        </div>
      )}
      <div className="flex justify-end mb-2">
        <button
          className={`px-3 py-1 rounded-l ${view === "grid" ? "bg-cu-purple text-cu-gold" : "bg-gray-200"}`}
          onClick={() => setView("grid")}
        >Grid View</button>
        <button
          className={`px-3 py-1 rounded-r ${view === "list" ? "bg-cu-purple text-cu-gold" : "bg-gray-200"}`}
          onClick={() => setView("list")}
        >List View</button>
      </div>
      {view === "grid" ? (
        <div className="overflow-x-auto">
          <table className="min-w-full border border-gray-300 bg-white">
            <thead>
              <tr>
                <th className="border p-2 bg-cu-purple text-cu-gold">Time</th>
                {DAYS.map(day => (
                  <th key={day} className="border p-2 bg-cu-purple text-cu-gold">{day}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {HOURS.map(hour => (
                <tr key={hour}>
                  <td className="border p-2 font-semibold bg-gray-50">{hour}:00 - {hour + 1}:00</td>
                  {DAYS.map(day => {
                    const cellCourses = timetable.filter(c => {
                      const start = parseInt(c.start_time.split(":")[0], 10);
                      return c.day === day && start === hour;
                    });
                    return (
                      <td key={day} className="border p-1 align-top min-w-[120px] h-16">
                        {cellCourses.map((course, idx) => (
                          <div
                            key={course.course_code + idx}
                            className="rounded p-1 mb-1 cursor-pointer relative"
                            style={{ background: getColor(course.course_code) }}
                            onClick={() => setSelected(course)}
                          >
                            <span className="font-bold">{course.course_code}</span>
                            <div className="text-xs">{course.room}</div>
                            <div className="text-xs">{course.lecturer}</div>
                          </div>
                        ))}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="bg-white rounded shadow p-4">
          {DAYS.map(day => (
            <div key={day} className="mb-4">
              <h3 className="font-bold text-cu-purple mb-2">{day}</h3>
              {timetable.filter(c => c.day === day).length === 0 && <div className="text-gray-400">No classes</div>}
              {timetable.filter(c => c.day === day).map((course, idx) => (
                <div
                  key={course.course_code + idx}
                  className="rounded p-2 mb-2 cursor-pointer border-l-4"
                  style={{ borderColor: getColor(course.course_code), background: "#f9fafb" }}
                  onClick={() => setSelected(course)}
                >
                  <span className="font-bold">{course.course_code}</span>
                  <span className="ml-2 text-xs">{course.room}</span>
                  <span className="ml-2 text-xs">{course.lecturer}</span>
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
      {selected && (
        <CourseCard course={selected} timetable={timetable} onClose={() => setSelected(null)} />
      )}
    </div>
  );
}
