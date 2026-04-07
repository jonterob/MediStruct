# Module Reference

## main.py
Primary UI and application orchestrator.

Main classes:
- `SilentMessageBox`: custom dialog widgets (info, warning, error, question)
- `ModernButton`: styled button with hover behavior
- `HospitalApp`: owns app state, tabs, and user action handlers

Important responsibilities:
- Initialize data structures and database
- Load state from DB at startup
- Route user actions to domain modules
- Refresh UI views and status outputs
- Save state on application close

## hash_table.py
In-memory patient index.

Classes:
- `PatientRecord`: patient value object
- `HashTable`: linear-probing hash table for insert/lookup/delete

Notes:
- Average lookup: O(1)
- Uses simple ordinal-sum hash function

## priority_queue.py
Triage queue management.

Classes:
- `TriagePatient`: triage record with priority metadata
- `PriorityQueue`: list-backed queue sorted by `(priority, arrival_time)`

Notes:
- Priority scale: `1` emergency, `2` serious, `3` minor
- Dequeue serves highest-priority, earliest-arrived patient

## appointment_calendar.py
2D schedule grid model.

Class:
- `AppointmentCalendar`

Notes:
- Days: 7 (Monday-Sunday)
- Slots: 10 (08:00-17:00)
- Grid cell holds `None` or `{patient_id, patient_name}`

## treatment_stack.py
Treatment history mechanics.

Classes:
- `TreatmentStack`: undo/redo action stacks
- `PatientTreatmentHistory`: per-patient treatment timeline map

Notes:
- Undo/redo follows standard LIFO stack behavior

## hospital_graph.py
Department routing graph.

Class:
- `HospitalGraph`

Notes:
- Departments are graph nodes with weighted edges
- `shortest_path(start, end)` implements Dijkstra-style traversal

## database.py
Persistence adapter for SQLite operations.

Class:
- `HospitalDatabase`

Capabilities:
- Table creation
- CRUD for patients, triage, appointments, treatments
- System settings (patient number)
- Statistics and backup operations
