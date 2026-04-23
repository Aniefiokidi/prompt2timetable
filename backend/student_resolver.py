import json
import os
import re
from typing import Dict, Any
from collections import defaultdict

DEPARTMENT_MAP = {
    # COE
    "EIE": ["Electrical and Information Engineering", "EIE", "Computer Engineering", "CEN",
            "Electrical and Electronics Engineering", "EEE", "Information and Communication Engineering", "ICE"],
    "MCE": ["Mechanical Engineering", "MCE", "MEE"],
    "CVE": ["Civil Engineering", "CVE"],
    "CHE": ["Chemical Engineering", "CHE", "TCH"],
    "PET": ["Petroleum Engineering", "PET", "PEE"],
    # CST
    "CIS": ["Computer and Information Sciences", "CIS", "Computer Science", "CSC",
            "Management Information Systems", "MIS"],
    "BCH": ["Biochemistry", "BCH"],
    "BIO": ["Biological Sciences", "BIO", "MCB", "Biology", "Microbiology"],
    "CHM": ["Chemistry", "CHM", "ICH", "Industrial Chemistry"],
    "MAT": ["Mathematics", "MAT", "MTH", "STA", "Industrial Mathematics"],
    "PHY": ["Physics", "PHY", "Industrial Physics"],
    "ARC": ["Architecture", "ARC", "FAA"],
    "BLD": ["Building Technology", "BLD", "BUD", "SVY"],
    "ESM": ["Estate Management", "ESM"],
    # CMSS
    "ACC": ["Accounting", "ACC"],
    "BUA": ["Business Administration", "BUA", "BUS"],
    "ECN": ["Economics", "ECN", "ECO", "CBS"],
    "FIN": ["Finance", "FIN", "BFN", "Financial Technology"],
    "MKT": ["Marketing", "MKT"],
    "MAC": ["Mass Communication", "MAC", "MCM", "PRE", "CMS"],
    "SOC": ["Sociology", "SOC"],
    "IRH": ["Industrial Relations and Human Resource Management", "IRH", "HMD", "IRHM"],
    # CLDS
    "ENG": ["English", "ENG", "LIT", "EHR", "FRE"],
    "IRL": ["International Relations", "IRL"],
    "PSS": ["Policy and Strategic Studies", "PSS", "AMS"],
    "POS": ["Political Science", "POS"],
    "PSY": ["Psychology", "PSY", "PSI", "SSC"],
}

# Course-code prefixes that belong to each department key
DEPT_CODE_PREFIXES = {
    "EIE": ["CEN", "EEE", "ICE", "EIE"],
    "MCE": ["MCE", "MEE"],
    "CVE": ["CVE"],
    "CHE": ["CHE", "TCH"],
    "PET": ["PET", "PEE"],
    "CIS": ["CSC", "MIS", "CIS", "CYB", "SEN", "IFT", "COS"],
    "BCH": ["BCH"],
    "BIO": ["BIO", "MCB"],
    "CHM": ["CHM", "ICH", "INS"],
    "MAT": ["MAT", "MTH", "STA", "IMT"],
    "PHY": ["PHY"],
    "ARC": ["ARC", "FAA"],
    "BLD": ["BLD", "BUD", "SVY"],
    "ESM": ["ESM", "MCT"],
    "ACC": ["ACC"],
    "BUA": ["BUA", "BUS"],
    "ECN": ["ECN", "ECO", "CBS"],
    "FIN": ["FIN", "BFN"],
    "MKT": ["MKT"],
    "MAC": ["MAC", "MCM", "PRE", "CMS"],
    "SOC": ["SOC"],
    "IRH": ["IRH", "HMD"],
    "ENG": ["ENG", "LIT", "EHR", "FRE"],
    "IRL": ["IRL"],
    "PSS": ["PSS", "AMS", "FAC"],
    "POS": ["POS"],
    "PSY": ["PSY", "PSI", "SSC"],
}

GENERAL_PREFIXES = ["GST", "DLD", "TMC", "EDS", "CIT", "COV", "GEC", "GET"]

def load_processed():
    path = os.path.join(os.path.dirname(__file__), 'data', 'processed_timetable.json')
    if not os.path.exists(path):
        data = {"timetable": []}
    else:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

    timetable = data.get("timetable", [])
    if timetable:
        return data

    # Auto-recover: regenerate processed_timetable.json from TIMETABLE/*.xlsx
    try:
        try:
            from preprocess import preprocess
        except ImportError:
            from backend.preprocess import preprocess
        generated = preprocess()
    except Exception as e:
        raise RuntimeError(
            "processed_timetable.json is missing/empty and auto-preprocess failed. "
            "Ensure TIMETABLE Excel files exist, then run: python backend/preprocess.py. "
            f"Underlying error: {e}"
        ) from e

    generated_rows = generated.get("timetable", [])
    if not generated_rows:
        raise RuntimeError(
            "processed_timetable.json has no timetable entries after preprocessing. "
            "Check TIMETABLE Excel files and required sheet/column structure, then rerun: "
            "python backend/preprocess.py"
        )

    return generated
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    timetable = data.get("timetable", [])
    if not timetable:
        raise RuntimeError(
            "processed_timetable.json has no timetable entries. "
            "Ensure TIMETABLE Excel files exist, then run: python backend/preprocess.py"
        )

    return data


def normalize_level(level):
    """Convert any level representation to an integer, e.g. '300L' → 300."""
    try:
        return int(re.sub(r"[^\d]", "", str(level)))
    except (ValueError, TypeError):
        return None


def parse_hour_from_time_label(time_label):
    if not time_label:
        return None
    m = re.match(r"^\s*(\d{1,2})", str(time_label))
    if not m:
        return None
    hour = int(m.group(1))
    return hour if 0 <= hour <= 23 else None


def format_hour(hour):
    return f"{hour:02d}:00"


def safe_duration_hours(raw_value):
    try:
        return max(1, int(float(raw_value)))
    except (TypeError, ValueError):
        return 1


def assign_missing_times(rows):
    """
    Fill TBA/missing start/end times with deterministic non-clashing slots per day.
    Existing valid time assignments are preserved.
    """
    rows_by_day = defaultdict(list)
    for row in rows:
        day = str(row.get("day", "Unknown"))
        rows_by_day[day].append(row)

    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    ordered_days = [d for d in day_order if d in rows_by_day] + [d for d in rows_by_day if d not in day_order]

    for day in ordered_days:
        day_rows = rows_by_day[day]
        used_hours = set()

        # Reserve hours already explicitly scheduled
        for row in day_rows:
            h = parse_hour_from_time_label(row.get("start_time"))
            if h is not None:
                duration = safe_duration_hours(row.get("hours", 1))
                for slot in range(h, min(h + duration, 24)):
                    used_hours.add(slot)

        # Assign sequential free hours to unscheduled rows
        next_hour = 7
        for row in day_rows:
            current_hour = parse_hour_from_time_label(row.get("start_time"))
            if current_hour is not None:
                # Ensure an end time exists for existing start time rows
                if not row.get("end_time") or str(row.get("end_time")).strip().upper() == "TBA":
                    duration = safe_duration_hours(row.get("hours", 1))
                    row["end_time"] = format_hour(min(current_hour + duration, 23))
                continue

            duration = safe_duration_hours(row.get("hours", 1))
            while any(slot in used_hours for slot in range(next_hour, min(next_hour + duration, 24))):
                next_hour += 1
            start_hour = next_hour
            end_hour = min(start_hour + duration, 23)
            row["start_time"] = format_hour(start_hour)
            row["end_time"] = format_hour(end_hour)
            for slot in range(start_hour, min(start_hour + duration, 24)):
                used_hours.add(slot)
            next_hour += 1

    return rows


def get_dept_key(dept_input: str) -> str:
    """Given any dept string (code or full name), return the canonical DEPARTMENT_MAP key."""
    if not dept_input:
        return ""
    d = dept_input.strip().upper()
    # Direct key match
    if d in DEPARTMENT_MAP:
        return d
    # Match against aliases
    for key, aliases in DEPARTMENT_MAP.items():
        for alias in aliases:
            if d == alias.upper():
                return key
    # Fuzzy substring match (full name contains alias)
    for key, aliases in DEPARTMENT_MAP.items():
        for alias in aliases:
            if alias.upper() in d or d in alias.upper():
                return key
    return ""


def resolve_dept_level_timetable(
    department: str = None,
    level=None,
    programme: str = None,
    college: str = None,
    department_code: str = None,
    department_name: str = None,
) -> Dict[str, Any]:

    data = load_processed()
    timetable = data["timetable"]

    # Determine canonical dept key
    dept_input = department_code or department_name or department or ""
    dept_key = get_dept_key(dept_input)
    allowed_prefixes = set(DEPT_CODE_PREFIXES.get(dept_key, []))

    # Normalize requested level
    level_int = normalize_level(level)

    def row_level_matches(row):
        """True if the row's level list includes level_int."""
        if level_int is None:
            return True
        row_level = row.get("level", [])
        # stored as list of ints or strings
        if isinstance(row_level, list):
            return any(normalize_level(l) == level_int for l in row_level)
        return normalize_level(row_level) == level_int

    def row_dept_matches(row):
        """True if course code prefix matches this dept, or it's a general course."""
        code = str(row.get("course_code", "")).strip().upper()
        prefix = re.match(r"([A-Z]{2,4})", code)
        prefix = prefix.group(1) if prefix else ""

        # General / university-wide courses always included
        if prefix in GENERAL_PREFIXES or row.get("is_general"):
            return True
        # Match by course-code prefix
        if prefix in allowed_prefixes:
            return True
        # Fall back: match stored department field
        stored_dept = str(row.get("department", "")).strip()
        stored_key = get_dept_key(stored_dept)
        if stored_key and stored_key == dept_key:
            return True
        return False

    filtered = [
        row for row in timetable
        if row_level_matches(row) and row_dept_matches(row)
    ]

    filtered = assign_missing_times(filtered)

    return {
        "department": dept_input,
        "department_code": department_code or dept_key,
        "department_name": department_name or department,
        "level": level,
        "programme": programme,
        "timetable": filtered,
    }
