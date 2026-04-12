# database.py
# SQLite Database connection for Kerugoya Hospital System

import sqlite3
import json
import hashlib
from datetime import datetime
from auth import hash_password

class HospitalDatabase:
    def __init__(self, db_name="hospital.db"):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Connect to SQLite database"""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        print(f"✅ Connected to database: {self.db_name}")
    
    def create_tables(self):
        """Create all necessary tables"""
        
        # Patients table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                contact TEXT,
                blood_group TEXT,
                allergies TEXT,
                registration_date TEXT,
                last_visit TEXT
            )
        ''')
        
        # Triage queue table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS triage_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT,
                name TEXT,
                condition TEXT,
                priority INTEGER,
                added_time TEXT,
                status TEXT DEFAULT 'waiting',
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
            )
        ''')
        
        # Appointments table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT,
                patient_name TEXT,
                day TEXT,
                day_index INTEGER,
                slot TEXT,
                slot_index INTEGER,
                booked_date TEXT,
                status TEXT DEFAULT 'scheduled',
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
            )
        ''')
        
        # Treatments table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS treatments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT,
                treatment TEXT,
                doctor TEXT,
                treatment_date TEXT,
                notes TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
            )
        ''')

        # Doctors table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                specialty TEXT,
                contact TEXT,
                availability TEXT,
                created_date TEXT
            )
        ''')

        # Billing table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT,
                patient_name TEXT,
                service TEXT,
                amount REAL,
                status TEXT DEFAULT 'Unpaid',
                created_date TEXT,
                paid_date TEXT,
                notes TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
            )
        ''')
        
        # System settings table (for auto-increment counter)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')

        # Users and roles table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                display_name TEXT,
                active INTEGER DEFAULT 1,
                created_at TEXT
            )
        ''')

        # Audit log table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                username TEXT,
                action TEXT,
                details TEXT
            )
        ''')
        
        # Insert default settings if not exists
        self.cursor.execute('''
            INSERT OR IGNORE INTO system_settings (key, value)
            VALUES ('last_patient_number', '0')
        ''')
        self.cursor.execute('''
            INSERT OR IGNORE INTO system_settings (key, value)
            VALUES ('theme', 'light')
        ''')
        self.cursor.execute('''
            INSERT OR IGNORE INTO system_settings (key, value)
            VALUES ('startup_tab', 'Patient Registration')
        ''')
        self.cursor.execute('''
            INSERT OR IGNORE INTO system_settings (key, value)
            VALUES ('auto_backup_on_exit', 'false')
        ''')
        self.cursor.execute('''
            INSERT OR IGNORE INTO system_settings (key, value)
            VALUES ('font_size', '10')
        ''')

        # Default admin account
        self.cursor.execute('''
            INSERT OR IGNORE INTO users (username, password_hash, role, display_name, active, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            'admin',
            hash_password('admin123'),
            'Admin',
            'System Administrator',
            1,
            datetime.now().isoformat()
        ))
        
        self.connection.commit()
        print("✅ All tables created successfully")
    
    # ========== PATIENT OPERATIONS ==========
    
    def save_patient(self, patient):
        """Save a patient to database"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO patients 
                (patient_id, name, age, contact, blood_group, allergies, registration_date, last_visit)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                patient.patient_id, patient.name, patient.age, 
                patient.contact, patient.blood_group, patient.allergies,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error saving patient: {e}")
            return False
    
    def get_patient(self, patient_id):
        """Get a patient by ID"""
        try:
            self.cursor.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,))
            row = self.cursor.fetchone()
            if row:
                return {
                    'patient_id': row[0],
                    'name': row[1],
                    'age': row[2],
                    'contact': row[3],
                    'blood_group': row[4],
                    'allergies': row[5],
                    'registration_date': row[6],
                    'last_visit': row[7]
                }
            return None
        except Exception as e:
            print(f"Error getting patient: {e}")
            return None
    
    def get_all_patients(self):
        """Get all patients"""
        try:
            self.cursor.execute('SELECT * FROM patients ORDER BY patient_id')
            rows = self.cursor.fetchall()
            return [{
                'patient_id': row[0],
                'name': row[1],
                'age': row[2],
                'contact': row[3],
                'blood_group': row[4],
                'allergies': row[5]
            } for row in rows]
        except Exception as e:
            print(f"Error getting patients: {e}")
            return []
    
    def delete_patient(self, patient_id):
        """Delete a patient"""
        try:
            # Also delete related records
            self.cursor.execute('DELETE FROM triage_queue WHERE patient_id = ?', (patient_id,))
            self.cursor.execute('DELETE FROM appointments WHERE patient_id = ?', (patient_id,))
            self.cursor.execute('DELETE FROM treatments WHERE patient_id = ?', (patient_id,))
            self.cursor.execute('DELETE FROM bills WHERE patient_id = ?', (patient_id,))
            self.cursor.execute('DELETE FROM patients WHERE patient_id = ?', (patient_id,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting patient: {e}")
            return False

    def update_patient(self, patient_id, name, age, contact, blood_group, allergies):
        """Update an existing patient record"""
        try:
            self.cursor.execute('''
                UPDATE patients
                SET name = ?, age = ?, contact = ?, blood_group = ?, allergies = ?, last_visit = ?
                WHERE patient_id = ?
            ''', (
                name, age, contact, blood_group, allergies,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                patient_id
            ))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating patient: {e}")
            return False
    
    def search_patients(self, search_term):
        """Search patients by name or ID"""
        try:
            self.cursor.execute('''
                SELECT * FROM patients 
                WHERE patient_id LIKE ? OR name LIKE ?
                ORDER BY patient_id
            ''', (f'%{search_term}%', f'%{search_term}%'))
            rows = self.cursor.fetchall()
            return [{
                'patient_id': row[0],
                'name': row[1],
                'age': row[2],
                'contact': row[3],
                'blood_group': row[4],
                'allergies': row[5]
            } for row in rows]
        except Exception as e:
            print(f"Error searching patients: {e}")
            return []
    
    # ========== TRIAGE OPERATIONS ==========
    
    def add_to_triage(self, patient_id, name, condition, priority):
        """Add patient to triage queue"""
        try:
            self.cursor.execute('''
                INSERT INTO triage_queue (patient_id, name, condition, priority, added_time, status)
                VALUES (?, ?, ?, ?, ?, 'waiting')
            ''', (patient_id, name, condition, priority, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding to triage: {e}")
            return False
    
    def get_triage_queue(self):
        """Get all patients in triage queue, ordered by priority"""
        try:
            self.cursor.execute('''
                SELECT * FROM triage_queue 
                WHERE status = 'waiting'
                ORDER BY priority ASC, added_time ASC
            ''')
            rows = self.cursor.fetchall()
            return [{
                'id': row[0],
                'patient_id': row[1],
                'name': row[2],
                'condition': row[3],
                'priority': row[4],
                'added_time': row[5]
            } for row in rows]
        except Exception as e:
            print(f"Error getting triage queue: {e}")
            return []
    
    def serve_next_patient(self):
        """Serve the next patient (remove from queue)"""
        try:
            # Get the next patient
            self.cursor.execute('''
                SELECT id FROM triage_queue 
                WHERE status = 'waiting'
                ORDER BY priority ASC, added_time ASC
                LIMIT 1
            ''')
            row = self.cursor.fetchone()
            if row:
                self.cursor.execute('UPDATE triage_queue SET status = "served" WHERE id = ?', (row[0],))
                self.connection.commit()
                return True
            return False
        except Exception as e:
            print(f"Error serving patient: {e}")
            return False
    
    # ========== APPOINTMENT OPERATIONS ==========
    
    def book_appointment(self, patient_id, patient_name, day, day_index, slot, slot_index):
        """Book an appointment"""
        try:
            # Check if slot is already booked
            self.cursor.execute('''
                SELECT * FROM appointments 
                WHERE day_index = ? AND slot_index = ? AND status = 'scheduled'
            ''', (day_index, slot_index))
            if self.cursor.fetchone():
                return False, "Slot already booked"
            
            self.cursor.execute('''
                INSERT INTO appointments 
                (patient_id, patient_name, day, day_index, slot, slot_index, booked_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'scheduled')
            ''', (patient_id, patient_name, day, day_index, slot, slot_index, 
                  datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            self.connection.commit()
            return True, "Appointment booked successfully"
        except Exception as e:
            print(f"Error booking appointment: {e}")
            return False, str(e)
    
    def get_appointments_for_day(self, day_index):
        """Get appointments for a specific day"""
        try:
            self.cursor.execute('''
                SELECT * FROM appointments 
                WHERE day_index = ? AND status = 'scheduled'
                ORDER BY slot_index
            ''', (day_index,))
            rows = self.cursor.fetchall()
            return [{
                'slot_index': row[6],
                'slot': row[5],
                'patient_id': row[1],
                'patient_name': row[2]
            } for row in rows]
        except Exception as e:
            print(f"Error getting appointments: {e}")
            return []
    
    def get_patient_appointments(self, patient_id):
        """Get all appointments for a patient"""
        try:
            self.cursor.execute('''
                SELECT day, slot FROM appointments 
                WHERE patient_id = ? AND status = 'scheduled'
                ORDER BY day_index, slot_index
            ''', (patient_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error getting patient appointments: {e}")
            return []
    
    # ========== TREATMENT OPERATIONS ==========
    
    def add_treatment(self, patient_id, treatment, doctor, notes=""):
        """Add a treatment record"""
        try:
            self.cursor.execute('''
                INSERT INTO treatments (patient_id, treatment, doctor, treatment_date, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (patient_id, treatment, doctor, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), notes))
            self.connection.commit()
            
            # Update patient's last visit
            self.cursor.execute('''
                UPDATE patients SET last_visit = ? WHERE patient_id = ?
            ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), patient_id))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding treatment: {e}")
            return False
    
    def get_treatment_history(self, patient_id):
        """Get treatment history for a patient"""
        try:
            self.cursor.execute('''
                SELECT * FROM treatments 
                WHERE patient_id = ?
                ORDER BY treatment_date DESC
            ''', (patient_id,))
            rows = self.cursor.fetchall()
            return [{
                'id': row[0],
                'treatment': row[2],
                'doctor': row[3],
                'treatment_date': row[4],
                'notes': row[5]
            } for row in rows]
        except Exception as e:
            print(f"Error getting treatment history: {e}")
            return []

    # ========== DOCTOR OPERATIONS ==========

    def save_doctor(self, doctor_id, name, specialty, contact, availability):
        """Save or update a doctor"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO doctors
                (doctor_id, name, specialty, contact, availability, created_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                doctor_id, name, specialty, contact, availability,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error saving doctor: {e}")
            return False

    def get_all_doctors(self):
        """Get all doctors"""
        try:
            self.cursor.execute('SELECT doctor_id, name, specialty, contact, availability FROM doctors ORDER BY name')
            rows = self.cursor.fetchall()
            return [{
                'doctor_id': row[0],
                'name': row[1],
                'specialty': row[2],
                'contact': row[3],
                'availability': row[4]
            } for row in rows]
        except Exception as e:
            print(f"Error getting doctors: {e}")
            return []

    def get_last_doctor_number(self):
        """Get the highest numeric doctor id in use"""
        try:
            self.cursor.execute('SELECT doctor_id FROM doctors')
            rows = self.cursor.fetchall()
            max_number = 0
            for row in rows:
                doctor_id = (row[0] or "").strip()
                digits = ''.join(ch for ch in doctor_id if ch.isdigit())
                if digits:
                    max_number = max(max_number, int(digits))
            return max_number
        except Exception as e:
            print(f"Error getting last doctor number: {e}")
            return 0

    def search_doctors(self, search_term):
        """Search doctors by id, name, or specialty"""
        try:
            self.cursor.execute('''
                SELECT doctor_id, name, specialty, contact, availability
                FROM doctors
                WHERE doctor_id LIKE ? OR name LIKE ? OR specialty LIKE ?
                ORDER BY name
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            rows = self.cursor.fetchall()
            return [{
                'doctor_id': row[0],
                'name': row[1],
                'specialty': row[2],
                'contact': row[3],
                'availability': row[4]
            } for row in rows]
        except Exception as e:
            print(f"Error searching doctors: {e}")
            return []

    # ========== BILLING OPERATIONS ==========

    def save_bill(self, patient_id, patient_name, service, amount, notes=""):
        """Create a billing record"""
        try:
            self.cursor.execute('''
                INSERT INTO bills
                (patient_id, patient_name, service, amount, status, created_date, paid_date, notes)
                VALUES (?, ?, ?, ?, 'Unpaid', ?, NULL, ?)
            ''', (
                patient_id, patient_name, service, amount,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                notes
            ))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error saving bill: {e}")
            return False

    def get_all_bills(self):
        """Get all bills"""
        try:
            self.cursor.execute('''
                SELECT id, patient_id, patient_name, service, amount, status, created_date, paid_date, notes
                FROM bills
                ORDER BY id DESC
            ''')
            rows = self.cursor.fetchall()
            return [{
                'id': row[0],
                'patient_id': row[1],
                'patient_name': row[2],
                'service': row[3],
                'amount': row[4],
                'status': row[5],
                'created_date': row[6],
                'paid_date': row[7],
                'notes': row[8]
            } for row in rows]
        except Exception as e:
            print(f"Error getting bills: {e}")
            return []

    def get_patient_bills(self, patient_id):
        """Get bills for a patient"""
        try:
            self.cursor.execute('''
                SELECT id, patient_id, patient_name, service, amount, status, created_date, paid_date, notes
                FROM bills
                WHERE patient_id = ?
                ORDER BY id DESC
            ''', (patient_id,))
            rows = self.cursor.fetchall()
            return [{
                'id': row[0],
                'patient_id': row[1],
                'patient_name': row[2],
                'service': row[3],
                'amount': row[4],
                'status': row[5],
                'created_date': row[6],
                'paid_date': row[7],
                'notes': row[8]
            } for row in rows]
        except Exception as e:
            print(f"Error getting patient bills: {e}")
            return []

    def mark_bill_paid(self, bill_id):
        """Mark a bill as paid"""
        try:
            self.cursor.execute('''
                UPDATE bills
                SET status = 'Paid', paid_date = ?
                WHERE id = ?
            ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), bill_id))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating bill payment: {e}")
            return False
    
    # ========== SYSTEM SETTINGS ==========
    
    def get_last_patient_number(self):
        """Get the last used patient number"""
        try:
            self.cursor.execute('SELECT value FROM system_settings WHERE key = "last_patient_number"')
            row = self.cursor.fetchone()
            return int(row[0]) if row else 0
        except Exception as e:
            print(f"Error getting last patient number: {e}")
            return 0
    
    def update_last_patient_number(self, number):
        """Update the last patient number"""
        try:
            self.cursor.execute('''
                UPDATE system_settings SET value = ? WHERE key = "last_patient_number"
            ''', (str(number),))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating last patient number: {e}")
            return False

    def get_system_setting(self, key):
        """Get a stored system setting."""
        try:
            self.cursor.execute('SELECT value FROM system_settings WHERE key = ?', (key,))
            row = self.cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            print(f"Error getting system setting '{key}': {e}")
            return None

    def update_system_setting(self, key, value):
        """Update or insert a system setting."""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO system_settings (key, value)
                VALUES (?, ?)
            ''', (key, str(value)))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating system setting '{key}': {e}")
            return False

    def create_user(self, username, password, role='Receptionist', display_name=None, active=True):
        """Create a new user account."""
        try:
            password_hash = hash_password(password)
            self.cursor.execute('''
                INSERT INTO users (username, password_hash, role, display_name, active, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                username,
                password_hash,
                role,
                display_name or username,
                1 if active else 0,
                datetime.now().isoformat()
            ))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error creating user '{username}': {e}")
            return False

    def get_user_by_username(self, username):
        """Return a single user record by username."""
        try:
            self.cursor.execute('''
                SELECT username, password_hash, role, display_name, active, created_at
                FROM users
                WHERE username = ?
            ''', (username,))
            row = self.cursor.fetchone()
            if not row:
                return None
            return {
                'username': row[0],
                'password_hash': row[1],
                'role': row[2],
                'display_name': row[3],
                'active': bool(row[4]),
                'created_at': row[5]
            }
        except Exception as e:
            print(f"Error fetching user '{username}': {e}")
            return None

    def get_all_users(self):
        """Return all user accounts."""
        try:
            self.cursor.execute('''
                SELECT username, role, display_name, active, created_at
                FROM users
                ORDER BY role, username
            ''')
            rows = self.cursor.fetchall()
            return [{
                'username': row[0],
                'role': row[1],
                'display_name': row[2],
                'active': bool(row[3]),
                'created_at': row[4]
            } for row in rows]
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []

    def update_user_role(self, username, role):
        """Update a user role."""
        try:
            self.cursor.execute('UPDATE users SET role = ? WHERE username = ?', (role, username))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating role for {username}: {e}")
            return False

    def deactivate_user(self, username):
        """Deactivate a user account."""
        try:
            self.cursor.execute('UPDATE users SET active = 0 WHERE username = ?', (username,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error deactivating user {username}: {e}")
            return False

    def audit_action(self, username, action, details=''):
        """Log a user activity or system event."""
        try:
            self.cursor.execute('''
                INSERT INTO audit_log (timestamp, username, action, details)
                VALUES (?, ?, ?, ?)
            ''', (
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                username,
                action,
                details
            ))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error writing audit log: {e}")
            return False
    
    # ========== STATISTICS ==========
    
    def get_statistics(self):
        """Get hospital statistics"""
        try:
            stats = {}
            
            # Total patients
            self.cursor.execute('SELECT COUNT(*) FROM patients')
            stats['total_patients'] = self.cursor.fetchone()[0]
            
            # Today's appointments
            today = datetime.now().strftime("%Y-%m-%d")
            self.cursor.execute('SELECT COUNT(*) FROM appointments WHERE booked_date LIKE ?', (f'{today}%',))
            stats['today_appointments'] = self.cursor.fetchone()[0]
            
            # Waiting in triage
            self.cursor.execute('SELECT COUNT(*) FROM triage_queue WHERE status = "waiting"')
            stats['waiting_triage'] = self.cursor.fetchone()[0]
            
            # Emergency cases
            self.cursor.execute('SELECT COUNT(*) FROM triage_queue WHERE priority = 1 AND status = "waiting"')
            stats['emergency_waiting'] = self.cursor.fetchone()[0]
            
            return stats
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}
    
    # ========== BACKUP & RESTORE ==========
    
    def backup_database(self, backup_name=None):
        """Backup the database to a file"""
        if not backup_name:
            backup_name = f"hospital_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        
        import shutil
        shutil.copy2(self.db_name, backup_name)
        return backup_name
    
    def clear_all_data(self):
        """Clear all data (for testing)"""
        try:
            self.cursor.execute('DELETE FROM treatments')
            self.cursor.execute('DELETE FROM appointments')
            self.cursor.execute('DELETE FROM triage_queue')
            self.cursor.execute('DELETE FROM patients')
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error clearing data: {e}")
            return False
    
    def close(self):
        """Close database connection"""
