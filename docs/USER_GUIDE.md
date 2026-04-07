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
3. Provide patient ID and name.
4. Book appointment.

Behavior:
- A slot can only hold one active appointment.

## Record Treatments

1. Open the Treatment tab.
2. Enter patient ID, treatment details, and doctor.
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
2. Search by patient ID or patient name.
3. Review details from returned records.

## Exit and Data Safety

- Close app normally so sync and last patient number are saved.
- Use backup from menu/options before major cleanup operations.

## Recommended Daily Flow

1. Register patient.
2. Add to triage when assessment is needed.
3. Schedule appointment if follow-up is required.
4. Record treatment after care is delivered.
5. Use routing tab for inter-department navigation guidance.
