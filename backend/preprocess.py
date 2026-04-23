import os
import json
import re
import pandas as pd
import numpy as np

# ── Paths ────────────────────────────────────────────────────────────────────
DATASET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'TIMETABLE')
OUTPUT_DIR  = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_PATH      = os.path.join(OUTPUT_DIR, 'processed_timetable.json')
SHARING_MAP_PATH = os.path.join(OUTPUT_DIR, 'course_sharing_map.json')

# ── Excel files (names exactly as they appear on disk) ───────────────────────
EXCEL_FILES = [
    "Full_Time_Table_Dataset_Monday_.xlsx",
    "Full_Time_Table_Dataset__Tuesday_.xlsx",
    "Full_Time_Table_Dataset_Friday_.xlsx",
    "TIMETABLE_SYSTEM_Wednesday_.xlsx",
    "Time_Table_Dataset__thursday_.xlsx",
    "LIST_OF_2025-2026_ALPHA_SEMESTER_COURSES.xlsx",
]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# ── Course-code → dept/programme/college map ─────────────────────────────────
COURSE_MAP = {
    # COE
    "CEN": {"dept": "Electrical and Information Engineering", "prog": "Computer Engineering",                    "college": "COE"},
    "EEE": {"dept": "Electrical and Information Engineering", "prog": "Electrical and Electronics Engineering",  "college": "COE"},
    "ICE": {"dept": "Electrical and Information Engineering", "prog": "Information and Communication Engineering","college": "COE"},
    "EIE": {"dept": "Electrical and Information Engineering", "prog": "ALL_EIE",                                 "college": "COE"},
    "MCE": {"dept": "Mechanical Engineering",                 "prog": "Mechanical Engineering",                  "college": "COE"},
    "MEE": {"dept": "Mechanical Engineering",                 "prog": "Mechanical Engineering",                  "college": "COE"},
    "CVE": {"dept": "Civil Engineering",                      "prog": "Civil Engineering",                       "college": "COE"},
    "CHE": {"dept": "Chemical Engineering",                   "prog": "Chemical Engineering",                    "college": "COE"},
    "TCH": {"dept": "Chemical Engineering",                   "prog": "Chemical Engineering",                    "college": "COE"},
    "PET": {"dept": "Petroleum Engineering",                  "prog": "Petroleum Engineering",                   "college": "COE"},
    "PEE": {"dept": "Petroleum Engineering",                  "prog": "Petroleum Engineering",                   "college": "COE"},
    "GEC": {"dept": "General Engineering",                    "prog": "ALL_COE",                                 "college": "COE"},
    "GET": {"dept": "General Engineering",                    "prog": "ALL_COE",                                 "college": "COE"},
    # CST
    "CSC": {"dept": "Computer and Information Sciences", "prog": "Computer Science",                "college": "CST"},
    "COS": {"dept": "Computer and Information Sciences", "prog": "Computer Science",                "college": "CST"},
    "CYB": {"dept": "Computer and Information Sciences", "prog": "Computer Science",                "college": "CST"},
    "SEN": {"dept": "Computer and Information Sciences", "prog": "Computer Science",                "college": "CST"},
    "MIS": {"dept": "Computer and Information Sciences", "prog": "Management Information Systems",  "college": "CST"},
    "CIS": {"dept": "Computer and Information Sciences", "prog": "CS_AND_MIS",                     "college": "CST"},
    "IFT": {"dept": "Computer and Information Sciences", "prog": "CS_AND_MIS",                     "college": "CST"},
    "BCH": {"dept": "Biochemistry",          "prog": "Biochemistry",                               "college": "CST"},
    "BIO": {"dept": "Biological Sciences",   "prog": "Applied Biology and Biotechnology",          "college": "CST"},
    "MCB": {"dept": "Biological Sciences",   "prog": "Microbiology",                               "college": "CST"},
    "CHM": {"dept": "Chemistry",             "prog": "Industrial Chemistry",                       "college": "CST"},
    "ICH": {"dept": "Chemistry",             "prog": "Industrial Chemistry",                       "college": "CST"},
    "INS": {"dept": "Chemistry",             "prog": "Industrial Chemistry",                       "college": "CST"},
    "MAT": {"dept": "Mathematics",           "prog": "Industrial Mathematics",                     "college": "CST"},
    "MTH": {"dept": "Mathematics",           "prog": "Industrial Mathematics",                     "college": "CST"},
    "STA": {"dept": "Mathematics",           "prog": "Industrial Mathematics (Statistics)",        "college": "CST"},
    "IMT": {"dept": "Mathematics",           "prog": "Industrial Mathematics",                     "college": "CST"},
    "PHY": {"dept": "Physics",               "prog": "Industrial Physics",                         "college": "CST"},
    "ARC": {"dept": "Architecture",          "prog": "Architecture",                               "college": "CST"},
    "FAA": {"dept": "Architecture",          "prog": "Architecture",                               "college": "CST"},
    "BLD": {"dept": "Building Technology",   "prog": "Building Technology",                        "college": "CST"},
    "BUD": {"dept": "Building Technology",   "prog": "Building Technology",                        "college": "CST"},
    "SVY": {"dept": "Building Technology",   "prog": "Building Technology",                        "college": "CST"},
    "ESM": {"dept": "Estate Management",     "prog": "Estate Management",                          "college": "CST"},
    "MCT": {"dept": "Estate Management",     "prog": "Estate Management",                          "college": "CST"},
    # CMSS
    "ACC": {"dept": "Accounting",                           "prog": "Accounting",                            "college": "CMSS"},
    "BUA": {"dept": "Business Administration",              "prog": "Business Administration",               "college": "CMSS"},
    "BUS": {"dept": "Business Administration",              "prog": "Business Administration",               "college": "CMSS"},
    "ECN": {"dept": "Economics",                            "prog": "Economics",                             "college": "CMSS"},
    "ECO": {"dept": "Economics",                            "prog": "Economics",                             "college": "CMSS"},
    "CBS": {"dept": "Economics",                            "prog": "Economics",                             "college": "CMSS"},
    "FIN": {"dept": "Finance",                              "prog": "Finance",                               "college": "CMSS"},
    "BFN": {"dept": "Finance",                              "prog": "Finance",                               "college": "CMSS"},
    "MKT": {"dept": "Marketing",                            "prog": "Marketing",                             "college": "CMSS"},
    "MAC": {"dept": "Mass Communication",                   "prog": "Mass Communication",                    "college": "CMSS"},
    "MCM": {"dept": "Mass Communication",                   "prog": "Mass Communication",                    "college": "CMSS"},
    "PRE": {"dept": "Mass Communication",                   "prog": "Public Relations and Advertising",      "college": "CMSS"},
    "CMS": {"dept": "Mass Communication",                   "prog": "Mass Communication",                    "college": "CMSS"},
    "SOC": {"dept": "Sociology",                            "prog": "Sociology",                             "college": "CMSS"},
    "IRH": {"dept": "Industrial Relations and HRM",         "prog": "Industrial Relations and HRM",          "college": "CMSS"},
    "HMD": {"dept": "Industrial Relations and HRM",         "prog": "Industrial Relations and HRM",          "college": "CMSS"},
    # CLDS
    "ENG": {"dept": "English",                    "prog": "English",                      "college": "CLDS"},
    "LIT": {"dept": "English",                    "prog": "English",                      "college": "CLDS"},
    "EHR": {"dept": "English",                    "prog": "Language Elective",            "college": "CLDS"},
    "FRE": {"dept": "English",                    "prog": "Language Elective",            "college": "CLDS"},
    "IRL": {"dept": "International Relations",    "prog": "International Relations",      "college": "CLDS"},
    "PSS": {"dept": "Policy and Strategic Studies","prog": "Policy and Strategic Studies","college": "CLDS"},
    "AMS": {"dept": "Policy and Strategic Studies","prog": "Policy and Strategic Studies","college": "CLDS"},
    "POS": {"dept": "Political Science",          "prog": "Political Science",            "college": "CLDS"},
    "PSY": {"dept": "Psychology",                 "prog": "Psychology",                   "college": "CLDS"},
    "PSI": {"dept": "Psychology",                 "prog": "Psychology",                   "college": "CLDS"},
    "SSC": {"dept": "Psychology",                 "prog": "Psychology",                   "college": "CLDS"},
    "FAC": {"dept": "Policy and Strategic Studies","prog": "Policy and Strategic Studies","college": "CLDS"},
    # General / university-wide
    "GST": {"dept": "General Studies",        "prog": "ALL", "college": "ALL"},
    "DLD": {"dept": "Leadership Development", "prog": "ALL", "college": "ALL"},
    "TMC": {"dept": "Total Man Concept",      "prog": "ALL", "college": "ALL"},
    "EDS": {"dept": "Entrepreneurial Studies","prog": "ALL", "college": "ALL"},
    "CIT": {"dept": "IT Skills",              "prog": "ALL", "college": "ALL"},
    "COV": {"dept": "Covenant Courses",       "prog": "ALL", "college": "ALL"},
}

# Courses that appear in multiple college sheets
CROSS_SHARING = {
    "FIN311":  (["CLDS", "CMSS", "CST"], [300]),
    "FIN316":  (["CMSS", "CST"],          [300]),
    "BFN416":  (["CMSS", "CST"],          [400]),
    "FIN416":  (["CMSS", "CST"],          [400]),
    "ACC111":  (["CMSS", "CST"],          [100]),
    "ACC112":  (["CMSS", "CST"],          [100]),
    "ACC317":  (["CLDS", "CMSS"],         [300]),
    "POS115":  (["CLDS", "CMSS"],         [100]),
    "POS412":  (["CLDS", "CMSS"],         [400]),
    "EHR313":  (["CLDS", "CMSS"],         [300]),
    "FRE332":  (["CLDS", "CMSS"],         [300]),
    "IRH416":  (["CLDS", "CMSS"],         [400]),
    "PSI411":  (["CLDS", "CMSS"],         [400]),
    "PSY411":  (["CLDS", "CMSS"],         [400]),
    "BUD211":  (["COE",  "CST"],          [200]),
    "GET233":  (["COE",  "CST"],          [200]),
    "CHM111":  (["CST",  "GENERAL"],      [100]),
}

CROSS_LEVEL = {
    "MAT112": [100, 200],
    "ACC414": [100, 200, 400],
    "CEN511": [300, 500],
    "ICE512": [400, 500],
}

GENERAL_PREFIXES   = ["GST", "DLD", "TMC", "EDS", "CIT", "COV"]
CMSS_100L_SHARED   = {"CBS111", "ECO113", "BUA111", "BUA112", "FIN111",
                       "ACC111", "ACC112", "ECN111", "LIT111", "LIT112",
                       "ENG112", "EHR112"}

# ── Helpers ──────────────────────────────────────────────────────────────────

def infer_day_from_filename(fname):
    fname_lower = fname.lower()
    for day in DAYS:
        if day.lower() in fname_lower:
            return day
    return "Unknown"


def extract_prefix(code):
    if not code or not isinstance(code, str):
        return ""
    m = re.match(r"([A-Za-z]{2,4})", code.strip())
    return m.group(1).upper() if m else code[:3].upper()


def normalize_level(raw):
    """Return a list of integer levels, e.g. '300' → [300], '100/200' → [100,200]."""
    if raw is None:
        return []
    s = str(raw).replace(".0", "").strip()
    nums = re.findall(r"\d{3}", s)
    return [int(n) for n in nums if 100 <= int(n) <= 900]


def to_native(obj):
    """Recursively convert numpy types to plain Python for JSON."""
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, dict):
        return {k: to_native(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_native(x) for x in obj]
    return obj


def safe_str(val, default="TBA"):
    """Convert a value to string, returning default for NaN / None / 'nan'."""
    if val is None:
        return default
    s = str(val).strip()
    return default if s.lower() in ("nan", "none", "") else s


def normalize_filename(name):
    """Normalize file names so space/underscore/parenthesis variations still match."""
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


# ── Main preprocess function (ONE definition only) ───────────────────────────

def preprocess():
    seen        = set()
    timetable   = []
    sharing_map = {}
    available_excel_files = {
        normalize_filename(fname): fname
        for fname in os.listdir(DATASET_DIR)
        if fname.lower().endswith(".xlsx")
    }

    for fname in EXCEL_FILES:
        fpath = os.path.join(DATASET_DIR, fname)
        if not os.path.exists(fpath):
            matched_name = available_excel_files.get(normalize_filename(fname))
            if matched_name:
                fpath = os.path.join(DATASET_DIR, matched_name)
            else:
                print(f"[SKIP] File not found: {fname}")
                continue

        if not os.path.exists(fpath):
            print(f"[SKIP] File not found: {fname}")
            continue

        day = infer_day_from_filename(os.path.basename(fpath))
        xls = pd.ExcelFile(fpath)

        for sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet, dtype=str)
            # Normalise column names
            df.columns = [str(c).strip() for c in df.columns]

            # Build a safe column-name map so we never hard-code apostrophes
            COL = {}
            for col in df.columns:
                cu = col.strip().upper()
                if "LECTURER" in cu:
                    COL["lecturer"] = col
                elif "CLASSROOM" in cu or "VENUE" in cu:
                    COL["room"] = col
                elif "COURSE CODE" in cu:
                    COL["code"] = col
                elif "COURSE TITLE" in cu:
                    COL["title"] = col
                elif "LEVEL" in cu:
                    COL["level"] = col
                elif "COURSE LOAD" in cu or "HOURS" in cu:
                    COL["hours"] = col
                elif "COURSE UNIT" in cu:
                    COL["units"] = col
                elif "SEMESTER" in cu:
                    COL["semester"] = col
                elif "STUDENT" in cu:
                    COL["students"] = col

            college_sheet = sheet.strip().upper()

            for _, row in df.iterrows():
                raw_code = safe_str(row.get(COL.get("code", ""), ""), "")
                if not raw_code or raw_code.upper() in ("NAN", "NONE", ""):
                    continue

                # Handle shared codes like "CHE335/TCH313"
                sub_codes = [c.strip().upper()
                             for c in re.split(r"[/\\]", raw_code) if c.strip()]

                raw_level    = safe_str(row.get(COL.get("level",    ""), ""), "Unknown")
                raw_title    = safe_str(row.get(COL.get("title",    ""), ""), "")
                raw_lecturer = safe_str(row.get(COL.get("lecturer", ""), ""), "TBA")
                raw_room     = safe_str(row.get(COL.get("room",     ""), ""), "TBA")
                raw_hours    = safe_str(row.get(COL.get("hours",    ""), ""), "0")
                raw_units    = safe_str(row.get(COL.get("units",    ""), ""), "0")
                raw_semester = safe_str(row.get(COL.get("semester", ""), ""), "Alpha")
                raw_students = safe_str(row.get(COL.get("students", ""), ""), "0")

                level_list = normalize_level(raw_level) or ["Unknown"]

                try:
                    hours = int(float(raw_hours))
                except ValueError:
                    hours = 0
                try:
                    units = int(float(raw_units))
                except ValueError:
                    units = 0
                try:
                    students = int(float(raw_students))
                except ValueError:
                    students = 0

                for code in sub_codes:
                    prefix   = extract_prefix(code)
                    mapping  = COURSE_MAP.get(prefix, {
                        "dept": "General Studies", "prog": "ALL", "college": "ALL"
                    })

                    is_general      = prefix in GENERAL_PREFIXES
                    shared_colleges = []
                    shared_levels   = []
                    sharing_type    = None
                    note            = ""

                    # Cross-sharing rules
                    base_code = re.sub(r"\s+", "", code)   # strip spaces
                    if base_code in CROSS_SHARING:
                        sc, sl = CROSS_SHARING[base_code]
                        shared_colleges = sc
                        shared_levels   = sl
                        sharing_type    = "cross_college"

                    if base_code in CROSS_LEVEL:
                        shared_levels = CROSS_LEVEL[base_code]
                        sharing_type  = "cross_level"

                    if is_general:
                        shared_colleges = ["ALL"]
                        shared_levels   = level_list if isinstance(level_list, list) else [level_list]
                        sharing_type    = "general"

                    if prefix in ("GEC", "GET") and mapping["college"] == "COE":
                        shared_colleges = ["COE"]
                        sharing_type    = "coe_general"

                    if base_code in CMSS_100L_SHARED:
                        shared_colleges = ["CMSS"]
                        shared_levels   = [100]
                        sharing_type    = "cmss_100l"

                    # Deduplication key (same course + day + room = one slot)
                    dedup = (code, day, raw_room, str(level_list))
                    if dedup in seen:
                        continue
                    seen.add(dedup)

                    entry = {
                        # Identity
                        "course_code":    code,
                        "course_title":   raw_title,
                        "day":            day,
                        "college":        mapping["college"],
                        "college_sheet":  college_sheet,
                        "department":     mapping["dept"],
                        "programme":      mapping["prog"],
                        "level":          level_list,
                        "semester":       raw_semester,
                        # Scheduling
                        "room":           raw_room,        # ← always present
                        "lecturer":       raw_lecturer,    # ← always present
                        "start_time":     "TBA",           # ← dataset has no time col
                        "end_time":       "TBA",
                        "hours":          hours,
                        "units":          units,
                        "students":       students,
                        # Sharing metadata
                        "is_general":     is_general,
                        "shared_colleges":shared_colleges,
                        "shared_levels":  shared_levels,
                        "sharing_type":   sharing_type,
                        "note":           note,
                    }

                    timetable.append(entry)

                    if sharing_type:
                        sharing_map[code] = {
                            "shared_colleges": shared_colleges,
                            "shared_levels":   shared_levels,
                            "type":            sharing_type,
                        }

    result = {"timetable": to_native(timetable)}

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    with open(SHARING_MAP_PATH, "w", encoding="utf-8") as f:
        json.dump(to_native(sharing_map), f, indent=2, ensure_ascii=False)

    print(f"[OK] Wrote {len(timetable)} entries → {OUTPUT_PATH}")
    return result


if __name__ == "__main__":
    preprocess()
