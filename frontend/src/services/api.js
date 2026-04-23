const API = "http://localhost:8000/api";

export async function getStudentTimetable({ college, department, department_code, department_name, programme, level }) {
  const res = await fetch(`${API}/student/timetable`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      college,
      department,
      department_code,
      department_name,
      programme,
      level
    })
  });
  if (!res.ok) throw new Error((await res.json()).error || "Failed to fetch timetable");
  return await res.json();
}

export async function getAllCourses() {
  const res = await fetch(`${API}/courses`);
  if (!res.ok) throw new Error("Failed to fetch courses");
  const data = await res.json();
  return data.courses || [];
}

export async function getDepartments() {
  const res = await fetch(`${API}/departments`);
  if (!res.ok) throw new Error("Failed to fetch departments");
  const data = await res.json();
  return data.departments || [];
}
