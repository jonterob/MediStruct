# User Guide

## Getting Started

1. Start the application:
- `python main.py`

2. On launch, the system:
- Connects to SQLite
- Loads saved patients, triage queue, appointments, and treatments

Before operating, verify:
- You are running from the project root directory.
- The database file is writable.
- You can see all workflow tabs in the main window.

## Register a Patient

1. Open the Registration tab.
2. Enter name, age, contact, blood group, and allergies.
3. Submit to generate/store patient ID.

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

## Record Treatments

1. Open the Treatment tab.
2. Select a patient by ID or name using the searchable dropdown field. Then enter treatment details and doctor.
3. Save treatment.
4. Use Undo/Redo when needed.
5. Use history view for patient treatment timeline.

## Find Department Route

1. Open the Routing tab.
2. Select start and destination departments.
3. Run shortest path.
4. Review department sequence and distance.

## Search Patients

1. Open Search tab.
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

1. Register patient.
2. Add to triage when assessment is needed.
3. Schedule appointment if follow-up is required.
4. Record treatment after care is delivered.
5. Use routing tab for inter-department navigation guidance.
