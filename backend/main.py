
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import json


from preprocess import preprocess, OUTPUT_PATH


app = FastAPI()



from evaluator import evaluate_timetable
from baselines import greedy_baseline, random_baseline
import time

# Health check endpoint
@app.get("/api/health")
def api_health():
    return {"status": "ok"}

# Compare endpoint: Real vs Greedy vs Random
@app.get("/api/compare")
def api_compare():
    processed_path = os.path.join(os.path.dirname(__file__), 'data', 'processed_timetable.json')
    with open(processed_path, 'r', encoding='utf-8') as f:
        real_data = json.load(f)['timetable']
    t0 = time.time()
    greedy = greedy_baseline()
    greedy_eval = evaluate_timetable(greedy, runtime=time.time()-t0)
    t1 = time.time()
    rand = random_baseline()
    rand_eval = evaluate_timetable(rand, runtime=time.time()-t1)
    t2 = time.time()
    real_eval = evaluate_timetable(real_data, runtime=time.time()-t2)
    return {
        "real": real_eval,
        "greedy": greedy_eval,
        "random": rand_eval,
        "real_sample": real_data[:10],
        "greedy_sample": greedy[:10],
        "random_sample": rand[:10]
    }

from student_resolver import resolve_dept_level_timetable
from fastapi import Body

@app.post("/api/student/timetable")
async def api_student_timetable(body: dict = Body(...)):
    try:
        college = body.get("college")
        department = body.get("department")
        programme = body.get("programme")
        level = body.get("level")
        if not (college and department and level):
            return JSONResponse(content={"error": "college, department, and level are required"}, status_code=400)
        result = resolve_dept_level_timetable(department, level, programme)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)




# Endpoint: GET /api/courses
@app.get("/api/courses")
def api_courses():
    path = os.path.join(os.path.dirname(__file__), 'data', 'processed_timetable.json')
    if not os.path.exists(path):
        return JSONResponse(content={"error": "No processed data found."}, status_code=404)
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    courses = sorted(set([str(row.get('course_code', '')).upper() for row in data['timetable'] if row.get('course_code')]))
    return JSONResponse(content={"courses": courses})

    
# Endpoint: GET /api/departments
@app.get("/api/departments")
def api_departments():
    path = os.path.join(os.path.dirname(__file__), 'data', 'processed_timetable.json')
    if not os.path.exists(path):
        return JSONResponse(content={"error": "No processed data found."}, status_code=404)
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    depts = {}
    for row in data['timetable']:
        dept = str(row.get('department', '')).upper()
        level = str(row.get('level', '')).upper()
        if dept not in depts:
            depts[dept] = set()
        depts[dept].add(level)
    result = [
        {"department_code": d, "department_name": d, "levels": sorted(list(levels))}
        for d, levels in depts.items()
    ]
    return JSONResponse(content={"departments": result})

# Allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
