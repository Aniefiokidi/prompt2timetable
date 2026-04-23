from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os, json, time

app = FastAPI()

# ── CORS (allow frontend dev server) ─────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'processed_timetable.json')

def load_timetable():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            "processed_timetable.json not found. "
            "Run: python backend/preprocess.py"
        )
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/api/health")
def api_health():
    exists = os.path.exists(DATA_PATH)
    return {"status": "ok", "data_ready": exists}


# ── Preprocess trigger ────────────────────────────────────────────────────────
@app.post("/api/preprocess")
def api_preprocess():
    """Trigger preprocessing of the Excel files."""
    try:
        from preprocess import preprocess
        result = preprocess()
        return {"status": "ok", "count": len(result.get("timetable", []))}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# ── Student timetable ─────────────────────────────────────────────────────────
@app.post("/api/student/timetable")
async def api_student_timetable(body: dict = Body(...)):
    try:
        college          = body.get("college")
        department       = body.get("department")
        department_code  = body.get("department_code")
        department_name  = body.get("department_name")
        programme        = body.get("programme")
        level            = body.get("level")

        if not level:
            return JSONResponse(
                content={"error": "level is required"}, status_code=400
            )
        if not (college or department or department_code or department_name):
            return JSONResponse(
                content={"error": "college or department is required"}, status_code=400
            )

        from student_resolver import resolve_dept_level_timetable
        result = resolve_dept_level_timetable(
            department=department,
            level=level,
            programme=programme,
            college=college,
            department_code=department_code,
            department_name=department_name,
        )
        return JSONResponse(content=result)
    except FileNotFoundError as e:
        return JSONResponse(content={"error": str(e)}, status_code=503)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# ── Courses list ──────────────────────────────────────────────────────────────
@app.get("/api/courses")
def api_courses():
    try:
        data = load_timetable()
        courses = sorted(set(
            str(r.get("course_code", "")).upper()
            for r in data["timetable"] if r.get("course_code")
        ))
        return JSONResponse(content={"courses": courses})
    except FileNotFoundError as e:
        return JSONResponse(content={"error": str(e)}, status_code=503)


# ── Departments list ──────────────────────────────────────────────────────────
@app.get("/api/departments")
def api_departments():
    try:
        data = load_timetable()
        depts = {}
        for row in data["timetable"]:
            dept   = str(row.get("department", "")).strip()
            prog   = str(row.get("programme",  "")).strip()
            college= str(row.get("college",    "")).strip()
            levels = row.get("level", [])
            if not dept or dept.lower() in ("nan","none",""):
                continue
            if dept not in depts:
                depts[dept] = {"college": college, "programmes": set(), "levels": set()}
            if prog:
                depts[dept]["programmes"].add(prog)
            if isinstance(levels, list):
                for l in levels:
                    depts[dept]["levels"].add(str(l))
            else:
                depts[dept]["levels"].add(str(levels))

        result = [
            {
                "department": d,
                "college": v["college"],
                "programmes": sorted(v["programmes"]),
                "levels": sorted(v["levels"]),
            }
            for d, v in sorted(depts.items())
        ]
        return JSONResponse(content={"departments": result})
    except FileNotFoundError as e:
        return JSONResponse(content={"error": str(e)}, status_code=503)


# ── Compare baselines ─────────────────────────────────────────────────────────
@app.get("/api/compare")
def api_compare():
    try:
        from evaluator import evaluate_timetable
        from baselines import greedy_baseline, random_baseline

        data = load_timetable()
        real = data["timetable"]

        t0 = time.time(); greedy = greedy_baseline(); greedy_eval = evaluate_timetable(greedy, time.time()-t0)
        t1 = time.time(); rand   = random_baseline();  rand_eval   = evaluate_timetable(rand,   time.time()-t1)
        t2 = time.time(); real_eval = evaluate_timetable(real, time.time()-t2)

        return {
            "real":          real_eval,
            "greedy":        greedy_eval,
            "random":        rand_eval,
            "real_sample":   real[:10],
            "greedy_sample": greedy[:10],
            "random_sample": rand[:10],
        }
    except FileNotFoundError as e:
        return JSONResponse(content={"error": str(e)}, status_code=503)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)