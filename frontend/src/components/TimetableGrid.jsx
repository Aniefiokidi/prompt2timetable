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

function parseStartHour(startTime) {
  if (!startTime) return null;
  const raw = String(startTime).trim();
  const m = raw.match(/^(\d{1,2})(?::\d{2})?\s*(AM|PM)?$/i);
  if (!m) return null;
  let hour = parseInt(m[1], 10);
  const meridiem = (m[2] || "").toUpperCase();
  if (meridiem === "PM" && hour < 12) hour += 12;
  if (meridiem === "AM" && hour === 12) hour = 0;
  return Number.isNaN(hour) ? null : hour;
}

function getTimeLabel(course) {
  const start = course.start_time || "TBA";
  const end = course.end_time || "TBA";
  return `${start} - ${end}`;
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
    <div className="w-full max-w-5xl mx-auto mt-4">
      {clashes.length > 0 && (
        <div className="bg-red-50 border border-red-300 text-red-700 px-4 py-3 rounded-lg mb-4 text-sm">
          Warning: {clashes.length} slot{clashes.length > 1 ? "s" : ""} have course clashes!
        </div>
      )}
      <div className="flex justify-end mb-3">
        <div className="bg-slate-100 rounded-lg p-1 border border-slate-200">
        <button
          className={`px-4 py-1.5 rounded-md ${view === "grid" ? "bg-cu-purple text-cu-gold shadow-sm" : "text-slate-700"}`}
          onClick={() => setView("grid")}
        >Grid View</button>
        <button
          className={`px-4 py-1.5 rounded-md ${view === "list" ? "bg-cu-purple text-cu-gold shadow-sm" : "text-slate-700"}`}
          onClick={() => setView("list")}
        >List View</button>
        </div>
      </div>
      {view === "grid" ? (
        <div className="overflow-x-auto rounded-xl border border-slate-200 shadow-sm bg-white">
          <table className="min-w-full">
            <thead>
              <tr>
                <th className="border-b border-r p-3 bg-cu-purple text-cu-gold">Time</th>
                {DAYS.map(day => (
                  <th key={day} className="border-b border-r last:border-r-0 p-3 bg-cu-purple text-cu-gold">{day}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {HOURS.map(hour => (
                <tr key={hour}>
                  <td className="border-b border-r p-2.5 font-semibold bg-slate-50 text-slate-700">{hour}:00 - {hour + 1}:00</td>
                  {DAYS.map(day => {
                    const cellCourses = timetable.filter(c => {
                      const start = parseStartHour(c.start_time);
                      return c.day === day && start === hour;
                    });
                    return (
                      <td key={day} className="border-b border-r last:border-r-0 p-1.5 align-top min-w-[140px] h-16">
                        {cellCourses.map((course, idx) => (
                          <div
                            key={course.course_code + idx}
                            className="rounded-md p-1.5 mb-1 cursor-pointer relative shadow-sm"
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
              <tr>
                <td className="border-r p-2.5 font-semibold bg-slate-50 text-slate-700">Unscheduled</td>
                {DAYS.map(day => {
                  const unscheduledCourses = timetable.filter(c => {
                    const start = parseStartHour(c.start_time);
                    return c.day === day && (start === null || Number.isNaN(start));
                  });
                  return (
                    <td key={`${day}-unscheduled`} className="border-r last:border-r-0 p-1.5 align-top min-w-[140px]">
                      {unscheduledCourses.map((course, idx) => (
                        <div
                          key={course.course_code + idx}
                          className="rounded-md p-1.5 mb-1 cursor-pointer relative shadow-sm"
                          style={{ background: getColor(course.course_code) }}
                          onClick={() => setSelected(course)}
                        >
                          <span className="font-bold">{course.course_code}</span>
                          <div className="text-xs">{course.room}</div>
                          <div className="text-xs">{getTimeLabel(course)}</div>
                        </div>
                      ))}
                    </td>
                  );
                })}
              </tr>
            </tbody>
          </table>
        </div>
      ) : (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4">
          {DAYS.map(day => (
            <div key={day} className="mb-4">
              <h3 className="font-bold text-cu-purple mb-2">{day}</h3>
              {timetable.filter(c => c.day === day).length === 0 && <div className="text-gray-400">No classes</div>}
              {timetable
                .filter(c => c.day === day)
                .sort((a, b) => {
                  const ah = parseStartHour(a.start_time);
                  const bh = parseStartHour(b.start_time);
                  if (ah === null && bh === null) return 0;
                  if (ah === null) return 1;
                  if (bh === null) return -1;
                  return ah - bh;
                })
                .map((course, idx) => (
                <div
                  key={course.course_code + idx}
                  className="rounded p-2 mb-2 cursor-pointer border-l-4"
                  style={{ borderColor: getColor(course.course_code), background: "#f9fafb" }}
                  onClick={() => setSelected(course)}
                >
                  <span className="font-bold">{course.course_code}</span>
                  <span className="ml-2 text-xs">{course.room}</span>
                  <span className="ml-2 text-xs">{course.lecturer}</span>
                  <span className="ml-2 text-xs font-medium">{getTimeLabel(course)}</span>
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
