import json
import os
from constraints import extract_constraints, load_processed_data

def build_few_shot_examples():
    # Example: course → timeslot assignment
    return [
        {
            "course_code": "CST101",
            "day": "Monday",
            "start_time": "09:00",
            "end_time": "11:00",
            "room": "LT1",
            "lecturer": "Dr. Smith",
            "level": "100",
            "department": "CST"
        },
        {
            "course_code": "MTH201",
            "day": "Tuesday",
            "start_time": "11:00",
            "end_time": "13:00",
            "room": "LT2",
            "lecturer": "Prof. Jane",
            "level": "200",
            "department": "CMSS"
        }
    ]

def build_prompt():
    constraints = extract_constraints()
    data = load_processed_data()
    courses = data['timetable']
    few_shot = build_few_shot_examples()
    system_prompt = (
        "You are a university timetable scheduling assistant. "
        "You must assign each course to a timeslot, room, and lecturer, strictly obeying all HARD constraints and minimizing SOFT constraint violations. "
        "Output must be a JSON array, one object per course, with fields: course_code, day, start_time, end_time, room, lecturer, level, department. "
        "HARD constraints: " + json.dumps(constraints['hard']) + ". "
        "SOFT constraints: " + json.dumps(constraints['soft']) + ". "
        "Here are a few examples of the expected output format: " + json.dumps(few_shot) + ". "
        "Do not invent courses or timeslots. Use only the provided course list."
    )
    user_prompt = (
        "Assign timeslots for the following courses (all departments):\n" +
        json.dumps([
            {
                "course_code": c.get("COURSE CODE", ""),
                "course_title": c.get("COURSE TITLE", ""),
                "lecturer": c.get("LECTURER'S NAME", ""),
                "room": c.get("CLASSROOM(VENUE)", ""),
                "level": c.get("LEVEL", ""),
                "department": c.get("DEPARTMENT", ""),
                "duration": c.get("COURSE LOAD(HOURS)", ""),
                "students": c.get("NO OF STUDENT PER COURSE", "")
            }
            for c in courses
        ], indent=2)
    )
    return {"system_prompt": system_prompt, "user_prompt": user_prompt}

if __name__ == "__main__":
    prompts = build_prompt()
    print(json.dumps(prompts, indent=2))
