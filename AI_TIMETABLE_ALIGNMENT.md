# AI-Powered University Timetable System Alignment

This project has been tailored toward the requested **chat-based AI timetable system** direction.

## 1) System Overview
- Web-based timetable platform with chat-style generation UI and timetable visualization.
- Existing backend already supports preprocessing, conflict-aware assignment, and evaluation endpoints.

## 2) User Interface Alignment
- Added dashboard-style home with cards and quick actions.
- Added left navigation with:
  - Upload Data
  - Generate Timetable
  - View Timetable
- Added chat-based assistant screen with side-by-side timetable panel.

## 3) Architecture Mapping
- **Data Layer**: `TIMETABLE/` raw files + `backend/data/processed_timetable.json`.
- **Processing Layer**: `backend/preprocess.py`, `backend/student_resolver.py`, conflict handling and assignment.
- **UI Layer**: React pages and components in `frontend/src`.

## 4) Stack Mapping (Current vs Target)
- Current frontend: React (JSX), CSS utilities.
- Current backend: FastAPI + Python.
- Current storage: JSON file outputs.
- Target in document: Flask + SQL DB + LLM API.

> Note: Current delivery keeps existing backend stable while adding UI/flow parity. Flask/DB migration can be phased next.

## 5) Workflow Support
1. Admin uploads/updates data (`TIMETABLE/`) and runs preprocess trigger.
2. User opens Generate Timetable chat interface.
3. Timetable displayed in grid/list.
4. Conflict detection shown in UI.
5. User can refine by new chat prompt / lookup filters.

## 6) Added/Extended Features
- Chat-based interaction screen (`/assistant`).
- Dashboard with quick actions (`/`).
- Upload data trigger page (`/upload`).
- Improved timetable viewing/export.
- Deterministic time assignment fallback for missing times.

## 7) Diagram Guidance
- Conceptual flow: User Prompt → Processing Layer → Timetable + Conflict Checks → UI.
- Workflow: Upload → Preprocess → Generate/Resolve → Validate → Display/Adjust.
- ERD targets: Courses ↔ Lecturers ↔ Rooms ↔ Timetable Slots.
- Activity loop: Generate → Review conflicts → Adjust prompt → Re-generate.
