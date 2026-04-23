import time
import json
import os
from collections import defaultdict

def load_timetable(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def check_hard_constraints(timetable):
    violations = defaultdict(list)
    seen_lecturer = set()
    seen_room = set()
    seen_group = set()
    for entry in timetable:
        key_lecturer = (entry['lecturer'], entry['day'], entry['start_time'])
        if key_lecturer in seen_lecturer:
            violations['lecturer_overlap'].append(entry)
        seen_lecturer.add(key_lecturer)
        key_room = (entry['room'], entry['day'], entry['start_time'])
        if key_room in seen_room:
            violations['room_overlap'].append(entry)
        seen_room.add(key_room)
        key_group = (entry['level'], entry['department'], entry['day'], entry['start_time'])
        if key_group in seen_group:
            violations['student_group_overlap'].append(entry)
        seen_group.add(key_group)
        # 2hr session cap
        start = int(entry['start_time'].split(':')[0])
        end = int(entry['end_time'].split(':')[0])
        if end - start > 2:
            violations['session_too_long'].append(entry)
    return violations

def soft_constraint_score(timetable):
    # Example: penalize back-to-back for lecturer, clustering, etc.
    # For demo, just return 80
    return 80

def room_utilization(timetable):
    rooms = defaultdict(list)
    for entry in timetable:
        rooms[entry['room']].append(entry)
    used = sum(1 for v in rooms.values() if v)
    total = len(rooms)
    return used / total if total else 0

def lecturer_load_distribution(timetable):
    load = defaultdict(lambda: defaultdict(int))
    for entry in timetable:
        load[entry['lecturer']][entry['day']] += 1
    return {lect: dict(days) for lect, days in load.items()}

def check_sessions_2hr(timetable):
    return [e for e in timetable if int(e['end_time'].split(':')[0]) - int(e['start_time'].split(':')[0]) > 2]

def evaluate_timetable(timetable, runtime=0):
    hard = check_hard_constraints(timetable)
    soft = soft_constraint_score(timetable)
    room_util = room_utilization(timetable)
    lecturer_load = lecturer_load_distribution(timetable)
    too_long = check_sessions_2hr(timetable)
    return {
        'hard_violations': {k: len(v) for k, v in hard.items()},
        'hard_violations_detail': {k: v for k, v in hard.items()},
        'soft_score': soft,
        'room_utilization': room_util,
        'lecturer_load': lecturer_load,
        'sessions_over_2hr': too_long,
        'runtime_sec': runtime
    }
