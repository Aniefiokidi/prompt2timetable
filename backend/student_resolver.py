import json
import os
from typing import Dict, Any

DEPARTMENT_MAP = {
    # COE
    "EIE": ["Electrical and Information Engineering", "EIE", "Computer Engineering", "CEN", "Electrical and Electronics Engineering", "EEE", "Information and Communication Engineering", "ICE"],
    "MCE": ["Mechanical Engineering", "MCE", "MEE"],
    "CVE": ["Civil Engineering", "CVE"],
    "CHE": ["Chemical Engineering", "CHE", "TCH"],
    "PET": ["Petroleum Engineering", "PET", "PEE"],
    # CST
    "CIS": ["Computer and Information Sciences", "CIS", "Computer Science", "CSC", "Management Information Systems", "MIS"],
    "BCH": ["Biochemistry", "BCH"],
    "BIO": ["Biological Sciences", "BIO", "MCB", "Biology", "Microbiology"],
    "CHM": ["Chemistry", "CHM", "ICH", "Industrial Chemistry"],
    "MAT": ["Mathematics", "MAT", "MTH", "STA", "Industrial Mathematics"],
    "PHY": ["Physics", "PHY", "Industrial Physics"],
    "ARC": ["Architecture", "ARC", "FAA"],
    "BLD": ["Building Technology", "BLD"],
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
    "ENG": ["English", "ENG", "LIT"],
    "IRL": ["International Relations", "IRL"],
    "PSS": ["Policy and Strategic Studies", "PSS"],
    "POS": ["Political Science", "POS"],
    "PSY": ["Psychology", "PSY", "PSI"],
}

def load_processed():
    path = os.path.join(os.path.dirname(__file__), 'data', 'processed_timetable.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize_level(level):
    try:
        return int(str(level).replace("L", "").strip())
    except Exception:
        return str(level).strip()

def get_dept_aliases(dept_code, dept_name):
    for code, aliases in DEPARTMENT_MAP.items():
        if dept_code and dept_code.strip().upper() == code:
            return [a.lower().strip() for a in aliases] + [code.lower().strip()]
        # Allow substring match for dept_name
        if dept_name:
            for alias in aliases:
                if alias.lower().strip() in dept_name.lower().strip() or dept_name.lower().strip() in alias.lower().strip():
                    return [a.lower().strip() for a in aliases] + [code.lower().strip()]
    out = []
    if dept_code:
        out.append(dept_code.lower().strip())
    if dept_name:
        out.append(dept_name.lower().strip())
    return out

def resolve_dept_level_timetable(
    department: str = None,
    level: str = None,
    programme: str = None,
    college: str = None,
    department_code: str = None,
    department_name: str = None
) -> Dict[str, Any]:
    data = load_processed()
    timetable = data['timetable']
    aliases = get_dept_aliases(department_code or department, department_name or department)
    level_norm = normalize_level(level)
    def match_level(row):
        row_level = row.get('level', '')
        shared_levels = row.get('shared_levels', [])
        # If row_level is a list, check membership
        if isinstance(row_level, list):
            return any(str(normalize_level(l)) == str(level_norm) for l in row_level)
        # If row_level is a string that looks like a list (e.g., '[300]'), try to eval
        if isinstance(row_level, str) and row_level.startswith('[') and row_level.endswith(']'):
            try:
                import ast
                levels = ast.literal_eval(row_level)
                return any(str(normalize_level(l)) == str(level_norm) for l in levels)
            except Exception:
                pass
        # If shared_levels is present and level_norm is int, check membership
        if shared_levels and isinstance(level_norm, int):
            return level_norm in [normalize_level(l) for l in shared_levels]
        # Otherwise, compare as string
        return str(normalize_level(row_level)) == str(level_norm)
    def match_dept(row):
        dept = row.get('department', '').lower().strip()
        code = row.get('course_code', '').lower().strip()
        prog = row.get('programme', '').lower().strip()
        # DEBUG: Print what is being compared
        print(f"DEBUG: Comparing dept='{dept}', code='{code}', prog='{prog}' to aliases={aliases}")
        for alias in aliases:
            if alias in dept:
                print(f"DEBUG: dept match: '{dept}' contains '{alias}'")
                return True
            if alias in prog:
                print(f"DEBUG: prog match: '{prog}' contains '{alias}'")
                return True
            if code.startswith(alias.lower()):
                print(f"DEBUG: code match: {code} startswith {alias.lower()}")
                return True
        return False
    def match_college(row):
        if not college:
            return True
        return row.get('college', '').lower().strip() == college.lower().strip()
    def is_general(row):
        dept = row.get('department', '').lower().strip()
        code = row.get('course_code', '').lower().strip()
        return any(x in dept for x in ['general', 'gst', 'dld', 'tmc']) or any(x in code for x in ['gst', 'dld', 'tmc'])
    filtered = [row for row in timetable if (match_college(row) and match_level(row) and (match_dept(row) or is_general(row)))]
    # DEBUG: Print how many rows match before/after programme filtering
    print(f"DEBUG: {len(filtered)} rows match college/level/dept for {department_code or department} {level}")
    # TEMP: Disable programme filtering to isolate bug
    # if programme:
    #     filtered = [row for row in filtered if str(row.get('programme', '')).strip().lower() == programme.strip().lower()]
    print(f"DEBUG: Returning {len(filtered)} rows for {department_code or department} {level}")
    return {
        "department": department,
        "department_code": department_code,
        "department_name": department_name,
        "level": level,
        "programme": programme,
        "timetable": filtered
    }
import json
import os
from typing import Dict, Any

def load_processed():
    path = os.path.join(os.path.dirname(__file__), 'data', 'processed_timetable.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def resolve_dept_level_timetable(department: str, level: str, programme: str = None) -> Dict[str, Any]:
    data = load_processed()
    timetable = data['timetable']
    filtered = [row for row in timetable if str(row.get('LEVEL', '')).strip() == str(level).strip() and str(row.get('DEPARTMENT', '')).strip().upper() == department.upper()]
    if programme:
        filtered = [row for row in filtered if str(row.get('PROGRAMME', '')).strip().lower() == programme.strip().lower()]
    return {
        "department": department,
        "level": level,
        "programme": programme,
        "timetable": filtered
    }
