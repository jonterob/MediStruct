# Troubleshooting

## App Does Not Start

Symptoms:
- Window does not open or Python exits immediately.

Checks:
1. Confirm Python is installed: `python --version`.
2. Run from project root where `main.py` exists.
3. Ensure no syntax errors were introduced in edited files.

## Tkinter Errors

Symptoms:
- Import or runtime UI errors.

Checks:
1. Verify Python installation includes Tkinter.
2. Reinstall/repair Python with Tcl/Tk support if missing.

## Database Connection Fails

Symptoms:
- App reports DB connection issues.

Checks:
1. Confirm write permission in project folder.
2. Ensure DB file is not locked by another process.
3. Try starting with a new DB filename in `HospitalDatabase(...)`.

## Duplicate or Missing Records

Symptoms:
- UI and DB appear out of sync.

Checks:
1. Use normal app close to trigger sync.
2. Avoid force-killing process during write operations.
3. Compare memory-backed views and DB table rows.

## Appointment Slot Conflicts

Symptoms:
- Booking fails for expected free slot.

Checks:
1. Confirm day and slot indexes map correctly.
2. Verify existing appointment row status is `scheduled`.

## Route Not Found

Symptoms:
- Path output empty or infinite distance.

Checks:
1. Ensure start and end department names are valid graph nodes.
2. Validate graph adjacency configuration in `hospital_graph.py`.

## Backup and Recovery

1. Use `backup_database()` before bulk cleanup.
2. To recover, replace active DB file with backup copy while app is closed.
3. Restart app and verify patient count/statistics.
