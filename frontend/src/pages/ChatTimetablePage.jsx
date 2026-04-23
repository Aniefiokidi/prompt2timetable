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
  const [pendingRequest, setPendingRequest] = useState(null);
  const [timetable, setTimetable] = useState(() => {
    const local = JSON.parse(window.localStorage.getItem("timetable") || "null");
    return local?.timetable?.length ? local.timetable : sampleTimetable;
  });

  const aliasConfig = useMemo(
    () => [
      { aliases: ["MIS", "MANAGEMENT INFORMATION SYSTEM", "MANAGEMENT INFORMATION SYSTEMS"], college: "CST", department_code: "CIS", department_name: "Department of Computer and Information Sciences", programme: "Management Information Systems" },
      { aliases: ["CSC", "COS", "COMPUTER SCIENCE"], college: "CST", department_code: "CIS", department_name: "Department of Computer and Information Sciences", programme: "Computer Science" },
      { aliases: ["ICE", "INFORMATION COMMUNICATION ENGINEERING", "INFORMATION AND COMMUNICATION ENGINEERING"], college: "COE", department_code: "EIE", department_name: "Department of Electrical and Information Engineering", programme: "Information and Communication Engineering" },
      { aliases: ["EIE", "EEE", "ELECTRICAL ENGINEERING", "ELECTRICAL AND ELECTRONICS ENGINEERING"], college: "COE", department_code: "EIE", department_name: "Department of Electrical and Information Engineering", programme: "Electrical and Electronics Engineering" },
      { aliases: ["CEN", "COMPUTER ENGINEERING"], college: "COE", department_code: "EIE", department_name: "Department of Electrical and Information Engineering", programme: "Computer Engineering" },
      { aliases: ["CHE", "CHEMICAL ENGINEERING"], college: "COE", department_code: "CHE", department_name: "Department of Chemical Engineering", programme: "Chemical Engineering" },
      { aliases: ["CVE", "CIVIL ENGINEERING"], college: "COE", department_code: "CVE", department_name: "Department of Civil Engineering", programme: "Civil Engineering" },
      { aliases: ["MEE", "MCE", "MECHANICAL ENGINEERING"], college: "COE", department_code: "MCE", department_name: "Department of Mechanical Engineering", programme: "Mechanical Engineering" },
      { aliases: ["PET", "PETROLEUM ENGINEERING"], college: "COE", department_code: "PET", department_name: "Department of Petroleum Engineering", programme: "Petroleum Engineering" },
      { aliases: ["ARC", "ARCHITECTURE"], college: "CST", department_code: "ARC", department_name: "Department of Architecture", programme: "Architecture" },
      { aliases: ["BLD", "BUILDING TECHNOLOGY"], college: "CST", department_code: "BLD", department_name: "Department of Building Technology", programme: "Building Technology" },
      { aliases: ["EST", "ESM", "ESTATE MANAGEMENT"], college: "CST", department_code: "ESM", department_name: "Department of Estate Management", programme: "Estate Management" },
      { aliases: ["BIO", "BIOLOGY", "MICROBIOLOGY", "BIOLOGICAL SCIENCES"], college: "CST", department_code: "BIO", department_name: "Department of Biological Sciences", programme: "Biology" },
      { aliases: ["BCH", "BIOCHEMISTRY"], college: "CST", department_code: "BCH", department_name: "Department of Biochemistry", programme: "Biochemistry" },
      { aliases: ["CHM", "ICH", "INDUSTRIAL CHEMISTRY", "CHEMISTRY"], college: "CST", department_code: "CHM", department_name: "Department of Chemistry", programme: "Industrial Chemistry" },
      { aliases: ["MTH", "MAT", "MATHEMATICS", "INDUSTRIAL MATHEMATICS"], college: "CST", department_code: "MAT", department_name: "Department of Mathematics", programme: "Industrial Mathematics (Computer Science Option)" },
      { aliases: ["PHY", "PHYSICS", "INDUSTRIAL PHYSICS"], college: "CST", department_code: "PHY", department_name: "Department of Physics", programme: "Industrial Physics (Electronics and IT Applications)" },
      { aliases: ["ENG", "ENGLISH"], college: "CLDS", department_code: "ENG", department_name: "Department of English", programme: "English" },
      { aliases: ["IRL", "INTERNATIONAL RELATIONS"], college: "CLDS", department_code: "IRL", department_name: "Department of International Relations", programme: "International Relations" },
      { aliases: ["PSS", "POLICY AND STRATEGIC STUDIES"], college: "CLDS", department_code: "PSS", department_name: "Department of Policy and Strategic Studies", programme: "Policy and Strategic Studies" },
      { aliases: ["PSC", "POS", "POLITICAL SCIENCE"], college: "CLDS", department_code: "POS", department_name: "Department of Political Science", programme: "Political Science" },
      { aliases: ["PSY", "PSI", "PSYCHOLOGY"], college: "CLDS", department_code: "PSY", department_name: "Department of Psychology", programme: "Psychology" },
      { aliases: ["ACC", "ACCOUNTING"], college: "CMSS", department_code: "ACC", department_name: "Department of Accounting", programme: "Accounting" },
      { aliases: ["BUS", "BUA", "BUSINESS ADMINISTRATION"], college: "CMSS", department_code: "BUA", department_name: "Department of Business Administration", programme: "Business Administration" },
      { aliases: ["ECO", "ECN", "ECONOMICS"], college: "CMSS", department_code: "ECN", department_name: "Department of Economics", programme: "Economics" },
      { aliases: ["FIN", "FINANCE", "FINANCIAL TECHNOLOGY"], college: "CMSS", department_code: "FIN", department_name: "Department of Finance", programme: "Finance" },
      { aliases: ["IRM", "IRH", "INDUSTRIAL RELATIONS", "HUMAN RESOURCE MANAGEMENT"], college: "CMSS", department_code: "IRH", department_name: "Department of Industrial Relations and Human Resource Management", programme: "Industrial Relations and Human Resource Management" },
      { aliases: ["MKT", "MARKETING"], college: "CMSS", department_code: "MKT", department_name: "Department of Marketing", programme: "Marketing" },
      { aliases: ["MAC", "MASS COMMUNICATION"], college: "CMSS", department_code: "MAC", department_name: "Department of Mass Communication", programme: "Mass Communication" },
      { aliases: ["SOC", "SOCIOLOGY"], college: "CMSS", department_code: "SOC", department_name: "Department of Sociology", programme: "Sociology" },
    ],
    []
  );

  const parsePrompt = (text) => {
    const upper = text.toUpperCase();
    const levelMatch = upper.match(/\b(100|200|300|400|500)\b/);
    const level = levelMatch ? levelMatch[1] : null;

    const codeMatch = upper.match(/\b([A-Z]{2,4})\s*\d{3}\b/);
    const codePrefix = codeMatch ? codeMatch[1] : null;
    const aliasEntry =
      aliasConfig.find((cfg) => cfg.aliases.some((a) => upper.includes(a))) ||
      (codePrefix ? aliasConfig.find((cfg) => cfg.aliases.includes(codePrefix)) : null);

    return {
      aliasEntry,
      level,
    };
  };

  const buildPayload = (parsed) => {
    if (!parsed?.aliasEntry || !parsed?.level) return null;
    return {
      college: parsed.aliasEntry.college,
      department: parsed.aliasEntry.department_code,
      department_code: parsed.aliasEntry.department_code,
      department_name: parsed.aliasEntry.department_name,
      programme: parsed.aliasEntry.programme,
      level: parsed.level,
    };
  };

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userText = input.trim();
    setMessages((prev) => [...prev, { role: "user", text: userText }]);
    setInput("");

    const parsed = parsePrompt(userText);
    const combined = {
      aliasEntry: parsed.aliasEntry || pendingRequest?.aliasEntry || null,
      level: parsed.level || pendingRequest?.level || null,
    };

    if (!combined.aliasEntry && combined.level) {
      setPendingRequest({ level: combined.level });
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: `Got level ${combined.level}. Please add department/course (e.g., MIS, ICE, EIE, Architecture, CSC111).` },
      ]);
      return;
    }

    if (combined.aliasEntry && !combined.level) {
      setPendingRequest({ aliasEntry: combined.aliasEntry });
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: `Got ${combined.aliasEntry.programme}. Please add the level (100/200/300/400/500).` },
      ]);
      return;
    }

    const payload = buildPayload(combined);
    if (!payload) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Please include a level and course/department. I understand short or full forms (e.g., MIS, ICE, EIE, Architecture, CSC111).",
        },
      ]);
      return;
    }

    try {
      setLoading(true);
      const data = await getStudentTimetable(payload);
      setTimetable(data.timetable || []);
      window.localStorage.setItem("timetable", JSON.stringify(data));
      setPendingRequest(null);
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
      <div className="grid grid-cols-1 xl:grid-cols-[minmax(320px,420px),minmax(0,1fr)] gap-4">
        <div className="rounded-xl border border-slate-200 bg-white overflow-hidden min-h-[560px]">
          <div className="px-4 py-3 border-b border-slate-200 flex items-center justify-between">
            <h3 className="font-semibold text-slate-800">AI Timetable Assistant</h3>
            <button
              className="text-xs rounded-md border px-2 py-1"
              onClick={() => {
                setPendingRequest(null);
                setMessages([{ role: "assistant", text: "New chat started. Ask for a timetable, e.g. '300 MIS' or 'Architecture 100'." }]);
              }}
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

        <div className="rounded-xl border border-slate-200 bg-white p-3 overflow-hidden">
          <TimetableGrid timetable={timetable} />
        </div>
      </div>
    </AppShell>
  );
}
