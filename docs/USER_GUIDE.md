# User Guide

## Getting Started

1. Start the application:
- `python main.py`

2. On launch, the system:
- Connects to SQLite
- Shows the login screen for staff access
- Loads saved patients, triage queue, appointments, treatments, doctors, billing, and settings

Before operating, verify:
- You are running from the project root directory.
- The database file is writable.
- You can see available workflow tabs after login.

### Default Login
- Username: `admin`
- Password: `admin123`

## Staff Login and Roles

1. Enter your staff username and password.
2. Click Login.
3. The app loads tabs based on your role.

Role access includes:
- `Admin`: full access, user management, settings, doctors, billing
- `Doctor`: patient list, doctor tools, triage, appointments, treatment, search, settings
- `Nurse`: patient list, triage, appointments, search, settings
- `Receptionist`: patient registration, patient list, appointments, search, settings
- `Billing`: patient list, billing, search, settings

## Register a Patient

1. Open the Patient Registration tab.
2. Enter name, age, contact, blood group, and allergies.
3. Submit to generate and persist patient ID.

Validation notes:
- Contact is expected as a 10-digit value.

## Manage Triage Queue

1. Open the Triage tab.
2. Provide patient ID, condition, and severity.
3. Add to queue.
4. Use Serve Next to process by urgency.

Priority mapping:
- 1: Emergency
- 2: Serious
- 3: Minor

Operational note:
- Lower number means higher urgency.

## Book Appointments

1. Open the Appointment tab.
2. Select day and time slot.
3. Select a patient by ID or name using the searchable dropdown field.
4. Book appointment.

Behavior:
- A slot can only hold one active appointment.

## Manage Doctors

1. Open the Doctors tab.
2. Add or update doctor records with specialty, contact, and availability.
3. Search or browse the doctor directory.
4. Use the directory to support treatment and scheduling workflows.

## Billing and Payments

1. Open the Billing tab.
2. Search for a patient or select from the billing register.
3. Enter service details, amount, and payment status.
4. Save billing records and track paid/unpaid invoices.

## Record Treatments

1. Open the Treatment tab.
2. Select a patient by ID or name using the searchable dropdown field.
3. Enter treatment details and doctor.
4. Save treatment.
5. Use Undo/Redo when needed.
6. View patient treatment history using the history tab.

## Find Department Route

1. Open the Routing tab.
2. Select start and destination departments.
3. Run shortest path.
4. Review department sequence and distance.

## Search Patients

1. Open the Search tab.
2. Search by patient ID or patient name in the same search field.
3. Review details from returned records.

## System Settings

1. Open the Settings tab.
2. Choose between Light Theme and Dark Theme.
3. Choose a default startup tab so the app opens directly to the workflow you use most.
4. Enable "Backup database on exit" to save a copy automatically when the app closes.
5. Choose a font size for easier reading.
6. Click Apply Theme to save your preference.
7. Refresh UI if needed to apply the current colors and font size across the app.

Notes:
- Theme changes and startup preferences are saved to the database and persist after restarting the app.
- You can also switch themes from the Settings menu in the top menu bar.

## Exit and Data Safety

- Close app normally so sync and last patient number are saved.
- Use backup from menu/options before major cleanup operations.

## Recommended Daily Flow

1. Login with your staff credentials.
2. Register and verify patient details.
3. Add patients to triage as needed.
4. Schedule appointments and capture follow-up care.
5. Record treatments and update billing/patient history.
6. Use routing for department navigation support.
