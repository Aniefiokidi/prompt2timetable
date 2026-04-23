import copy
import random
import json

def simulated_annealing(timetable, iterations=1000):
    best = copy.deepcopy(timetable)
    current = copy.deepcopy(timetable)
    best_score = count_violations(best)
    temp = 1.0
    cooling = 0.995
    for i in range(iterations):
        a, b = random.sample(range(len(current)), 2)
        current[a], current[b] = current[b], current[a]
        score = count_violations(current)
        if score < best_score or random.random() < temp:
            if score < best_score:
                best = copy.deepcopy(current)
                best_score = score
        else:
            current[a], current[b] = current[b], current[a]
        temp *= cooling
    return best

def greedy_repair(timetable):
    timetable = copy.deepcopy(timetable)
    violations = find_violations(timetable)
    for v in violations:
        idx = v['index']
        for j, entry in enumerate(timetable):
            if j != idx and not is_conflict(entry, timetable[idx]):
                timetable[idx], timetable[j] = timetable[j], timetable[idx]
                break
    return timetable

def rule_based_validator(timetable):
    violations = find_violations(timetable)
    return violations

def count_violations(timetable):
    return len(find_violations(timetable))

def find_violations(timetable):
    # Simple hard constraint checks
    seen = set()
    violations = []
    for i, entry in enumerate(timetable):
        key = (entry['lecturer'], entry['day'], entry['start_time'])
        if key in seen:
            violations.append({'index': i, 'reason': 'Lecturer overlap'})
        seen.add(key)
        room_key = (entry['room'], entry['day'], entry['start_time'])
        if room_key in seen:
            violations.append({'index': i, 'reason': 'Room overlap'})
        seen.add(room_key)
        group_key = (entry['level'], entry['department'], entry['day'], entry['start_time'])
        if group_key in seen:
            violations.append({'index': i, 'reason': 'Student group overlap'})
        seen.add(group_key)
        # Add more checks as needed
    return violations

def is_conflict(a, b):
    return (
        a['lecturer'] == b['lecturer'] and a['day'] == b['day'] and a['start_time'] == b['start_time']
    ) or (
        a['room'] == b['room'] and a['day'] == b['day'] and a['start_time'] == b['start_time']
    ) or (
        a['level'] == b['level'] and a['department'] == b['department'] and a['day'] == b['day'] and a['start_time'] == b['start_time']
    )

def optimize_timetable(timetable):
    sa = simulated_annealing(timetable)
    gr = greedy_repair(sa)
    violations = rule_based_validator(gr)
    return {"optimized": gr, "violations": violations}
