import os
import json
import pandas as pd
import re

DATASET_DIR = os.path.join(os.path.dirname(__file__), '..', 'TIMETABLE')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'processed_timetable.json')
SHARING_MAP_PATH = os.path.join(OUTPUT_DIR, 'course_sharing_map.json')

EXCEL_FILES = [
    "Full Time Table Dataset (Monday).xlsx",
    "Full Time Table Dataset (Tuesday).xlsx",
    "Full Time Table Dataset(Friday).xlsx",
    "TIMETABLE SYSTEM(Wednesday).xlsx",
    "Time Table Dataset (thursday).xlsx",
    "LIST OF 2025-2026 ALPHA SEMESTER COURSES.xlsx"
]

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# === DEFINITIVE CU COURSE CODE → DEPT/PROG/COLLEGE MAPPING ===
COURSE_MAP = {
  # COE
  "CEN": {"dept": "Electrical and Information Engineering", "prog": "Computer Engineering", "college": "COE"},
  "EEE": {"dept": "Electrical and Information Engineering", "prog": "Electrical and Electronics Engineering", "college": "COE"},
  "ICE": {"dept": "Electrical and Information Engineering", "prog": "Information and Communication Engineering", "college": "COE"},
  "EIE": {"dept": "Electrical and Information Engineering", "prog": "ALL_EIE", "college": "COE"},
  "MCE": {"dept": "Mechanical Engineering", "prog": "Mechanical Engineering", "college": "COE"},
  "MEE": {"dept": "Mechanical Engineering", "prog": "Mechanical Engineering", "college": "COE"},
  "CVE": {"dept": "Civil Engineering", "prog": "Civil Engineering", "college": "COE"},
  "CHE": {"dept": "Chemical Engineering", "prog": "Chemical Engineering", "college": "COE"},
  "TCH": {"dept": "Chemical Engineering", "prog": "Chemical Engineering", "college": "COE"},
  "PET": {"dept": "Petroleum Engineering", "prog": "Petroleum Engineering", "college": "COE"},
  "PEE": {"dept": "Petroleum Engineering", "prog": "Petroleum Engineering", "college": "COE"},
  "GEC": {"dept": "General Engineering", "prog": "ALL_COE", "college": "COE"},
  "GET": {"dept": "General Engineering", "prog": "ALL_COE", "college": "COE"},
  # CST
  "CSC": {"dept": "Computer and Information Sciences", "prog": "Computer Science", "college": "CST"},
  "COS": {"dept": "Computer and Information Sciences", "prog": "Computer Science", "college": "CST"},
  "CYB": {"dept": "Computer and Information Sciences", "prog": "Computer Science", "college": "CST"},
  "SEN": {"dept": "Computer and Information Sciences", "prog": "Computer Science", "college": "CST"},
  "MIS": {"dept": "Computer and Information Sciences", "prog": "Management Information Systems", "college": "CST"},
  "CIS": {"dept": "Computer and Information Sciences", "prog": "CS_AND_MIS", "college": "CST"},
  "IFT": {"dept": "Computer and Information Sciences", "prog": "CS_AND_MIS", "college": "CST"},
  "BCH": {"dept": "Biochemistry", "prog": "Biochemistry", "college": "CST"},
  "BIO": {"dept": "Biological Sciences", "prog": "Applied Biology and Biotechnology", "college": "CST"},
  "MCB": {"dept": "Biological Sciences", "prog": "Microbiology", "college": "CST"},
  "CHM": {"dept": "Chemistry", "prog": "Industrial Chemistry", "college": "CST"},
  "ICH": {"dept": "Chemistry", "prog": "Industrial Chemistry", "college": "CST"},
  "INS": {"dept": "Chemistry", "prog": "Industrial Chemistry", "college": "CST"},
  "MAT": {"dept": "Mathematics", "prog": "Industrial Mathematics", "college": "CST"},
  "MTH": {"dept": "Mathematics", "prog": "Industrial Mathematics", "college": "CST"},
  "STA": {"dept": "Mathematics", "prog": "Industrial Mathematics (Statistics)", "college": "CST"},
  "IMT": {"dept": "Mathematics", "prog": "Industrial Mathematics", "college": "CST"},
  "PHY": {"dept": "Physics", "prog": "Industrial Physics", "college": "CST"},
  "ARC": {"dept": "Architecture", "prog": "Architecture", "college": "CST"},
  "FAA": {"dept": "Architecture", "prog": "Architecture", "college": "CST"},
  "BLD": {"dept": "Building Technology", "prog": "Building Technology", "college": "CST"},
  "BUD": {"dept": "Building Technology", "prog": "Building Technology", "college": "CST"},
  "SVY": {"dept": "Building Technology", "prog": "Building Technology", "college": "CST"},
  "ESM": {"dept": "Estate Management", "prog": "Estate Management", "college": "CST"},
  "MCT": {"dept": "Estate Management", "prog": "Estate Management", "college": "CST"},
  # CMSS
  "ACC": {"dept": "Accounting", "prog": "Accounting", "college": "CMSS"},
  "BUA": {"dept": "Business Administration", "prog": "Business Administration", "college": "CMSS"},
  "BUS": {"dept": "Business Administration", "prog": "Business Administration", "college": "CMSS"},
  "ECN": {"dept": "Economics", "prog": "Economics", "college": "CMSS"},
  "ECO": {"dept": "Economics", "prog": "Economics", "college": "CMSS"},
  "CBS": {"dept": "Economics", "prog": "Economics", "college": "CMSS"},
  "FIN": {"dept": "Finance", "prog": "Finance", "college": "CMSS"},
  "BFN": {"dept": "Finance", "prog": "Finance", "college": "CMSS"},
  "MKT": {"dept": "Marketing", "prog": "Marketing", "college": "CMSS"},
  "MAC": {"dept": "Mass Communication", "prog": "Mass Communication", "college": "CMSS"},
  "MCM": {"dept": "Mass Communication", "prog": "Mass Communication", "college": "CMSS"},
  "PRE": {"dept": "Mass Communication", "prog": "Public Relations and Advertising", "college": "CMSS"},
  "CMS": {"dept": "Mass Communication", "prog": "Mass Communication", "college": "CMSS"},
  "SOC": {"dept": "Sociology", "prog": "Sociology", "college": "CMSS"},
  "IRH": {"dept": "Industrial Relations and HRM", "prog": "Industrial Relations and HRM", "college": "CMSS"},
  "HMD": {"dept": "Industrial Relations and HRM", "prog": "Industrial Relations and HRM", "college": "CMSS"},
  # CLDS
  "ENG": {"dept": "English", "prog": "English", "college": "CLDS"},
  "LIT": {"dept": "English", "prog": "English", "college": "CLDS"},
  "IRL": {"dept": "International Relations", "prog": "International Relations", "college": "CLDS"},
  "PSS": {"dept": "Policy and Strategic Studies", "prog": "Policy and Strategic Studies", "college": "CLDS"},
  "AMS": {"dept": "Policy and Strategic Studies", "prog": "Policy and Strategic Studies", "college": "CLDS"},
  "POS": {"dept": "Political Science", "prog": "Political Science", "college": "CLDS"},
  "PSY": {"dept": "Psychology", "prog": "Psychology", "college": "CLDS"},
  "PSI": {"dept": "Psychology", "prog": "Psychology", "college": "CLDS"},
  "SSC": {"dept": "Psychology", "prog": "Psychology", "college": "CLDS"},
  "EHR": {"dept": "English", "prog": "English", "college": "CLDS"},
  "FRE": {"dept": "English", "prog": "Language Elective", "college": "CLDS"},
  "FAC": {"dept": "Policy and Strategic Studies", "prog": "Policy and Strategic Studies", "college": "CLDS"},
  # UNIVERSITY-WIDE / GENERAL
  "GST":  {"dept": "General Studies", "prog": "ALL", "college": "ALL"},
  "DLD":  {"dept": "Leadership Development", "prog": "ALL", "college": "ALL"},
  "TMC":  {"dept": "Total Man Concept", "prog": "ALL", "college": "ALL"},
  "EDS":  {"dept": "Entrepreneurial Studies", "prog": "ALL", "college": "ALL"},
  "CIT":  {"dept": "IT Skills", "prog": "ALL", "college": "ALL"},
  "CST":  {"dept": "Library/ICT Studies", "prog": "ALL_CST_100L", "college": "ALL"},
  "COV":  {"dept": "Covenant Courses", "prog": "ALL", "college": "ALL"},
}

# === SPECIAL RULES ===
CMSS_100L_CODES = ["CBS111", "ECO113", "BUA111", "BUA112", "FIN111", "ACC111", "ACC112", "ECN111", "LIT111", "LIT112", "ENG112", "EHR112"]
COE_100L_CST_CODES = ["MAT", "PHY", "CHM", "GEC", "EDS", "TMC", "CST", "GST"]
GENERAL_PREFIXES = ["TMC", "EDS", "GST", "CIT", "DLD", "COV"]

def normalize_course_code(code):
    if pd.isna(code):
        return []
    # Remove all spaces
    code = str(code).replace(" ", "").upper()
    # Handle slashes (shared codes)
    codes = code.replace("\\", "/").split("/")
    return [c for c in codes if c]

def extract_prefix(code):
    # Always extract first 2-4 alpha chars
    m = re.match(r"([A-Z]{2,4})", code)
    return m.group(1) if m else code[:3]

def normalize_level(level):
    if pd.isna(level):
        return []
    s = str(level).upper().replace("LEVEL", "").replace("L", "").replace("&", "/").replace("-", "/")
    s = re.sub(r"[^0-9/]+", "", s)
    if not s:
        return []
    parts = [int(x) for x in s.split("/") if x.isdigit()]
    return sorted(set(parts))

def preprocess():
    all_rows = []
    for fname in EXCEL_FILES:
        fpath = os.path.join(DATASET_DIR, fname)
        if not os.path.exists(fpath):
            continue
        xls = pd.ExcelFile(fpath)
        for sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet)
            day = infer_day_from_filename(fname)
            df['DAY'] = day
            df['COLLEGE_SHEET'] = sheet.strip().upper()
            all_rows.append(df)
    if not all_rows:
        raise Exception("No data found in Excel files.")
    df = pd.concat(all_rows, ignore_index=True)

    df = df.dropna(subset=['COURSE CODE'])
    df['COURSE CODE'] = df['COURSE CODE'].apply(normalize_course_code)
    df = df.explode('COURSE CODE')
    df['COURSE CODE'] = df['COURSE CODE'].str.strip().str.upper()
    df['LEVEL'] = df['LEVEL'].fillna("Unknown").astype(str)
    df['CLASSROOM(VENUE)'] = df.get('CLASSROOM(VENUE)', pd.Series(["TBA"]*len(df))).fillna("TBA").astype(str).str.upper()
    df['COURSE LOAD(HOURS)'] = pd.to_numeric(df.get('COURSE LOAD(HOURS)', 1), errors='coerce').fillna(1).astype(int)
    df['COURSE TITLE'] = df.get('COURSE TITLE', pd.Series([""]*len(df))).astype(str)
    df['DAY'] = df['DAY'].astype(str)

    seen = set()
    timetable = []
    course_sharing_map = {}

    for idx, row in df.iterrows():
        course_code = row['COURSE CODE']
        if not course_code:
            continue
        prefix = extract_prefix(course_code)
        level_list = normalize_level(row['LEVEL'])
        if not level_list:
            level_list = ["Unknown"]
        day = row['DAY']
        venue = row['CLASSROOM(VENUE)']
        hours = row['COURSE LOAD(HOURS)']
        course_title = row['COURSE TITLE']
        college_sheet = row['COLLEGE_SHEET']

        # Default mapping
        mapping = COURSE_MAP.get(prefix, {"dept": "General Studies", "prog": "ALL", "college": "ALL"})
        college = mapping["college"]
        department = mapping["dept"]
        programme = mapping["prog"]

        shared_colleges = []
        shared_levels = []
        sharing_type = None
        note = ""

        # === RULE 1: Engineering 100L in CST ===
        if college == "COE" and 100 in level_list and prefix in COE_100L_CST_CODES:
            note = "100L_in_CST"
        # === RULE 2: CMSS College-wide 100L courses ===
        if course_code in CMSS_100L_CODES:
            shared_colleges = ["CMSS"]
            shared_levels = [100]
            sharing_type = "cmss_100l"
        # === RULE 3: General Studies for ALL students ===
        if prefix in GENERAL_PREFIXES:
            shared_colleges = ["ALL"]
            shared_levels = [*level_list]
            sharing_type = "general"
        # === RULE 4: COE General Engineering (GEC/GET) ===
        if prefix in ["GEC", "GET"] and college == "COE" and any(l in [200,300,400,500] for l in level_list):
            shared_colleges = ["COE"]
            shared_levels = [l for l in level_list if l in [200,300,400,500]]
            sharing_type = "coe_general"
        # === RULE 5: BUD courses shared ===
        if course_code == "BUD211":
            shared_colleges = ["CST", "COE"]
            sharing_type = "bud_shared"

        dedup_key = (course_code, day, venue, tuple(level_list))
        if dedup_key in seen:
            continue
        seen.add(dedup_key)

        # Map to optimizer-required fields
        # Robustly extract optimizer-required fields
        lecturer = row["LECTURER'S NAME"] if "LECTURER'S NAME" in row and pd.notna(row["LECTURER'S NAME"]) else "Unknown"
        start_time = row["TIME"] if "TIME" in row and pd.notna(row["TIME"]) else "TBA"
        room = row["CLASSROOM(VENUE)"] if "CLASSROOM(VENUE)" in row and pd.notna(row["CLASSROOM(VENUE)"]) else venue

        entry = {
            "course_code": course_code,
            "course_title": course_title,
            "day": day,
            "venue": venue,
            "level": level_list,
            "hours": hours,
            "college": college,
            "department": department,
            "programme": programme,
            "shared_colleges": shared_colleges,
            "shared_levels": shared_levels,
            "sharing_type": sharing_type,
            "note": note,
            "lecturer": lecturer,
            "start_time": start_time,
            "room": room
        }
        timetable.append(entry)

        if sharing_type:
            course_sharing_map[course_code] = {
                "shared_colleges": shared_colleges,
                "shared_levels": shared_levels,
                "type": sharing_type
            }

    result = {
        "timetable": timetable
    }
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    with open(SHARING_MAP_PATH, "w", encoding="utf-8") as f:
        json.dump(course_sharing_map, f, indent=2)

    return result

CROSS_SHARING = {
    "FIN311": (["CLDS", "CMSS", "CST"], [300]),
    "FIN316": (["CMSS", "CST"], [300]),
    "BFN416": (["CMSS", "CST"], [400]),
    "FIN416": (["CMSS", "CST"], [400]),
    "ACC111": (["CMSS", "CST"], [100]),
    "ACC112": (["CMSS", "CST"], [100]),
    "ACC317": (["CLDS", "CMSS"], [300]),
    "POS115": (["CLDS", "CMSS"], [100]),
    "POS412": (["CLDS", "CMSS"], [400]),
    "EHR313": (["CLDS", "CMSS"], [300]),
    "FRE332": (["CLDS", "CMSS"], [300]),
    "IRH416": (["CLDS", "CMSS"], [400]),
    "PSI411": (["CLDS", "CMSS"], [400]),
    "PSY411": (["CLDS", "CMSS"], [400]),
    "BUD211": (["COE", "CST"], [200]),
    "GET233": (["COE", "CST"], [200]),
    "CHM111": (["CST", "GENERAL"], [100]),
}

CROSS_LEVEL = {
    "MAT112": [100, 200],
    "ACC414": [100, 200, 400],
    "CEN511": [300, 500],
    "ICE512": [400, 500],
}

GENERAL_COURSE_PREFIXES = ["GST", "DLD", "TMC", "EDS", "AMS", "COV"]

def extract_prefix(course_code):
    if not course_code or not isinstance(course_code, str):
        return ""
    m = re.match(r"([A-Z]{2,4})", course_code)
    return m.group(1) if m else course_code[:3]

def preprocess():
    all_rows = []
    for fname in EXCEL_FILES:
        fpath = os.path.join(DATASET_DIR, fname)
        if not os.path.exists(fpath):
            continue
        xls = pd.ExcelFile(fpath)
        for sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet)
            day = infer_day_from_filename(fname)
            df['DAY'] = day
            df['COLLEGE_SHEET'] = sheet.strip().upper()
            all_rows.append(df)
    if not all_rows:
        raise Exception("No data found in Excel files.")
    df = pd.concat(all_rows, ignore_index=True)

    df = df.dropna(subset=['COURSE CODE'])
    df['COURSE CODE'] = df['COURSE CODE'].astype(str).str.strip().str.upper()
    df['LEVEL'] = df['LEVEL'].fillna("Unknown").astype(str).str.replace('.0', '', regex=False)
    df['CLASSROOM(VENUE)'] = df.get('CLASSROOM(VENUE)', pd.Series(["TBA"]*len(df))).fillna("TBA").astype(str).str.upper()
    df['COURSE LOAD(HOURS)'] = pd.to_numeric(df.get('COURSE LOAD(HOURS)', 1), errors='coerce').fillna(1).astype(int)
    df['COURSE TITLE'] = df.get('COURSE TITLE', pd.Series([""]*len(df))).astype(str)
    df['DAY'] = df['DAY'].astype(str)

    seen = set()
    timetable = []
    course_sharing_map = {}

    for idx, row in df.iterrows():
        course_code = row['COURSE CODE']
        prefix = extract_prefix(course_code)
        level = row['LEVEL']


def infer_day_from_filename(fname):
    fname = fname.lower()
    for day in DAYS:
        if day.lower() in fname:
            return day
    return "Unknown"

if __name__ == "__main__":
    preprocess()
import os
import json
import pandas as pd

DATASET_DIR = os.path.join(os.path.dirname(__file__), '..', 'TIMETABLE')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'processed_timetable.json')

EXCEL_FILES = [
    "Full Time Table Dataset (Monday).xlsx",
    "Full Time Table Dataset (Tuesday).xlsx",
    "Full Time Table Dataset(Friday).xlsx",
    "TIMETABLE SYSTEM(Wednesday).xlsx",
    "Time Table Dataset (thursday).xlsx",
    "LIST OF 2025-2026 ALPHA SEMESTER COURSES.xlsx"
]

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

def normalize_course_code(code):
    if pd.isna(code):
        return None
    # Handle shared codes like "CHE335/TCH313"
    return [c.strip().upper() for c in str(code).replace("\\", "/").split("/") if c.strip()]

def preprocess():
    all_rows = []
    for fname in EXCEL_FILES:
        fpath = os.path.join(DATASET_DIR, fname)
        if not os.path.exists(fpath):
            continue
        xls = pd.ExcelFile(fpath)
        for sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet)
            df['DAY'] = infer_day_from_filename(fname)
            df['DEPARTMENT'] = sheet
            all_rows.append(df)
    if not all_rows:
        raise Exception("No data found in Excel files.")
    df = pd.concat(all_rows, ignore_index=True)

    # Clean and normalize
    df = df.dropna(subset=['COURSE CODE', "COURSE TITLE"])
    df['COURSE CODE'] = df['COURSE CODE'].apply(normalize_course_code)
    df = df.explode('COURSE CODE')
    df['COURSE CODE'] = df['COURSE CODE'].str.strip().str.upper()
    df['LECTURER\'S NAME'] = df['LECTURER\'S NAME'].fillna("Unknown").str.title()
    df['CLASSROOM(VENUE)'] = df['CLASSROOM(VENUE)'].fillna("TBA").str.upper()
    df['LEVEL'] = df['LEVEL'].fillna("Unknown").astype(str)
    df['SEMESTER'] = df['SEMESTER'].fillna("Unknown").astype(str)
    df['NO OF STUDENT PER COURSE'] = pd.to_numeric(df['NO OF STUDENT PER COURSE'], errors='coerce').fillna(0).astype(int)

    # Map to timeslots
    df['TIMESLOT'] = df.apply(lambda row: map_timeslot(row), axis=1)

    # Extract unique entities
    unique_courses = sorted(df['COURSE CODE'].dropna().unique())
    unique_lecturers = sorted(df['LECTURER\'S NAME'].dropna().unique())
    unique_rooms = sorted(df['CLASSROOM(VENUE)'].dropna().unique())
    unique_departments = sorted(df['DEPARTMENT'].dropna().unique())
    unique_levels = sorted(df['LEVEL'].dropna().unique())
    unique_timeslots = sorted(df['TIMESLOT'].dropna().unique())

    # Convert all numpy types to native Python types for JSON serialization
    import numpy as np
    def to_native(obj):
        if isinstance(obj, np.generic):
            return obj.item()
        def preprocess():
            # CU mapping for department and programme
            CU_PROGRAMME_MAP = {
                # COE
                ("Department of Chemical Engineering",): ["Chemical Engineering"],
                ("Department of Civil Engineering",): ["Civil Engineering"],
                ("Department of Electrical and Information Engineering",): [
                    "Computer Engineering", "Electrical and Electronics Engineering", "Information and Communication Engineering"
                ],
                ("Department of Mechanical Engineering",): ["Mechanical Engineering"],
                ("Department of Petroleum Engineering",): ["Petroleum Engineering"],
                # CST
                ("Department of Architecture",): ["Architecture"],
                ("Department of Building Technology",): ["Building Technology"],
                ("Department of Estate Management",): ["Estate Management"],
                ("Department of Biological Sciences",): ["Biology", "Microbiology"],
                ("Department of Biochemistry",): ["Biochemistry"],
                ("Department of Chemistry",): ["Industrial Chemistry"],
                ("Department of Computer and Information Sciences",): ["Computer Science", "Management Information Systems"],
                ("Department of Mathematics",): ["Industrial Mathematics (Computer Science Option)", "Industrial Mathematics (Statistics Option)"],
                ("Department of Physics",): ["Industrial Physics (Applied Geophysics)", "Industrial Physics (Electronics and IT Applications)", "Industrial Physics (Renewable Energy)"],
                # CLDS
                ("Department of English",): ["English"],
                ("Department of International Relations",): ["International Relations"],
                ("Department of Policy and Strategic Studies",): ["Policy and Strategic Studies"],
                ("Department of Political Science",): ["Political Science"],
                ("Department of Psychology",): ["Psychology"],
                # CMSS
                ("Department of Accounting",): ["Accounting"],
                ("Department of Business Administration",): ["Business Administration"],
                ("Department of Economics",): ["Economics"],
                ("Department of Finance",): ["Finance", "Financial Technology"],
                ("Department of Industrial Relations and Human Resource Management",): ["Industrial Relations and Human Resource Management"],
                ("Department of Marketing",): ["Marketing"],
                ("Department of Mass Communication",): ["Mass Communication"],
                ("Department of Sociology",): ["Sociology"],
            }

            # Helper: assign programme based on department and course code (if possible)
            def infer_programme(department, course_code, course_title):
                # For departments with only one programme, assign directly
                for dept_keys, progs in CU_PROGRAMME_MAP.items():
                    if department in dept_keys:
                        if len(progs) == 1:
                            return progs[0]
                        # For multi-programme departments, use course code/title heuristics
                        # (customize this logic as needed for your data)
                        if department == "Department of Computer and Information Sciences":
                            if course_code and course_code.startswith("MIS"):
                                return "Management Information Systems"
                            return "Computer Science"
                        if department == "Department of Mathematics":
                            if course_title and "statistics" in course_title.lower():
                                return "Industrial Mathematics (Statistics Option)"
                            return "Industrial Mathematics (Computer Science Option)"
                        if department == "Department of Physics":
                            if course_title and "geophysics" in course_title.lower():
                                return "Industrial Physics (Applied Geophysics)"
                            if course_title and "electronics" in course_title.lower():
                                return "Industrial Physics (Electronics and IT Applications)"
                            if course_title and "renewable" in course_title.lower():
                                return "Industrial Physics (Renewable Energy)"
                            return progs[0]
                        if department == "Department of Biological Sciences":
                            if course_title and "microbio" in course_title.lower():
                                return "Microbiology"
                            return "Biology"
                        if department == "Department of Finance":
                            if course_title and "technology" in course_title.lower():
                                return "Financial Technology"
                            return "Finance"
                        # Default to first programme
                        return progs[0]
                return "Unknown"

            all_rows = []
            for fname in EXCEL_FILES:
                fpath = os.path.join(DATASET_DIR, fname)
                if not os.path.exists(fpath):
                    continue
                xls = pd.ExcelFile(fpath)
                for sheet in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet)
                    df['DAY'] = infer_day_from_filename(fname)
                    df['DEPARTMENT'] = sheet
                    all_rows.append(df)
            if not all_rows:
                raise Exception("No data found in Excel files.")
            df = pd.concat(all_rows, ignore_index=True)

            # Clean and normalize
            df = df.dropna(subset=['COURSE CODE', "COURSE TITLE"])
            df['COURSE CODE'] = df['COURSE CODE'].apply(normalize_course_code)
            df = df.explode('COURSE CODE')
            df['COURSE CODE'] = df['COURSE CODE'].str.strip().str.upper()
            df['LECTURER\'S NAME'] = df['LECTURER\'S NAME'].fillna("Unknown").str.title()
            df['CLASSROOM(VENUE)'] = df['CLASSROOM(VENUE)'].fillna("TBA").str.upper()
            df['LEVEL'] = df['LEVEL'].fillna("Unknown").astype(str)
            df['SEMESTER'] = df['SEMESTER'].fillna("Unknown").astype(str)
            df['NO OF STUDENT PER COURSE'] = pd.to_numeric(df['NO OF STUDENT PER COURSE'], errors='coerce').fillna(0).astype(int)

            # Add PROGRAMME field
            df['PROGRAMME'] = df.apply(lambda row: infer_programme(row['DEPARTMENT'], row['COURSE CODE'], row['COURSE TITLE']), axis=1)

            # Map to timeslots
            df['TIMESLOT'] = df.apply(lambda row: map_timeslot(row), axis=1)

            # Extract unique entities
            unique_courses = sorted(df['COURSE CODE'].dropna().unique())
            unique_lecturers = sorted(df['LECTURER\'S NAME'].dropna().unique())
            unique_rooms = sorted(df['CLASSROOM(VENUE)'].dropna().unique())
            unique_departments = sorted(df['DEPARTMENT'].dropna().unique())
            unique_levels = sorted(df['LEVEL'].dropna().unique())
            unique_timeslots = sorted(df['TIMESLOT'].dropna().unique())

            # Output
            import numpy as np
            def to_native(obj):
                if isinstance(obj, np.generic):
                    return obj.item()
                if isinstance(obj, dict):
                    return {k: to_native(v) for k, v in obj.items()}
                if isinstance(obj, list):
                    return [to_native(x) for x in obj]
                return obj

            result = {
                "courses": to_native(unique_courses),
                "lecturers": to_native(unique_lecturers),
                "rooms": to_native(unique_rooms),
                "departments": to_native(unique_departments),
                "levels": to_native(unique_levels),
                "timeslots": to_native(unique_timeslots),
                "timetable": to_native(df.to_dict(orient="records"))
            }
            with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
            return result
