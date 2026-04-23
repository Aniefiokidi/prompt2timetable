import json
import os

def load_processed_data():
    path = os.path.join(os.path.dirname(__file__), 'data', 'processed_timetable.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_constraints():
    data = load_processed_data()
    timetable = data['timetable']
    # HARD CONSTRAINTS
    hard = {
        "no_lecturer_overlap": [],
        "no_room_overlap": [],
        "no_student_group_overlap": [],
        "course_duration_match": [],
        "room_capacity": []
    }
    # SOFT CONSTRAINTS
    soft = {
        "avoid_back_to_back_lecturer": [],
        "spread_lecturer_load": [],
        "avoid_3hr_clustering": [],
        "balance_room_utilization": []
    }
    # Build sets for checking
    lecturer_times = {}
    room_times = {}
    group_times = {}
    room_capacities = {}
    for entry in timetable:
        lecturer = entry.get("LECTURER'S NAME", "Unknown")
        room = entry.get("CLASSROOM(VENUE)", "TBA")
        level = entry.get("LEVEL", "Unknown")
        dept = entry.get("DEPARTMENT", "Unknown")
        course = entry.get("COURSE CODE", "")
        timeslot = entry.get("TIMESLOT", None)
        duration = entry.get("COURSE LOAD(HOURS)", 1)
        n_students = entry.get("NO OF STUDENT PER COURSE", 0)
        # Hard constraints
        lecturer_times.setdefault(lecturer, set()).add(timeslot)
        room_times.setdefault(room, set()).add(timeslot)
        group = f"{level}_{dept}"
        group_times.setdefault(group, set()).add(timeslot)
        # Room capacity
        room_capacities.setdefault(room, 1000)  # Default large if unknown
        hard["room_capacity"].append({"room": room, "capacity": room_capacities[room], "required": n_students, "course": course})
        # Duration
        hard["course_duration_match"].append({"course": course, "duration": duration})
    # Fill hard constraint lists
    hard["no_lecturer_overlap"] = list(lecturer_times.keys())
    hard["no_room_overlap"] = list(room_times.keys())
    hard["no_student_group_overlap"] = list(group_times.keys())
    # SOFT constraints (examples, not full logic)
    soft["avoid_back_to_back_lecturer"] = list(lecturer_times.keys())
    soft["spread_lecturer_load"] = list(lecturer_times.keys())
    soft["avoid_3hr_clustering"] = [c for c in timetable if c.get("COURSE LOAD(HOURS)", 1) >= 3]
    soft["balance_room_utilization"] = list(room_times.keys())
    return {"hard": hard, "soft": soft}

if __name__ == "__main__":
    constraints = extract_constraints()
    print(json.dumps(constraints, indent=2))
import json
import os

def load_processed_data():
    path = os.path.join(os.path.dirname(__file__), 'data', 'processed_timetable.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_constraints():
    data = load_processed_data()
    timetable = data['timetable']
    # HARD CONSTRAINTS
    hard = {
        "no_lecturer_overlap": [],
        "no_room_overlap": [],
        "no_student_group_overlap": [],
        "course_duration_match": [],
        "room_capacity": []
    }
    # SOFT CONSTRAINTS
    soft = {
        "avoid_back_to_back_lecturer": [],
        "spread_lecturer_load": [],
        "avoid_3hr_clustering": [],
        "balance_room_utilization": []
    }
    # Build sets for checking
    lecturer_times = {}
    room_times = {}
    group_times = {}
    room_capacities = {}
    for entry in timetable:
        lecturer = entry.get("LECTURER'S NAME", "Unknown")
        room = entry.get("CLASSROOM(VENUE)", "TBA")
        level = entry.get("LEVEL", "Unknown")
        dept = entry.get("DEPARTMENT", "Unknown")
        course = entry.get("COURSE CODE", "")
        timeslot = entry.get("TIMESLOT", None)
        duration = entry.get("COURSE LOAD(HOURS)", 1)
        n_students = entry.get("NO OF STUDENT PER COURSE", 0)
        # Hard constraints
        lecturer_times.setdefault(lecturer, set()).add(timeslot)
        room_times.setdefault(room, set()).add(timeslot)
        group = f"{level}_{dept}"
        group_times.setdefault(group, set()).add(timeslot)
        # Room capacity
        room_capacities.setdefault(room, 1000)  # Default large if unknown
        hard["room_capacity"].append({"room": room, "capacity": room_capacities[room], "required": n_students, "course": course})
        # Duration
        hard["course_duration_match"].append({"course": course, "duration": duration})
    # Fill hard constraint lists
    hard["no_lecturer_overlap"] = list(lecturer_times.keys())
    hard["no_room_overlap"] = list(room_times.keys())
    hard["no_student_group_overlap"] = list(group_times.keys())
    # SOFT constraints (examples, not full logic)
    soft["avoid_back_to_back_lecturer"] = list(lecturer_times.keys())
    soft["spread_lecturer_load"] = list(lecturer_times.keys())
    soft["avoid_3hr_clustering"] = [c for c in timetable if c.get("COURSE LOAD(HOURS)", 1) >= 3]
    soft["balance_room_utilization"] = list(room_times.keys())
    return {"hard": hard, "soft": soft}

if __name__ == "__main__":
    constraints = extract_constraints()
    print(json.dumps(constraints, indent=2))
