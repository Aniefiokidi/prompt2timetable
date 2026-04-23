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
        # Skip clash checks if start_time is 'TBA'
        if entry.get('start_time', 'TBA') == 'TBA':
            continue
        key = (entry.get('lecturer', 'TBA'), entry.get('day', 'TBA'), entry.get('start_time', 'TBA'))
        if key in seen:
            violations.append({'index': i, 'reason': 'Lecturer overlap'})
        seen.add(key)
        room_key = (entry.get('room', 'TBA'), entry.get('day', 'TBA'), entry.get('start_time', 'TBA'))
        if room_key in seen:
            violations.append({'index': i, 'reason': 'Room overlap'})
        seen.add(room_key)
        group_key = (entry.get('level', 'TBA'), entry.get('department', 'TBA'), entry.get('day', 'TBA'), entry.get('start_time', 'TBA'))
        if group_key in seen:
            violations.append({'index': i, 'reason': 'Student group overlap'})
        seen.add(group_key)
        # Add more checks as needed
    return violations

def is_conflict(a, b):
    # If either entry has TBA times, cannot determine clash, skip
    if a.get('start_time', 'TBA') == 'TBA' or b.get('start_time', 'TBA') == 'TBA':
        return False
    return (
        a.get('lecturer', 'TBA') == b.get('lecturer', 'TBA') and a.get('day', 'TBA') == b.get('day', 'TBA') and a.get('start_time', 'TBA') == b.get('start_time', 'TBA')
    ) or (
        a.get('room', 'TBA') == b.get('room', 'TBA') and a.get('day', 'TBA') == b.get('day', 'TBA') and a.get('start_time', 'TBA') == b.get('start_time', 'TBA')
    ) or (
        a.get('level', 'TBA') == b.get('level', 'TBA') and a.get('department', 'TBA') == b.get('department', 'TBA') and a.get('day', 'TBA') == b.get('day', 'TBA') and a.get('start_time', 'TBA') == b.get('start_time', 'TBA')
    )

def optimize_timetable(timetable):
    sa = simulated_annealing(timetable)
    gr = greedy_repair(sa)
    violations = rule_based_validator(gr)
    return {"optimized": gr, "violations": violations}
