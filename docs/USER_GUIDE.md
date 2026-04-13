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

## Logout and Session Management

1. To logout, open the File menu and select Logout.
2. All unsaved data is synced to the database.
3. You are returned to the login screen without closing the app.
4. You can log back in with the same or different credentials.

Notes:
- Logout syncs your current work automatically—no data is lost.
- Use Logout to switch accounts without restarting the application.

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

1. Open the Settings tab (⚙️ Settings).
2. Adjust your preferences:
   - **Theme**: Choose Light Theme or Dark Theme
   - **Startup Tab**: Select which tab opens by default on app launch
   - **Auto Backup**: Enable automatic database backup on exit
   - **Font Size**: Choose from 10, 12, 14, or 16pt
3. Click "Apply Theme" to save theme changes.
4. Click "Refresh UI" to immediately apply selected theme colors and fonts.
5. Current settings are displayed at the bottom and persist after app restart.

### Admin User Management
- Admins only: Create new staff accounts under the "User Management" section
- Enter username, password, and select a role (Admin, Doctor, Nurse, Receptionist, or Billing)
- Click "Create User" to add the account
- View existing users in the "Existing Users" list

Notes:
- Theme changes and startup preferences are saved to the database and persist after restarting the app.
- You can also switch themes from the Settings menu in the top menu bar.
- Settings panel uses full-screen layout for better visibility and accessibility.

## Exit and Data Safety

- **Logout**: Use File → Logout to end your session and return to the login screen. All data is synced automatically.
- **Exit App**: Use File → Exit to close the application. If auto-backup is enabled, a database backup is created.
- Normal close/logout triggers sync and last patient number saves.
- Use backup from menu/options before major cleanup operations.

## Recommended Daily Flow

1. Login with your staff credentials.
2. Register and verify patient details.
3. Add patients to triage as needed.
4. Schedule appointments and capture follow-up care.
5. Record treatments and update billing/patient history.
6. Use routing for department navigation support.
