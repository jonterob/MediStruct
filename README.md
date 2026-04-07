🏥 Kerugoya Hospital System (MediStruct)
<div align="center">
https://img.shields.io/badge/version-4.0-blue
https://img.shields.io/badge/database-SQLite-green
https://img.shields.io/badge/python-3.7+-yellow
https://img.shields.io/badge/license-MIT-red

A Comprehensive Healthcare Management System with Multiple Data Structures

Features • Data Structures • Installation • Usage • Database • Team

</div>
📋 Overview
The Kerugoya Hospital Management System is a feature-rich desktop application designed to streamline hospital operations including patient registration, triage management, appointment scheduling, treatment tracking, and department routing. The system demonstrates the practical implementation of multiple data structures in a real-world healthcare scenario.

🎯 Thematic Area
Healthcare Application for Kerugoya Hospital - A complete digital solution for managing hospital workflows, patient records, and clinical operations.

✨ Features
1. Patient Registration Module
Auto-increment Patient IDs (KGH001, KGH002, KGH003...)

Validation for contact numbers (10 digits)

Blood group dropdown selection

SQLite persistence - Data survives application restarts

Real-time ID preview - Shows next available ID

2. Triage Queue Management
Priority-based queueing (Emergency → Serious → Minor)

Color-coded display (Red for emergency, Orange for serious, Green for minor)

Serve next patient functionality

Wait time tracking

Database-backed queue persistence

3. Appointment Calendar
7-day weekly schedule (Monday to Sunday)

10 time slots (8:00 AM to 5:00 PM hourly)

Slot availability checking

Visual schedule display

Database synchronization

4. Treatment History
Undo/Redo functionality for treatment records

Doctor attribution for each treatment

Timestamp tracking

Patient-specific history view

Last visit tracking

5. Department Routing
Shortest path finding using Dijkstra's algorithm

Interactive department selection

Distance and time estimation

Visual path display

6. Patient Directory
Search functionality by name or ID

Comprehensive patient listing

Contact and blood group display

Real-time statistics

7. Database Features
SQLite integration for data persistence

Auto-save on close

Manual sync option

Backup and restore capability

Database statistics viewer

📊 Data Structures Implemented
Data Structure	Purpose	Complexity	Implementation
Hash Table	Patient Record Storage	O(1) average lookup	Linear probing collision resolution
Priority Queue	Triage Management	O(log n) enqueue/dequeue	Emergency → Serious → Minor ordering
Array (2D)	Appointment Calendar	O(1) access	7 days × 10 slots grid
Stack	Treatment History	O(1) push/pop	Undo/Redo functionality
Graph	Department Routing	O(V²) Dijkstra	Adjacency list representation
Detailed Data Structure Analysis
🔹 Hash Table (Patient Records)
Size: 100 buckets

Collision Resolution: Linear probing

Key: Patient ID (e.g., KGH001)

Operations: Insert, lookup, delete (O(1) average)

Use Case: Fast patient retrieval by ID

🔹 Priority Queue (Triage System)
Implementation: Sorted list with timestamp tie-breaking

Priorities:

Priority 1: 🔴 Emergency (highest)

Priority 2: 🟡 Serious

Priority 3: 🟢 Minor (lowest)

Use Case: Ensuring critical patients are seen first

🔹 2D Array (Appointment Calendar)
Dimensions: 7 rows × 10 columns

Access Time: O(1) direct indexing

Use Case: Fixed schedule with predictable slot access

🔹 Stack (Treatment History)
Dual-stack design: Undo stack + Redo stack

Operations: Push, pop, peek

Use Case: Medical record correction and rollback

🔹 Graph (Department Routing)
Nodes: 8 hospital departments

Edges: Weighted connections (distance in units)

Algorithm: Dijkstra's shortest path

Use Case: Finding fastest routes between departments

🗄️ Database Schema
Tables Structure
sql
-- Patients Table
CREATE TABLE patients (
    patient_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    contact TEXT,
    blood_group TEXT,
    allergies TEXT,
    registration_date TEXT,
    last_visit TEXT
);

-- Triage Queue Table
CREATE TABLE triage_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT,
    name TEXT,
    condition TEXT,
    priority INTEGER,
    added_time TEXT,
    status TEXT DEFAULT 'waiting'
);

-- Appointments Table
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT,
    patient_name TEXT,
    day TEXT,
    day_index INTEGER,
    slot TEXT,
    slot_index INTEGER,
    booked_date TEXT,
    status TEXT DEFAULT 'scheduled'
);

-- Treatments Table
CREATE TABLE treatments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT,
    treatment TEXT,
    doctor TEXT,
    treatment_date TEXT,
    notes TEXT
);

-- System Settings Table
CREATE TABLE system_settings (
    key TEXT PRIMARY KEY,
    value TEXT
);
🚀 Installation
Prerequisites
Python 3.7 or higher

pip package manager

Step-by-Step Installation
Clone or extract the project

bash
unzip kerugoya_hospital_system.zip
cd kerugoya_hospital_system
Install required dependencies

bash
pip install tkinter
Note: tkinter usually comes pre-installed with Python

Run the application

bash
python main.py
File Structure
text
kerugoya_hospital_system/
├── main.py                    # Main application entry point
├── database.py                # SQLite database operations
├── hash_table.py              # Hash table implementation
├── priority_queue.py          # Priority queue for triage
├── appointment_calendar.py    # 2D array calendar
├── treatment_stack.py         # Stack for undo/redo
├── hospital_graph.py          # Graph for routing
├── data_storage.py            # JSON backup utility
└── kerugoya_hospital.db       # SQLite database (auto-created)
💻 Usage Guide
1. Starting the Application
bash
python main.py
2. Registering a Patient
Navigate to "📋 Patient Registration" tab

System auto-generates Patient ID (e.g., KGH001)

Fill in:

Full Name (required)

Age (required, 0-150)

Contact (10 digits, numbers only)

Blood Group (dropdown selection)

Allergies (optional)

Click "✅ Register Patient"

3. Managing Triage Queue
Go to "🚑 Triage Queue" tab

Enter existing Patient ID

Describe the condition

Select priority level:

🔴 Emergency (1)

🟡 Serious (2)

🟢 Minor (3)

Click "➕ Add to Queue"

Use "🚨 Serve Next" to process patients in priority order

4. Booking Appointments
Navigate to "📅 Appointments" tab

Enter Patient ID

Select day (Monday-Sunday)

Choose time slot (8:00-17:00)

Click "📅 Book Appointment"

5. Recording Treatments
Go to "💊 Treatment History" tab

Enter Patient ID

Write treatment description

Enter doctor's name

Click "💊 Record Treatment"

Use "↩️ Undo Last" or "↪️ Redo Last" for corrections

6. Finding Department Routes
Navigate to "🗺️ Department Routing" tab

Select "From Department" (e.g., Reception)

Select "To Department" (e.g., ICU)

Click "🗺️ Find Shortest Path"

View route and estimated time

7. Searching Patients
Go to "🔍 Search Patient" tab

Enter Patient ID (e.g., KGH001)

Click "🔍 Search"

View complete patient details including appointments and treatments

8. Database Operations
Sync to Database: Manual sync from memory to database

Backup Database: Create timestamped backup file

Export to CSV: Export all patients to CSV format

Database Statistics: View hospital analytics

🎨 User Interface Features
Color Scheme
Primary: #2c5f8a (Hospital blue)

Secondary: #2ecc71 (Success green)

Danger: #e74c3c (Alert red)

Warning: #f39c12 (Warning orange)

Info: #3498db (Information blue)

Interactive Elements
Modern Buttons with hover effects

Silent Message Boxes (no Windows beep)

Responsive Layout (adapts to screen size)

Tabbed Interface for organized navigation

Real-time Date/Time Display

Status Bar with connection indicator

🔧 Technical Specifications
System Requirements
Component	Minimum Requirement
OS	Windows 7/8/10/11, macOS, Linux
Python	3.7 or higher
RAM	512 MB
Disk Space	50 MB
Display	1024×768 resolution
Performance Metrics
Operation	Time Complexity	Actual Performance
Patient Lookup	O(1)	< 1ms
Triage Enqueue	O(log n)	< 1ms
Route Finding	O(V²)	< 10ms
Appointment Booking	O(1)	< 1ms
Treatment Undo/Redo	O(1)	< 1ms
📈 Database Statistics
The system automatically tracks:

Total registered patients

Today's appointments

Patients waiting in triage

Emergency cases pending

Treatment history per patient

🔒 Data Persistence
Automatic Saving
Patient registrations are saved immediately

Triage queue updates are synced

Appointments are stored in real-time

Treatment records are persisted

Last patient number is maintained across sessions

Manual Backup
JSON Export: patients_backup.csv

Database Backup: hospital_backup_YYYYMMDD_HHMMSS.db

👥 Team Information
Group Assignment: CAT 2 Take Away - Machine Learning Course

Institution: Kerugoya Hospital / Academic Institution

Project Type: Group Project (5 members)

🧪 Testing
Sample Data
The system includes sample patients for testing:

ID	Name	Age	Contact	Blood Group
KGH001	John Mwangi	45	0712345678	O+
KGH002	Mary Wanjiku	30	0723456789	A+
KGH003	Peter Otieno	60	0734567890	B+
KGH004	Grace Akinyi	25	0745678901	AB+
Test Scenarios
Patient Registration: Verify ID auto-increment

Triage Priority: Ensure emergency patients are served first

Appointment Booking: Check slot availability validation

Undo/Redo: Test treatment history rollback

Route Finding: Validate path calculations

Data Persistence: Close and reopen to verify data retention

🐛 Known Issues & Solutions
Issue	Solution
Database locked error	Close other connections, restart application
Patient ID jumps	Fixed in v4.0 - now sequential
Windows beep on messages	Disabled via ctypes
🔄 Version History
Version	Date	Changes
1.0	Initial	Basic data structures
2.0	Update	Added database support
3.0	Update	GUI improvements
4.0	Current	Fixed auto-increment, added routing
📞 Support
For issues or questions regarding this project:

Check the Database Statistics for system health

Verify database file exists (kerugoya_hospital.db)

Ensure Python 3.7+ is installed

Run python main.py from terminal to see error messages

📄 License
This project is submitted for academic purposes as part of the Machine Learning course CAT 2 Take Away assignment.

🙏 Acknowledgments
SQLite for embedded database

Tkinter for GUI framework

Dijkstra's algorithm for pathfinding

All team members for their contributions

<div align="center">
Made with ❤️ for Kerugoya Hospital

"Efficient Healthcare Through Technology"

</div>
