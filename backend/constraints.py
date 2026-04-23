import json
import os

def load_processed_data():
    path = os.path.join(os.path.dirname(__file__), 'data', 'processed_timetable.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_constraints():
    data = load_processed_data()
    timetable = data['timetable']

    lecturer_slots  = {}
    room_slots      = {}
    group_slots     = {}

    hard = {
        "no_lecturer_overlap":      [],
        "no_room_overlap":          [],
        "no_student_group_overlap": [],
        "course_duration_match":    [],
        "room_capacity":            [],
        "max_session_2hrs":         [],
    }
    soft = {
        "avoid_back_to_back_lecturer": [],
        "spread_lecturer_load":        [],
        "avoid_3hr_clustering":        [],
        "balance_room_utilization":    [],
    }

    for entry in timetable:
        lecturer = entry.get("lecturer",     "Unknown")
        room     = entry.get("room",         "TBA")
        level    = entry.get("level",        "Unknown")
        dept     = entry.get("department",   "Unknown")
        code     = entry.get("course_code",  "")
        hours    = entry.get("hours",        1)
        students = entry.get("students",     0)
        day      = entry.get("day",          "Unknown")

        # Hard: session > 2 hrs
        if isinstance(hours, (int, float)) and hours > 2:
            hard["max_session_2hrs"].append({
                "course": code, "hours": hours,
                "note": "must be split across days"
            })

        # Hard: duration tracking
        hard["course_duration_match"].append({
            "course": code, "duration": hours
        })

        # Hard: room capacity
        hard["room_capacity"].append({
            "room": room, "required": students, "course": code
        })

        # Slot tracking for overlap checks
        slot = (day, entry.get("start_time", "TBA"))
        lecturer_slots.setdefault(lecturer, []).append(slot)
        room_slots.setdefault(room,         []).append(slot)
        group = f"{level}_{dept}"
        group_slots.setdefault(group,       []).append(slot)

    # Summarise overlap candidates
    hard["no_lecturer_overlap"]      = list(lecturer_slots.keys())
    hard["no_room_overlap"]          = list(room_slots.keys())
    hard["no_student_group_overlap"] = list(group_slots.keys())

    # Soft summaries
    soft["avoid_back_to_back_lecturer"] = list(lecturer_slots.keys())
    soft["spread_lecturer_load"]        = list(lecturer_slots.keys())
    soft["avoid_3hr_clustering"]        = [
        e["course"] for e in hard["max_session_2hrs"]
    ]
    soft["balance_room_utilization"]    = list(room_slots.keys())

    return {"hard": hard, "soft": soft}


if __name__ == "__main__":
    print(json.dumps(extract_constraints(), indent=2))