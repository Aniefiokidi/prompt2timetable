import re

DEPT_MAP = {
    "CSC": "Computer Science",
    "EEE": "Electrical Engineering",
    "MEC": "Mechanical Engineering",
    "MEE": "Mechatronics Engineering",
    "SEN": "Software Engineering",
    "BCH": "Biochemistry",
    # Add more as needed
}

MATRIC_PATTERN = re.compile(r"^CU(\\d{2})/([A-Z]{3})/(\\d{5})$", re.IGNORECASE)

class MatricValidationError(Exception):
    pass

def validate_matric_number(matric_number: str):
    if not isinstance(matric_number, str):
        raise MatricValidationError("Matric number must be a string.")
    match = MATRIC_PATTERN.match(matric_number.strip().upper())
    if not match:
        raise MatricValidationError("Matric number must be in format CU[YY]/[DEPT]/[NNNNN], e.g., CU25/CSC/12345.")
    year, dept, num = match.groups()
    if dept not in DEPT_MAP:
        raise MatricValidationError(f"Unknown department code: {dept}")
    return {
        "year": year,
        "department_code": dept,
        "department_name": DEPT_MAP[dept],
        "number": num
    }
