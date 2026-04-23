import json
import os
import re
from typing import Dict, Any

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
        raise FileNotFoundError(
            f"processed_timetable.json not found at {path}. "
            "Please run: python backend/preprocess.py"
        )
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

    return {
        "department": dept_input,
        "department_code": department_code or dept_key,
        "department_name": department_name or department,
        "level": level,
        "programme": programme,
        "timetable": filtered,
    }
