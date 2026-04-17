# database.py
# SQLite Database connection for MediStruct

import os
import sqlite3
import json
import hashlib
from datetime import datetime
from auth import hash_password

class HospitalDatabase:
    def __init__(self, db_name="medistruct.db"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if db_name == "medistruct.db":
            default_db_path = os.path.join(script_dir, db_name)
            legacy_db_path = os.path.join(script_dir, "kerugoya_hospital.db")
            if not os.path.exists(default_db_path) and os.path.exists(legacy_db_path):
                db_name = legacy_db_path
                print("⚠️ Using legacy database file kerugoya_hospital.db until physical rename is complete.")
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Connect to SQLite database"""
        self.connection = sqlite3.connect(self.db_name)
        
        # Enable Write-Ahead Logging (WAL) for concurrency and crash safety
        self.connection.execute('PRAGMA journal_mode=WAL;')
        # Optimize synchronization for WAL mode
        self.connection.execute('PRAGMA synchronous=NORMAL;')
        # Enforce foreign key constraints for data integrity
        self.connection.execute('PRAGMA foreign_keys=ON;')
        
        self.cursor = self.connection.cursor()
        print(f"✅ Connected to database: {self.db_name} (WAL Mode Enabled)")
    
    def create_tables(self):
        """Create all necessary tables"""
        
        # Hospital table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS hospitals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT,
                phone TEXT,
                created_date TEXT
            )
        ''')

        # Patients table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                contact TEXT,
                blood_group TEXT,
                allergies TEXT,
                medical_record_number TEXT,
                insurance_provider TEXT,
                policy_number TEXT,
                emergency_contact TEXT,
                primary_physician TEXT,
                next_of_kin TEXT,
                address TEXT,
                hospital_id INTEGER,
                registration_date TEXT,
                last_visit TEXT,
                FOREIGN KEY(hospital_id) REFERENCES hospitals(id)
            )
        ''')

        # Wards table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS wards (
                ward_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                level TEXT,
                capacity INTEGER DEFAULT 0,
                hospital_id INTEGER,
                created_date TEXT,
                FOREIGN KEY(hospital_id) REFERENCES hospitals(id)
            )
        ''')

        # Beds table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS beds (
                bed_id TEXT PRIMARY KEY,
                ward_id TEXT,
                room_number TEXT,
                status TEXT DEFAULT 'available',
                patient_id TEXT,
                created_date TEXT,
                FOREIGN KEY(ward_id) REFERENCES wards(ward_id),
                FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
            )
        ''')

        # Admissions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS admissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT,
                ward_id TEXT,
                bed_id TEXT,
                admission_date TEXT,
                expected_discharge_date TEXT,
                discharge_date TEXT,
                status TEXT DEFAULT 'admitted',
                notes TEXT,
                FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
                FOREIGN KEY(ward_id) REFERENCES wards(ward_id),
                FOREIGN KEY(bed_id) REFERENCES beds(bed_id)
            )
        ''')

        # Lab orders table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS lab_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT,
                order_code TEXT,
                test_name TEXT,
                requested_by TEXT,
                status TEXT DEFAULT 'requested',
                ordered_date TEXT,
                result_text TEXT,
                result_date TEXT,
                FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
            )
        ''')

        # Medication inventory table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS medication_inventory (
                med_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                dosage_form TEXT,
                quantity INTEGER DEFAULT 0,
                unit_price REAL DEFAULT 0.0,
                last_updated TEXT
            )
        ''')

        # Insurance claims table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS insurance_claims (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT,
                provider TEXT,
                policy_number TEXT,
                claim_status TEXT DEFAULT 'submitted',
                amount REAL DEFAULT 0.0,
                submitted_date TEXT,
                processed_date TEXT,
                notes TEXT,
                FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
            )
        ''')

        # Documents table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT,
                document_type TEXT,
                filename TEXT,
                file_path TEXT,
                uploaded_date TEXT,
                description TEXT,
                FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
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

        # Ensure any legacy patient table gets the new hospital-scale columns
        self._ensure_patient_table_columns()

        # Default hospital and ward records for larger facility support
        self.cursor.execute('''
            INSERT OR IGNORE INTO hospitals (id, name, address, phone, created_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            1,
            'Central Hospital',
            '123 Health Way, Countyville',
            '+1-800-HEALTH',
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))

        self.cursor.execute('''
            INSERT OR IGNORE INTO wards (ward_id, name, level, capacity, hospital_id, created_date)
            VALUES
                ('WARD1', 'General Medicine', 'Level 1', 20, 1, ?),
                ('WARD2', 'Surgery', 'Level 2', 20, 1, ?),
                ('WARD3', 'Maternity', 'Level 2', 15, 1, ?)
        ''', (
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))

        # Create a few initial beds for operations
        default_beds = [
            ('BED01', 'WARD1', '101', 'available'),
            ('BED02', 'WARD1', '102', 'available'),
            ('BED03', 'WARD1', '103', 'available'),
            ('BED11', 'WARD2', '201', 'available'),
            ('BED12', 'WARD2', '202', 'available'),
            ('BED21', 'WARD3', '301', 'available')
        ]
        for bed_id, ward_id, room_number, status in default_beds:
            self.cursor.execute('''
                INSERT OR IGNORE INTO beds (bed_id, ward_id, room_number, status, created_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (bed_id, ward_id, room_number, status, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        self.connection.commit()
        print("✅ All tables created successfully")
    
    def _ensure_patient_table_columns(self):
        """Add missing columns to the patients table if using an older database schema."""
        try:
            self.cursor.execute('PRAGMA table_info(patients)')
            columns = [row[1] for row in self.cursor.fetchall()]
            required_columns = [
                ('medical_record_number', 'TEXT'),
                ('insurance_provider', 'TEXT'),
                ('policy_number', 'TEXT'),
                ('emergency_contact', 'TEXT'),
                ('primary_physician', 'TEXT'),
                ('next_of_kin', 'TEXT'),
                ('address', 'TEXT'),
                ('hospital_id', 'INTEGER'),
                ('registration_date', 'TEXT'),
                ('last_visit', 'TEXT')
            ]
            for name, col_type in required_columns:
                if name not in columns:
                    self.cursor.execute(f'ALTER TABLE patients ADD COLUMN {name} {col_type}')
            self.connection.commit()
        except Exception as e:
            print(f"Warning: could not migrate patient schema: {e}")

    # ========== PATIENT OPERATIONS ==========
    
    def save_patient(self, patient):
        """Save a patient to database"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO patients 
                (patient_id, name, age, contact, blood_group, allergies, medical_record_number,
                 insurance_provider, policy_number, emergency_contact, primary_physician, next_of_kin,
                 address, hospital_id, registration_date, last_visit)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                patient.patient_id,
                patient.name,
                patient.age,
                patient.contact,
                patient.blood_group,
                patient.allergies,
                getattr(patient, 'medical_record_number', None),
                getattr(patient, 'insurance_provider', None),
                getattr(patient, 'policy_number', None),
                getattr(patient, 'emergency_contact', None),
                getattr(patient, 'primary_physician', None),
                getattr(patient, 'next_of_kin', None),
                getattr(patient, 'address', None),
                getattr(patient, 'hospital_id', None),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error saving patient: {e}")
            return False

    def save_patients_batch(self, patients):
        """Save multiple patients in a single transaction for efficiency and atomicity"""
        if not patients:
            return True
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = [
                (p.patient_id, p.name, p.age, p.contact, p.blood_group, p.allergies, now, now)
                for p in patients
            ]
            # Explicit transaction start
            self.connection.execute("BEGIN TRANSACTION")
            self.cursor.executemany('''
                INSERT OR REPLACE INTO patients 
                (patient_id, name, age, contact, blood_group, allergies, registration_date, last_visit)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', data)
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error during batch patient save: {e}")
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
            patients = []
            for row in rows:
                patients.append({
                    'patient_id': row[0] if len(row) > 0 else None,
                    'name': row[1] if len(row) > 1 else None,
                    'age': row[2] if len(row) > 2 else None,
                    'contact': row[3] if len(row) > 3 else None,
                    'blood_group': row[4] if len(row) > 4 else None,
                    'allergies': row[5] if len(row) > 5 else None,
                    'medical_record_number': row[6] if len(row) > 6 else None,
                    'insurance_provider': row[7] if len(row) > 7 else None,
                    'policy_number': row[8] if len(row) > 8 else None,
                    'emergency_contact': row[9] if len(row) > 9 else None,
                    'primary_physician': row[10] if len(row) > 10 else None,
                    'next_of_kin': row[11] if len(row) > 11 else None,
                    'address': row[12] if len(row) > 12 else None,
                    'hospital_id': row[13] if len(row) > 13 else None,
                    'registration_date': row[14] if len(row) > 14 else None,
                    'last_visit': row[15] if len(row) > 15 else None,
                })
            return patients
        except Exception as e:
            print(f"Error getting patients: {e}")
            return []
    
    def get_hospital_wards(self):
        """Get all hospital wards"""
        try:
            self.cursor.execute('SELECT ward_id, name, level, capacity, hospital_id FROM wards ORDER BY ward_id')
            rows = self.cursor.fetchall()
            return [{
                'ward_id': row[0],
                'name': row[1],
                'level': row[2],
                'capacity': row[3],
                'hospital_id': row[4]
            } for row in rows]
        except Exception as e:
            print(f"Error getting wards: {e}")
            return []

    def get_beds(self, ward_id=None):
        """Get beds optionally filtered by ward"""
        try:
            if ward_id:
                self.cursor.execute('SELECT bed_id, ward_id, room_number, status, patient_id FROM beds WHERE ward_id = ? ORDER BY bed_id', (ward_id,))
            else:
                self.cursor.execute('SELECT bed_id, ward_id, room_number, status, patient_id FROM beds ORDER BY bed_id')
            rows = self.cursor.fetchall()
            return [{
                'bed_id': row[0],
                'ward_id': row[1],
                'room_number': row[2],
                'status': row[3],
                'patient_id': row[4]
            } for row in rows]
        except Exception as e:
            print(f"Error getting beds: {e}")
            return []

    def get_available_beds(self, ward_id=None):
        """Get available beds for a ward or all wards"""
        try:
            if ward_id:
                self.cursor.execute('SELECT bed_id, ward_id, room_number FROM beds WHERE status = "available" AND ward_id = ? ORDER BY bed_id', (ward_id,))
            else:
                self.cursor.execute('SELECT bed_id, ward_id, room_number FROM beds WHERE status = "available" ORDER BY ward_id, bed_id')
            rows = self.cursor.fetchall()
            return [{
                'bed_id': row[0],
                'ward_id': row[1],
                'room_number': row[2]
            } for row in rows]
        except Exception as e:
            print(f"Error getting available beds: {e}")
            return []

    def admit_patient(self, patient_id, ward_id, bed_id, expected_discharge_date=None, notes=""):
        """Admit a patient to a ward and bed."""
        try:
            self.cursor.execute('SELECT status FROM beds WHERE bed_id = ?', (bed_id,))
            bed = self.cursor.fetchone()
            if not bed or bed[0] != 'available':
                return False, 'Selected bed is not available'

            self.cursor.execute('''
                INSERT INTO admissions (patient_id, ward_id, bed_id, admission_date, expected_discharge_date, status, notes)
                VALUES (?, ?, ?, ?, ?, 'admitted', ?)
            ''', (
                patient_id,
                ward_id,
                bed_id,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                expected_discharge_date,
                notes
            ))
            self.cursor.execute('''
                UPDATE beds SET status = 'occupied', patient_id = ? WHERE bed_id = ?
            ''', (patient_id, bed_id))
            self.connection.commit()
            return True, 'Patient admitted successfully'
        except Exception as e:
            self.connection.rollback()
            print(f"Error admitting patient: {e}")
            return False, str(e)

    def discharge_patient(self, admission_id):
        """Discharge a patient and free up the bed."""
        try:
            self.cursor.execute('SELECT bed_id FROM admissions WHERE id = ? AND status = "admitted"', (admission_id,))
            row = self.cursor.fetchone()
            if not row:
                return False
            bed_id = row[0]
            self.cursor.execute('''
                UPDATE admissions
                SET discharge_date = ?, status = 'discharged'
                WHERE id = ?
            ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), admission_id))
            self.cursor.execute('''
                UPDATE beds SET status = 'available', patient_id = NULL WHERE bed_id = ?
            ''', (bed_id,))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error discharging patient: {e}")
            return False

    def get_active_admissions(self):
        """Get all active admissions."""
        try:
            self.cursor.execute('''
                SELECT admissions.id, admissions.patient_id, patients.name, admissions.ward_id, admissions.bed_id,
                       admissions.admission_date, admissions.expected_discharge_date, admissions.notes
                FROM admissions
                LEFT JOIN patients ON admissions.patient_id = patients.patient_id
                WHERE admissions.status = 'admitted'
                ORDER BY admissions.admission_date DESC
            ''')
            rows = self.cursor.fetchall()
            return [{
                'id': row[0],
                'patient_id': row[1],
                'patient_name': row[2],
                'ward_id': row[3],
                'bed_id': row[4],
                'admission_date': row[5],
                'expected_discharge_date': row[6],
                'notes': row[7]
            } for row in rows]
        except Exception as e:
            print(f"Error getting admissions: {e}")
            return []

    def create_lab_order(self, patient_id, order_code, test_name, requested_by, status='requested'):
        """Create a lab order."""
        try:
            self.cursor.execute('''
                INSERT INTO lab_orders (patient_id, order_code, test_name, requested_by, status, ordered_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (patient_id, order_code, test_name, requested_by, status, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error creating lab order: {e}")
            return False

    def get_lab_orders(self, patient_id=None):
        """Get lab orders, optionally for a patient."""
        try:
            if patient_id:
                self.cursor.execute('SELECT id, patient_id, order_code, test_name, requested_by, status, ordered_date, result_text, result_date FROM lab_orders WHERE patient_id = ? ORDER BY ordered_date DESC', (patient_id,))
            else:
                self.cursor.execute('SELECT id, patient_id, order_code, test_name, requested_by, status, ordered_date, result_text, result_date FROM lab_orders ORDER BY ordered_date DESC')
            rows = self.cursor.fetchall()
            return [{
                'id': row[0],
                'patient_id': row[1],
                'order_code': row[2],
                'test_name': row[3],
                'requested_by': row[4],
                'status': row[5],
                'ordered_date': row[6],
                'result_text': row[7],
                'result_date': row[8]
            } for row in rows]
        except Exception as e:
            print(f"Error getting lab orders: {e}")
            return []

    def save_medication(self, med_id, name, dosage_form, quantity, unit_price):
        """Save or update medication stock."""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO medication_inventory (med_id, name, dosage_form, quantity, unit_price, last_updated)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (med_id, name, dosage_form, quantity, unit_price, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error saving medication: {e}")
            return False

    def get_medication_inventory(self):
        """Get the medication inventory."""
        try:
            self.cursor.execute('SELECT med_id, name, dosage_form, quantity, unit_price, last_updated FROM medication_inventory ORDER BY name')
            rows = self.cursor.fetchall()
            return [{
                'med_id': row[0],
                'name': row[1],
                'dosage_form': row[2],
                'quantity': row[3],
                'unit_price': row[4],
                'last_updated': row[5]
            } for row in rows]
        except Exception as e:
            print(f"Error getting medication inventory: {e}")
            return []

    def submit_insurance_claim(self, patient_id, provider, policy_number, amount, notes=''):
        """Submit an insurance claim."""
        try:
            self.cursor.execute('''
                INSERT INTO insurance_claims (patient_id, provider, policy_number, claim_status, amount, submitted_date, notes)
                VALUES (?, ?, ?, 'submitted', ?, ?, ?)
            ''', (patient_id, provider, policy_number, amount, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), notes))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error submitting insurance claim: {e}")
            return False

    def get_insurance_claims(self, patient_id=None):
        """Get insurance claims optionally for a patient."""
        try:
            if patient_id:
                self.cursor.execute('SELECT id, patient_id, provider, policy_number, claim_status, amount, submitted_date, processed_date, notes FROM insurance_claims WHERE patient_id = ? ORDER BY submitted_date DESC', (patient_id,))
            else:
                self.cursor.execute('SELECT id, patient_id, provider, policy_number, claim_status, amount, submitted_date, processed_date, notes FROM insurance_claims ORDER BY submitted_date DESC')
            rows = self.cursor.fetchall()
            return [{
                'id': row[0],
                'patient_id': row[1],
                'provider': row[2],
                'policy_number': row[3],
                'claim_status': row[4],
                'amount': row[5],
                'submitted_date': row[6],
                'processed_date': row[7],
                'notes': row[8]
            } for row in rows]
        except Exception as e:
            print(f"Error getting insurance claims: {e}")
            return []

    def save_document(self, patient_id, document_type, filename, file_path, description=''):
        """Save metadata for a patient document."""
        try:
            self.cursor.execute('''
                INSERT INTO documents (patient_id, document_type, filename, file_path, uploaded_date, description)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                patient_id,
                document_type,
                filename,
                file_path,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                description
            ))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error saving document: {e}")
            return False

    def get_documents(self, patient_id=None):
        """Get document metadata optionally filtered by patient."""
        try:
            if patient_id:
                self.cursor.execute('SELECT id, patient_id, document_type, filename, file_path, uploaded_date, description FROM documents WHERE patient_id = ? ORDER BY uploaded_date DESC', (patient_id,))
            else:
                self.cursor.execute('SELECT id, patient_id, document_type, filename, file_path, uploaded_date, description FROM documents ORDER BY uploaded_date DESC')
            rows = self.cursor.fetchall()
            return [{
                'id': row[0],
                'patient_id': row[1],
                'document_type': row[2],
                'filename': row[3],
                'file_path': row[4],
                'uploaded_date': row[5],
                'description': row[6]
            } for row in rows]
        except Exception as e:
            print(f"Error getting documents: {e}")
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

    def update_patient(self, patient_id, name, age, contact, blood_group, allergies,
                       medical_record_number=None, insurance_provider=None,
                       policy_number=None, emergency_contact=None, primary_physician=None,
                       next_of_kin=None, address=None, hospital_id=None):
        """Update an existing patient record"""
        try:
            self.cursor.execute('''
                UPDATE patients
                SET name = ?, age = ?, contact = ?, blood_group = ?, allergies = ?,
                    medical_record_number = ?, insurance_provider = ?, policy_number = ?,
                    emergency_contact = ?, primary_physician = ?, next_of_kin = ?, address = ?,
                    hospital_id = ?, last_visit = ?
                WHERE patient_id = ?
            ''', (
                name, age, contact, blood_group, allergies,
                medical_record_number, insurance_provider, policy_number,
                emergency_contact, primary_physician, next_of_kin, address,
                hospital_id,
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
        try:
            if self.connection:
                self.connection.commit()
                self.connection.close()
                self.connection = None
                self.cursor = None
                print("✅ Database connection closed")
                return True
        except Exception as e:
            print(f"Error closing database: {e}")
        return False
