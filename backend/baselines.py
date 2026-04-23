import json
import os
import random
from copy import deepcopy

def load_processed():
    path = os.path.join(os.path.dirname(__file__), 'data', 'processed_timetable.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def greedy_baseline():
    data = load_processed()
    timetable = []
    used = set()
    for entry in data['timetable']:
        # Assign first available slot, cap at 2hr per session
        duration = int(entry.get('COURSE LOAD(HOURS)', 1))
        sessions = []
        while duration > 0:
            session_len = min(2, duration)
            # For demo, assign to next available day/hour
            for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
                for hour in range(7, 18):
                    slot = (entry['course_code'], day, hour)
                    if slot not in used:
                        used.add(slot)
                        sessions.append({
                            **entry,
                            'day': day,
                            'start_time': f"{hour:02d}:00",
                            'end_time': f"{hour+session_len:02d}:00",
                        })
                        duration -= session_len
                        break
                if duration <= 0:
                    break
        timetable.extend(sessions)
    return timetable

def random_baseline():
    data = load_processed()
    timetable = []
    for entry in data['timetable']:
        duration = int(entry.get('COURSE LOAD(HOURS)', 1))
        sessions = []
        while duration > 0:
            session_len = min(2, duration)
            day = random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
            hour = random.randint(7, 16)
            sessions.append({
                **entry,
                'day': day,
                'start_time': f"{hour:02d}:00",
                'end_time': f"{hour+session_len:02d}:00",
            })
            duration -= session_len
        timetable.extend(sessions)
    return timetable
