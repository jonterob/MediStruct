# KERUGOYA HOSPITAL SYSTEM
# WITH AUTO-INCREMENT ID, VALIDATION, IMPROVED UI, SILENT MESSAGE BOXES, AND SQLITE DATABASE

import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
import os
import json
import re
import sys

# Suppress Windows default beep sound on message boxes
if sys.platform == 'win32':
    import ctypes
    # Disable system beep
    try:
        ctypes.windll.user32.MessageBeep = lambda x: None
    except:
        pass

# Import all modules
from hash_table import HashTable, PatientRecord
from priority_queue import PriorityQueue, TriagePatient
from appointment_calendar import AppointmentCalendar
from treatment_stack import TreatmentStack, PatientTreatmentHistory
from hospital_graph import HospitalGraph

# Import database module
from database import HospitalDatabase

# Modern color scheme
COLORS = {
    'primary': '#2c5f8a',
    'primary_light': '#4a7fa5',
    'secondary': '#2ecc71',
    'secondary_dark': '#27ae60',
    'danger': '#e74c3c',
    'danger_dark': '#c0392b',
    'warning': '#f39c12',
    'info': '#3498db',
    'info_dark': '#2980b9',
    'light_bg': '#f0f7fc',
    'white': '#ffffff',
    'gray': '#95a5a6',
    'gray_dark': '#7f8c8d',
    'text': '#2c3e50',
    'border': '#d5e8f0'
}

# Custom silent message box class with improved display
class SilentMessageBox:
    @staticmethod
    def show_info(title, message, parent=None):
        """Show info dialog - centered, smaller, instant, professional"""
        dialog = tk.Toplevel(parent) if parent else tk.Toplevel()
        dialog.title(title)
        dialog.configure(bg=COLORS['white'])
        dialog.transient(parent) if parent else None
        dialog.grab_set()
        dialog.focus_force()
        
        # Fixed smaller size for better appearance
        width = 380
        height = 180
        
        # Center on parent or screen
        dialog.update_idletasks()
        if parent and parent.winfo_exists():
            parent_x = parent.winfo_rootx()
            parent_y = parent.winfo_rooty()
            parent_width = parent.winfo_width()
            parent_height = parent.winfo_height()
            x = parent_x + (parent_width // 2) - (width // 2)
            y = parent_y + (parent_height // 2) - (height // 2)
        else:
            x = (dialog.winfo_screenwidth() // 2) - (width // 2)
            y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Main container with rounded corners effect
        main_frame = tk.Frame(dialog, bg=COLORS['white'], relief='flat', bd=1)
        main_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Content frame
        content_frame = tk.Frame(main_frame, bg=COLORS['white'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Icon
        icon_label = tk.Label(content_frame, text="✓", font=('Segoe UI', 42, 'bold'), 
                              bg=COLORS['white'], fg=COLORS['secondary'])
        icon_label.pack(pady=(0, 10))
        
        # Message with proper formatting
        message_label = tk.Label(content_frame, text=message, font=('Segoe UI', 10), 
                                 bg=COLORS['white'], fg=COLORS['text'], 
                                 wraplength=320, justify='center')
        message_label.pack(pady=(0, 15), expand=True)
        
        # OK Button
        btn = tk.Button(content_frame, text="OK", command=dialog.destroy,
                       bg=COLORS['secondary'], fg='white', font=('Segoe UI', 10, 'bold'),
                       padx=35, pady=5, bd=0, cursor='hand2', relief='flat',
                       activebackground=COLORS['secondary_dark'], activeforeground='white')
        btn.pack()
        
        # Keyboard shortcuts
        dialog.bind('<Return>', lambda e: dialog.destroy())
        dialog.bind('<Escape>', lambda e: dialog.destroy())
        dialog.after(10, lambda: btn.focus())
        
        # Center the button
        btn.pack_propagate(False)
        
        dialog.wait_window()
    
    @staticmethod
    def show_error(title, message, parent=None):
        """Show error dialog - centered, smaller, instant, professional"""
        dialog = tk.Toplevel(parent) if parent else tk.Toplevel()
        dialog.title(title)
        dialog.configure(bg=COLORS['white'])
        dialog.transient(parent) if parent else None
        dialog.grab_set()
        dialog.focus_force()
        
        # Fixed smaller size for better appearance
        width = 380
        height = 180
        
        # Center on parent or screen
        dialog.update_idletasks()
        if parent and parent.winfo_exists():
            parent_x = parent.winfo_rootx()
            parent_y = parent.winfo_rooty()
            parent_width = parent.winfo_width()
            parent_height = parent.winfo_height()
            x = parent_x + (parent_width // 2) - (width // 2)
            y = parent_y + (parent_height // 2) - (height // 2)
        else:
            x = (dialog.winfo_screenwidth() // 2) - (width // 2)
            y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Main container
        main_frame = tk.Frame(dialog, bg=COLORS['white'], relief='flat', bd=1)
        main_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Content frame
        content_frame = tk.Frame(main_frame, bg=COLORS['white'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Icon
        icon_label = tk.Label(content_frame, text="✗", font=('Segoe UI', 42, 'bold'), 
                              bg=COLORS['white'], fg=COLORS['danger'])
        icon_label.pack(pady=(0, 10))
        
        # Message
        message_label = tk.Label(content_frame, text=message, font=('Segoe UI', 10), 
                                 bg=COLORS['white'], fg=COLORS['text'], 
                                 wraplength=320, justify='center')
        message_label.pack(pady=(0, 15), expand=True)
        
        # OK Button
        btn = tk.Button(content_frame, text="OK", command=dialog.destroy,
                       bg=COLORS['danger'], fg='white', font=('Segoe UI', 10, 'bold'),
                       padx=35, pady=5, bd=0, cursor='hand2', relief='flat',
                       activebackground=COLORS['danger_dark'], activeforeground='white')
        btn.pack()
        
        # Keyboard shortcuts
        dialog.bind('<Return>', lambda e: dialog.destroy())
        dialog.bind('<Escape>', lambda e: dialog.destroy())
        dialog.after(10, lambda: btn.focus())
        
        dialog.wait_window()
    
    @staticmethod
    def show_warning(title, message, parent=None):
        """Show warning dialog - centered, smaller, instant, professional"""
        dialog = tk.Toplevel(parent) if parent else tk.Toplevel()
        dialog.title(title)
        dialog.configure(bg=COLORS['white'])
        dialog.transient(parent) if parent else None
        dialog.grab_set()
        dialog.focus_force()
        
        # Fixed smaller size for better appearance
        width = 380
        height = 180
        
        # Center on parent or screen
        dialog.update_idletasks()
        if parent and parent.winfo_exists():
            parent_x = parent.winfo_rootx()
            parent_y = parent.winfo_rooty()
            parent_width = parent.winfo_width()
            parent_height = parent.winfo_height()
            x = parent_x + (parent_width // 2) - (width // 2)
            y = parent_y + (parent_height // 2) - (height // 2)
        else:
            x = (dialog.winfo_screenwidth() // 2) - (width // 2)
            y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Main container
        main_frame = tk.Frame(dialog, bg=COLORS['white'], relief='flat', bd=1)
        main_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Content frame
        content_frame = tk.Frame(main_frame, bg=COLORS['white'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Icon
        icon_label = tk.Label(content_frame, text="⚠", font=('Segoe UI', 42, 'bold'), 
                              bg=COLORS['white'], fg=COLORS['warning'])
        icon_label.pack(pady=(0, 10))
        
        # Message
        message_label = tk.Label(content_frame, text=message, font=('Segoe UI', 10), 
                                 bg=COLORS['white'], fg=COLORS['text'], 
                                 wraplength=320, justify='center')
        message_label.pack(pady=(0, 15), expand=True)
        
        # OK Button
        btn = tk.Button(content_frame, text="OK", command=dialog.destroy,
                       bg=COLORS['warning'], fg='white', font=('Segoe UI', 10, 'bold'),
                       padx=35, pady=5, bd=0, cursor='hand2', relief='flat',
                       activebackground=COLORS['info_dark'], activeforeground='white')
        btn.pack()
        
        # Keyboard shortcuts
        dialog.bind('<Return>', lambda e: dialog.destroy())
        dialog.bind('<Escape>', lambda e: dialog.destroy())
        dialog.after(10, lambda: btn.focus())
        
        dialog.wait_window()
    
    @staticmethod
    def ask_question(title, message, parent=None):
        """Show question dialog with Yes/Cancel buttons - centered, smaller, instant"""
        result = [False]
        
        dialog = tk.Toplevel(parent) if parent else tk.Toplevel()
        dialog.title(title)
        dialog.configure(bg=COLORS['white'])
        dialog.transient(parent) if parent else None
        dialog.grab_set()
        dialog.focus_force()
        
        # Fixed size for question dialog
        width = 400
        height = 190
        
        # Center on parent or screen
        dialog.update_idletasks()
        if parent and parent.winfo_exists():
            parent_x = parent.winfo_rootx()
            parent_y = parent.winfo_rooty()
            parent_width = parent.winfo_width()
            parent_height = parent.winfo_height()
            x = parent_x + (parent_width // 2) - (width // 2)
            y = parent_y + (parent_height // 2) - (height // 2)
        else:
            x = (dialog.winfo_screenwidth() // 2) - (width // 2)
            y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Main container
        main_frame = tk.Frame(dialog, bg=COLORS['white'], relief='flat', bd=1)
        main_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Content frame
        content_frame = tk.Frame(main_frame, bg=COLORS['white'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Icon
        icon_label = tk.Label(content_frame, text="?", font=('Segoe UI', 42, 'bold'), 
                              bg=COLORS['white'], fg=COLORS['info'])
        icon_label.pack(pady=(0, 10))
        
        # Message
        message_label = tk.Label(content_frame, text=message, font=('Segoe UI', 10), 
                                 bg=COLORS['white'], fg=COLORS['text'], 
                                 wraplength=340, justify='center')
        message_label.pack(pady=(0, 15), expand=True)
        
        # Button frame
        button_frame = tk.Frame(content_frame, bg=COLORS['white'])
        button_frame.pack()
        
        def on_yes():
            result[0] = True
            dialog.destroy()
        
        def on_no():
            result[0] = False
            dialog.destroy()
        
        # Yes Button
        btn_yes = tk.Button(button_frame, text="Yes", command=on_yes,
                           bg=COLORS['secondary'], fg='white', font=('Segoe UI', 10, 'bold'),
                           padx=25, pady=5, bd=0, cursor='hand2', relief='flat',
                           activebackground=COLORS['secondary_dark'], activeforeground='white')
        btn_yes.pack(side='left', padx=10)
        
        # Cancel Button
        btn_no = tk.Button(button_frame, text="Cancel", command=on_no,
                          bg=COLORS['danger'], fg='white', font=('Segoe UI', 10, 'bold'),
                          padx=25, pady=5, bd=0, cursor='hand2', relief='flat',
                          activebackground=COLORS['danger_dark'], activeforeground='white')
        btn_no.pack(side='left', padx=10)
        
        # Keyboard shortcuts
        dialog.bind('<Return>', lambda e: on_yes())
        dialog.bind('<Escape>', lambda e: on_no())
        dialog.after(10, lambda: btn_yes.focus())
        
        dialog.wait_window()
        
        return result[0]


class ModernButton(tk.Button):
    """Custom modern button widget"""
    def __init__(self, parent, text, command, color='primary', **kwargs):
        bg_color = COLORS.get(color, COLORS['primary'])
        hover_color = COLORS.get(f'{color}_dark', COLORS['primary_light'])
        
        super().__init__(parent, text=text, command=command,
                        bg=bg_color, fg='white', font=('Segoe UI', 10, 'bold'),
                        padx=20, pady=8, bd=0, cursor='hand2', relief='flat', **kwargs)
        
        self.default_bg = bg_color
        self.hover_bg = hover_color
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, e):
        self.config(bg=self.hover_bg)
    
    def on_leave(self, e):
        self.config(bg=self.default_bg)


class HospitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kerugoya Hospital Management System - Database Edition")
        
        # Make window responsive
        self.root.configure(bg=COLORS['light_bg'])
        
        # Get screen dimensions for responsive sizing
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set window size (80% of screen, max 1400x800)
        window_width = min(int(screen_width * 0.85), 1400)
        window_height = min(int(screen_height * 0.85), 800)
        
        # Center window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Make window resizable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Initialize DATABASE
        self.db = HospitalDatabase("kerugoya_hospital.db")
        
        # Initialize data structures
        self.patient_db = HashTable()
        self.triage_queue = PriorityQueue()
        self.calendar = AppointmentCalendar()
        self.treatment_stack = TreatmentStack()
        self.patient_treatments = PatientTreatmentHistory()
        self.hospital_map = HospitalGraph()
        
        # Load data from DATABASE into memory
        self.load_from_database()
        
        # FIXED: Auto-increment counter - get from database and DON'T increment on display
        self.last_patient_number = self.db.get_last_patient_number()
        self.current_display_id = None  # Store current display ID without incrementing
        
        # Current user session
        self.current_patient_id = None
        
        # Create GUI
        self.create_header()
        self.create_menu()
        self.create_main_dashboard()
        self.create_status_bar()
        
        # FIXED: Update patient ID display WITHOUT auto-incrementing
        self.update_patient_id_display()
        
        # Bind close event to auto-save to database
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Update status
        self.update_status("Connected to SQLite Database")
    
    def load_from_database(self):
        """Load all data from database into memory data structures"""
        try:
            # Load patients
            patients = self.db.get_all_patients()
            for p in patients:
                patient = PatientRecord(
                    p['patient_id'], p['name'], p['age'],
                    p['contact'], p['blood_group'], p['allergies']
                )
                self.patient_db.insert(patient)
            
            # Load triage queue
            triage_patients = self.db.get_triage_queue()
            for tp in triage_patients:
                triage_patient = TriagePatient(
                    tp['patient_id'], tp['name'], 
                    tp['condition'], tp['priority']
                )
                self.triage_queue.enqueue(triage_patient)
            
            # Load appointments
            for day in range(7):
                appointments = self.db.get_appointments_for_day(day)
                for appt in appointments:
                    self.calendar.calendar[day][appt['slot_index']] = {
                        'patient_id': appt['patient_id'],
                        'patient_name': appt['patient_name']
                    }
            
            # Load treatment history
            for patient in patients:
                treatments = self.db.get_treatment_history(patient['patient_id'])
                for t in treatments:
                    self.patient_treatments.add_treatment(
                        patient['patient_id'],
                        t['treatment'],
                        t['doctor'],
                        t['treatment_date']
                    )
            
            print(f"✅ Loaded {len(patients)} patients from database")
            
        except Exception as e:
            print(f"Error loading from database: {e}")
            self.load_sample_data()
    
    def sync_to_database(self):
        """Sync memory data structures to database"""
        try:
            # Save all patients
            patients = self.patient_db.get_all()
            for patient in patients:
                self.db.save_patient(patient)
            
            print(f"✅ Synced {len(patients)} patients to database")
            SilentMessageBox.show_info("Sync Complete", f"✅ Successfully synced {len(patients)} patients to database", self.root)
            return True
        except Exception as e:
            SilentMessageBox.show_error("Sync Failed", f"❌ Error syncing to database: {e}", self.root)
            return False
    
    def on_closing(self):
        """Handle application closing - save to database"""
        self.sync_to_database()
        self.db.update_last_patient_number(self.last_patient_number)
        self.db.close()
        self.root.destroy()
    
    def create_header(self):
        """Create modern header with logo and title"""
        header_frame = tk.Frame(self.root, bg=COLORS['primary'], height=80)
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        header_frame.grid_propagate(False)
        
        # Configure header columns
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=0)
        
        # Title
        title_frame = tk.Frame(header_frame, bg=COLORS['primary'])
        title_frame.grid(row=0, column=0, padx=20, pady=15, sticky='w')
        
        tk.Label(title_frame, text="🏥", font=('Segoe UI', 32), bg=COLORS['primary']).pack(side='left', padx=(0, 10))
        
        text_frame = tk.Frame(title_frame, bg=COLORS['primary'])
        text_frame.pack(side='left')
        
        tk.Label(text_frame, text="KERUGOYA HOSPITAL", font=('Segoe UI', 18, 'bold'),
                bg=COLORS['primary'], fg='white').pack(anchor='w')
        tk.Label(text_frame, text="Management Information System (SQLite Database)", font=('Segoe UI', 10),
                bg=COLORS['primary'], fg=COLORS['light_bg']).pack(anchor='w')
        
        # Date and time
        self.datetime_frame = tk.Frame(header_frame, bg=COLORS['primary'])
        self.datetime_frame.grid(row=0, column=1, padx=20, pady=15, sticky='e')
        
        self.date_label = tk.Label(self.datetime_frame, font=('Segoe UI', 11, 'bold'),
                                   bg=COLORS['primary'], fg='white')
        self.date_label.pack()
        self.time_label = tk.Label(self.datetime_frame, font=('Segoe UI', 10),
                                   bg=COLORS['primary'], fg=COLORS['light_bg'])
        self.time_label.pack()
        
        self.update_datetime()
    
    def update_datetime(self):
        """Update date and time display"""
        now = datetime.now()
        self.date_label.config(text=now.strftime("%A, %B %d, %Y"))
        self.time_label.config(text=now.strftime("%I:%M:%S %p"))
        self.root.after(1000, self.update_datetime)
    
    def create_menu(self):
        """Create modern menu bar with database options"""
        menubar = tk.Menu(self.root, bg=COLORS['primary'], fg='white', activebackground=COLORS['primary_light'])
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg='white', fg=COLORS['text'])
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Sync to Database", command=self.sync_to_database)
        file_menu.add_command(label="Backup Database", command=self.backup_database)
        file_menu.add_separator()
        file_menu.add_command(label="Export to CSV", command=self.export_to_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0, bg='white', fg=COLORS['text'])
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Database Statistics", command=self.show_db_stats)
        view_menu.add_command(label="Refresh All", command=self.refresh_all_displays)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg='white', fg=COLORS['text'])
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Database Info", command=self.show_db_info)
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        status_frame = tk.Frame(self.root, bg=COLORS['gray'], height=25)
        status_frame.grid(row=3, column=0, sticky='ew', pady=(10, 0))
        status_frame.grid_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="Connected to SQLite Database", font=('Segoe UI', 9),
                                     bg=COLORS['gray'], fg='white')
        self.status_label.pack(side='left', padx=10)
        
        # Database indicator
        self.db_indicator = tk.Label(status_frame, text="● SQLite Active", font=('Segoe UI', 9),
                                       bg=COLORS['gray'], fg=COLORS['secondary'])
        self.db_indicator.pack(side='right', padx=10)
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.root.after(3000, lambda: self.status_label.config(text="Ready"))
    
    def backup_database(self):
        """Create database backup"""
        backup_file = self.db.backup_database()
        SilentMessageBox.show_info("Backup Created", f"✅ Database backed up to:\n{backup_file}", self.root)
        self.update_status(f"Database backed up to {backup_file}")
    
    def show_db_stats(self):
        """Show database statistics"""
        stats = self.db.get_statistics()
        
        stats_text = f"📊 HOSPITAL DATABASE STATISTICS\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n👥 Total Patients:      {stats.get('total_patients', 0)}\n\n📅 Today's Appointments: {stats.get('today_appointments', 0)}\n\n🚑 Waiting in Triage:    {stats.get('waiting_triage', 0)}\n🔴 Emergency Waiting:    {stats.get('emergency_waiting', 0)}\n\n💾 Database File:        kerugoya_hospital.db"
        
        SilentMessageBox.show_info("Database Statistics", stats_text, self.root)
    
    def show_db_info(self):
        """Show database information"""
        info_text = "📁 DATABASE INFORMATION\n\nDatabase File: kerugoya_hospital.db\nType: SQLite (Serverless)\n\nTables Created:\n✓ patients\n✓ triage_queue\n✓ appointments\n✓ treatments\n✓ system_settings\n\nFeatures:\n✓ Auto-save on close\n✓ Data persists after PC restart\n✓ Multi-user ready\n✓ Backup capability"
        
        SilentMessageBox.show_info("Database Information", info_text, self.root)
    
    def create_main_dashboard(self):
        """Create main dashboard with notebook tabs"""
        # Create main container frame
        main_container = tk.Frame(self.root, bg=COLORS['light_bg'])
        main_container.grid(row=2, column=0, sticky='nsew', padx=10, pady=5)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Style for notebook
        style = ttk.Style()
        style.configure('Custom.TNotebook', background=COLORS['light_bg'])
        style.configure('Custom.TNotebook.Tab', padding=[12, 5], font=('Segoe UI', 10))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # Create all tabs
        self.create_registration_tab()
        self.create_patient_list_tab()
        self.create_triage_tab()
        self.create_appointment_tab()
        self.create_treatment_tab()
        self.create_routing_tab()
        self.create_search_tab()
    
    def create_registration_tab(self):
        """Patient registration form - CENTERED and IMPROVED"""
        self.registration_tab = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.registration_tab, text="📋 Patient Registration")
        
        # Create a frame to center the content
        center_frame = tk.Frame(self.registration_tab, bg=COLORS['light_bg'])
        center_frame.pack(expand=True, fill='both')
        
        # Configure grid to center content
        center_frame.grid_rowconfigure(0, weight=1)
        center_frame.grid_rowconfigure(2, weight=1)
        center_frame.grid_columnconfigure(0, weight=1)
        center_frame.grid_columnconfigure(2, weight=1)
        
        # Main content frame (centered)
        content_frame = tk.Frame(center_frame, bg=COLORS['white'], relief='flat', bd=1)
        content_frame.grid(row=1, column=1, padx=40, pady=30, sticky='nsew')
        
        # Title
        title_label = tk.Label(content_frame, text="NEW PATIENT REGISTRATION", 
                                font=('Segoe UI', 20, 'bold'), bg=COLORS['white'], fg=COLORS['primary'])
        title_label.pack(pady=(20, 30))
        
        # Form frame
        form_frame = tk.Frame(content_frame, bg=COLORS['white'])
        form_frame.pack(padx=40, pady=10)
        
        # Configure grid columns for alignment
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=2)
        
        # Patient ID (Auto-generated - display only)
        tk.Label(form_frame, text="Patient ID:", font=('Segoe UI', 11, 'bold'), bg=COLORS['white'], 
                fg=COLORS['text']).grid(row=0, column=0, sticky='e', padx=10, pady=10)
        self.pid_display_label = tk.Label(form_frame, text="", font=('Segoe UI', 12, 'bold'), 
                                         bg=COLORS['light_bg'], fg=COLORS['info'], width=25, anchor='w', 
                                         relief='solid', bd=1, padx=5)
        self.pid_display_label.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        
        # Full Name
        tk.Label(form_frame, text="Full Name:", font=('Segoe UI', 11), bg=COLORS['white'], 
                fg=COLORS['text']).grid(row=1, column=0, sticky='e', padx=10, pady=10)
        self.name_entry = tk.Entry(form_frame, width=35, font=('Segoe UI', 11), relief='solid', bd=1)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        
        # Age
        tk.Label(form_frame, text="Age:", font=('Segoe UI', 11), bg=COLORS['white'], 
                fg=COLORS['text']).grid(row=2, column=0, sticky='e', padx=10, pady=10)
        self.age_entry = tk.Entry(form_frame, width=35, font=('Segoe UI', 11), relief='solid', bd=1)
        self.age_entry.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
        
        # Contact (10 digits with validation)
        tk.Label(form_frame, text="Contact (10 digits):", font=('Segoe UI', 11), bg=COLORS['white'], 
                fg=COLORS['text']).grid(row=3, column=0, sticky='e', padx=10, pady=10)
        self.contact_entry = tk.Entry(form_frame, width=35, font=('Segoe UI', 11), relief='solid', bd=1)
        self.contact_entry.grid(row=3, column=1, padx=10, pady=10, sticky='ew')
        
        # Add contact validation to limit to 10 digits
        self.contact_entry.bind('<KeyRelease>', self.validate_contact_length)
        
        # Blood Group
        tk.Label(form_frame, text="Blood Group:", font=('Segoe UI', 11), bg=COLORS['white'], 
                fg=COLORS['text']).grid(row=4, column=0, sticky='e', padx=10, pady=10)
        self.blood_group_var = tk.StringVar()
        blood_groups = ["Select Blood Group", "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
        self.blood_group_combo = ttk.Combobox(form_frame, textvariable=self.blood_group_var, 
                                              values=blood_groups, width=32, font=('Segoe UI', 11))
        self.blood_group_combo.grid(row=4, column=1, padx=10, pady=10, sticky='ew')
        self.blood_group_combo.set("Select Blood Group")
        
        # Allergies
        tk.Label(form_frame, text="Allergies:", font=('Segoe UI', 11), bg=COLORS['white'], 
                fg=COLORS['text']).grid(row=5, column=0, sticky='e', padx=10, pady=10)
        self.allergies_entry = tk.Entry(form_frame, width=35, font=('Segoe UI', 11), relief='solid', bd=1)
        self.allergies_entry.grid(row=5, column=1, padx=10, pady=10, sticky='ew')
        
        # Required fields note
        note_frame = tk.Frame(form_frame, bg=COLORS['white'])
        note_frame.grid(row=6, column=0, columnspan=2, pady=15)
        tk.Label(note_frame, text="* Required fields", font=('Segoe UI', 9), 
                bg=COLORS['white'], fg=COLORS['danger']).pack()
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg=COLORS['white'])
        button_frame.grid(row=7, column=0, columnspan=2, pady=25)
        
        ModernButton(button_frame, text="✅ Register Patient", command=self.register_patient, 
                    color='secondary').pack(side='left', padx=10)
        ModernButton(button_frame, text="🗑️ Clear Form", command=self.clear_registration_form, 
                    color='danger').pack(side='left', padx=10)
    
    def validate_contact_length(self, event=None):
        """Limit contact field to exactly 10 digits"""
        current = self.contact_entry.get()
        # Remove any non-digit characters
        filtered = ''.join([c for c in current if c.isdigit()])
        if len(filtered) > 10:
            filtered = filtered[:10]
        if filtered != current:
            self.contact_entry.delete(0, tk.END)
            self.contact_entry.insert(0, filtered)
    
    def create_patient_list_tab(self):
        """Patient directory tab"""
        self.patient_list_tab = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.patient_list_tab, text="📊 Patient Directory")
        
        frame = tk.Frame(self.patient_list_tab, bg=COLORS['light_bg'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(frame, text="REGISTERED PATIENTS DIRECTORY", 
                font=('Segoe UI', 18, 'bold'), bg=COLORS['light_bg'], fg=COLORS['primary']).pack(pady=10)
        
        # Search bar
        search_frame = tk.Frame(frame, bg=COLORS['light_bg'])
        search_frame.pack(pady=15)
        
        tk.Label(search_frame, text="Search:", bg=COLORS['light_bg'], font=('Segoe UI', 11)).pack(side='left', padx=5)
        self.patient_search_entry = tk.Entry(search_frame, width=40, font=('Segoe UI', 11), relief='solid', bd=1)
        self.patient_search_entry.pack(side='left', padx=5)
        ModernButton(search_frame, text="🔍 Search", command=self.search_in_patient_list, 
                    color='info').pack(side='left', padx=5)
        ModernButton(search_frame, text="Show All", command=self.update_patient_list_display, 
                    color='secondary').pack(side='left', padx=5)
        
        # Patient list display
        self.patient_list_display = scrolledtext.ScrolledText(frame, height=18, width=100, 
                                                              font=('Consolas', 10), wrap=tk.NONE)
        self.patient_list_display.pack(pady=10, fill='both', expand=True)
        
        # Stats label
        self.patient_stats_label = tk.Label(frame, text="", bg=COLORS['light_bg'], 
                                           font=('Segoe UI', 11, 'bold'), fg=COLORS['info'])
        self.patient_stats_label.pack(pady=5)
        
        self.update_patient_list_display()
    
    def create_triage_tab(self):
        """Triage queue management"""
        self.triage_tab = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.triage_tab, text="🚑 Triage Queue")
        
        # Two-column layout
        left_frame = tk.Frame(self.triage_tab, bg=COLORS['light_bg'])
        left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        right_frame = tk.Frame(self.triage_tab, bg=COLORS['light_bg'])
        right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        # Left panel - Add to queue (Card)
        add_card = tk.Frame(left_frame, bg=COLORS['white'], relief='flat', bd=1)
        add_card.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(add_card, text="ADD TO TRIAGE QUEUE", font=('Segoe UI', 16, 'bold'), 
                bg=COLORS['white'], fg=COLORS['primary']).pack(pady=15)
        
        form_frame = tk.Frame(add_card, bg=COLORS['white'])
        form_frame.pack(pady=20, padx=20)
        
        # Patient ID
        tk.Label(form_frame, text="Patient ID:", bg=COLORS['white'], font=('Segoe UI', 11)).grid(row=0, column=0, pady=10, sticky='e')
        self.triage_pid_entry = tk.Entry(form_frame, width=25, font=('Segoe UI', 11), relief='solid', bd=1)
        self.triage_pid_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Condition
        tk.Label(form_frame, text="Condition:", bg=COLORS['white'], font=('Segoe UI', 11)).grid(row=1, column=0, pady=10, sticky='e')
        self.condition_entry = tk.Entry(form_frame, width=35, font=('Segoe UI', 11), relief='solid', bd=1)
        self.condition_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Priority
        tk.Label(form_frame, text="Priority:", bg=COLORS['white'], font=('Segoe UI', 11)).grid(row=2, column=0, pady=10, sticky='ne')
        priority_frame = tk.Frame(form_frame, bg=COLORS['white'])
        priority_frame.grid(row=2, column=1, pady=10, padx=10, sticky='w')
        
        self.priority_var = tk.StringVar(value="3")
        priorities = [("🔴 Emergency (1)", "1"), ("🟡 Serious (2)", "2"), ("🟢 Minor (3)", "3")]
        for text, value in priorities:
            tk.Radiobutton(priority_frame, text=text, variable=self.priority_var, 
                          value=value, bg=COLORS['white'], font=('Segoe UI', 10)).pack(anchor='w', pady=2)
        
        ModernButton(add_card, text="➕ Add to Queue", command=self.add_to_triage, 
                    color='info').pack(pady=20)
        
        # Right panel - Queue display
        queue_card = tk.Frame(right_frame, bg=COLORS['white'], relief='flat', bd=1)
        queue_card.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(queue_card, text="CURRENT TRIAGE QUEUE", font=('Segoe UI', 16, 'bold'), 
                bg=COLORS['white'], fg=COLORS['primary']).pack(pady=15)
        
        self.queue_display = scrolledtext.ScrolledText(queue_card, height=15, width=55, 
                                                       font=('Consolas', 10))
        self.queue_display.pack(pady=10, padx=10, fill='both', expand=True)
        
        button_frame = tk.Frame(queue_card, bg=COLORS['white'])
        button_frame.pack(pady=15)
        ModernButton(button_frame, text="🚨 Serve Next", command=self.serve_next, 
                    color='danger').pack(side='left', padx=5)
        ModernButton(button_frame, text="🔄 Refresh", command=self.update_queue_display, 
                    color='gray').pack(side='left', padx=5)
        
        self.update_queue_display()
    
    def create_appointment_tab(self):
        """Appointment scheduling"""
        self.appointment_tab = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.appointment_tab, text="📅 Appointments")
        
        # Two-column layout
        left_frame = tk.Frame(self.appointment_tab, bg=COLORS['light_bg'])
        left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        right_frame = tk.Frame(self.appointment_tab, bg=COLORS['light_bg'])
        right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        # Left panel - Book appointment
        book_card = tk.Frame(left_frame, bg=COLORS['white'], relief='flat', bd=1)
        book_card.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(book_card, text="BOOK APPOINTMENT", font=('Segoe UI', 16, 'bold'), 
                bg=COLORS['white'], fg=COLORS['primary']).pack(pady=15)
        
        form_frame = tk.Frame(book_card, bg=COLORS['white'])
        form_frame.pack(pady=20, padx=20)
        
        # Patient ID
        tk.Label(form_frame, text="Patient ID:", bg=COLORS['white'], font=('Segoe UI', 11)).grid(row=0, column=0, pady=10, sticky='e')
        self.appt_pid_entry = tk.Entry(form_frame, width=25, font=('Segoe UI', 11), relief='solid', bd=1)
        self.appt_pid_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Day
        tk.Label(form_frame, text="Day:", bg=COLORS['white'], font=('Segoe UI', 11)).grid(row=1, column=0, pady=10, sticky='e')
        self.day_var = tk.StringVar()
        day_menu = ttk.Combobox(form_frame, textvariable=self.day_var, values=self.calendar.days, 
                                width=22, font=('Segoe UI', 11))
        day_menu.grid(row=1, column=1, pady=10, padx=10)
        
        # Time Slot
        tk.Label(form_frame, text="Time Slot:", bg=COLORS['white'], font=('Segoe UI', 11)).grid(row=2, column=0, pady=10, sticky='e')
        self.slot_var = tk.StringVar()
        slot_menu = ttk.Combobox(form_frame, textvariable=self.slot_var, values=self.calendar.slots, 
                                 width=22, font=('Segoe UI', 11))
        slot_menu.grid(row=2, column=1, pady=10, padx=10)
        
        ModernButton(book_card, text="📅 Book Appointment", command=self.book_appointment, 
                    color='secondary').pack(pady=20)
        
        # Right panel - View schedule
        schedule_card = tk.Frame(right_frame, bg=COLORS['white'], relief='flat', bd=1)
        schedule_card.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(schedule_card, text="WEEKLY SCHEDULE", font=('Segoe UI', 16, 'bold'), 
                bg=COLORS['white'], fg=COLORS['primary']).pack(pady=15)
        
        self.schedule_display = scrolledtext.ScrolledText(schedule_card, height=18, width=60, 
                                                          font=('Consolas', 9))
        self.schedule_display.pack(pady=10, padx=10, fill='both', expand=True)
        
        ModernButton(schedule_card, text="🔄 Refresh Schedule", command=self.update_schedule_display, 
                    color='info').pack(pady=15)
        
        self.update_schedule_display()
    
    def create_treatment_tab(self):
        """Treatment history with undo/redo"""
        self.treatment_tab = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.treatment_tab, text="💊 Treatment History")
        
        # Two-column layout
        left_frame = tk.Frame(self.treatment_tab, bg=COLORS['light_bg'])
        left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        right_frame = tk.Frame(self.treatment_tab, bg=COLORS['light_bg'])
        right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        # Left panel - Add treatment
        treatment_card = tk.Frame(left_frame, bg=COLORS['white'], relief='flat', bd=1)
        treatment_card.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(treatment_card, text="ADD TREATMENT", font=('Segoe UI', 16, 'bold'), 
                bg=COLORS['white'], fg=COLORS['primary']).pack(pady=15)
        
        form_frame = tk.Frame(treatment_card, bg=COLORS['white'])
        form_frame.pack(pady=20, padx=20)
        
        # Patient ID
        tk.Label(form_frame, text="Patient ID:", bg=COLORS['white'], font=('Segoe UI', 11)).grid(row=0, column=0, pady=10, sticky='e')
        self.treatment_pid_entry = tk.Entry(form_frame, width=25, font=('Segoe UI', 11), relief='solid', bd=1)
        self.treatment_pid_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Treatment
        tk.Label(form_frame, text="Treatment:", bg=COLORS['white'], font=('Segoe UI', 11)).grid(row=1, column=0, pady=10, sticky='ne')
        self.treatment_desc = tk.Text(form_frame, height=4, width=35, font=('Segoe UI', 11), relief='solid', bd=1)
        self.treatment_desc.grid(row=1, column=1, pady=10, padx=10)
        
        # Doctor
        tk.Label(form_frame, text="Doctor:", bg=COLORS['white'], font=('Segoe UI', 11)).grid(row=2, column=0, pady=10, sticky='e')
        self.doctor_entry = tk.Entry(form_frame, width=25, font=('Segoe UI', 11), relief='solid', bd=1)
        self.doctor_entry.grid(row=2, column=1, pady=10, padx=10)
        
        button_frame = tk.Frame(treatment_card, bg=COLORS['white'])
        button_frame.pack(pady=20)
        ModernButton(button_frame, text="💊 Record Treatment", command=self.add_treatment, 
                    color='secondary').pack(side='left', padx=5)
        ModernButton(button_frame, text="↩️ Undo Last", command=self.undo_treatment, 
                    color='warning').pack(side='left', padx=5)
        ModernButton(button_frame, text="↪️ Redo Last", command=self.redo_treatment, 
                    color='info').pack(side='left', padx=5)
        
        # Right panel - View history
        history_card = tk.Frame(right_frame, bg=COLORS['white'], relief='flat', bd=1)
        history_card.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(history_card, text="TREATMENT HISTORY", font=('Segoe UI', 16, 'bold'), 
                bg=COLORS['white'], fg=COLORS['primary']).pack(pady=15)
        
        search_frame = tk.Frame(history_card, bg=COLORS['white'])
        search_frame.pack(pady=10)
        tk.Label(search_frame, text="Patient ID:", bg=COLORS['white'], font=('Segoe UI', 11)).pack(side='left', padx=5)
        self.view_history_entry = tk.Entry(search_frame, width=20, font=('Segoe UI', 11), relief='solid', bd=1)
        self.view_history_entry.pack(side='left', padx=5)
        ModernButton(search_frame, text="Show History", command=self.show_treatment_history, 
                    color='info').pack(side='left', padx=5)
        
        self.history_display = scrolledtext.ScrolledText(history_card, height=15, width=55, 
                                                         font=('Consolas', 10))
        self.history_display.pack(pady=10, padx=10, fill='both', expand=True)
    
    def create_routing_tab(self):
        """Department routing using graph"""
        self.routing_tab = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.routing_tab, text="🗺️ Department Routing")
        
        frame = tk.Frame(self.routing_tab, bg=COLORS['light_bg'])
        frame.pack(pady=30, padx=30, fill='both', expand=True)
        
        tk.Label(frame, text="FIND SHORTEST PATH BETWEEN DEPARTMENTS", 
                font=('Segoe UI', 18, 'bold'), bg=COLORS['light_bg'], fg=COLORS['primary']).pack(pady=10)
        
        # Input frame (card)
        input_card = tk.Frame(frame, bg=COLORS['white'], relief='flat', bd=1)
        input_card.pack(pady=20, padx=20, fill='x')
        
        input_inner = tk.Frame(input_card, bg=COLORS['white'])
        input_inner.pack(pady=20, padx=20)
        
        tk.Label(input_inner, text="From Department:", bg=COLORS['white'], font=('Segoe UI', 11)).grid(row=0, column=0, padx=10, pady=10)
        self.from_dept = ttk.Combobox(input_inner, values=self.hospital_map.get_all_departments(), 
                                      width=30, font=('Segoe UI', 10))
        self.from_dept.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(input_inner, text="To Department:", bg=COLORS['white'], font=('Segoe UI', 11)).grid(row=0, column=2, padx=10, pady=10)
        self.to_dept = ttk.Combobox(input_inner, values=self.hospital_map.get_all_departments(), 
                                    width=30, font=('Segoe UI', 10))
        self.to_dept.grid(row=0, column=3, padx=10, pady=10)
        
        ModernButton(input_inner, text="🗺️ Find Shortest Path", command=self.find_shortest_path, 
                    color='secondary').grid(row=0, column=4, padx=20)
        
        # Result display
        self.path_result = scrolledtext.ScrolledText(frame, height=12, width=90, font=('Consolas', 10))
        self.path_result.pack(pady=20)
        
        # Department list
        info_frame = tk.Frame(frame, bg=COLORS['light_bg'])
        info_frame.pack(pady=10)
        tk.Label(info_frame, text="📍 Available Departments:", bg=COLORS['light_bg'], 
                font=('Segoe UI', 10, 'bold')).pack()
        dept_list = " → ".join(self.hospital_map.get_all_departments())
        tk.Label(info_frame, text=dept_list, bg=COLORS['light_bg'], wraplength=700, 
                font=('Segoe UI', 9), fg=COLORS['gray_dark']).pack()
    
    def create_search_tab(self):
        """Search for patient records"""
        self.search_tab = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.search_tab, text="🔍 Search Patient")
        
        frame = tk.Frame(self.search_tab, bg=COLORS['light_bg'])
        frame.pack(pady=40)
        
        tk.Label(frame, text="SEARCH PATIENT RECORD", font=('Segoe UI', 20, 'bold'), 
                bg=COLORS['light_bg'], fg=COLORS['primary']).pack(pady=10)
        
        search_card = tk.Frame(frame, bg=COLORS['white'], relief='flat', bd=1)
        search_card.pack(pady=20, padx=20)
        
        search_inner = tk.Frame(search_card, bg=COLORS['white'])
        search_inner.pack(pady=30, padx=30)
        
        tk.Label(search_inner, text="Enter Patient ID:", bg=COLORS['white'], 
                font=('Segoe UI', 12)).pack(side='left', padx=10)
        self.search_entry = tk.Entry(search_inner, width=30, font=('Segoe UI', 12), relief='solid', bd=1)
        self.search_entry.pack(side='left', padx=10)
        ModernButton(search_inner, text="🔍 Search", command=self.search_patient, 
                    color='info').pack(side='left', padx=10)
        
        self.search_result = scrolledtext.ScrolledText(frame, height=20, width=90, font=('Consolas', 10))
        self.search_result.pack(pady=20)
    
    # ========== FUNCTIONALITY METHODS ==========
    
    def get_last_patient_number(self):
        """Get the last patient number from database"""
        return self.db.get_last_patient_number()
    
    def generate_patient_id(self):
        """FIXED: Generate next patient ID and increment the counter"""
        self.last_patient_number += 1
        # Save the updated counter to database immediately
        self.db.update_last_patient_number(self.last_patient_number)
        return f"KGH{self.last_patient_number:03d}"
    
    def update_patient_id_display(self):
        """FIXED: Update the displayed patient ID WITHOUT auto-incrementing on refresh"""
        # Generate the NEXT ID that will be used for registration
        next_id_num = self.last_patient_number + 1
        next_id = f"KGH{next_id_num:03d}"
        if hasattr(self, 'pid_display_label'):
            self.pid_display_label.config(text=next_id)
    
    def validate_contact(self, contact):
        """Validate contact number (10 digits)"""
        return contact.isdigit() and len(contact) == 10
    
    def export_to_csv(self):
        """Export patient data to CSV for backup"""
        try:
            patients = self.patient_db.get_all()
            with open("patients_backup.csv", "w") as f:
                f.write("Patient ID,Name,Age,Contact,Blood Group,Allergies\n")
                for p in patients:
                    f.write(f"{p.patient_id},{p.name},{p.age},{p.contact},{p.blood_group},{p.allergies}\n")
            SilentMessageBox.show_info("Export", f"✅ Exported {len(patients)} patients to patients_backup.csv", self.root)
            self.update_status(f"Exported {len(patients)} patients")
        except Exception as e:
            SilentMessageBox.show_error("Error", f"❌ Export failed: {e}", self.root)
    
    def refresh_all_displays(self):
        """Refresh all displays"""
        self.update_patient_list_display()
        self.update_queue_display()
        self.update_schedule_display()
        # FIXED: Update patient ID display WITHOUT incrementing
        self.update_patient_id_display()
        SilentMessageBox.show_info("Refreshed", "✅ All displays have been refreshed!", self.root)
        self.update_status("All displays refreshed")
    
    def register_patient(self):
        """Register a new patient with validation and save to database"""
        # Validate inputs
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        contact = self.contact_entry.get().strip()
        blood_group = self.blood_group_var.get()
        allergies = self.allergies_entry.get().strip()
        
        # Validation
        if not name:
            SilentMessageBox.show_error("Error", "❌ Patient Name is required!", self.root)
            return
        
        if not age:
            SilentMessageBox.show_error("Error", "❌ Age is required!", self.root)
            return
        
        if not age.isdigit() or int(age) < 0 or int(age) > 150:
            SilentMessageBox.show_error("Error", "❌ Please enter a valid age (0-150)!", self.root)
            return
        
        if not contact:
            SilentMessageBox.show_error("Error", "❌ Contact number is required!", self.root)
            return
        
        if not self.validate_contact(contact):
            SilentMessageBox.show_error("Error", "❌ Contact must be exactly 10 digits (numbers only)!", self.root)
            return
        
        if not blood_group or blood_group == "Select Blood Group":
            SilentMessageBox.show_error("Error", "❌ Please select a blood group!", self.root)
            return
        
        # FIXED: Generate patient ID (this will increment the counter)
        patient_id = self.generate_patient_id()
        
        # Create patient object
        patient = PatientRecord(patient_id, name, age, contact, blood_group, allergies)
        
        # Save to memory
        if self.patient_db.insert(patient):
            # Save to DATABASE (counter already updated in generate_patient_id)
            if self.db.save_patient(patient):
                SilentMessageBox.show_info("Success", 
                    f"✅ Patient {name} registered successfully!\n\n🆔 Patient ID: {patient_id}\n💾 Saved to SQLite Database", self.root)
                
                self.clear_registration_form()
                self.update_patient_list_display()
                # FIXED: Update the display to show the NEXT ID
                self.update_patient_id_display()
                self.update_status(f"Patient {name} registered and saved to database")
            else:
                SilentMessageBox.show_error("Error", "❌ Database error! Patient not saved.", self.root)
        else:
            SilentMessageBox.show_error("Error", "❌ Failed to register patient. Database may be full.", self.root)
    
    def clear_registration_form(self):
        """Clear registration form"""
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.blood_group_var.set("Select Blood Group")
        self.allergies_entry.delete(0, tk.END)
        self.name_entry.focus()
    
    def update_patient_list_display(self):
        """Update the patient directory display"""
        self.patient_list_display.delete(1.0, tk.END)
        patients = self.patient_db.get_all()
        
        if patients:
            # Header
            self.patient_list_display.insert(tk.END, "=" * 95 + "\n")
            self.patient_list_display.insert(tk.END, f"{'ID':<12} {'Name':<30} {'Age':<6} {'Contact':<13} {'Blood':<8} {'Allergies':<20}\n")
            self.patient_list_display.insert(tk.END, "=" * 95 + "\n")
            
            # Patient data
            for p in patients:
                self.patient_list_display.insert(tk.END, f"{p.patient_id:<12} {p.name[:28]:<30} {p.age:<6} {p.contact:<13} {p.blood_group:<8} {p.allergies[:18]:<20}\n")
            
            self.patient_list_display.insert(tk.END, "=" * 95 + "\n")
            self.patient_list_display.insert(tk.END, f"\n📊 Total Patients: {len(patients)}")
            self.patient_stats_label.config(text=f"📊 Total Patients Registered: {len(patients)}")
        else:
            self.patient_list_display.insert(tk.END, "No patients registered yet.\nClick 'Patient Registration' tab to add patients.")
            self.patient_stats_label.config(text="📊 Total Patients Registered: 0")
    
    def search_in_patient_list(self):
        """Search patient in the list"""
        search_term = self.patient_search_entry.get().strip().lower()
        if not search_term:
            self.update_patient_list_display()
            return
        
        patients = self.patient_db.get_all()
        filtered = [p for p in patients if search_term in p.name.lower() or search_term in p.patient_id.lower()]
        
        self.patient_list_display.delete(1.0, tk.END)
        if filtered:
            self.patient_list_display.insert(tk.END, "=" * 95 + "\n")
            self.patient_list_display.insert(tk.END, f"{'ID':<12} {'Name':<30} {'Age':<6} {'Contact':<13} {'Blood':<8} {'Allergies':<20}\n")
            self.patient_list_display.insert(tk.END, "=" * 95 + "\n")
            for p in filtered:
                self.patient_list_display.insert(tk.END, f"{p.patient_id:<12} {p.name[:28]:<30} {p.age:<6} {p.contact:<13} {p.blood_group:<8} {p.allergies[:18]:<20}\n")
            self.patient_list_display.insert(tk.END, "=" * 95 + "\n")
            self.patient_list_display.insert(tk.END, f"\n📊 Showing {len(filtered)} of {len(patients)} patients")
        else:
            self.patient_list_display.insert(tk.END, f"No patients found matching '{search_term}'")
        
        self.patient_stats_label.config(text=f"Total Patients: {len(patients)} | Showing: {len(filtered)}")
    
    def add_to_triage(self):
        """Add patient to triage queue with database"""
        pid = self.triage_pid_entry.get().strip()
        condition = self.condition_entry.get().strip()
        priority = int(self.priority_var.get())
        
        if not pid:
            SilentMessageBox.show_error("Error", "❌ Patient ID required!", self.root)
            return
        
        if not condition:
            SilentMessageBox.show_error("Error", "❌ Please enter patient condition!", self.root)
            return
        
        # Check if patient exists
        patient = self.patient_db.lookup(pid)
        if not patient:
            SilentMessageBox.show_error("Error", f"❌ Patient {pid} not found!\n\nPlease register the patient first.", self.root)
            return
        
        # Add to memory
        triage_patient = TriagePatient(pid, patient.name, condition, priority)
        self.triage_queue.enqueue(triage_patient)
        
        # Add to DATABASE
        if self.db.add_to_triage(pid, patient.name, condition, priority):
            SilentMessageBox.show_info("Success", 
                f"✅ {patient.name} added to triage queue with priority {priority}\n💾 Saved to database", self.root)
        else:
            SilentMessageBox.show_warning("Warning", "Added to memory but database save failed!", self.root)
        
        # Clear inputs
        self.triage_pid_entry.delete(0, tk.END)
        self.condition_entry.delete(0, tk.END)
        self.update_queue_display()
        self.update_status(f"{patient.name} added to triage queue")
    
    def serve_next(self):
        """Serve the next patient from queue and update database"""
        patient = self.triage_queue.dequeue()
        if patient:
            # Update database
            self.db.serve_next_patient()
            SilentMessageBox.show_info("Serving Patient", f"🚨 Now serving:\n\n{patient}", self.root)
            self.update_queue_display()
            self.update_status(f"Serving patient: {patient.name}")
        else:
            SilentMessageBox.show_warning("Queue Empty", "⚠️ No patients in the triage queue.", self.root)
    
    def update_queue_display(self):
        """Update queue display with colors"""
        self.queue_display.delete(1.0, tk.END)
        
        # Configure color tags
        self.queue_display.tag_configure("emergency", foreground="#e74c3c", font=('Consolas', 10, 'bold'))
        self.queue_display.tag_configure("serious", foreground="#f39c12", font=('Consolas', 10, 'bold'))
        self.queue_display.tag_configure("minor", foreground="#27ae60", font=('Consolas', 10))
        self.queue_display.tag_configure("header", foreground="#2c5f8a", font=('Consolas', 10, 'bold'))
        
        queue_patients = self.triage_queue.get_all()
        
        if queue_patients:
            self.queue_display.insert(tk.END, "=" * 55 + "\n", "header")
            self.queue_display.insert(tk.END, "TRIAGE QUEUE (Emergency First)\n", "header")
            self.queue_display.insert(tk.END, "=" * 55 + "\n\n", "header")
            
            for i, patient in enumerate(queue_patients, 1):
                if patient.priority == 1:
                    tag = "emergency"
                    priority_symbol = "🔴"
                elif patient.priority == 2:
                    tag = "serious"
                    priority_symbol = "🟡"
                else:
                    tag = "minor"
                    priority_symbol = "🟢"
                
                display_text = f"{i}. {priority_symbol} {patient}\n"
                self.queue_display.insert(tk.END, display_text, tag)
            
            self.queue_display.insert(tk.END, "\n" + "=" * 55 + "\n", "header")
            self.queue_display.insert(tk.END, f"📊 Total waiting: {len(queue_patients)}", "header")
        else:
            self.queue_display.insert(tk.END, "Queue is empty.", "minor")
    
    def book_appointment(self):
        """Book an appointment with database"""
        pid = self.appt_pid_entry.get().strip()
        day = self.day_var.get()
        slot = self.slot_var.get()
        
        if not pid or not day or not slot:
            SilentMessageBox.show_error("Error", "❌ Please fill all fields!", self.root)
            return
        
        # Check if patient exists
        patient = self.patient_db.lookup(pid)
        if not patient:
            SilentMessageBox.show_error("Error", f"❌ Patient {pid} not found!\n\nPlease register the patient first.", self.root)
            return
        
        day_index = self.calendar.days.index(day)
        slot_index = self.calendar.slots.index(slot)
        
        # Book in DATABASE first
        success, message = self.db.book_appointment(
            pid, patient.name, day, day_index, slot, slot_index
        )
        
        if success:
            # Also update memory
            self.calendar.book_appointment(day_index, slot_index, pid, patient.name)
            SilentMessageBox.show_info("Success", f"✅ {message}\n💾 Saved to database", self.root)
            self.update_schedule_display()
            self.update_status(f"Appointment booked for {patient.name}")
        else:
            SilentMessageBox.show_error("Error", f"❌ {message}", self.root)
    
    def update_schedule_display(self):
        """Update schedule display"""
        self.schedule_display.delete(1.0, tk.END)
        self.schedule_display.insert(tk.END, self.calendar.display_week_schedule())
    
    def add_treatment(self):
        """Add treatment record with database"""
        pid = self.treatment_pid_entry.get().strip()
        treatment = self.treatment_desc.get(1.0, tk.END).strip()
        doctor = self.doctor_entry.get().strip()
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        if not pid or not treatment or not doctor:
            SilentMessageBox.show_error("Error", "❌ Please fill all fields!", self.root)
            return
        
        # Check if patient exists
        patient = self.patient_db.lookup(pid)
        if not patient:
            SilentMessageBox.show_error("Error", f"❌ Patient {pid} not found!\n\nPlease register the patient first.", self.root)
            return
        
        # Add to memory
        self.treatment_stack.add_treatment(pid, treatment, doctor, date)
        self.patient_treatments.add_treatment(pid, treatment, doctor, date)
        
        # Add to DATABASE
        if self.db.add_treatment(pid, treatment, doctor):
            SilentMessageBox.show_info("Success", f"✅ Treatment recorded for {patient.name}\n💾 Saved to database", self.root)
        else:
            SilentMessageBox.show_warning("Warning", "Treatment saved in memory but database save failed!", self.root)
        
        # Clear fields
        self.treatment_pid_entry.delete(0, tk.END)
        self.treatment_desc.delete(1.0, tk.END)
        self.doctor_entry.delete(0, tk.END)
        self.update_status(f"Treatment recorded for {patient.name}")
    
    def undo_treatment(self):
        """Undo last treatment"""
        result = self.treatment_stack.undo()
        SilentMessageBox.show_info("Undo", f"↩️ {result}", self.root)
        self.update_status("Undo operation performed")
    
    def redo_treatment(self):
        """Redo last treatment"""
        result = self.treatment_stack.redo()
        SilentMessageBox.show_info("Redo", f"↪️ {result}", self.root)
        self.update_status("Redo operation performed")
    
    def show_treatment_history(self):
        """Show treatment history for a patient"""
        pid = self.view_history_entry.get().strip()
        if not pid:
            SilentMessageBox.show_error("Error", "❌ Enter Patient ID!", self.root)
            return
        
        history = self.patient_treatments.get_history(pid)
        self.history_display.delete(1.0, tk.END)
        
        if history:
            self.history_display.insert(tk.END, "=" * 55 + "\n")
            self.history_display.insert(tk.END, f"Treatment History for {pid}\n")
            self.history_display.insert(tk.END, "=" * 55 + "\n\n")
            for i, h in enumerate(history, 1):
                self.history_display.insert(tk.END, f"{i}. 📅 Date: {h['date']}\n")
                self.history_display.insert(tk.END, f"   👨‍⚕️ Doctor: {h['doctor']}\n")
                self.history_display.insert(tk.END, f"   💊 Treatment: {h['treatment']}\n")
                self.history_display.insert(tk.END, "-" * 55 + "\n")
        else:
            self.history_display.insert(tk.END, f"No treatment records found for patient {pid}")
    
    def find_shortest_path(self):
        """Find shortest path between departments"""
        start = self.from_dept.get()
        end = self.to_dept.get()
        
        if not start or not end:
            SilentMessageBox.show_error("Error", "❌ Select both departments!", self.root)
            return
        
        path, distance = self.hospital_map.shortest_path(start, end)
        
        self.path_result.delete(1.0, tk.END)
        if path:
            self.path_result.insert(tk.END, "=" * 60 + "\n")
            self.path_result.insert(tk.END, "SHORTEST PATH RESULT\n")
            self.path_result.insert(tk.END, "=" * 60 + "\n\n")
            self.path_result.insert(tk.END, f"📍 From: {start}\n")
            self.path_result.insert(tk.END, f"🎯 To: {end}\n\n")
            self.path_result.insert(tk.END, f"🚶 Route: {' → '.join(path)}\n\n")
            self.path_result.insert(tk.END, f"📏 Total distance: {distance} units\n")
            self.path_result.insert(tk.END, f"⏱️ Estimated walking time: {distance * 2} minutes\n")
            self.update_status(f"Path found from {start} to {end}")
        else:
            self.path_result.insert(tk.END, f"No path found from {start} to {end}")
            self.update_status("No path found")
    
    def search_patient(self):
        """Search for patient by ID"""
        pid = self.search_entry.get().strip().upper()
        
        if not pid:
            SilentMessageBox.show_error("Error", "❌ Enter Patient ID!", self.root)
            return
        
        patient = self.patient_db.lookup(pid)
        
        self.search_result.delete(1.0, tk.END)
        
        if patient:
            self.search_result.insert(tk.END, "=" * 70 + "\n")
            self.search_result.insert(tk.END, "PATIENT DETAILS\n")
            self.search_result.insert(tk.END, "=" * 70 + "\n\n")
            self.search_result.insert(tk.END, f"🆔 Patient ID:      {patient.patient_id}\n")
            self.search_result.insert(tk.END, f"👤 Name:            {patient.name}\n")
            self.search_result.insert(tk.END, f"📅 Age:             {patient.age}\n")
            self.search_result.insert(tk.END, f"📞 Contact:         {patient.contact}\n")
            self.search_result.insert(tk.END, f"🩸 Blood Group:     {patient.blood_group}\n")
            self.search_result.insert(tk.END, f"⚠️ Allergies:       {patient.allergies}\n")
            
            # Get appointments from database
            appointments = self.db.get_patient_appointments(pid)
            if appointments:
                self.search_result.insert(tk.END, f"\n📅 Appointments:\n")
                for appt in appointments:
                    self.search_result.insert(tk.END, f"   • {appt[0]} at {appt[1]}\n")
            else:
                self.search_result.insert(tk.END, f"\n📅 Appointments:    None scheduled\n")
            
            # Get treatment history
            treatments = self.patient_treatments.get_history(pid)
            if treatments:
                self.search_result.insert(tk.END, f"\n💊 Recent Treatments (Last 3):\n")
                for t in treatments[-3:]:
                    self.search_result.insert(tk.END, f"   • {t['date'][:10]}: {t['treatment'][:50]}\n")
            
            self.update_status(f"Found patient: {patient.name}")
        else:
            self.search_result.insert(tk.END, f"❌ Patient {pid} not found in database.\n\n")
            self.search_result.insert(tk.END, "Please check the Patient ID or register the patient first.")
            self.update_status(f"Patient {pid} not found")
    
    def load_sample_data(self):
        """Load sample data for demonstration and save to database"""
        sample_patients = [
            ("KGH001", "John Mwangi", "45", "0712345678", "O+", "None"),
            ("KGH002", "Mary Wanjiku", "30", "0723456789", "A+", "Penicillin"),
            ("KGH003", "Peter Otieno", "60", "0734567890", "B+", "None"),
            ("KGH004", "Grace Akinyi", "25", "0745678901", "AB+", "Sulfa")
        ]
        
        for pid, name, age, contact, blood, allergies in sample_patients:
            patient = PatientRecord(pid, name, age, contact, blood, allergies)
            self.patient_db.insert(patient)
            self.db.save_patient(patient)
        
        # Update last patient number
        self.last_patient_number = 4
        self.db.update_last_patient_number(self.last_patient_number)
        self.update_patient_list_display()
        self.update_patient_id_display()
        self.update_status("Sample data loaded and saved to database")
    
    def show_about(self):
        """Show about dialog"""
        SilentMessageBox.show_info("About Kerugoya Hospital System", 
            "🏥 KERUGOYA HOSPITAL MANAGEMENT SYSTEM\n\nVersion 4.0 (SQLite Database Edition)\n\nDeveloped for CAT 2 Take Away\nMachine Learning Course\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n📊 DATA STRUCTURES IMPLEMENTED:\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n✓ Hash Table     → Patient Records (O(1) lookup)\n✓ Priority Queue → Triage System (Emergency first)\n✓ Array          → Appointment Calendar (7x10 grid)\n✓ Stack          → Treatment History (Undo/Redo)\n✓ Graph          → Department Routing (Shortest path)\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n🗄️ DATABASE FEATURES:\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n• SQLite Database (kerugoya_hospital.db)\n• Auto-save on close\n• Data persists after PC restart\n• Multi-user ready\n• Backup capability\n\n✨ OTHER FEATURES:\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n• Auto-increment Patient IDs (KGH001, KGH002...)\n• Contact number validation (10 digits)\n• Blood group dropdown selection\n• Separate Patient Directory tab\n• Silent message boxes (no Windows sound)", self.root)


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalApp(root)
    root.mainloop()