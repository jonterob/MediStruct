# Developer Guide

## Prerequisites

- Python 3.7+
- Tkinter available in Python installation
- SQLite (bundled with Python standard library via `sqlite3`)

## Run Locally

1. Open project directory.
2. Run:
- `python main.py`

## Project Layout

- `main.py`: UI and orchestration
- `database.py`: persistence layer
- `hash_table.py`: patient hash table
- `priority_queue.py`: triage queue
- `appointment_calendar.py`: appointment grid
- `treatment_stack.py`: treatment stack/history
- `hospital_graph.py`: route graph
- `kerugoya_hospital.db`: SQLite database file

## Architecture Conventions

- User actions start in UI handlers under `HospitalApp`.
- In-memory data structures are updated for immediate app state.
- Database methods persist workflow events.
- Displays are refreshed through dedicated update methods.

## Extending the System

### Add a new feature tab
1. Create a `create_<feature>_tab()` method in `HospitalApp`.
2. Add controls and bind actions.
3. Add handler methods and UI refresh methods.
4. Add persistence methods in `HospitalDatabase` if data should survive restart.

### Add a new data structure module
1. Create a dedicated module file.
2. Keep class API focused and testable.
3. Initialize it in `HospitalApp.__init__`.
4. Wire UI workflow to it and persist required data.

## Testing Recommendations

Current repository has no automated tests. Recommended first targets:

1. `HashTable` collision, update, and delete behavior.
2. `PriorityQueue` ordering and stability for equal priorities.
3. Appointment booking collision prevention.
4. Graph shortest path correctness.
5. Database CRUD smoke tests using temporary DB file.

## Refactoring Opportunities

- Split `main.py` into UI views and service/controller modules.
- Add typed interfaces (`typing`) and docstrings for key methods.
- Introduce a tests directory with `pytest`.
