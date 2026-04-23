import React, { useState, useEffect } from "react";
import { getDepartments } from "../services/api";

const DEPT_MAP = {
  CSC: "Computer Science",
  EEE: "Electrical Engineering",
  MEC: "Mechanical Engineering",
  MEE: "Mechatronics Engineering",
  SEN: "Software Engineering",
  BCH: "Biochemistry",
  // Add more as needed
};

function formatMatric(val) {
  // Auto-insert slashes as user types
  let v = val.replace(/[^a-zA-Z0-9]/g, "").toUpperCase();
  if (v.length > 2) v = v.slice(0, 2) + "/" + v.slice(2);
  if (v.length > 6) v = v.slice(0, 6) + "/" + v.slice(6);
  return v.slice(0, 12);
}

function validateMatric(val) {
  const re = /^CU(\d{2})\/([A-Z]{3})\/(\d{5})$/i;
  const match = re.exec(val.trim().toUpperCase());
  if (!match) return { valid: false, dept: "" };
  const dept = match[2];
  return { valid: !!DEPT_MAP[dept], dept: DEPT_MAP[dept] || dept };
}

export default function MatricInput({ value, onChange }) {
  const [input, setInput] = useState(value || "");
  const [touched, setTouched] = useState(false);
  const { valid, dept } = validateMatric(input);

  useEffect(() => {
    onChange(input, valid, dept);
    // eslint-disable-next-line
  }, [input, valid, dept]);

  return (
    <div className="mb-4">
      <label className="block mb-1 font-medium text-cu-purple">Matric Number</label>
      <input
        type="text"
        className={`w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 ${valid ? "border-green-500 focus:ring-green-300" : touched ? "border-red-500 focus:ring-red-300" : "focus:ring-cu-gold"}`}
        value={input}
        onChange={e => setInput(formatMatric(e.target.value))}
        onBlur={() => setTouched(true)}
        placeholder="CU25/CSC/01234"
        maxLength={12}
        autoComplete="off"
      />
      {valid && (
        <div className="text-green-700 mt-1 flex items-center gap-1">
          <span>✔️</span> Valid
        </div>
      )}
      {!valid && touched && (
        <div className="text-red-600 mt-1">
          Invalid format. Example: CU25/CSC/01234
        </div>
      )}
    </div>
  );
}
