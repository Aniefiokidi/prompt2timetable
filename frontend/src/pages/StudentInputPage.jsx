import React, { useState, useEffect } from "react";
import { getDepartments, getStudentTimetable } from "../services/api";


const CU_STRUCTURE = [
  {
    college: "COE",
    name: "College of Engineering",
    departments: [
      { name: "Department of Chemical Engineering", code: "CHE", programmes: ["Chemical Engineering"] },
      { name: "Department of Civil Engineering", code: "CVE", programmes: ["Civil Engineering"] },
      { name: "Department of Electrical and Information Engineering", code: "EIE", programmes: ["Computer Engineering", "Electrical and Electronics Engineering", "Information and Communication Engineering"] },
      { name: "Department of Mechanical Engineering", code: "MEE", programmes: ["Mechanical Engineering"] },
      { name: "Department of Petroleum Engineering", code: "PET", programmes: ["Petroleum Engineering"] },
    ]
  },
  {
    college: "CST",
    name: "College of Science and Technology",
    departments: [
      { name: "Department of Architecture", code: "ARC", programmes: ["Architecture"] },
      { name: "Department of Building Technology", code: "BLD", programmes: ["Building Technology"] },
      { name: "Department of Estate Management", code: "EST", programmes: ["Estate Management"] },
      { name: "Department of Biological Sciences", code: "BIO", programmes: ["Biology", "Microbiology"] },
      { name: "Department of Biochemistry", code: "BCH", programmes: ["Biochemistry"] },
      { name: "Department of Chemistry", code: "CHM", programmes: ["Industrial Chemistry"] },
      { name: "Department of Computer and Information Sciences", code: "CIS", programmes: ["Computer Science", "Management Information Systems"] },
      { name: "Department of Mathematics", code: "MTH", programmes: ["Industrial Mathematics (Computer Science Option)", "Industrial Mathematics (Statistics Option)"] },
      { name: "Department of Physics", code: "PHY", programmes: ["Industrial Physics (Applied Geophysics)", "Industrial Physics (Electronics and IT Applications)", "Industrial Physics (Renewable Energy)"] },
    ]
  },
  {
    college: "CLDS",
    name: "College of Leadership and Development Studies",
    departments: [
      { name: "Department of English", code: "ENG", programmes: ["English"] },
      { name: "Department of International Relations", code: "IRL", programmes: ["International Relations"] },
      { name: "Department of Policy and Strategic Studies", code: "PSS", programmes: ["Policy and Strategic Studies"] },
      { name: "Department of Political Science", code: "PSC", programmes: ["Political Science"] },
      { name: "Department of Psychology", code: "PSY", programmes: ["Psychology"] },
    ]
  },
  {
    college: "CMSS",
    name: "College of Management and Social Sciences",
    departments: [
      { name: "Department of Accounting", code: "ACC", programmes: ["Accounting"] },
      { name: "Department of Business Administration", code: "BUS", programmes: ["Business Administration"] },
      { name: "Department of Economics", code: "ECO", programmes: ["Economics"] },
      { name: "Department of Finance", code: "FIN", programmes: ["Finance", "Financial Technology"] },
      { name: "Department of Industrial Relations and Human Resource Management", code: "IRM", programmes: ["Industrial Relations and Human Resource Management"] },
      { name: "Department of Marketing", code: "MKT", programmes: ["Marketing"] },
      { name: "Department of Mass Communication", code: "MAC", programmes: ["Mass Communication"] },
      { name: "Department of Sociology", code: "SOC", programmes: ["Sociology"] },
    ]
  }
];

const LEVELS = ["100", "200", "300", "400", "500"];

export default function StudentInputPage() {
  const [selectedCollege, setSelectedCollege] = useState("");
  const [selectedDepartment, setSelectedDepartment] = useState("");
  const [selectedProgramme, setSelectedProgramme] = useState("");
  const [selectedLevel, setSelectedLevel] = useState("");
  const [error, setError] = useState("");

  const collegeList = CU_STRUCTURE.map(c => ({ code: c.college, name: c.name }));
  const departmentList = selectedCollege
    ? CU_STRUCTURE.find(c => c.college === selectedCollege)?.departments || []
    : [];
  const programmeList = selectedDepartment
    ? departmentList.find(d => d.code === selectedDepartment)?.programmes || []
    : [];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    if (!selectedCollege || !selectedDepartment || !selectedLevel || (programmeList.length > 1 && !selectedProgramme)) {
      setError("Please select your College, Department, Programme (if applicable), and Level.");
      return;
    }
    try {
      // Find department object for code and name
      const deptObj = departmentList.find(d => d.code === selectedDepartment) || {};
      const data = await getStudentTimetable({
        college: selectedCollege,
        department: selectedDepartment, // code
        department_code: selectedDepartment,
        department_name: deptObj.name,
        programme: programmeList.length > 1 ? selectedProgramme : programmeList[0],
        level: selectedLevel
      });
      window.localStorage.setItem("timetable", JSON.stringify(data));
      window.location.href = "/timetable";
    } catch (err) {
      setError(err.message || "Failed to fetch timetable.");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-white p-4">
      <form className="bg-cu-purple/10 rounded-xl shadow-lg p-8 w-full max-w-md" onSubmit={handleSubmit}>
        <h2 className="text-2xl font-bold mb-4 text-cu-purple">Departmental Timetable Lookup</h2>
        <div className="mb-4">
          <label className="block mb-1 font-medium text-cu-purple">College</label>
          <select
            className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cu-gold"
            value={selectedCollege}
            onChange={e => {
              setSelectedCollege(e.target.value);
              setSelectedDepartment("");
              setSelectedProgramme("");
            }}
          >
            <option value="">Select College</option>
            {collegeList.map(c => <option key={c.code} value={c.code}>{c.name}</option>)}
          </select>
        </div>
        <div className="mb-4">
          <label className="block mb-1 font-medium text-cu-purple">Department</label>
          <select
            className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cu-gold"
            value={selectedDepartment}
            onChange={e => {
              setSelectedDepartment(e.target.value);
              setSelectedProgramme("");
            }}
            disabled={!selectedCollege}
          >
            <option value="">Select Department</option>
            {departmentList.map(d => (
              <option key={d.code} value={d.code}>{d.name}</option>
            ))}
          </select>
        </div>
        {programmeList.length > 1 && (
          <div className="mb-4">
            <label className="block mb-1 font-medium text-cu-purple">Programme</label>
            <select
              className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cu-gold"
              value={selectedProgramme}
              onChange={e => setSelectedProgramme(e.target.value)}
              disabled={!selectedDepartment}
            >
              <option value="">Select Programme</option>
              {programmeList.map(p => (
                <option key={p} value={p}>{p}</option>
              ))}
            </select>
          </div>
        )}
        <div className="mb-4">
          <label className="block mb-1 font-medium text-cu-purple">Level</label>
          <select
            className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cu-gold"
            value={selectedLevel}
            onChange={e => setSelectedLevel(e.target.value)}
          >
            <option value="">Select Level</option>
            {LEVELS.map(l => <option key={l} value={l}>{l}</option>)}
          </select>
        </div>
        {error && <div className="mt-4 text-red-600">{error}</div>}
        <button
          type="submit"
          className="mt-8 w-full bg-cu-purple hover:bg-purple-900 text-cu-gold font-semibold px-6 py-3 rounded-lg shadow transition-all"
        >
          View Timetable
        </button>
      </form>
    </div>
  );
}
