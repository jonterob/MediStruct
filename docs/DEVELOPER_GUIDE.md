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

- `main.py`: UI, authentication, and orchestration
- `auth.py`: staff login, roles, and permission model
- `database.py`: persistence layer and schema management
- `hash_table.py`: patient hash table
- `priority_queue.py`: triage queue
- `appointment_calendar.py`: appointment grid
- `treatment_stack.py`: treatment stack/history
- `hospital_graph.py`: route graph
- `kerugoya_hospital.db`: SQLite database file

## Architecture Conventions

- User actions start in UI handlers under `HospitalApp`.
- In-memory data structures are updated for immediate app state.
- Database methods persist workflow events and settings.
- Login and role permissions are enforced before building the main UI.
- Displays are refreshed through dedicated update methods.

## Extending the System

### Add a new feature tab
1. Create a `create_<feature>_tab()` method in `HospitalApp`.
2. Add controls and bind actions.
3. Add handler methods and UI refresh methods.
4. Add persistence methods in `HospitalDatabase` if data should survive restart.

### Authentication and Authorization
- `auth.py` manages staff accounts, password hashing, roles, and permissions.
- Default admin account is created on first run with username `admin`.
- `main.py` uses role-specific tab access to hide or show workflow tabs.
- `logout()` method syncs data, clears UI, and returns to login screen without closing the app.
- `authenticate_user()` validates credentials and establishes the current user session.

### Theme and Settings Support
- The `system_settings` table stores user interface preferences such as `theme`, `startup_tab`, `auto_backup_on_exit`, and `font_size`.
- `main.py` loads saved settings on startup using `load_system_settings()` and applies them through `set_theme()` and `apply_font_size()`.
- `apply_theme_to_widget()` recursively updates widget colors for the selected theme.
- Patient and doctor selection fields use helper methods such as `resolve_patient_id()` and `get_patient_dropdown_values()`.

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
6. Authentication login and role access controls.
7. Billing record save and status updates.

## Refactoring Opportunities

- Split `main.py` into UI views, service controllers, and authentication services.
- Add typed interfaces (`typing`) and docstrings for key methods.
- Introduce a tests directory with `pytest`.
- Separate settings and backup logic into smaller support modules.
