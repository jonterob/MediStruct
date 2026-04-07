# Database Documentation

## Engine and File

- Engine: SQLite
- Access layer: `HospitalDatabase` in `database.py`
- Default database file used by app: `kerugoya_hospital.db`

## Tables

### patients
Stores core patient profile and visit metadata.

Columns:
- `patient_id` TEXT PRIMARY KEY
- `name` TEXT NOT NULL
- `age` INTEGER
- `contact` TEXT
- `blood_group` TEXT
- `allergies` TEXT
- `registration_date` TEXT
- `last_visit` TEXT

### triage_queue
Stores queued triage records and processing state.

Columns:
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `patient_id` TEXT
- `name` TEXT
- `condition` TEXT
- `priority` INTEGER
- `added_time` TEXT
- `status` TEXT DEFAULT 'waiting'

### appointments
Stores scheduled appointments by day and slot index.

Columns:
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `patient_id` TEXT
- `patient_name` TEXT
- `day` TEXT
- `day_index` INTEGER
- `slot` TEXT
- `slot_index` INTEGER
- `booked_date` TEXT
- `status` TEXT DEFAULT 'scheduled'

### treatments
Stores treatment events for patients.

Columns:
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `patient_id` TEXT
- `treatment` TEXT
- `doctor` TEXT
- `treatment_date` TEXT
- `notes` TEXT

### system_settings
Stores app settings such as auto-increment counters.

Columns:
- `key` TEXT PRIMARY KEY
- `value` TEXT

Default key inserted:
- `last_patient_number` = `0`

## CRUD and Workflow Behavior

- Patient registration uses `save_patient()`.
- Patient retrieval uses `get_patient()` and `get_all_patients()`.
- Triage insertion uses `add_to_triage()`.
- Triage serving marks one row as `served` using `serve_next_patient()`.
- Appointment booking prevents duplicate active slot occupancy.
- Treatment insertion updates patient `last_visit` timestamp.

## Statistics

`get_statistics()` returns:
- Total patients
- Appointments booked today
- Waiting triage count
- Emergency waiting count

## Backup and Maintenance

- `backup_database()` copies DB file to timestamped backup.
- `clear_all_data()` deletes patient-linked records for reset/testing.
- `close()` should be called on shutdown.

## Integrity and Current Limitations

- Foreign keys are declared but SQLite pragma enforcement is not explicitly enabled in code.
- Some workflows are represented both in-memory and in DB; consistency depends on correct sync timing.
- Timestamp values are stored as TEXT in current schema.
