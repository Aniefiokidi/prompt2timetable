import React, { useMemo, useState } from "react";
import AppShell from "../components/AppShell";
import TimetableGrid from "../components/TimetableGrid";
import { getStudentTimetable } from "../services/api";

const seedMessages = [
  { role: "assistant", text: "Hello Admin! 👋 How can I help you today?" },
  { role: "user", text: "Generate timetable for 200 level Computer Science." },
  { role: "assistant", text: "Sure! I’ll prepare the timetable and run conflict checks." },
];

const sampleTimetable = [
  { day: "Monday", course_code: "CSC201", room: "Room 101", lecturer: "Dr. Adebayo", start_time: "08:00", end_time: "10:00" },
  { day: "Tuesday", course_code: "MTH201", room: "Room 102", lecturer: "Dr. Bello", start_time: "08:00", end_time: "10:00" },
  { day: "Thursday", course_code: "PHY202", room: "Lab 1", lecturer: "Dr. Jibril", start_time: "08:00", end_time: "10:00" },
  { day: "Wednesday", course_code: "CSC205", room: "Room 101", lecturer: "Dr. Adebayo", start_time: "10:00", end_time: "12:00" },
  { day: "Friday", course_code: "CSC203", room: "Room 101", lecturer: "Dr. Adebayo", start_time: "10:00", end_time: "12:00" },
];

export default function ChatTimetablePage() {
  const [messages, setMessages] = useState(seedMessages);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [timetable, setTimetable] = useState(() => {
    const local = JSON.parse(window.localStorage.getItem("timetable") || "null");
    return local?.timetable?.length ? local.timetable : sampleTimetable;
  });

  const aliasConfig = useMemo(
    () => ({
      MIS: {
        aliases: ["MIS", "MANAGEMENT INFORMATION SYSTEM", "MANAGEMENT INFORMATION SYSTEMS"],
        college: "CST",
        department_code: "CIS",
        department_name: "Department of Computer and Information Sciences",
        programme: "Management Information Systems",
      },
      ICE: {
        aliases: ["ICE", "INFORMATION COMMUNICATION ENGINEERING", "INFORMATION AND COMMUNICATION ENGINEERING"],
        college: "COE",
        department_code: "EIE",
        department_name: "Department of Electrical and Information Engineering",
        programme: "Information and Communication Engineering",
      },
      EIE: {
        aliases: ["EIE", "EEE", "ELECTRICAL ENGINEERING", "ELECTRICAL AND ELECTRONICS ENGINEERING"],
        college: "COE",
        department_code: "EIE",
        department_name: "Department of Electrical and Information Engineering",
        programme: "Electrical and Electronics Engineering",
      },
      CSC: {
        aliases: ["CSC", "COMPUTER SCIENCE"],
        college: "CST",
        department_code: "CIS",
        department_name: "Department of Computer and Information Sciences",
        programme: "Computer Science",
      },
      MAC: {
        aliases: ["MAC", "MASS COMMUNICATION"],
        college: "CMSS",
        department_code: "MAC",
        department_name: "Department of Mass Communication",
        programme: "Mass Communication",
      },
    }),
    []
  );

  const parsePrompt = (text) => {
    const upper = text.toUpperCase();
    const levelMatch = upper.match(/\b(100|200|300|400|500)\b/);
    const level = levelMatch ? levelMatch[1] : null;

    const aliasEntry = Object.values(aliasConfig).find((cfg) => cfg.aliases.some((a) => upper.includes(a)));
    if (!aliasEntry || !level) return null;

    return {
      college: aliasEntry.college,
      department: aliasEntry.department_code,
      department_code: aliasEntry.department_code,
      department_name: aliasEntry.department_name,
      programme: aliasEntry.programme,
      level,
    };
  };

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userText = input.trim();
    setMessages((prev) => [...prev, { role: "user", text: userText }]);
    setInput("");

    const payload = parsePrompt(userText);
    if (!payload) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Please include both a level (e.g., 200) and a course/department keyword (e.g., MIS, ICE, EIE, CSC, MAC).",
        },
      ]);
      return;
    }

    try {
      setLoading(true);
      const data = await getStudentTimetable(payload);
      setTimetable(data.timetable || []);
      window.localStorage.setItem("timetable", JSON.stringify(data));
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: `Timetable generated for ${payload.level} level ${payload.programme}.` },
      ]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: e.message || "Unable to generate timetable right now." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppShell title="AI Timetable Assistant" subtitle="Chat-based timetable generation + live timetable view.">
      <div className="grid grid-cols-1 xl:grid-cols-[360px,1fr] gap-4">
        <div className="rounded-xl border border-slate-200 bg-white overflow-hidden">
          <div className="px-4 py-3 border-b border-slate-200 flex items-center justify-between">
            <h3 className="font-semibold text-slate-800">AI Timetable Assistant</h3>
            <button
              className="text-xs rounded-md border px-2 py-1"
              onClick={() => setMessages([{ role: "assistant", text: "New chat started. Ask for a timetable, e.g. 'Generate 300 MIS timetable'." }])}
            >
              New Chat
            </button>
          </div>
          <div className="p-3 h-[460px] overflow-y-auto space-y-3 bg-slate-50">
            {messages.map((m, i) => (
              <div
                key={i}
                className={`max-w-[90%] rounded-xl px-3 py-2 text-sm ${m.role === "user" ? "ml-auto bg-cu-purple text-white" : "bg-white border border-slate-200 text-slate-700"}`}
              >
                {m.text}
              </div>
            ))}
          </div>
          <div className="p-3 border-t border-slate-200 flex gap-2">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              className="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm"
              placeholder="Type your request..."
            />
            <button onClick={sendMessage} disabled={loading} className="rounded-lg bg-cu-purple text-cu-gold px-4 disabled:opacity-50">
              {loading ? "..." : "Send"}
            </button>
          </div>
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-3">
          <TimetableGrid timetable={timetable} />
        </div>
      </div>
    </AppShell>
  );
}
