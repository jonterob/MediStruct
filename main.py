# MEDISTRUCT
# WITH AUTO-INCREMENT ID, VALIDATION, IMPROVED UI, SILENT MESSAGE BOXES AND SQLITE DATABASE

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
from datetime import datetime
import os
import json
import re
import sys
import tempfile
import zipfile
from xml.sax.saxutils import escape

try:
    from PIL import Image, ImageDraw, ImageTk, ImageOps
except ImportError:
    Image = ImageDraw = ImageTk = ImageOps = None

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
from auth import verify_password, USER_ROLES

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

THEMES = {
    'light': {
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
    },
    'dark': {
        'primary': '#1f3a5a',
        'primary_light': '#346189',
        'secondary': '#1abc9c',
        'secondary_dark': '#16a085',
        'danger': '#e74c3c',
        'danger_dark': '#c0392b',
        'warning': '#d35400',
        'info': '#3498db',
        'info_dark': '#2980b9',
        'light_bg': '#1f2833',
        'white': '#2c3e50',
        'gray': '#7f8c8d',
        'gray_dark': '#95a5a6',
        'text': '#ecf0f1',
        'border': '#34495e'
    }
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
        self.root.title("MediStruct")
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.header_logo_image = None
        
        # Make window responsive
        self.root.configure(bg=COLORS['light_bg'])
        self.configure_app_icon()
        
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
        self.db = HospitalDatabase("medistruct.db")
        self.theme_mode_var = tk.StringVar()
        self.startup_tab_var = tk.StringVar()
        self.auto_backup_var = tk.BooleanVar()
        self.font_size_var = tk.StringVar()
        self.load_system_settings()
        
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
        self.last_doctor_number = self.db.get_last_doctor_number()
        
        # Current user session
        self.current_patient_id = None
        self.current_user = None
        self.login_frame = None
        self.user_listbox = None

        # Bind close event to auto-save to database
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Show login screen inside the main window before loading the full UI
        self.show_login_screen()
        
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
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
                patient.mark_clean()  # Data from DB is clean
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
            self.update_status("Database load failed")

    def load_system_settings(self):
        """Load system settings such as theme and startup preferences from database."""
        try:
            active_theme = self.db.get_system_setting('theme') or 'light'
            self.theme_mode_var.set(active_theme)
            self.set_theme(active_theme)

            startup_tab = self.db.get_system_setting('startup_tab') or 'Patient Registration'
            self.startup_tab_var.set(startup_tab)

            auto_backup = self.db.get_system_setting('auto_backup_on_exit') or 'false'
            self.auto_backup_var.set(str(auto_backup).lower() == 'true')

            font_size = self.db.get_system_setting('font_size') or '10'
            self.font_size_var.set(font_size)
            self.apply_font_size(font_size)
        except Exception as e:
            print(f"Error loading system settings: {e}")
            self.set_theme('light')
            self.startup_tab_var.set('Patient Registration')
            self.auto_backup_var.set(False)
            self.font_size_var.set('10')
            self.apply_font_size('10')

    def set_theme(self, theme_name):
        """Apply a theme palette to the whole application."""
        theme_data = THEMES.get(theme_name, THEMES['light'])
        for key, value in theme_data.items():
            COLORS[key] = value
        self.active_theme = theme_name
        self.theme_mode_var.set(theme_name)
        self.configure_style()
        if hasattr(self, 'root'):
            try:
                self.root.configure(bg=COLORS['light_bg'])
            except Exception:
                pass
        if hasattr(self, 'notebook'):
            self.apply_theme_to_widget(self.root)

    def configure_style(self):
        """Configure ttk style for theme-aware elements."""
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Custom.TNotebook', background=COLORS['light_bg'])
        style.configure('Custom.TNotebook.Tab', background=COLORS['white'], foreground=COLORS['text'], padding=[8, 4], font=('Segoe UI', 9, 'bold'))
        style.map('Custom.TNotebook.Tab', background=[('selected', COLORS['primary']), ('active', COLORS['primary_light'])], foreground=[('selected','white'), ('active','white')])
        style.configure('TCombobox', fieldbackground=COLORS['white'], background=COLORS['white'], foreground=COLORS['text'])
        style.configure('TMenubutton', background=COLORS['white'], foreground=COLORS['text'])

    def change_theme(self):
        """Change the current theme and persist the selection."""
        selected_theme = self.theme_mode_var.get()
        if not selected_theme:
            return
        self.set_theme(selected_theme)
        self.db.update_system_setting('theme', selected_theme)
        if hasattr(self, 'current_theme_label'):
            self.current_theme_label.config(text=f"Active theme: {selected_theme.title()}")
        self.refresh_settings_summary()
        self.update_status(f"Theme set to {selected_theme.title()}")

    def change_startup_tab(self):
        selected_tab = self.startup_tab_var.get()
        self.db.update_system_setting('startup_tab', selected_tab)
        self.refresh_settings_summary()
        self.update_status(f"Startup tab set to {selected_tab}")

    def change_auto_backup(self):
        enabled = self.auto_backup_var.get()
        self.db.update_system_setting('auto_backup_on_exit', str(enabled).lower())
        self.update_status(f"Auto backup on exit {'enabled' if enabled else 'disabled'}")

    def change_font_size(self):
        selected_size = self.font_size_var.get()
        self.db.update_system_setting('font_size', selected_size)
        self.apply_font_size(selected_size)
        self.refresh_settings_summary()
        self.update_status(f"Font size set to {selected_size}")

    def apply_font_size(self, size):
        try:
            font_size = int(size)
        except ValueError:
            font_size = 10
        self.root.option_add('*Font', ('Segoe UI', font_size))
        if hasattr(self, 'root'):
            self.apply_theme_to_widget(self.root)

    def refresh_settings_summary(self):
        if hasattr(self, 'current_settings_label'):
            self.current_settings_label.config(
                text=f"Theme: {self.active_theme.title()} · Font: {self.font_size_var.get()} · Startup: {self.startup_tab_var.get()}"
            )

    def create_user_account(self):
        """Create a new staff user account from admin settings."""
        username = self.new_user_username_var.get().strip()
        password = self.new_user_password_var.get().strip()
        role = self.new_user_role_var.get().strip()

        if not username or not password or not role:
            SilentMessageBox.show_error("User Creation Failed", "Please enter a username, password, and role.", self.root)
            return

        created = self.db.create_user(username, password, role)
        if created:
            self.refresh_user_list()
            self.new_user_username_var.set("")
            self.new_user_password_var.set("")
            self.new_user_role_var.set('Receptionist')
            SilentMessageBox.show_info("User Created", f"User '{username}' has been created.", self.root)
        else:
            SilentMessageBox.show_error("User Creation Failed", "Could not create user. The username may already exist.", self.root)

    def refresh_user_list(self):
        if not hasattr(self, 'user_listbox'):
            return
        users = self.db.get_all_users()
        self.user_listbox.config(state='normal')
        self.user_listbox.delete('1.0', tk.END)
        if users:
            for user in users:
                status = 'Active' if user['active'] else 'Inactive'
                self.user_listbox.insert(tk.END, f"{user['username']} — {user['role']} — {status}\n")
        else:
            self.user_listbox.insert(tk.END, "No user accounts found.\n")
        self.user_listbox.config(state='disabled')

    def apply_startup_tab(self):
        if not hasattr(self, 'notebook'):
            return
        name = self.startup_tab_var.get() or 'Patient Registration'
        tab_mapping = {
            'Patient Registration': self.registration_tab,
            'Edit Patients': self.edit_patient_tab,
            'Patient Directory': self.patient_list_tab,
            'Doctors': self.doctor_tab,
            'Triage Queue': self.triage_tab,
            'Appointments': self.appointment_tab,
            'Treatment History': self.treatment_tab,
            'Billing': self.billing_tab,
            'Hospital Operations': self.hospital_tab,
            'Lab Orders': self.lab_orders_tab,
            'Pharmacy Inventory': self.inventory_tab,
            'Insurance Claims': self.insurance_tab,
            'Patient Documents': self.documents_tab,
            'Department Routing': self.routing_tab,
            'Search Patient': self.search_tab,
            'Settings': self.settings_tab,
        }
        self.notebook.select(tab_mapping.get(name, self.registration_tab))

    def apply_role_permissions(self):
        """Show or hide notebook tabs based on the user's role."""
        if not self.current_user or not hasattr(self, 'notebook'):
            return

        role = self.current_user.get('role', 'Receptionist')
        allowed_tabs = {
            'Admin': ['registration_tab', 'edit_patient_tab', 'patient_list_tab', 'doctor_tab', 'triage_tab', 'appointment_tab', 'treatment_tab', 'billing_tab', 'hospital_tab', 'lab_orders_tab', 'inventory_tab', 'insurance_tab', 'documents_tab', 'routing_tab', 'search_tab', 'settings_tab'],
            'Doctor': ['patient_list_tab', 'doctor_tab', 'triage_tab', 'appointment_tab', 'treatment_tab', 'hospital_tab', 'lab_orders_tab', 'documents_tab', 'search_tab', 'settings_tab'],
            'Nurse': ['patient_list_tab', 'triage_tab', 'appointment_tab', 'hospital_tab', 'lab_orders_tab', 'inventory_tab', 'documents_tab', 'search_tab', 'settings_tab'],
            'Receptionist': ['registration_tab', 'patient_list_tab', 'appointment_tab', 'hospital_tab', 'insurance_tab', 'documents_tab', 'search_tab', 'settings_tab'],
            'Billing': ['patient_list_tab', 'billing_tab', 'hospital_tab', 'insurance_tab', 'documents_tab', 'search_tab', 'settings_tab']
        }.get(role, ['registration_tab', 'patient_list_tab', 'search_tab', 'settings_tab'])

        tabs = {
            'registration_tab': self.registration_tab,
            'edit_patient_tab': self.edit_patient_tab,
            'patient_list_tab': self.patient_list_tab,
            'doctor_tab': self.doctor_tab,
            'triage_tab': self.triage_tab,
            'appointment_tab': self.appointment_tab,
            'treatment_tab': self.treatment_tab,
            'billing_tab': self.billing_tab,
            'hospital_tab': self.hospital_tab,
            'lab_orders_tab': self.lab_orders_tab,
            'inventory_tab': self.inventory_tab,
            'insurance_tab': self.insurance_tab,
            'documents_tab': self.documents_tab,
            'routing_tab': self.routing_tab,
            'search_tab': self.search_tab,
            'settings_tab': self.settings_tab,
        }

        for key, tab in tabs.items():
            if key not in allowed_tabs:
                try:
                    self.notebook.hide(tab)
                except Exception:
                    pass
            else:
                try:
                    self.notebook.add(tab)
                except Exception:
                    pass

    def apply_theme_to_widget(self, widget):
        """Recursively apply theme colors to supported widgets."""
        light_widgets = {'white', '#ffffff', '#f0f7fc', '#eef6fb', '#f8fbfd', '#f8fbfd'}
        try:
            current_bg = widget.cget('bg')
        except Exception:
            current_bg = None

        try:
            if isinstance(widget, (tk.Frame, tk.LabelFrame, tk.Canvas)):
                if current_bg in light_widgets:
                    widget.config(bg=COLORS['white'])
            elif isinstance(widget, tk.Label):
                if current_bg in light_widgets:
                    widget.config(bg=COLORS['white'], fg=COLORS['text'])
            elif isinstance(widget, tk.Entry):
                widget.config(bg=COLORS['white'], fg=COLORS['text'], insertbackground=COLORS['text'])
            elif isinstance(widget, tk.Text):
                widget.config(bg=COLORS['white'], fg=COLORS['text'], insertbackground=COLORS['text'])
            elif isinstance(widget, tk.Radiobutton):
                widget.config(bg=COLORS['white'], fg=COLORS['text'], selectcolor=COLORS['light_bg'], activebackground=COLORS['white'])
            elif isinstance(widget, tk.Menu):
                widget.config(bg=COLORS['white'], fg=COLORS['text'], activebackground=COLORS['primary_light'])
        except Exception:
            pass

        for child in widget.winfo_children():
            self.apply_theme_to_widget(child)

    def sync_to_database(self):
        """Sync memory data structures to database"""
        try:
            # Only sync patients that have been modified
            dirty_patients = [p for p in self.patient_db.get_all() if p.dirty]
            if dirty_patients:
                if self.db.save_patients_batch(dirty_patients):
                    for p in dirty_patients:
                        p.mark_clean()
            print(f"✅ Synced {len(dirty_patients)} modified patients")
            return True
        except Exception as e:
            SilentMessageBox.show_error("Sync Failed", f"❌ Error syncing to database: {e}", self.root)
            return False
    
    def on_closing(self):
        """Handle application closing - save to database."""
        try:
            if self.auto_backup_var.get():
                self.backup_database()
            # Perform final syncs
            self.sync_to_database()
            self.db.update_last_patient_number(self.last_patient_number)
        except Exception as e:
            print(f"Error during shutdown sync: {e}")
        finally:
            self.db.close()
            self.root.destroy()

    def logout(self):
        """Logout the current user and return to the login screen."""
        if self.current_user:
            username = self.current_user.get('username', 'Unknown')
            role = self.current_user.get('role', 'Unknown')
            self.db.audit_action(username, 'logout', f"Logged out {username} ({role})")
            self.update_status(f"Logging out {username}...")

        self.sync_to_database()
        self.db.update_last_patient_number(self.last_patient_number)
        self.current_user = None

        if hasattr(self, 'datetime_update_job') and self.datetime_update_job:
            self.root.after_cancel(self.datetime_update_job)
            self.datetime_update_job = None
        if hasattr(self, 'status_after_id') and self.status_after_id:
            self.root.after_cancel(self.status_after_id)
            self.status_after_id = None

        self.root.config(menu=None)
        self.root.unbind('<Return>')

        for widget in self.root.winfo_children():
            widget.destroy()

        self.show_login_screen()

    def find_logo_path(self, extensions):
        """Return the first matching logo path from common project locations."""
        search_paths = [
            "logo",
            "hospital_logo",
            os.path.join("assets", "logo"),
            os.path.join("assets", "hospital_logo"),
            os.path.join("images", "logo"),
            os.path.join("images", "hospital_logo"),
        ]

        for base_name in search_paths:
            for extension in extensions:
                candidate = os.path.join(self.base_dir, f"{base_name}.{extension}")
                if os.path.exists(candidate):
                    return candidate
        return None

    def configure_app_icon(self):
        """Apply a custom window icon when an .ico file is available."""
        icon_path = self.find_logo_path(["ico"])
        if not icon_path:
            return

        try:
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Could not load app icon: {e}")

    def load_logo_image(self, max_size):
        """Load and scale a logo image to fit within the requested size."""
        logo_path = self.find_logo_path(["png", "gif"])
        if not logo_path:
            return None

        try:
            image = tk.PhotoImage(file=logo_path)
            width = image.width()
            height = image.height()
            scale = max((width + max_size - 1) // max_size, (height + max_size - 1) // max_size, 1)
            if scale > 1:
                image = image.subsample(scale, scale)
            return image
        except Exception as e:
            print(f"Could not load logo image: {e}")
            return None

    def load_circular_logo(self, logo_path, size):
        """Load a logo image, crop transparent margin, and resize it to fit the target size."""
        if Image is None or ImageTk is None or ImageOps is None:
            return None

        try:
            pil_img = Image.open(logo_path).convert('RGBA')
            bbox = pil_img.getbbox()
            if bbox:
                pil_img = pil_img.crop(bbox)
            pil_img = ImageOps.contain(
                pil_img,
                (size, size),
                method=Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.LANCZOS
            )
            return ImageTk.PhotoImage(pil_img)
        except Exception as e:
            print(f"Could not load circular logo image: {e}")
            return None

    def load_header_logo(self):
        """Load the smaller logo used in the header."""
        return self.load_logo_image(48)

    def load_splash_logo(self):
        """Load a larger logo for the startup splash screen."""
        return self.load_logo_image(120)

    def create_logo_badge(self, parent, image=None, diameter=72, bg_color=None, circle_color=None, emoji_size=28):
        """Render the logo inside a circular badge for a softer branded look."""
        bg_color = bg_color or parent.cget("bg")
        circle_color = circle_color or COLORS['white']

        badge = tk.Canvas(
            parent,
            width=diameter,
            height=diameter,
            bg=bg_color,
            bd=0,
            highlightthickness=0,
            relief='flat'
        )
        inset = 2
        badge.create_oval(
            inset,
            inset,
            diameter - inset,
            diameter - inset,
            fill=circle_color,
            outline=""
        )

        center = diameter // 2
        if image:
            badge.create_image(center, center, image=image)
            badge.logo_image = image
        else:
            badge.create_text(
                center,
                center,
                text="🏥",
                font=('Segoe UI', emoji_size),
                fill=COLORS['primary']
            )

        return badge

    def show_startup_splash(self):
        """Show a startup splash screen before revealing the main window."""
        splash_logo = self.load_splash_logo()
        if not splash_logo:
            self.root.deiconify()
            return

        splash = tk.Toplevel(self.root)
        splash.overrideredirect(True)
        splash.configure(bg=COLORS['white'])

        splash_width = 500
        splash_height = 320
        screen_width = splash.winfo_screenwidth()
        screen_height = splash.winfo_screenheight()
        x = (screen_width - splash_width) // 2
        y = (screen_height - splash_height) // 2
        splash.geometry(f"{splash_width}x{splash_height}+{x}+{y}")

        container = tk.Frame(splash, bg=COLORS['white'], bd=0, relief='flat', highlightthickness=0)
        container.pack(fill='both', expand=True)

        splash_badge = self.create_logo_badge(
            container,
            image=splash_logo,
            diameter=136,
            bg_color=COLORS['white'],
            circle_color=COLORS['light_bg'],
            emoji_size=42
        )
        splash_badge.pack(pady=(30, 18))
        tk.Label(
            container,
            text="MediStruct",
            font=('Segoe UI', 20, 'bold'),
            bg=COLORS['white'],
            fg=COLORS['primary']
        ).pack()
        tk.Label(
            container,
            text="Hospital System",
            font=('Segoe UI', 11),
            bg=COLORS['white'],
            fg=COLORS['text']
        ).pack(pady=(4, 18))

        loading_label = tk.Label(
            container,
            text="Loading application...",
            font=('Segoe UI', 10),
            bg=COLORS['white'],
            fg=COLORS['gray_dark']
        )
        loading_label.pack(pady=(0, 8))

        stages = [
            "Starting system...",
            "Loading patient records...",
            "Preparing dashboard...",
            "Opening application..."
        ]

        def update_stage(index=0):
            if not splash.winfo_exists():
                return
            loading_label.config(text=stages[index])
            if index + 1 < len(stages):
                splash.after(700, lambda: update_stage(index + 1))

        def close_splash():
            if splash.winfo_exists():
                splash.destroy()
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()

        splash.logo_image = splash_logo
        update_stage()
        splash.after(3200, close_splash)
    
    def initialize_ui(self):
        """Build the main application UI after successful login."""
        self.root.deiconify()
        self.create_header()
        self.create_menu()
        self.create_main_dashboard()
        self.apply_role_permissions()
        self.apply_startup_tab()
        self.create_status_bar()
        self.update_patient_id_display()
        self.update_doctor_id_display()
        self.refresh_settings_summary()

    def show_login_screen(self):
        """Show login prompt inside the main window before the main UI loads."""
        if hasattr(self, 'login_frame') and self.login_frame:
            self.login_frame.destroy()

        self.login_frame = tk.Frame(self.root, bg='#eef5fb')
        self.login_frame.grid(row=0, column=0, sticky='nsew')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.login_frame.grid_rowconfigure(0, weight=1)
        self.login_frame.grid_columnconfigure(0, weight=1)

        center_wrapper = tk.Frame(self.login_frame, bg='#eef5fb')
        center_wrapper.grid(row=0, column=0, sticky='nsew')
        center_wrapper.grid_rowconfigure(0, weight=1)
        center_wrapper.grid_rowconfigure(1, weight=0)
        center_wrapper.grid_rowconfigure(2, weight=1)
        center_wrapper.grid_columnconfigure(0, weight=1)
        center_wrapper.grid_columnconfigure(1, weight=0)
        center_wrapper.grid_columnconfigure(2, weight=1)

        shadow = tk.Frame(center_wrapper, bg='#d4e1ed')
        shadow.grid(row=1, column=1)
        shadow.grid_propagate(False)
        shadow.configure(width=620, height=500)

        card = tk.Frame(center_wrapper, bg=COLORS['white'], bd=0, relief='flat', highlightthickness=1, highlightbackground='#dbe4ed', width=600, height=500)
        card.grid(row=1, column=1)
        card.grid_propagate(False)
        card.grid_rowconfigure(0, weight=1)
        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=1)

        left_panel = tk.Frame(card, bg=COLORS['primary'])
        left_panel.grid(row=0, column=0, sticky='nsew')
        left_panel.grid_propagate(False)

        right_panel = tk.Frame(card, bg=COLORS['white'])
        right_panel.grid(row=0, column=1, sticky='nsew')
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        logo_circle = tk.Canvas(left_panel, width=100, height=100, bg=COLORS['primary'], highlightthickness=0)
        logo_circle.create_oval(6, 6, 94, 94, fill=COLORS['white'], outline='')

        self.login_logo_image = None
        logo_path = os.path.join(self.base_dir, 'logo.png')
        if os.path.exists(logo_path):
            try:
                self.login_logo_image = self.load_circular_logo(logo_path, 70)
                if self.login_logo_image is None:
                    self.login_logo_image = tk.PhotoImage(file=logo_path)
                logo_circle.create_image(50, 50, image=self.login_logo_image)
            except Exception:
                logo_circle.create_text(50, 50, text='🏥', font=('Segoe UI', 32), fill=COLORS['primary'])
        else:
            logo_circle.create_text(50, 50, text='🏥', font=('Segoe UI', 32), fill=COLORS['primary'])

        logo_circle.pack(pady=(48, 16))

        tk.Label(left_panel, text='MediStruct', font=('Segoe UI', 16, 'bold'), bg=COLORS['primary'], fg='white', wraplength=220, justify='center').pack(padx=24, pady=(0, 8))
        tk.Label(left_panel, text='Secure system access for medical staff and hospital administrators.', font=('Segoe UI', 10), bg=COLORS['primary'], fg='#eaf4fb', wraplength=220, justify='center').pack(padx=20)

        left_features = tk.Frame(left_panel, bg=COLORS['primary'])
        left_features.pack(padx=20, pady=(20, 0), fill='x')
        for text in ['Fast access', 'Role-based login', 'Encrypted credentials']:
            feature = tk.Frame(left_features, bg=COLORS['primary'])
            feature.pack(fill='x', pady=4)
            tk.Label(feature, text='•', font=('Segoe UI', 10, 'bold'), bg=COLORS['primary'], fg='#eaf4fb').pack(side='left')
            tk.Label(feature, text=text, font=('Segoe UI', 10), bg=COLORS['primary'], fg='#eaf4fb').pack(side='left', padx=(6, 0))

        form_container = tk.Frame(right_panel, bg=COLORS['white'])
        form_container.pack(fill='both', expand=True, padx=36, pady=40)
        form_container.grid_columnconfigure(0, weight=1)

        tk.Label(form_container, text='Welcome Back', font=('Segoe UI', 22, 'bold'), bg=COLORS['white'], fg=COLORS['text']).grid(row=0, column=0, sticky='w')
        tk.Label(form_container, text='Sign in to continue to the hospital dashboard.', font=('Segoe UI', 10), bg=COLORS['white'], fg=COLORS['gray_dark']).grid(row=1, column=0, sticky='w', pady=(4, 20))

        tk.Label(form_container, text='Username', bg=COLORS['white'], fg=COLORS['text'], anchor='w', font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky='w', pady=(0, 6))
        self.login_username_var = tk.StringVar()
        username_entry = tk.Entry(form_container, textvariable=self.login_username_var, font=('Segoe UI', 10), bd=0, relief='solid', highlightthickness=1, highlightbackground=COLORS['border'], highlightcolor=COLORS['primary'], insertbackground=COLORS['text'])
        username_entry.grid(row=3, column=0, sticky='ew', pady=(0, 14), ipady=10)

        tk.Label(form_container, text='Password', bg=COLORS['white'], fg=COLORS['text'], anchor='w', font=('Segoe UI', 10, 'bold')).grid(row=4, column=0, sticky='w', pady=(0, 6))
        self.login_password_var = tk.StringVar()
        password_entry = tk.Entry(form_container, textvariable=self.login_password_var, font=('Segoe UI', 10), bd=0, relief='solid', highlightthickness=1, highlightbackground=COLORS['border'], highlightcolor=COLORS['primary'], show='*', insertbackground=COLORS['text'])
        password_entry.grid(row=5, column=0, sticky='ew', pady=(0, 24), ipady=10)

        button_frame = tk.Frame(form_container, bg=COLORS['white'])
        button_frame.grid(row=6, column=0, sticky='ew')
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        tk.Button(button_frame, text='Login', command=self.authenticate_user, bg=COLORS['primary'], fg='white', font=('Segoe UI', 10, 'bold'), bd=0, padx=20, pady=14, cursor='hand2', activebackground=COLORS['primary_light']).grid(row=0, column=0, sticky='ew')
        tk.Button(button_frame, text='Exit', command=self.root.destroy, bg=COLORS['gray'], fg='white', font=('Segoe UI', 10, 'bold'), bd=0, padx=20, pady=14, cursor='hand2', activebackground=COLORS['gray_dark']).grid(row=0, column=1, sticky='ew', padx=(14, 0))

        footer = tk.Label(form_container, text='Admin and staff accounts only.', font=('Segoe UI', 8), bg=COLORS['white'], fg=COLORS['gray_dark'])
        footer.grid(row=7, column=0, sticky='w', pady=(22, 0))

        self.root.bind('<Return>', lambda event: self.authenticate_user())
        username_entry.focus()

    def authenticate_user(self):
        """Verify login credentials and initialize the app on success."""
        username = self.login_username_var.get().strip()
        password = self.login_password_var.get().strip()
        if not username or not password:
            SilentMessageBox.show_error("Login Failed", "Please enter a username and password.", self.root)
            return

        user = self.db.get_user_by_username(username)
        if not user:
            SilentMessageBox.show_error("Login Failed", "Invalid username or password.", self.root)
            return

        if not user['active']:
            SilentMessageBox.show_error("Login Failed", "This account is deactivated.", self.root)
            return

        if not verify_password(password, user['password_hash']):
            SilentMessageBox.show_error("Login Failed", "Invalid username or password.", self.root)
            return

        self.current_user = user
        self.db.audit_action(username, 'login', f"Logged in as {username} ({user['role']})")
        if hasattr(self, 'login_frame') and self.login_frame:
            self.login_frame.destroy()
            self.login_frame = None
        self.root.unbind('<Return>')
        self.initialize_ui()

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

        self.header_logo_image = self.load_header_logo()
        if self.header_logo_image:
            logo_badge = self.create_logo_badge(
                title_frame,
                image=self.header_logo_image,
                diameter=54,
                bg_color=COLORS['primary'],
                circle_color=COLORS['white'],
                emoji_size=22
            )
            logo_badge.pack(side='left', padx=(0, 12))
        else:
            logo_badge = self.create_logo_badge(
                title_frame,
                diameter=54,
                bg_color=COLORS['primary'],
                circle_color=COLORS['white'],
                emoji_size=22
            )
            logo_badge.pack(side='left', padx=(0, 12))
        
        text_frame = tk.Frame(title_frame, bg=COLORS['primary'])
        text_frame.pack(side='left')
        
        tk.Label(text_frame, text="MediStruct", font=('Segoe UI', 18, 'bold'),
                bg=COLORS['primary'], fg='white').pack(anchor='w')
        tk.Label(text_frame, text="Hospital System", font=('Segoe UI', 10),
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
        if not hasattr(self, 'date_label') or not self.date_label.winfo_exists():
            return

        now = datetime.now()
        self.date_label.config(text=now.strftime("%A, %B %d, %Y"))
        self.time_label.config(text=now.strftime("%I:%M:%S %p"))
        self.datetime_update_job = self.root.after(1000, self.update_datetime)

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
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Export to CSV", command=self.export_to_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0, bg='white', fg=COLORS['text'])
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Database Statistics", command=self.show_db_stats)
        view_menu.add_command(label="Refresh All", command=self.refresh_all_displays)
        view_menu.add_command(label="Open Settings", command=lambda: self.notebook.select(self.settings_tab))
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0, bg='white', fg=COLORS['text'])
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_radiobutton(label="Light Theme", variable=self.theme_mode_var, value='light', command=self.change_theme)
        settings_menu.add_radiobutton(label="Dark Theme", variable=self.theme_mode_var, value='dark', command=self.change_theme)
        settings_menu.add_checkbutton(label="Auto Backup on Exit", variable=self.auto_backup_var, command=self.change_auto_backup)
        settings_menu.add_separator()
        settings_menu.add_command(label="Open Settings", command=lambda: self.notebook.select(self.settings_tab))
        
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
        
        self.status_label = tk.Label(status_frame, text="Connected to secure storage", font=('Segoe UI', 9),
                                     bg=COLORS['gray'], fg='white')
        self.status_label.pack(side='left', padx=10)
        
        # Database indicator
        self.db_indicator = tk.Label(status_frame, text="● Storage Active", font=('Segoe UI', 9),
                                       bg=COLORS['gray'], fg=COLORS['secondary'])
        self.db_indicator.pack(side='right', padx=10)
    
    def update_status(self, message):
        """Update status bar message"""
        if not hasattr(self, 'status_label') or self.status_label is None:
            return
        self.status_label.config(text=message)
        self.status_after_id = self.root.after(3000, self._reset_status_ready)

    def _reset_status_ready(self):
        if hasattr(self, 'status_label') and self.status_label is not None and self.status_label.winfo_exists():
            self.status_label.config(text="Ready")

    def backup_database(self):
        """Create database backup"""
        backup_file = self.db.backup_database()
        SilentMessageBox.show_info("Backup Created", f"✅ Database backed up to:\n{backup_file}", self.root)
        self.update_status(f"Database backed up to {backup_file}")
    
    def show_db_stats(self):
        """Show database statistics"""
        stats = self.db.get_statistics()
        
        stats_text = f"📊 HOSPITAL DATABASE STATISTICS\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n👥 Total Patients:      {stats.get('total_patients', 0)}\n\n📅 Today's Appointments: {stats.get('today_appointments', 0)}\n\n🚑 Waiting in Triage:    {stats.get('waiting_triage', 0)}\n🔴 Emergency Waiting:    {stats.get('emergency_waiting', 0)}\n\n💾 Database File:        medistruct.db"
        
        SilentMessageBox.show_info("Database Statistics", stats_text, self.root)
    
    def show_db_info(self):
        """Show database information"""
        info_text = "📁 DATABASE INFORMATION\n\nDatabase File: medistruct.db\nType: SQLite (Serverless)\n\nTables Created:\n✓ patients\n✓ triage_queue\n✓ appointments\n✓ treatments\n✓ doctors\n✓ bills\n✓ system_settings\n✓ hospitals\n✓ wards\n✓ beds\n✓ admissions\n✓ lab_orders\n✓ medication_inventory\n✓ insurance_claims\n✓ documents\n\nFeatures:\n✓ Auto-save on close\n✓ Data persists after PC restart\n✓ Multi-user ready\n✓ Backup capability\n✓ Ward/bed/admission management\n✓ Hospital operations support"
        
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
        style.configure('Custom.TNotebook.Tab', padding=[8, 4], font=('Segoe UI', 9, 'bold'))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # Create all tabs
        self.create_registration_tab()
        self.create_edit_patient_tab()
        self.create_patient_list_tab()
        self.create_doctor_tab()
        self.create_triage_tab()
        self.create_appointment_tab()
        self.create_treatment_tab()
        self.create_billing_tab()
        self.create_hospital_operations_tab()
        self.create_lab_orders_tab()
        self.create_inventory_tab()
        self.create_insurance_tab()
        self.create_documents_tab()
        self.create_routing_tab()
        self.create_search_tab()
        self.create_settings_tab()
    
    def create_registration_tab(self):
        """Patient registration form - CENTERED and IMPROVED"""
        self.registration_tab = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.registration_tab, text="📋 Patient Registration")

        center_frame = tk.Frame(self.registration_tab, bg=COLORS['light_bg'])
        center_frame.pack(fill='both', expand=True)

        content_frame = tk.Frame(center_frame, bg='#eef6fb', relief='flat', bd=1, width=760)
        content_frame.pack(padx=20, pady=20, anchor='n')

        banner = tk.Frame(content_frame, bg=COLORS['primary'], height=84)
        banner.pack(fill='x')
        banner.pack_propagate(False)
        tk.Label(banner, text="📝", font=('Segoe UI', 24), bg=COLORS['primary'], fg='white').pack(side='left', padx=(18, 10), pady=14)
        banner_text = tk.Frame(banner, bg=COLORS['primary'])
        banner_text.pack(side='left', pady=14)
        tk.Label(banner_text, text="NEW PATIENT REGISTRATION", font=('Segoe UI', 16, 'bold'),
                 bg=COLORS['primary'], fg='white').pack(anchor='w')
        tk.Label(banner_text, text="Capture demographic details before clinical workflows",
                 font=('Segoe UI', 9), bg=COLORS['primary'], fg=COLORS['light_bg']).pack(anchor='w', pady=(2, 0))

        form_card = tk.Frame(content_frame, bg='white', relief='flat', bd=0)
        form_card.pack(padx=14, pady=14, fill='both', expand=True)

        form_frame = tk.Frame(form_card, bg='white')
        form_frame.pack(padx=24, pady=18, fill='x')
        
        # Configure grid columns for alignment
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=2)
        
        # Patient ID (Auto-generated - display only)
        tk.Label(form_frame, text="🆔 Patient ID", font=('Segoe UI', 10, 'bold'), bg='white', 
                fg=COLORS['primary']).grid(row=0, column=0, sticky='w', padx=8, pady=8)
        self.pid_display_label = tk.Label(form_frame, text="", font=('Segoe UI', 12, 'bold'), 
                                         bg='#f8fbfd', fg=COLORS['info'], width=25, anchor='w', 
                                         relief='solid', bd=1, padx=5)
        self.pid_display_label.grid(row=0, column=1, padx=8, pady=8, sticky='ew')
        
        # Full Name
        tk.Label(form_frame, text="👤 Full Name", font=('Segoe UI', 10, 'bold'), bg='white', 
                fg=COLORS['primary']).grid(row=1, column=0, sticky='w', padx=8, pady=8)
        self.name_entry = tk.Entry(form_frame, width=35, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.name_entry.grid(row=1, column=1, padx=8, pady=8, sticky='ew')
        
        # Age
        tk.Label(form_frame, text="📅 Age", font=('Segoe UI', 10, 'bold'), bg='white', 
                fg=COLORS['primary']).grid(row=2, column=0, sticky='w', padx=8, pady=8)
        self.age_entry = tk.Entry(form_frame, width=35, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.age_entry.grid(row=2, column=1, padx=8, pady=8, sticky='ew')
        
        # Contact (10 digits with validation)
        tk.Label(form_frame, text="📞 Contact (10 digits)", font=('Segoe UI', 10, 'bold'), bg='white', 
                fg=COLORS['primary']).grid(row=3, column=0, sticky='w', padx=8, pady=8)
        self.contact_entry = tk.Entry(form_frame, width=35, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.contact_entry.grid(row=3, column=1, padx=8, pady=8, sticky='ew')
        
        # Add contact validation to limit to 10 digits
        self.contact_entry.bind('<KeyRelease>', self.validate_contact_length)
        
        # Blood Group
        tk.Label(form_frame, text="🩸 Blood Group", font=('Segoe UI', 10, 'bold'), bg='white', 
                fg=COLORS['primary']).grid(row=4, column=0, sticky='w', padx=8, pady=8)
        self.blood_group_var = tk.StringVar()
        blood_groups = ["Select Blood Group", "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
        self.blood_group_combo = ttk.Combobox(form_frame, textvariable=self.blood_group_var, 
                                              values=blood_groups, width=32, font=('Segoe UI', 11))
        self.blood_group_combo.grid(row=4, column=1, padx=8, pady=8, sticky='ew')
        self.blood_group_combo.set("Select Blood Group")
        
        # Allergies
        tk.Label(form_frame, text="⚠️ Allergies", font=('Segoe UI', 10, 'bold'), bg='white', 
                fg=COLORS['primary']).grid(row=5, column=0, sticky='w', padx=8, pady=8)
        self.allergies_entry = tk.Entry(form_frame, width=35, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.allergies_entry.grid(row=5, column=1, padx=8, pady=8, sticky='ew')
        
        # Required fields note
        note_frame = tk.Frame(form_frame, bg='white')
        note_frame.grid(row=6, column=0, columnspan=2, pady=10)
        tk.Label(note_frame, text="* Required fields", font=('Segoe UI', 9), 
                bg='white', fg=COLORS['danger']).pack()
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg='white')
        button_frame.grid(row=7, column=0, columnspan=2, pady=16)
        
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

    def create_edit_patient_tab(self):
        """Edit existing patient records"""
        self.edit_patient_tab = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.edit_patient_tab, text="✏️ Edit Patients")

        left_frame = tk.Frame(self.edit_patient_tab, bg=COLORS['light_bg'])
        left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        right_frame = tk.Frame(self.edit_patient_tab, bg=COLORS['light_bg'])
        right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        edit_card = tk.Frame(left_frame, bg='#eef6fb', relief='flat', bd=1)
        edit_card.pack(fill='both', expand=True, padx=10, pady=10)

        banner = tk.Frame(edit_card, bg=COLORS['primary'], height=88)
        banner.pack(fill='x')
        banner.pack_propagate(False)
        tk.Label(banner, text="✏️", font=('Segoe UI', 26), bg=COLORS['primary'], fg='white').pack(side='left', padx=(18, 10), pady=18)
        banner_text = tk.Frame(banner, bg=COLORS['primary'])
        banner_text.pack(side='left', pady=16)
        tk.Label(banner_text, text="EDIT PATIENT RECORD", font=('Segoe UI', 16, 'bold'),
                 bg=COLORS['primary'], fg='white').pack(anchor='w')
        tk.Label(banner_text, text="Load a patient, update details, and save changes back to the register",
                 font=('Segoe UI', 10), bg=COLORS['primary'], fg=COLORS['light_bg']).pack(anchor='w', pady=(3, 0))

        form_card = tk.Frame(edit_card, bg='white', relief='flat', bd=0)
        form_card.pack(fill='both', expand=True, padx=16, pady=16)
        form_frame = tk.Frame(form_card, bg='white')
        form_frame.pack(fill='x', padx=18, pady=18)
        form_frame.grid_columnconfigure(1, weight=1)

        tk.Label(form_frame, text="🆔 Patient ID", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, padx=8, pady=8, sticky='w')
        self.edit_patient_id_var = tk.StringVar()
        self.edit_pid_combo = ttk.Combobox(
            form_frame,
            textvariable=self.edit_patient_id_var,
            width=22,
            font=('Segoe UI', 11),
            state='normal',
            postcommand=self.update_edit_patient_dropdown
        )
        self.edit_pid_combo.grid(row=0, column=1, padx=8, pady=8, sticky='ew')
        ModernButton(form_frame, text="Load", command=self.load_patient_for_edit, color='info').grid(row=0, column=2, padx=8, pady=8)

        search_row = tk.Frame(form_frame, bg='white')
        search_row.grid(row=1, column=0, columnspan=3, sticky='ew', padx=8, pady=(0, 8))
        tk.Label(search_row, text="🔎 Search patient", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11)).pack(side='left')
        self.edit_patient_search_entry = tk.Entry(search_row, font=('Segoe UI', 10), relief='solid', bd=1, bg='#f8fbfd')
        self.edit_patient_search_entry.pack(side='left', fill='x', expand=True, padx=8)
        ModernButton(search_row, text="Search", command=self.search_edit_patients, color='info').pack(side='left')

        tk.Label(form_frame, text="👤 Full Name", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=2, column=0, padx=8, pady=8, sticky='w')
        self.edit_name_entry = tk.Entry(form_frame, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.edit_name_entry.grid(row=2, column=1, columnspan=2, padx=8, pady=8, sticky='ew')

        tk.Label(form_frame, text="📅 Age", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=3, column=0, padx=8, pady=8, sticky='w')
        self.edit_age_entry = tk.Entry(form_frame, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.edit_age_entry.grid(row=3, column=1, columnspan=2, padx=8, pady=8, sticky='ew')

        tk.Label(form_frame, text="📞 Contact", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=4, column=0, padx=8, pady=8, sticky='w')
        self.edit_contact_entry = tk.Entry(form_frame, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.edit_contact_entry.grid(row=4, column=1, columnspan=2, padx=8, pady=8, sticky='ew')

        tk.Label(form_frame, text="🩸 Blood Group", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=5, column=0, padx=8, pady=8, sticky='w')
        self.edit_blood_group_var = tk.StringVar()
        self.edit_blood_group_combo = ttk.Combobox(form_frame, textvariable=self.edit_blood_group_var,
                                                   values=["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"],
                                                   font=('Segoe UI', 11), width=20)
        self.edit_blood_group_combo.grid(row=4, column=1, columnspan=2, padx=8, pady=8, sticky='ew')

        tk.Label(form_frame, text="⚠️ Allergies", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=6, column=0, padx=8, pady=8, sticky='w')
        self.edit_allergies_entry = tk.Entry(form_frame, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.edit_allergies_entry.grid(row=6, column=1, columnspan=2, padx=8, pady=8, sticky='ew')

        button_frame = tk.Frame(edit_card, bg='#eef6fb')
        button_frame.pack(pady=(0, 18))
        ModernButton(button_frame, text="💾 Save Changes", command=self.save_patient_changes, color='secondary').pack(side='left', padx=6)
        ModernButton(button_frame, text="🧹 Clear", command=self.clear_edit_patient_form, color='gray').pack(side='left', padx=6)

        list_card = tk.Frame(right_frame, bg='#eef6fb', relief='flat', bd=1)
        list_card.pack(fill='both', expand=True, padx=10, pady=10)
        tk.Label(list_card, text="PATIENTS READY TO EDIT", font=('Segoe UI', 16, 'bold'),
                 bg='#eef6fb', fg=COLORS['primary']).pack(pady=14)
        table_card = tk.Frame(list_card, bg='white')
        table_card.pack(padx=16, pady=(0, 16), fill='both', expand=True)

        self.configure_edit_patient_table_style()
        columns = ("patient_id", "name", "contact", "blood_group")
        self.edit_patient_display = ttk.Treeview(
            table_card,
            columns=columns,
            show='headings',
            style='EditPatient.Treeview'
        )
        self.edit_patient_display.heading("patient_id", text="Patient ID")
        self.edit_patient_display.heading("name", text="Full Name")
        self.edit_patient_display.heading("contact", text="Contact")
        self.edit_patient_display.heading("blood_group", text="Blood Group")

        self.edit_patient_display.column("patient_id", width=95, minwidth=85, anchor='center')
        self.edit_patient_display.column("name", width=170, minwidth=140, anchor='w')
        self.edit_patient_display.column("contact", width=120, minwidth=100, anchor='center')
        self.edit_patient_display.column("blood_group", width=90, minwidth=80, anchor='center')

        y_scroll = ttk.Scrollbar(table_card, orient='vertical', command=self.edit_patient_display.yview)
        x_scroll = ttk.Scrollbar(table_card, orient='horizontal', command=self.edit_patient_display.xview)
        self.edit_patient_display.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(0, weight=1)
        self.edit_patient_display.grid(row=0, column=0, sticky='nsew')
        y_scroll.grid(row=0, column=1, sticky='ns')
        x_scroll.grid(row=1, column=0, sticky='ew')
        self.update_edit_patient_list()

    def create_doctor_tab(self):
        """Doctor management"""
        self.doctor_tab = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.doctor_tab, text="👨‍⚕️ Doctors")

        left_frame = tk.Frame(self.doctor_tab, bg=COLORS['light_bg'])
        left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        right_frame = tk.Frame(self.doctor_tab, bg=COLORS['light_bg'])
        right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        form_card = tk.Frame(left_frame, bg='#eef6fb', relief='flat', bd=1)
        form_card.pack(fill='both', expand=True, padx=10, pady=10)
        banner = tk.Frame(form_card, bg=COLORS['secondary_dark'], height=88)
        banner.pack(fill='x')
        banner.pack_propagate(False)
        tk.Label(banner, text="👨‍⚕️", font=('Segoe UI', 24), bg=COLORS['secondary_dark'], fg='white').pack(side='left', padx=(18, 10), pady=18)
        banner_text = tk.Frame(banner, bg=COLORS['secondary_dark'])
        banner_text.pack(side='left', pady=16)
        tk.Label(banner_text, text="DOCTOR MANAGEMENT", font=('Segoe UI', 16, 'bold'),
                 bg=COLORS['secondary_dark'], fg='white').pack(anchor='w')
        tk.Label(banner_text, text="Maintain doctors, specialties, contacts, and availability in one place",
                 font=('Segoe UI', 10), bg=COLORS['secondary_dark'], fg='#dff5e8').pack(anchor='w', pady=(3, 0))

        inner = tk.Frame(form_card, bg='white')
        inner.pack(fill='both', expand=True, padx=16, pady=16)
        form = tk.Frame(inner, bg='white')
        form.pack(fill='x', padx=18, pady=18)
        form.grid_columnconfigure(1, weight=1)

        tk.Label(form, text="🆔 Doctor ID", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, padx=8, pady=8, sticky='w')
        self.doctor_id_entry = tk.Entry(form, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.doctor_id_entry.grid(row=0, column=1, padx=8, pady=8, sticky='ew')
        self.doctor_id_entry.configure(state='readonly')
        tk.Label(form, text="👤 Name", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=1, column=0, padx=8, pady=8, sticky='w')
        self.doctor_name_entry = tk.Entry(form, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.doctor_name_entry.grid(row=1, column=1, padx=8, pady=8, sticky='ew')
        tk.Label(form, text="🩺 Specialty", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=2, column=0, padx=8, pady=8, sticky='w')
        self.doctor_specialty_entry = tk.Entry(form, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.doctor_specialty_entry.grid(row=2, column=1, padx=8, pady=8, sticky='ew')
        tk.Label(form, text="📞 Contact", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=3, column=0, padx=8, pady=8, sticky='w')
        self.doctor_contact_entry = tk.Entry(form, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.doctor_contact_entry.grid(row=3, column=1, padx=8, pady=8, sticky='ew')
        tk.Label(form, text="🕒 Availability", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=4, column=0, padx=8, pady=8, sticky='w')
        self.doctor_availability_entry = tk.Entry(form, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.doctor_availability_entry.grid(row=4, column=1, padx=8, pady=8, sticky='ew')

        buttons = tk.Frame(form_card, bg='#eef6fb')
        buttons.pack(pady=(0, 18))
        ModernButton(buttons, text="💾 Save Doctor", command=self.save_doctor_record, color='secondary').pack(side='left', padx=6)
        ModernButton(buttons, text="🧹 Clear", command=self.clear_doctor_form, color='gray').pack(side='left', padx=6)

        list_card = tk.Frame(right_frame, bg='#eef6fb', relief='flat', bd=1)
        list_card.pack(fill='both', expand=True, padx=10, pady=10)
        top = tk.Frame(list_card, bg='#eef6fb')
        top.pack(fill='x', padx=16, pady=(16, 10))
        tk.Label(top, text="DOCTOR DIRECTORY", font=('Segoe UI', 16, 'bold'), bg='#eef6fb', fg=COLORS['primary']).pack(anchor='w')
        search_row = tk.Frame(top, bg='#eef6fb')
        search_row.pack(fill='x', pady=(8, 0))
        self.doctor_search_entry = tk.Entry(search_row, width=24, font=('Segoe UI', 10), relief='solid', bd=1, bg='white')
        self.doctor_search_entry.pack(side='left', padx=(0, 10))
        ModernButton(search_row, text="Search", command=self.search_doctors_display, color='info').pack(side='left', padx=4)
        ModernButton(search_row, text="Show All", command=self.update_doctor_list_display, color='secondary').pack(side='left', padx=4)
        table_card = tk.Frame(list_card, bg='white')
        table_card.pack(padx=16, pady=(0, 16), fill='both', expand=True)

        self.configure_doctor_table_style()
        columns = ("doctor_id", "name", "specialty", "contact", "availability")
        self.doctor_display = ttk.Treeview(
            table_card,
            columns=columns,
            show='headings',
            style='DoctorDirectory.Treeview'
        )
        self.doctor_display.heading("doctor_id", text="Doctor ID")
        self.doctor_display.heading("name", text="Doctor Name")
        self.doctor_display.heading("specialty", text="Specialty")
        self.doctor_display.heading("contact", text="Contact")
        self.doctor_display.heading("availability", text="Availability")

        self.doctor_display.column("doctor_id", width=90, minwidth=80, anchor='center')
        self.doctor_display.column("name", width=145, minwidth=125, anchor='w')
        self.doctor_display.column("specialty", width=120, minwidth=105, anchor='w')
        self.doctor_display.column("contact", width=115, minwidth=95, anchor='center')
        self.doctor_display.column("availability", width=145, minwidth=125, anchor='w')

        y_scroll = ttk.Scrollbar(table_card, orient='vertical', command=self.doctor_display.yview)
        x_scroll = ttk.Scrollbar(table_card, orient='horizontal', command=self.doctor_display.xview)
        self.doctor_display.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(0, weight=1)
        self.doctor_display.grid(row=0, column=0, sticky='nsew')
        y_scroll.grid(row=0, column=1, sticky='ns')
        x_scroll.grid(row=1, column=0, sticky='ew')
        self.update_doctor_list_display()

    def create_billing_tab(self):
        """Billing and payments"""
        self.billing_tab = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.billing_tab, text="💳 Billing")

        self.billing_tab.grid_columnconfigure(0, weight=1, uniform='billing_columns')
        self.billing_tab.grid_columnconfigure(1, weight=1, uniform='billing_columns')
        self.billing_tab.grid_rowconfigure(0, weight=1)

        left_frame = tk.Frame(self.billing_tab, bg=COLORS['light_bg'])
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(10, 5), pady=10)
        right_frame = tk.Frame(self.billing_tab, bg=COLORS['light_bg'])
        right_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 10), pady=10)

        form_card = tk.Frame(left_frame, bg='#eef6fb', relief='flat', bd=1)
        form_card.pack(fill='both', expand=True, padx=10, pady=10)
        banner = tk.Frame(form_card, bg=COLORS['warning'], height=88)
        banner.pack(fill='x')
        banner.pack_propagate(False)
        tk.Label(banner, text="💳", font=('Segoe UI', 24), bg=COLORS['warning'], fg='white').pack(side='left', padx=(18, 10), pady=18)
        banner_text = tk.Frame(banner, bg=COLORS['warning'])
        banner_text.pack(side='left', pady=16)
        tk.Label(banner_text, text="BILLING & PAYMENTS", font=('Segoe UI', 16, 'bold'),
                 bg=COLORS['warning'], fg='white').pack(anchor='w')
        tk.Label(banner_text, text="Create bills, review balances, and mark payments quickly",
                 font=('Segoe UI', 10), bg=COLORS['warning'], fg='#fff3d8').pack(anchor='w', pady=(3, 0))

        inner = tk.Frame(form_card, bg='white')
        inner.pack(fill='both', expand=True, padx=16, pady=16)
        form = tk.Frame(inner, bg='white')
        form.pack(fill='x', padx=18, pady=18)
        form.grid_columnconfigure(1, weight=1)

        tk.Label(form, text="🔎 Patient", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, padx=8, pady=8, sticky='w')
        self.bill_patient_id_var = tk.StringVar()
        self.bill_patient_id_combo = ttk.Combobox(
            form,
            textvariable=self.bill_patient_id_var,
            font=('Segoe UI', 11),
            state='normal',
            postcommand=self.update_billing_patient_dropdown
        )
        self.bill_patient_id_combo.grid(row=0, column=1, padx=8, pady=8, sticky='ew')

        ModernButton(form, text="Search", command=self.search_billing_patients, color='info').grid(row=1, column=1, sticky='e', padx=8, pady=(0, 8))

        tk.Label(form, text="🧾 Service", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=2, column=0, padx=8, pady=8, sticky='w')
        self.bill_service_entry = tk.Entry(form, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.bill_service_entry.grid(row=2, column=1, padx=8, pady=8, sticky='ew')
        tk.Label(form, text="💰 Amount", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=3, column=0, padx=8, pady=8, sticky='w')
        self.bill_amount_entry = tk.Entry(form, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.bill_amount_entry.grid(row=3, column=1, padx=8, pady=8, sticky='ew')
        tk.Label(form, text="📝 Notes", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=4, column=0, padx=8, pady=8, sticky='nw')
        self.bill_notes_text = tk.Text(form, height=4, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd', wrap='word')
        self.bill_notes_text.grid(row=4, column=1, padx=8, pady=8, sticky='ew')

        buttons = tk.Frame(form_card, bg='#eef6fb')
        buttons.pack(pady=(0, 18))
        ModernButton(buttons, text="➕ Create Bill", command=self.create_bill_record, color='secondary').pack(side='left', padx=6)
        ModernButton(buttons, text="✅ Mark Paid", command=self.mark_selected_bill_paid, color='info').pack(side='left', padx=6)
        ModernButton(buttons, text="🧹 Clear", command=self.clear_billing_form, color='gray').pack(side='left', padx=6)

        list_card = tk.Frame(right_frame, bg='#eef6fb', relief='flat', bd=1)
        list_card.pack(fill='both', expand=True, padx=10, pady=10)
        top = tk.Frame(list_card, bg='#eef6fb')
        top.pack(fill='x', padx=16, pady=(16, 10))
        tk.Label(top, text="BILLING REGISTER", font=('Segoe UI', 16, 'bold'), bg='#eef6fb', fg=COLORS['primary']).pack(side='left')
        self.bill_filter_entry = tk.Entry(top, width=22, font=('Segoe UI', 10), relief='solid', bd=1, bg='white')
        self.bill_filter_entry.pack(side='left', padx=10)
        ModernButton(top, text="Search", command=self.filter_billing_display, color='info').pack(side='left', padx=4)
        ModernButton(top, text="Show All", command=self.update_billing_display, color='secondary').pack(side='left', padx=4)
        self.selected_bill_id_var = tk.StringVar()
        self.bill_selected_label = tk.Label(list_card, text="Selected Bill ID: None", bg='#eef6fb', fg=COLORS['gray_dark'], font=('Segoe UI', 10, 'bold'))
        self.bill_selected_label.pack(anchor='w', padx=16)

        split_frame = tk.Frame(list_card, bg='#eef6fb')
        split_frame.pack(fill='both', expand=True, padx=16, pady=(8, 16))
        split_frame.grid_rowconfigure(0, weight=1, uniform='billing_split')
        split_frame.grid_rowconfigure(1, weight=1, uniform='billing_split')
        split_frame.grid_columnconfigure(0, weight=1)

        bill_list_frame = tk.Frame(split_frame, bg='#eef6fb')
        bill_list_frame.grid(row=0, column=0, sticky='nsew', pady=(0, 8))
        self.bill_listbox = tk.Listbox(
            bill_list_frame,
            height=10,
            font=('Segoe UI', 10),
            relief='flat',
            bd=0,
            bg='#f8fbfd',
            fg=COLORS['text'],
            selectbackground=COLORS['primary'],
            selectforeground='white',
            activestyle='none'
        )
        self.bill_listbox.pack(fill='both', expand=True)
        self.bill_listbox.bind("<<ListboxSelect>>", self.on_bill_select)

        billing_detail_frame = tk.Frame(split_frame, bg='#eef6fb')
        billing_detail_frame.grid(row=1, column=0, sticky='nsew', pady=(8, 0))
        self.billing_display = scrolledtext.ScrolledText(billing_detail_frame, height=10, font=('Segoe UI', 10),
                                                         bg='#f8fbfd', fg=COLORS['text'], relief='flat', bd=0,
                                                         padx=16, pady=16, wrap='word')
        self.billing_display.pack(fill='both', expand=True)
        self.configure_billing_display()
        self.update_billing_display()
        self.update_billing_patient_dropdown()
    
    def create_hospital_operations_tab(self):
        """Ward, bed, and admission management for hospital-scale support."""
        self.hospital_tab = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.hospital_tab, text="🏥 Hospital Operations")

        left_frame = tk.Frame(self.hospital_tab, bg=COLORS['light_bg'])
        left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        right_frame = tk.Frame(self.hospital_tab, bg=COLORS['light_bg'])
        right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        form_card = tk.Frame(left_frame, bg='#eef6fb', relief='flat', bd=1)
        form_card.pack(fill='both', expand=True, padx=10, pady=10)

        banner = tk.Frame(form_card, bg=COLORS['primary'], height=90)
        banner.pack(fill='x')
        banner.pack_propagate(False)
        tk.Label(banner, text="🏥", font=('Segoe UI', 28), bg=COLORS['primary'], fg='white').pack(side='left', padx=(18, 10), pady=18)
        banner_text = tk.Frame(banner, bg=COLORS['primary'])
        banner_text.pack(side='left', pady=18)
        tk.Label(banner_text, text="HOSPITAL OPERATIONS", font=('Segoe UI', 16, 'bold'),
                 bg=COLORS['primary'], fg='white').pack(anchor='w')
        tk.Label(banner_text, text="Manage wards, beds, and admissions for larger facilities.",
                 font=('Segoe UI', 10), bg=COLORS['primary'], fg='#dbeef8').pack(anchor='w', pady=(3, 0))

        form = tk.Frame(form_card, bg='white')
        form.pack(fill='both', expand=True, padx=18, pady=18)
        form.grid_columnconfigure(1, weight=1)

        tk.Label(form, text="🔎 Patient", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, sticky='w', padx=8, pady=8)
        self.hospital_patient_var = tk.StringVar()
        self.hospital_patient_combo = ttk.Combobox(
            form,
            textvariable=self.hospital_patient_var,
            width=28,
            font=('Segoe UI', 11),
            state='normal',
            postcommand=self.update_hospital_patient_dropdown
        )
        self.hospital_patient_combo.grid(row=0, column=1, padx=8, pady=8, sticky='ew')

        tk.Label(form, text="🏷️ Ward", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=1, column=0, sticky='w', padx=8, pady=8)
        self.ward_var = tk.StringVar()
        self.ward_combo = ttk.Combobox(form, textvariable=self.ward_var,
                                       font=('Segoe UI', 11), state='readonly')
        self.ward_combo.grid(row=1, column=1, padx=8, pady=8, sticky='ew')
        self.ward_combo.bind('<<ComboboxSelected>>', lambda _: self.update_hospital_bed_dropdown())

        tk.Label(form, text="🛏 Bed", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=2, column=0, sticky='w', padx=8, pady=8)
        self.bed_var = tk.StringVar()
        self.bed_combo = ttk.Combobox(form, textvariable=self.bed_var, font=('Segoe UI', 11), state='readonly')
        self.bed_combo.grid(row=2, column=1, padx=8, pady=8, sticky='ew')

        tk.Label(form, text="📅 Expected Discharge", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=3, column=0, sticky='w', padx=8, pady=8)
        self.expected_discharge_entry = tk.Entry(form, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.expected_discharge_entry.grid(row=3, column=1, padx=8, pady=8, sticky='ew')

        tk.Label(form, text="📝 Notes", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=4, column=0, sticky='nw', padx=8, pady=8)
        self.hospital_notes_text = tk.Text(form, height=5, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd', wrap='word')
        self.hospital_notes_text.grid(row=4, column=1, padx=8, pady=8, sticky='ew')

        button_frame = tk.Frame(form_card, bg='white')
        button_frame.pack(fill='x', padx=18, pady=(0, 18))
        ModernButton(button_frame, text="➕ Admit Patient", command=self.admit_patient_to_bed, color='secondary').pack(side='left', padx=6)
        ModernButton(button_frame, text="🔄 Refresh", command=self.load_hospital_operations_data, color='info').pack(side='left', padx=6)

        list_card = tk.Frame(right_frame, bg='#eef6fb', relief='flat', bd=1)
        list_card.pack(fill='both', expand=True, padx=10, pady=10)

        admission_banner = tk.Frame(list_card, bg=COLORS['warning'], height=88)
        admission_banner.pack(fill='x')
        admission_banner.pack_propagate(False)
        tk.Label(admission_banner, text="📄", font=('Segoe UI', 26), bg=COLORS['warning'], fg='white').pack(side='left', padx=(18, 10), pady=18)
        admission_banner_text = tk.Frame(admission_banner, bg=COLORS['warning'])
        admission_banner_text.pack(side='left', pady=18)
        tk.Label(admission_banner_text, text="ACTIVE ADMISSIONS", font=('Segoe UI', 16, 'bold'),
                 bg=COLORS['warning'], fg='white').pack(anchor='w')
        tk.Label(admission_banner_text, text="Monitor which patients occupy beds and discharge them cleanly.",
                 font=('Segoe UI', 10), bg=COLORS['warning'], fg='#fff3d8').pack(anchor='w', pady=(3, 0))

        self.admission_listbox = tk.Listbox(list_card, font=('Segoe UI', 10), bg='#f8fbfd', fg=COLORS['text'],
                                            selectbackground=COLORS['primary'], selectforeground='white', activestyle='none')
        self.admission_listbox.pack(fill='both', expand=True, padx=16, pady=16)
        self.admission_listbox.bind('<<ListboxSelect>>', self.on_admission_select)

        admit_actions = tk.Frame(list_card, bg='#eef6fb')
        admit_actions.pack(fill='x', padx=16, pady=(0, 16))
        ModernButton(admit_actions, text="✅ Discharge Selected", command=self.discharge_selected_admission, color='danger').pack(side='left', padx=6)
        ModernButton(admit_actions, text="📊 Refresh Status", command=self.load_hospital_operations_data, color='gray').pack(side='left', padx=6)

        self.bed_status_label = tk.Label(list_card, text="Beds and occupancy will appear after refresh.",
                                         bg='#eef6fb', fg=COLORS['text'], font=('Segoe UI', 10), wraplength=300, justify='left')
        self.bed_status_label.pack(fill='x', padx=16, pady=(0, 12))

        self.load_hospital_operations_data()

    def admit_patient_to_bed(self):
        patient_value = self.hospital_patient_var.get().strip()
        if ' - ' in patient_value:
            patient_id = patient_value.split(' - ', 1)[0].upper()
        else:
            patient_id = patient_value.upper()

        ward_id = self.ward_var.get().strip()
        if ' - ' in ward_id:
            ward_id = ward_id.split(' - ', 1)[0]

        bed_id = self.bed_var.get().strip()
        if ' ' in bed_id:
            bed_id = bed_id.split(' ', 1)[0]

        expected_discharge = self.expected_discharge_entry.get().strip() or None
        notes = self.hospital_notes_text.get('1.0', tk.END).strip()

        if not patient_id or not ward_id or not bed_id:
            SilentMessageBox.show_error('Admission Error', 'Please select a patient, ward, and available bed.', self.root)
            return

        success, message = self.db.admit_patient(patient_id, ward_id, bed_id, expected_discharge, notes)
        if success:
            self.load_hospital_operations_data()
            SilentMessageBox.show_info('Admission Complete', message, self.root)
            self.update_status(f'Admitted {patient_id} to {bed_id}')
        else:
            SilentMessageBox.show_error('Admission Failed', message, self.root)
            self.update_status(f'Admission failed: {message}')

    def discharge_selected_admission(self):
        selection = self.admission_listbox.curselection()
        if not selection:
            SilentMessageBox.show_error('Selection Required', 'Select an admission from the list before discharging.', self.root)
            return

        admission_line = self.admission_listbox.get(selection[0])
        admission_id = admission_line.split(':', 1)[0]
        if admission_id.isdigit() and self.db.discharge_patient(int(admission_id)):
            self.load_hospital_operations_data()
            SilentMessageBox.show_info('Discharged', 'Patient has been discharged and bed is now available.', self.root)
            self.update_status('Patient discharged successfully')
        else:
            SilentMessageBox.show_error('Discharge Failed', 'Unable to discharge the selected admission.', self.root)

    def load_hospital_operations_data(self):
        wards = self.db.get_hospital_wards()
        ward_values = [f"{ward['ward_id']} - {ward['name']}" for ward in wards]
        self.ward_combo['values'] = ward_values
        if ward_values and not self.ward_var.get():
            self.ward_var.set(ward_values[0])

        self.update_hospital_patient_dropdown()
        self.update_hospital_bed_dropdown()

        active = self.db.get_active_admissions()
        self.admission_listbox.delete(0, tk.END)
        for item in active:
            self.admission_listbox.insert(tk.END, f"{item['id']}: {item['patient_id']} - {item['patient_name']} | {item['ward_id']}/{item['bed_id']} ({item['admission_date']})")

        beds = self.db.get_beds()
        total = len(beds)
        occupied = len([b for b in beds if b['status'] == 'occupied'])
        available = len([b for b in beds if b['status'] == 'available'])
        self.bed_status_label.config(text=f"Beds: {total} total · {available} available · {occupied} occupied")

    def update_hospital_bed_dropdown(self):
        ward_id = self.ward_var.get().strip()
        if ' - ' in ward_id:
            ward_id = ward_id.split(' - ', 1)[0]
        available = self.db.get_available_beds(ward_id if ward_id else None)
        self.bed_combo['values'] = [f"{bed['bed_id']} ({bed['room_number']})" for bed in available]
        if available:
            self.bed_var.set(f"{available[0]['bed_id']} ({available[0]['room_number']})")

    def update_hospital_patient_dropdown(self, patients=None):
        self.hospital_patient_combo['values'] = self.get_patient_dropdown_values(patients)

    def create_lab_orders_tab(self):
        """Laboratory order creation, tracking, and status review."""
        self.lab_orders_tab = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.lab_orders_tab, text="🧪 Lab Orders")

        left_frame = tk.Frame(self.lab_orders_tab, bg=COLORS['light_bg'])
        left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        right_frame = tk.Frame(self.lab_orders_tab, bg=COLORS['light_bg'])
        right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        form_card = tk.Frame(left_frame, bg='#eef6fb', relief='flat', bd=1)
        form_card.pack(fill='both', expand=True, padx=10, pady=10)
        banner = tk.Frame(form_card, bg=COLORS['info'], height=90)
        banner.pack(fill='x')
        banner.pack_propagate(False)
        tk.Label(banner, text="🧪", font=('Segoe UI', 28), bg=COLORS['info'], fg='white').pack(side='left', padx=(18, 10), pady=18)
        banner_text = tk.Frame(banner, bg=COLORS['info'])
        banner_text.pack(side='left', pady=18)
        tk.Label(banner_text, text="LAB ORDERS", font=('Segoe UI', 16, 'bold'),
                 bg=COLORS['info'], fg='white').pack(anchor='w')
        tk.Label(banner_text, text="Request tests and monitor laboratory workflow across patients.",
                 font=('Segoe UI', 10), bg=COLORS['info'], fg='#d8eef8').pack(anchor='w', pady=(3, 0))

        form = tk.Frame(form_card, bg='white')
        form.pack(fill='both', expand=True, padx=18, pady=18)
        form.grid_columnconfigure(1, weight=1)

        tk.Label(form, text="🔎 Patient", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, sticky='w', padx=8, pady=8)
        self.lab_order_patient_var = tk.StringVar()
        self.lab_order_patient_combo = ttk.Combobox(form, textvariable=self.lab_order_patient_var,
                                                   font=('Segoe UI', 11), state='normal', postcommand=self.update_lab_order_patient_dropdown)
        self.lab_order_patient_combo.grid(row=0, column=1, padx=8, pady=8, sticky='ew')

        tk.Label(form, text="🧾 Order Code", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=1, column=0, sticky='w', padx=8, pady=8)
        self.lab_order_code_entry = tk.Entry(form, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.lab_order_code_entry.grid(row=1, column=1, padx=8, pady=8, sticky='ew')

        tk.Label(form, text="🧬 Test Name", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=2, column=0, sticky='w', padx=8, pady=8)
        self.lab_order_test_entry = tk.Entry(form, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.lab_order_test_entry.grid(row=2, column=1, padx=8, pady=8, sticky='ew')

        tk.Label(form, text="👩‍⚕️ Requested By", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=3, column=0, sticky='w', padx=8, pady=8)
        self.lab_order_requested_by_entry = tk.Entry(form, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.lab_order_requested_by_entry.grid(row=3, column=1, padx=8, pady=8, sticky='ew')

        tk.Label(form, text="📋 Result Notes", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=4, column=0, sticky='nw', padx=8, pady=8)
        self.lab_order_results_text = tk.Text(form, height=5, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd', wrap='word')
        self.lab_order_results_text.grid(row=4, column=1, padx=8, pady=8, sticky='ew')

        button_frame = tk.Frame(form_card, bg='white')
        button_frame.pack(fill='x', padx=18, pady=(0, 18))
        ModernButton(button_frame, text="➕ Request Lab Order", command=self.submit_lab_order, color='secondary').pack(side='left', padx=6)
        ModernButton(button_frame, text="🔄 Refresh", command=self.load_lab_orders_data, color='info').pack(side='left', padx=6)

        list_card = tk.Frame(right_frame, bg='#eef6fb', relief='flat', bd=1)
        list_card.pack(fill='both', expand=True, padx=10, pady=10)
        top = tk.Frame(list_card, bg='#eef6fb')
        top.pack(fill='x', padx=16, pady=(16, 10))
        tk.Label(top, text="LAB ORDER REGISTER", font=('Segoe UI', 16, 'bold'), bg='#eef6fb', fg=COLORS['primary']).pack(side='left')
        self.lab_order_filter_entry = tk.Entry(top, width=24, font=('Segoe UI', 10), relief='solid', bd=1, bg='white')
        self.lab_order_filter_entry.pack(side='left', padx=10)
        ModernButton(top, text="Search", command=self.search_lab_orders, color='info').pack(side='left', padx=4)
        ModernButton(top, text="Show All", command=self.load_lab_orders_data, color='secondary').pack(side='left', padx=4)

        self.lab_order_tree = ttk.Treeview(list_card, columns=('id', 'patient', 'code', 'test', 'requested_by', 'status', 'ordered_date', 'result_date'), show='headings', height=14)
        self.lab_order_tree.heading('id', text='ID')
        self.lab_order_tree.heading('patient', text='Patient')
        self.lab_order_tree.heading('code', text='Code')
        self.lab_order_tree.heading('test', text='Test')
        self.lab_order_tree.heading('requested_by', text='Requested By')
        self.lab_order_tree.heading('status', text='Status')
        self.lab_order_tree.heading('ordered_date', text='Ordered Date')
        self.lab_order_tree.heading('result_date', text='Result Date')
        self.lab_order_tree.column('id', width=40, anchor='center')
        self.lab_order_tree.column('patient', width=120)
        self.lab_order_tree.column('code', width=80)
        self.lab_order_tree.column('test', width=140)
        self.lab_order_tree.column('requested_by', width=110)
        self.lab_order_tree.column('status', width=95, anchor='center')
        self.lab_order_tree.column('ordered_date', width=120, anchor='center')
        self.lab_order_tree.column('result_date', width=120, anchor='center')
        self.lab_order_tree.pack(fill='both', expand=True, padx=16, pady=(0, 16))

        self.update_lab_order_patient_dropdown()
        self.load_lab_orders_data()

    def load_lab_orders_data(self, patient_id=None):
        if patient_id:
            orders = self.db.get_lab_orders(patient_id)
        else:
            filter_term = self.lab_order_filter_entry.get().strip() if hasattr(self, 'lab_order_filter_entry') else ''
            orders = self.db.get_lab_orders()
            if filter_term:
                orders = [order for order in orders if filter_term.lower() in order['patient_id'].lower() or filter_term.lower() in order['test_name'].lower() or filter_term.lower() in order['order_code'].lower()]

        self.lab_order_tree.delete(*self.lab_order_tree.get_children())
        for order in orders:
            self.lab_order_tree.insert('', tk.END, values=(order['id'], order['patient_id'], order['order_code'], order['test_name'], order['requested_by'], order['status'], order['ordered_date'], order['result_date'] or ''))

    def submit_lab_order(self):
        patient_value = self.lab_order_patient_var.get().strip()
        patient_id = patient_value.split(' - ', 1)[0].upper() if ' - ' in patient_value else patient_value.upper()
        order_code = self.lab_order_code_entry.get().strip() or f"LAB-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        test_name = self.lab_order_test_entry.get().strip()
        requested_by = self.lab_order_requested_by_entry.get().strip() or (self.current_user.get('display_name') if self.current_user else 'Staff')

        if not patient_id or not test_name:
            SilentMessageBox.show_error('Lab Order Error', 'Please select a patient and enter the test name.', self.root)
            return

        if self.db.create_lab_order(patient_id, order_code, test_name, requested_by):
            self.load_lab_orders_data()
            SilentMessageBox.show_info('Lab Order Submitted', 'The lab order was created successfully.', self.root)
            self.update_status(f'Lab order created for {patient_id}')
        else:
            SilentMessageBox.show_error('Submission Failed', 'Unable to create the lab order.', self.root)

    def search_lab_orders(self):
        self.load_lab_orders_data()

    def update_lab_order_patient_dropdown(self, patients=None):
        self.lab_order_patient_combo['values'] = self.get_patient_dropdown_values(patients)

    def create_inventory_tab(self):
        """Medication inventory management for clinics and hospitals."""
        self.inventory_tab = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.inventory_tab, text="💊 Pharmacy Inventory")

        left_frame = tk.Frame(self.inventory_tab, bg=COLORS['light_bg'])
        left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        right_frame = tk.Frame(self.inventory_tab, bg=COLORS['light_bg'])
        right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        form_card = tk.Frame(left_frame, bg='#eef6fb', relief='flat', bd=1)
        form_card.pack(fill='both', expand=True, padx=10, pady=10)
        banner = tk.Frame(form_card, bg=COLORS['secondary_dark'], height=90)
        banner.pack(fill='x')
        banner.pack_propagate(False)
        tk.Label(banner, text="💊", font=('Segoe UI', 28), bg=COLORS['secondary_dark'], fg='white').pack(side='left', padx=(18, 10), pady=18)
        banner_text = tk.Frame(banner, bg=COLORS['secondary_dark'])
        banner_text.pack(side='left', pady=18)
        tk.Label(banner_text, text="PHARMACY INVENTORY", font=('Segoe UI', 16, 'bold'),
                 bg=COLORS['secondary_dark'], fg='white').pack(anchor='w')
        tk.Label(banner_text, text="Track medicine stock, price, and reorder levels.",
                 font=('Segoe UI', 10), bg=COLORS['secondary_dark'], fg='#d8f7e6').pack(anchor='w', pady=(3, 0))

        form = tk.Frame(form_card, bg='white')
        form.pack(fill='both', expand=True, padx=18, pady=18)
        form.grid_columnconfigure(1, weight=1)

        tk.Label(form, text="🆔 Medication ID", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, sticky='w', padx=8, pady=8)
        self.med_id_entry = tk.Entry(form, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.med_id_entry.grid(row=0, column=1, padx=8, pady=8, sticky='ew')

        tk.Label(form, text="📛 Name", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=1, column=0, sticky='w', padx=8, pady=8)
        self.med_name_entry = tk.Entry(form, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.med_name_entry.grid(row=1, column=1, padx=8, pady=8, sticky='ew')

        tk.Label(form, text="💊 Dosage", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=2, column=0, sticky='w', padx=8, pady=8)
        self.med_dosage_entry = tk.Entry(form, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.med_dosage_entry.grid(row=2, column=1, padx=8, pady=8, sticky='ew')

        tk.Label(form, text="📦 Quantity", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=3, column=0, sticky='w', padx=8, pady=8)
        self.med_quantity_entry = tk.Entry(form, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.med_quantity_entry.grid(row=3, column=1, padx=8, pady=8, sticky='ew')

        tk.Label(form, text="💲 Unit Price", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=4, column=0, sticky='w', padx=8, pady=8)
        self.med_price_entry = tk.Entry(form, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.med_price_entry.grid(row=4, column=1, padx=8, pady=8, sticky='ew')

        button_frame = tk.Frame(form_card, bg='white')
        button_frame.pack(fill='x', padx=18, pady=(0, 18))
        ModernButton(button_frame, text="💾 Save Medication", command=self.save_medication_inventory_record, color='secondary').pack(side='left', padx=6)
        ModernButton(button_frame, text="🔄 Refresh", command=self.load_medication_inventory, color='info').pack(side='left', padx=6)

        list_card = tk.Frame(right_frame, bg='#eef6fb', relief='flat', bd=1)
        list_card.pack(fill='both', expand=True, padx=10, pady=10)
        top = tk.Frame(list_card, bg='#eef6fb')
        top.pack(fill='x', padx=16, pady=(16, 10))
        tk.Label(top, text="MEDICATION INVENTORY", font=('Segoe UI', 16, 'bold'), bg='#eef6fb', fg=COLORS['primary']).pack(side='left')
        ModernButton(top, text="Show All", command=self.load_medication_inventory, color='secondary').pack(side='left', padx=4)

        self.med_inventory_tree = ttk.Treeview(list_card, columns=('med_id', 'name', 'dosage_form', 'quantity', 'unit_price', 'updated'), show='headings', height=16)
        self.med_inventory_tree.heading('med_id', text='ID')
        self.med_inventory_tree.heading('name', text='Name')
        self.med_inventory_tree.heading('dosage_form', text='Dosage Form')
        self.med_inventory_tree.heading('quantity', text='Qty')
        self.med_inventory_tree.heading('unit_price', text='Unit Price')
        self.med_inventory_tree.heading('updated', text='Last Updated')
        self.med_inventory_tree.column('med_id', width=70, anchor='center')
        self.med_inventory_tree.column('name', width=140)
        self.med_inventory_tree.column('dosage_form', width=100)
        self.med_inventory_tree.column('quantity', width=70, anchor='center')
        self.med_inventory_tree.column('unit_price', width=90, anchor='center')
        self.med_inventory_tree.column('updated', width=130, anchor='center')
        self.med_inventory_tree.pack(fill='both', expand=True, padx=16, pady=(0, 16))

        self.load_medication_inventory()

    def load_medication_inventory(self):
        inventory = self.db.get_medication_inventory()
        self.med_inventory_tree.delete(*self.med_inventory_tree.get_children())
        for med in inventory:
            self.med_inventory_tree.insert('', tk.END, values=(med['med_id'], med['name'], med['dosage_form'], med['quantity'], f"{med['unit_price']:.2f}", med['last_updated'] or ''))

    def save_medication_inventory_record(self):
        med_id = self.med_id_entry.get().strip().upper()
        name = self.med_name_entry.get().strip()
        dosage = self.med_dosage_entry.get().strip()
        quantity = self.med_quantity_entry.get().strip()
        unit_price = self.med_price_entry.get().strip()

        if not med_id or not name:
            SilentMessageBox.show_error('Inventory Error', 'Medication ID and name are required.', self.root)
            return

        try:
            quantity_val = int(quantity)
            price_val = float(unit_price or 0)
        except ValueError:
            SilentMessageBox.show_error('Inventory Error', 'Quantity must be an integer and price must be numeric.', self.root)
            return

        if self.db.save_medication(med_id, name, dosage, quantity_val, price_val):
            self.load_medication_inventory()
            SilentMessageBox.show_info('Inventory Saved', 'Medication inventory has been updated.', self.root)
            self.update_status(f'Saved medication {med_id}')
        else:
            SilentMessageBox.show_error('Save Failed', 'Unable to save medication inventory.', self.root)

    def create_insurance_tab(self):
        """Insurance claim submission and review panel."""
        self.insurance_tab = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.insurance_tab, text="💼 Insurance Claims")

        left_frame = tk.Frame(self.insurance_tab, bg=COLORS['light_bg'])
        left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        right_frame = tk.Frame(self.insurance_tab, bg=COLORS['light_bg'])
        right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        form_card = tk.Frame(left_frame, bg='#eef6fb', relief='flat', bd=1)
        form_card.pack(fill='both', expand=True, padx=10, pady=10)
        banner = tk.Frame(form_card, bg=COLORS['warning'], height=90)
        banner.pack(fill='x')
        banner.pack_propagate(False)
        tk.Label(banner, text="💼", font=('Segoe UI', 28), bg=COLORS['warning'], fg='white').pack(side='left', padx=(18, 10), pady=18)
        banner_text = tk.Frame(banner, bg=COLORS['warning'])
        banner_text.pack(side='left', pady=18)
        tk.Label(banner_text, text="INSURANCE CLAIMS", font=('Segoe UI', 16, 'bold'),
                 bg=COLORS['warning'], fg='white').pack(anchor='w')
        tk.Label(banner_text, text="Submit and review patient claims from the front desk or billing team.",
                 font=('Segoe UI', 10), bg=COLORS['warning'], fg='#fff3d8').pack(anchor='w', pady=(3, 0))

        form = tk.Frame(form_card, bg='white')
        form.pack(fill='both', expand=True, padx=18, pady=18)
        form.grid_columnconfigure(1, weight=1)

        tk.Label(form, text="🔎 Patient", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, sticky='w', padx=8, pady=8)
        self.claim_patient_var = tk.StringVar()
        self.claim_patient_combo = ttk.Combobox(form, textvariable=self.claim_patient_var,
                                               font=('Segoe UI', 11), state='normal', postcommand=self.update_claim_patient_dropdown)
        self.claim_patient_combo.grid(row=0, column=1, padx=8, pady=8, sticky='ew')

        tk.Label(form, text="🏢 Provider", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=1, column=0, sticky='w', padx=8, pady=8)
        self.claim_provider_entry = tk.Entry(form, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.claim_provider_entry.grid(row=1, column=1, padx=8, pady=8, sticky='ew')

        tk.Label(form, text="📝 Policy Number", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=2, column=0, sticky='w', padx=8, pady=8)
        self.claim_policy_entry = tk.Entry(form, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.claim_policy_entry.grid(row=2, column=1, padx=8, pady=8, sticky='ew')

        tk.Label(form, text="💰 Amount", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=3, column=0, sticky='w', padx=8, pady=8)
        self.claim_amount_entry = tk.Entry(form, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.claim_amount_entry.grid(row=3, column=1, padx=8, pady=8, sticky='ew')

        tk.Label(form, text="📝 Notes", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=4, column=0, sticky='nw', padx=8, pady=8)
        self.claim_notes_text = tk.Text(form, height=5, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd', wrap='word')
        self.claim_notes_text.grid(row=4, column=1, padx=8, pady=8, sticky='ew')

        button_frame = tk.Frame(form_card, bg='white')
        button_frame.pack(fill='x', padx=18, pady=(0, 18))
        ModernButton(button_frame, text="➕ Submit Claim", command=self.submit_insurance_claim, color='secondary').pack(side='left', padx=6)
        ModernButton(button_frame, text="🔄 Refresh", command=self.load_insurance_claims_data, color='info').pack(side='left', padx=6)

        list_card = tk.Frame(right_frame, bg='#eef6fb', relief='flat', bd=1)
        list_card.pack(fill='both', expand=True, padx=10, pady=10)
        top = tk.Frame(list_card, bg='#eef6fb')
        top.pack(fill='x', padx=16, pady=(16, 10))
        tk.Label(top, text="INSURANCE CLAIMS", font=('Segoe UI', 16, 'bold'), bg='#eef6fb', fg=COLORS['primary']).pack(side='left')
        ModernButton(top, text="Show All", command=self.load_insurance_claims_data, color='secondary').pack(side='left', padx=4)

        self.insurance_tree = ttk.Treeview(list_card, columns=('id', 'patient', 'provider', 'policy', 'status', 'amount', 'submitted', 'processed'), show='headings', height=16)
        self.insurance_tree.heading('id', text='ID')
        self.insurance_tree.heading('patient', text='Patient')
        self.insurance_tree.heading('provider', text='Provider')
        self.insurance_tree.heading('policy', text='Policy Number')
        self.insurance_tree.heading('status', text='Status')
        self.insurance_tree.heading('amount', text='Amount')
        self.insurance_tree.heading('submitted', text='Submitted')
        self.insurance_tree.heading('processed', text='Processed')
        self.insurance_tree.column('id', width=40, anchor='center')
        self.insurance_tree.column('patient', width=110)
        self.insurance_tree.column('provider', width=110)
        self.insurance_tree.column('policy', width=120)
        self.insurance_tree.column('status', width=90, anchor='center')
        self.insurance_tree.column('amount', width=80, anchor='center')
        self.insurance_tree.column('submitted', width=120, anchor='center')
        self.insurance_tree.column('processed', width=120, anchor='center')
        self.insurance_tree.pack(fill='both', expand=True, padx=16, pady=(0, 16))

        self.update_claim_patient_dropdown()
        self.load_insurance_claims_data()

    def load_insurance_claims_data(self, patient_id=None):
        claims = self.db.get_insurance_claims(patient_id) if patient_id else self.db.get_insurance_claims()
        self.insurance_tree.delete(*self.insurance_tree.get_children())
        for claim in claims:
            self.insurance_tree.insert('', tk.END, values=(claim['id'], claim['patient_id'], claim['provider'], claim['policy_number'], claim['claim_status'], f"{claim['amount']:.2f}", claim['submitted_date'], claim['processed_date'] or ''))

    def submit_insurance_claim(self):
        patient_value = self.claim_patient_var.get().strip()
        patient_id = patient_value.split(' - ', 1)[0].upper() if ' - ' in patient_value else patient_value.upper()
        provider = self.claim_provider_entry.get().strip()
        policy = self.claim_policy_entry.get().strip()
        amount = self.claim_amount_entry.get().strip()
        notes = self.claim_notes_text.get('1.0', tk.END).strip()

        if not patient_id or not provider or not policy or not amount:
            SilentMessageBox.show_error('Claim Error', 'Please complete the patient, provider, policy, and amount fields.', self.root)
            return

        try:
            amount_val = float(amount)
        except ValueError:
            SilentMessageBox.show_error('Claim Error', 'Amount must be a valid number.', self.root)
            return

        if self.db.submit_insurance_claim(patient_id, provider, policy, amount_val, notes):
            self.load_insurance_claims_data()
            SilentMessageBox.show_info('Claim Submitted', 'Insurance claim submitted successfully.', self.root)
            self.update_status(f'Insurance claim submitted for {patient_id}')
        else:
            SilentMessageBox.show_error('Submit Failed', 'Unable to submit insurance claim.', self.root)

    def update_claim_patient_dropdown(self, patients=None):
        self.claim_patient_combo['values'] = self.get_patient_dropdown_values(patients)

    def create_documents_tab(self):
        """Patient documents and file metadata management."""
        self.documents_tab = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.documents_tab, text="📁 Patient Documents")

        left_frame = tk.Frame(self.documents_tab, bg=COLORS['light_bg'])
        left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        right_frame = tk.Frame(self.documents_tab, bg=COLORS['light_bg'])
        right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        form_card = tk.Frame(left_frame, bg='#eef6fb', relief='flat', bd=1)
        form_card.pack(fill='both', expand=True, padx=10, pady=10)
        banner = tk.Frame(form_card, bg=COLORS['gray_dark'], height=90)
        banner.pack(fill='x')
        banner.pack_propagate(False)
        tk.Label(banner, text="📁", font=('Segoe UI', 28), bg=COLORS['gray_dark'], fg='white').pack(side='left', padx=(18, 10), pady=18)
        banner_text = tk.Frame(banner, bg=COLORS['gray_dark'])
        banner_text.pack(side='left', pady=18)
        tk.Label(banner_text, text="PATIENT DOCUMENTS", font=('Segoe UI', 16, 'bold'),
                 bg=COLORS['gray_dark'], fg='white').pack(anchor='w')
        tk.Label(banner_text, text="Store document metadata and quickly open patient files.",
                 font=('Segoe UI', 10), bg=COLORS['gray_dark'], fg='#dfe2e8').pack(anchor='w', pady=(3, 0))

        form = tk.Frame(form_card, bg='white')
        form.pack(fill='both', expand=True, padx=18, pady=18)
        form.grid_columnconfigure(1, weight=1)

        tk.Label(form, text="🔎 Patient", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, sticky='w', padx=8, pady=8)
        self.document_patient_var = tk.StringVar()
        self.document_patient_combo = ttk.Combobox(form, textvariable=self.document_patient_var,
                                                   font=('Segoe UI', 11), state='normal', postcommand=self.update_document_patient_dropdown)
        self.document_patient_combo.grid(row=0, column=1, padx=8, pady=8, sticky='ew')

        tk.Label(form, text="📄 Document Type", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=1, column=0, sticky='w', padx=8, pady=8)
        self.document_type_entry = tk.Entry(form, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.document_type_entry.grid(row=1, column=1, padx=8, pady=8, sticky='ew')

        tk.Label(form, text="📝 Description", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=2, column=0, sticky='nw', padx=8, pady=8)
        self.document_description_text = tk.Text(form, height=4, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd', wrap='word')
        self.document_description_text.grid(row=2, column=1, padx=8, pady=8, sticky='ew')

        tk.Label(form, text="📂 File Path", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=3, column=0, sticky='w', padx=8, pady=8)
        path_frame = tk.Frame(form, bg='white')
        path_frame.grid(row=3, column=1, padx=8, pady=8, sticky='ew')
        self.document_path_var = tk.StringVar()
        self.document_path_entry = tk.Entry(path_frame, textvariable=self.document_path_var, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.document_path_entry.pack(side='left', fill='x', expand=True)
        tk.Button(path_frame, text='Browse', command=self.browse_document_file, bg=COLORS['secondary'], fg='white', bd=0, padx=12, pady=6, cursor='hand2').pack(side='left', padx=(8, 0))

        button_frame = tk.Frame(form_card, bg='white')
        button_frame.pack(fill='x', padx=18, pady=(0, 18))
        ModernButton(button_frame, text="💾 Save Document", command=self.save_document_metadata, color='secondary').pack(side='left', padx=6)
        ModernButton(button_frame, text="🔄 Refresh", command=self.load_documents_data, color='info').pack(side='left', padx=6)

        list_card = tk.Frame(right_frame, bg='#eef6fb', relief='flat', bd=1)
        list_card.pack(fill='both', expand=True, padx=10, pady=10)
        top = tk.Frame(list_card, bg='#eef6fb')
        top.pack(fill='x', padx=16, pady=(16, 10))
        tk.Label(top, text="DOCUMENT REGISTER", font=('Segoe UI', 16, 'bold'), bg='#eef6fb', fg=COLORS['primary']).pack(side='left')
        tk.Button(top, text='Open Selected File', command=self.open_selected_document, bg=COLORS['info'], fg='white', bd=0, padx=10, pady=6, cursor='hand2').pack(side='left', padx=8)

        self.document_tree = ttk.Treeview(list_card, columns=('id', 'patient', 'type', 'filename', 'path', 'uploaded', 'description'), show='headings', height=16)
        self.document_tree.heading('id', text='ID')
        self.document_tree.heading('patient', text='Patient')
        self.document_tree.heading('type', text='Type')
        self.document_tree.heading('filename', text='Filename')
        self.document_tree.heading('path', text='File Path')
        self.document_tree.heading('uploaded', text='Uploaded')
        self.document_tree.heading('description', text='Description')
        self.document_tree.column('id', width=40, anchor='center')
        self.document_tree.column('patient', width=110)
        self.document_tree.column('type', width=110)
        self.document_tree.column('filename', width=140)
        self.document_tree.column('path', width=170)
        self.document_tree.column('uploaded', width=110, anchor='center')
        self.document_tree.column('description', width=180)
        self.document_tree.pack(fill='both', expand=True, padx=16, pady=(0, 16))

        self.update_document_patient_dropdown()
        self.load_documents_data()

    def browse_document_file(self):
        path = filedialog.askopenfilename(title='Select Document File', filetypes=[('All Files', '*.*')])
        if path:
            self.document_path_var.set(path)
            self.document_type_entry.delete(0, tk.END)
            self.document_type_entry.insert(0, os.path.splitext(path)[1].lstrip('.').upper() or 'Other')

    def save_document_metadata(self):
        patient_value = self.document_patient_var.get().strip()
        patient_id = patient_value.split(' - ', 1)[0].upper() if ' - ' in patient_value else patient_value.upper()
        document_type = self.document_type_entry.get().strip() or 'General'
        file_path = self.document_path_var.get().strip()
        description = self.document_description_text.get('1.0', tk.END).strip()

        if not patient_id or not file_path:
            SilentMessageBox.show_error('Document Error', 'Please select a patient and attach a file.', self.root)
            return

        filename = os.path.basename(file_path)
        if self.db.save_document(patient_id, document_type, filename, file_path, description):
            self.load_documents_data()
            SilentMessageBox.show_info('Document Saved', 'Document metadata saved successfully.', self.root)
            self.update_status(f'Document saved for {patient_id}')
        else:
            SilentMessageBox.show_error('Save Failed', 'Unable to save document metadata.', self.root)

    def open_selected_document(self):
        selection = self.document_tree.selection()
        if not selection:
            SilentMessageBox.show_error('No Selection', 'Select a document record to open its file.', self.root)
            return
        item = self.document_tree.item(selection[0])
        path = item['values'][4]
        if path and os.path.exists(path):
            try:
                os.startfile(path)
            except Exception:
                SilentMessageBox.show_error('Open Error', 'Unable to open the file path directly.', self.root)
        else:
            SilentMessageBox.show_error('Missing File', 'The stored file path does not exist on disk.', self.root)

    def update_document_patient_dropdown(self, patients=None):
        self.document_patient_combo['values'] = self.get_patient_dropdown_values(patients)

    def load_documents_data(self):
        docs = self.db.get_documents()
        self.document_tree.delete(*self.document_tree.get_children())
        for doc in docs:
            self.document_tree.insert('', tk.END, values=(doc['id'], doc['patient_id'], doc['document_type'], doc['filename'], doc['file_path'], doc['uploaded_date'], doc['description']))

    def on_admission_select(self, event=None):
        selection = self.admission_listbox.curselection()
        if selection:
            selected = self.admission_listbox.get(selection[0])
            self.update_status(f"Selected admission: {selected}")

    def create_patient_list_tab(self):
        """Patient directory tab"""
        self.patient_list_tab = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.patient_list_tab, text="📊 Patient Directory")
        
        frame = tk.Frame(self.patient_list_tab, bg=COLORS['light_bg'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)

        directory_card = tk.Frame(frame, bg='#eef6fb', relief='flat', bd=1)
        directory_card.pack(fill='both', expand=True, padx=10, pady=10)

        banner = tk.Frame(directory_card, bg=COLORS['info_dark'], height=88)
        banner.pack(fill='x')
        banner.pack_propagate(False)
        tk.Label(banner, text="🗂", font=('Segoe UI', 26), bg=COLORS['info_dark'], fg='white').pack(side='left', padx=(18, 10), pady=18)
        banner_text = tk.Frame(banner, bg=COLORS['info_dark'])
        banner_text.pack(side='left', pady=16)
        tk.Label(banner_text, text="REGISTERED PATIENT DIRECTORY", font=('Segoe UI', 16, 'bold'),
                 bg=COLORS['info_dark'], fg='white').pack(anchor='w')
        tk.Label(banner_text, text="Search the register quickly or browse every patient record in one place",
                 font=('Segoe UI', 10), bg=COLORS['info_dark'], fg='#dbeef8').pack(anchor='w', pady=(3, 0))

        search_card = tk.Frame(directory_card, bg='white', relief='flat', bd=0)
        search_card.pack(fill='x', padx=16, pady=(16, 10))
        search_frame = tk.Frame(search_card, bg='white')
        search_frame.pack(fill='x', padx=14, pady=14)

        tk.Label(search_frame, text="🔎 Search", bg='white', font=('Segoe UI', 11, 'bold'), fg=COLORS['primary']).pack(side='left', padx=5)
        self.patient_search_entry = tk.Entry(search_frame, width=40, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.patient_search_entry.pack(side='left', padx=5)
        ModernButton(search_frame, text="🔍 Search", command=self.search_in_patient_list, 
                    color='info').pack(side='left', padx=5)
        ModernButton(search_frame, text="✏️ Edit Patient", command=self.open_edit_patient_from_directory,
                    color='warning').pack(side='left', padx=5)
        ModernButton(search_frame, text="🗂 Show All", command=self.update_patient_list_display, 
                    color='secondary').pack(side='left', padx=5)
        ModernButton(search_frame, text="🖨 Export / Print", command=self.export_patient_directory_report,
                    color='primary').pack(side='left', padx=5)

        table_card = tk.Frame(directory_card, bg='white')
        table_card.pack(padx=16, pady=(0, 10), fill='both', expand=True)

        self.configure_patient_directory_table_style()
        columns = ("patient_id", "name", "age", "contact", "blood_group", "allergies")
        self.patient_list_display = ttk.Treeview(
            table_card,
            columns=columns,
            show='headings',
            style='PatientDirectory.Treeview'
        )
        self.patient_list_display.heading("patient_id", text="Patient ID")
        self.patient_list_display.heading("name", text="Full Name")
        self.patient_list_display.heading("age", text="Age")
        self.patient_list_display.heading("contact", text="Contact")
        self.patient_list_display.heading("blood_group", text="Blood Group")
        self.patient_list_display.heading("allergies", text="Allergies")

        self.patient_list_display.column("patient_id", width=95, minwidth=85, anchor='center')
        self.patient_list_display.column("name", width=160, minwidth=140, anchor='w')
        self.patient_list_display.column("age", width=55, minwidth=45, anchor='center')
        self.patient_list_display.column("contact", width=120, minwidth=100, anchor='center')
        self.patient_list_display.column("blood_group", width=85, minwidth=75, anchor='center')
        self.patient_list_display.column("allergies", width=170, minwidth=145, anchor='w')

        y_scroll = ttk.Scrollbar(table_card, orient='vertical', command=self.patient_list_display.yview)
        x_scroll = ttk.Scrollbar(table_card, orient='horizontal', command=self.patient_list_display.xview)
        self.patient_list_display.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(0, weight=1)
        self.patient_list_display.grid(row=0, column=0, sticky='nsew')
        y_scroll.grid(row=0, column=1, sticky='ns')
        x_scroll.grid(row=1, column=0, sticky='ew')

        self.patient_stats_label = tk.Label(directory_card, text="", bg='#eef6fb', 
                                           font=('Segoe UI', 11, 'bold'), fg=COLORS['info_dark'])
        self.patient_stats_label.pack(pady=(0, 12))
        
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
        add_card = tk.Frame(left_frame, bg='#eef6fb', relief='flat', bd=1)
        add_card.pack(fill='both', expand=True, padx=10, pady=10)

        banner = tk.Frame(add_card, bg=COLORS['danger_dark'], height=88)
        banner.pack(fill='x')
        banner.pack_propagate(False)
        tk.Label(banner, text="🚑", font=('Segoe UI', 26), bg=COLORS['danger_dark'], fg='white').pack(side='left', padx=(18, 10), pady=18)
        banner_text = tk.Frame(banner, bg=COLORS['danger_dark'])
        banner_text.pack(side='left', pady=16)
        tk.Label(banner_text, text="ADD TO TRIAGE QUEUE", font=('Segoe UI', 16, 'bold'),
                 bg=COLORS['danger_dark'], fg='white').pack(anchor='w')
        tk.Label(banner_text, text="Prioritize urgent cases clearly before they enter the waiting queue",
                 font=('Segoe UI', 10), bg=COLORS['danger_dark'], fg='#f8d9d5').pack(anchor='w', pady=(3, 0))

        tk.Label(add_card, text="🩺 Select severity carefully. Emergency patients appear first in the queue.",
                 font=('Segoe UI', 10, 'bold'), bg='white', fg=COLORS['text'], padx=16, pady=10).pack(anchor='w', padx=16, pady=(16, 10))

        form_card = tk.Frame(add_card, bg='white', relief='flat', bd=0)
        form_card.pack(fill='both', expand=True, padx=16, pady=(0, 10))
        form_frame = tk.Frame(form_card, bg='white')
        form_frame.pack(pady=18, padx=18, fill='x')
        
        # Patient ID
        tk.Label(form_frame, text="🆔 Patient ID", bg='white', font=('Segoe UI', 11, 'bold'), fg=COLORS['primary']).grid(row=0, column=0, pady=10, sticky='w')
        self.triage_patient_id_var = tk.StringVar()
        self.triage_pid_combo = ttk.Combobox(
            form_frame,
            textvariable=self.triage_patient_id_var,
            width=18,
            font=('Segoe UI', 11),
            state='normal',
            postcommand=self.update_triage_patient_dropdown
        )
        self.triage_pid_combo.grid(row=0, column=1, pady=10, padx=10, sticky='w')

        search_row = tk.Frame(form_frame, bg='white')
        search_row.grid(row=1, column=0, columnspan=2, sticky='ew', padx=10, pady=(0, 10))
        tk.Label(search_row, text="🔎 Search patient", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11)).pack(side='left')
        self.triage_patient_search_entry = tk.Entry(search_row, font=('Segoe UI', 10), relief='solid', bd=1, bg='#f8fbfd')
        self.triage_patient_search_entry.pack(side='left', fill='x', expand=True, padx=8)
        ModernButton(search_row, text="Search", command=self.search_triage_patients, color='info').pack(side='left')

        # Condition
        tk.Label(form_frame, text="📝 Condition", bg='white', font=('Segoe UI', 11, 'bold'), fg=COLORS['primary']).grid(row=2, column=0, pady=10, sticky='w')
        self.condition_entry = tk.Entry(form_frame, width=24, font=('Segoe UI', 11), relief='solid', bd=1, bg='#f8fbfd')
        self.condition_entry.grid(row=2, column=1, pady=10, padx=10, sticky='w')

        # Priority
        tk.Label(form_frame, text="🚨 Priority", bg='white', font=('Segoe UI', 11, 'bold'), fg=COLORS['primary']).grid(row=3, column=0, pady=10, sticky='nw')
        priority_frame = tk.Frame(form_frame, bg='white')
        priority_frame.grid(row=3, column=1, pady=10, padx=10, sticky='w')
        form_frame.grid_columnconfigure(1, weight=1)
        
        self.priority_var = tk.StringVar(value="3")
        priorities = [("🔴 Emergency (1)", "1"), ("🟡 Serious (2)", "2"), ("🟢 Minor (3)", "3")]
        for text, value in priorities:
            tk.Radiobutton(priority_frame, text=text, variable=self.priority_var, 
                          value=value, bg='white', font=('Segoe UI', 10)).pack(anchor='w', pady=2)
        
        ModernButton(add_card, text="➕ Add to Queue", command=self.add_to_triage, 
                    color='info').pack(pady=20)
        
        # Right panel - Queue display
        queue_card = tk.Frame(right_frame, bg='#eef6fb', relief='flat', bd=1)
        queue_card.pack(fill='both', expand=True, padx=10, pady=10)

        queue_banner = tk.Frame(queue_card, bg=COLORS['warning'], height=88)
        queue_banner.pack(fill='x')
        queue_banner.pack_propagate(False)
        tk.Label(queue_banner, text="📋", font=('Segoe UI', 26), bg=COLORS['warning'], fg='white').pack(side='left', padx=(18, 10), pady=18)
        queue_banner_text = tk.Frame(queue_banner, bg=COLORS['warning'])
        queue_banner_text.pack(side='left', pady=16)
        tk.Label(queue_banner_text, text="CURRENT TRIAGE QUEUE", font=('Segoe UI', 16, 'bold'),
                 bg=COLORS['warning'], fg='white').pack(anchor='w')
        tk.Label(queue_banner_text, text="Emergency cases stay visible and easy to act on",
                 font=('Segoe UI', 10), bg=COLORS['warning'], fg='#fff3d8').pack(anchor='w', pady=(3, 0))

        self.queue_display = scrolledtext.ScrolledText(queue_card, height=15, width=55, 
                                                       font=('Consolas', 10), bg='#f8fbfd', fg=COLORS['text'],
                                                       relief='flat', bd=0, padx=16, pady=16)
        self.queue_display.pack(pady=12, padx=16, fill='both', expand=True)
        
        button_frame = tk.Frame(queue_card, bg='#eef6fb')
        button_frame.pack(pady=(0, 15))
        ModernButton(button_frame, text="🚨 Serve Next", command=self.serve_next, 
                    color='danger').pack(side='left', padx=5)
        ModernButton(button_frame, text="🔄 Refresh", command=self.update_queue_display, 
                    color='gray').pack(side='left', padx=5)
        ModernButton(button_frame, text="🖨 Export / Print", command=self.export_triage_report,
                    color='primary').pack(side='left', padx=5)
        
        self.update_queue_display()
        self.update_triage_patient_dropdown()
    
    def get_triage_patient_id(self):
        """Return the patient ID selected in the triage patient dropdown."""
        patient_value = self.triage_patient_id_var.get().strip()
        if ' - ' in patient_value:
            return patient_value.split(' - ', 1)[0].upper()
        return patient_value.upper()

    def update_triage_patient_dropdown(self, patients=None):
        """Load patient list into the triage patient dropdown."""
        patients = patients if patients is not None else self.patient_db.get_all()
        sorted_patients = sorted(patients, key=lambda p: p.patient_id)
        values = [f"{patient.patient_id} - {patient.name}" for patient in sorted_patients]
        self.triage_pid_combo['values'] = values

    def search_triage_patients(self):
        """Search patients by name or ID for the triage dropdown."""
        search_term = self.triage_patient_search_entry.get().strip()
        if not search_term:
            self.update_triage_patient_dropdown()
            return

        matches = [
            patient for patient in self.patient_db.get_all()
            if search_term.lower() in patient.patient_id.lower() or search_term.lower() in patient.name.lower()
        ]
        self.update_triage_patient_dropdown(matches)
        if matches:
            first_value = f"{matches[0].patient_id} - {matches[0].name}"
            self.triage_patient_id_var.set(first_value)
            self.update_status(f"Found {len(matches)} patient(s); selected first match.")
        else:
            self.triage_patient_id_var.set("")
            SilentMessageBox.show_error("No patient", f"❌ No patient found for '{search_term}'.", self.root)

    def get_patient_dropdown_values(self, patients=None):
        patients = patients if patients is not None else self.patient_db.get_all()
        sorted_patients = sorted(patients, key=lambda p: p.patient_id)
        return [f"{patient.patient_id} - {patient.name}" for patient in sorted_patients]

    def update_appointment_patient_dropdown(self, patients=None):
        self.appt_pid_combo['values'] = self.get_patient_dropdown_values(patients)

    def search_appointment_patients(self):
        search_term = self.appt_patient_id_var.get().strip()
        if not search_term:
            self.update_appointment_patient_dropdown()
            return

        matches = [
            patient for patient in self.patient_db.get_all()
            if search_term.lower() in patient.patient_id.lower() or search_term.lower() in patient.name.lower()
        ]
        self.update_appointment_patient_dropdown(matches)
        if matches:
            self.appt_patient_id_var.set(f"{matches[0].patient_id} - {matches[0].name}")
            self.update_status(f"Found {len(matches)} patient(s); selected first match.")
        else:
            self.appt_patient_id_var.set("")
            SilentMessageBox.show_error("No patient", f"❌ No patient found for '{search_term}'.", self.root)

    def update_treatment_patient_dropdown(self, patients=None):
        self.treatment_pid_combo['values'] = self.get_patient_dropdown_values(patients)

    def search_treatment_patients(self):
        search_term = self.treatment_pid_var.get().strip()
        if not search_term:
            self.update_treatment_patient_dropdown()
            return

        matches = [
            patient for patient in self.patient_db.get_all()
            if search_term.lower() in patient.patient_id.lower() or search_term.lower() in patient.name.lower()
        ]
        self.update_treatment_patient_dropdown(matches)
        if matches:
            self.treatment_pid_var.set(f"{matches[0].patient_id} - {matches[0].name}")
            self.update_status(f"Found {len(matches)} patient(s); selected first match.")
        else:
            self.treatment_pid_var.set("")
            SilentMessageBox.show_error("No patient", f"❌ No patient found for '{search_term}'.", self.root)

    def update_history_patient_dropdown(self, patients=None):
        self.view_history_combo['values'] = self.get_patient_dropdown_values(patients)

    def update_search_patient_dropdown(self, patients=None):
        self.search_combo['values'] = self.get_patient_dropdown_values(patients)

    def resolve_patient_id(self, selection):
        selection = selection.strip()
        if not selection:
            return ""
        if ' - ' in selection:
            return selection.split(' - ', 1)[0].upper()

        candidate = selection.upper()
        if self.patient_db.lookup(candidate):
            return candidate

        matches = [p for p in self.patient_db.get_all() if selection.lower() in p.name.lower()]
        if len(matches) == 1:
            return matches[0].patient_id
        return candidate

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
        book_card = tk.Frame(left_frame, bg='#eef6fb', relief='flat', bd=1)
        book_card.pack(fill='both', expand=True, padx=10, pady=10)

        banner = tk.Frame(book_card, bg=COLORS['secondary_dark'], height=88)
        banner.pack(fill='x')
        banner.pack_propagate(False)
        tk.Label(banner, text="📅", font=('Segoe UI', 26), bg=COLORS['secondary_dark'], fg='white').pack(side='left', padx=(18, 10), pady=18)
        banner_text = tk.Frame(banner, bg=COLORS['secondary_dark'])
        banner_text.pack(side='left', pady=16)
        tk.Label(banner_text, text="BOOK APPOINTMENT", font=('Segoe UI', 16, 'bold'),
                 bg=COLORS['secondary_dark'], fg='white').pack(anchor='w')
        tk.Label(banner_text, text="Schedule visits by patient, day, and time slot with a cleaner booking form",
                 font=('Segoe UI', 10), bg=COLORS['secondary_dark'], fg='#dff5e8').pack(anchor='w', pady=(3, 0))

        tk.Label(book_card, text="🗓 Choose a day and time slot before sending the booking to the weekly schedule.",
                 font=('Segoe UI', 10, 'bold'), bg='white', fg=COLORS['text'], padx=16, pady=10).pack(anchor='w', padx=16, pady=(16, 10))

        form_card = tk.Frame(book_card, bg='white', relief='flat', bd=0)
        form_card.pack(fill='both', expand=True, padx=16, pady=(0, 10))
        form_frame = tk.Frame(form_card, bg='white')
        form_frame.pack(pady=18, padx=18, fill='x')
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Patient
        tk.Label(form_frame, text="🔎 Patient", bg='white', font=('Segoe UI', 11, 'bold'), fg=COLORS['primary']).grid(row=0, column=0, pady=10, sticky='w')
        self.appt_patient_id_var = tk.StringVar()
        self.appt_pid_combo = ttk.Combobox(
            form_frame,
            textvariable=self.appt_patient_id_var,
            width=25,
            font=('Segoe UI', 11),
            state='normal',
            postcommand=self.update_appointment_patient_dropdown
        )
        self.appt_pid_combo.grid(row=0, column=1, pady=10, padx=10, sticky='ew')
        ModernButton(form_frame, text="Search", command=self.search_appointment_patients, color='info').grid(row=0, column=2, padx=8, pady=10)
        
        # Day
        tk.Label(form_frame, text="📆 Day", bg='white', font=('Segoe UI', 11, 'bold'), fg=COLORS['primary']).grid(row=1, column=0, pady=10, sticky='w')
        self.day_var = tk.StringVar()
        self.day_menu = ttk.Combobox(form_frame, textvariable=self.day_var, values=self.calendar.days, 
                                width=22, font=('Segoe UI', 11))
        self.day_menu.grid(row=1, column=1, pady=10, padx=10, sticky='ew')
        
        # Time Slot
        tk.Label(form_frame, text="⏰ Time Slot", bg='white', font=('Segoe UI', 11, 'bold'), fg=COLORS['primary']).grid(row=2, column=0, pady=10, sticky='w')
        self.slot_var = tk.StringVar()
        self.slot_menu = ttk.Combobox(form_frame, textvariable=self.slot_var, values=self.calendar.slots, 
                                 width=22, font=('Segoe UI', 11))
        self.slot_menu.grid(row=2, column=1, pady=10, padx=10, sticky='ew')
        
        ModernButton(book_card, text="📅 Book Appointment", command=self.book_appointment, 
                    color='secondary').pack(pady=20)
        
        # Right panel - View schedule
        schedule_card = tk.Frame(right_frame, bg='#eef6fb', relief='flat', bd=1)
        schedule_card.pack(fill='both', expand=True, padx=10, pady=10)

        schedule_banner = tk.Frame(schedule_card, bg=COLORS['info_dark'], height=88)
        schedule_banner.pack(fill='x')
        schedule_banner.pack_propagate(False)
        tk.Label(schedule_banner, text="🗓", font=('Segoe UI', 26), bg=COLORS['info_dark'], fg='white').pack(side='left', padx=(18, 10), pady=18)
        schedule_banner_text = tk.Frame(schedule_banner, bg=COLORS['info_dark'])
        schedule_banner_text.pack(side='left', pady=16)
        tk.Label(schedule_banner_text, text="WEEKLY SCHEDULE", font=('Segoe UI', 16, 'bold'),
                 bg=COLORS['info_dark'], fg='white').pack(anchor='w')
        tk.Label(schedule_banner_text, text="Review booked slots clearly before printing or refreshing the agenda",
                 font=('Segoe UI', 10), bg=COLORS['info_dark'], fg='#dbeef8').pack(anchor='w', pady=(3, 0))

        self.schedule_display = scrolledtext.ScrolledText(schedule_card, height=18, width=60, 
                                                          font=('Consolas', 9), bg='#f8fbfd', fg=COLORS['text'],
                                                          relief='flat', bd=0, padx=16, pady=16)
        self.schedule_display.pack(pady=12, padx=16, fill='both', expand=True)
        self.configure_schedule_display()

        schedule_button_frame = tk.Frame(schedule_card, bg='#eef6fb')
        schedule_button_frame.pack(pady=(0, 15))
        ModernButton(schedule_button_frame, text="🔄 Refresh Schedule", command=self.update_schedule_display, 
                    color='info').pack(side='left', padx=5)
        ModernButton(schedule_button_frame, text="🖨 Export / Print", command=self.export_appointments_report,
                    color='primary').pack(side='left', padx=5)
        
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
        treatment_card = tk.Frame(left_frame, bg='#eef6fb', relief='flat', bd=1)
        treatment_card.pack(fill='both', expand=True, padx=10, pady=10)

        treatment_banner = tk.Frame(treatment_card, bg=COLORS['secondary_dark'], height=88)
        treatment_banner.pack(fill='x')
        treatment_banner.pack_propagate(False)
        tk.Label(treatment_banner, text="💉", font=('Segoe UI', 26), bg=COLORS['secondary_dark'], fg='white').pack(side='left', padx=(18, 10), pady=18)

        treatment_banner_text = tk.Frame(treatment_banner, bg=COLORS['secondary_dark'])
        treatment_banner_text.pack(side='left', pady=16)
        tk.Label(treatment_banner_text, text="ADD TREATMENT RECORD", font=('Segoe UI', 16, 'bold'),
                bg=COLORS['secondary_dark'], fg='white').pack(anchor='w')
        tk.Label(treatment_banner_text, text="Capture clinical notes clearly before sending them to the patient history",
                font=('Segoe UI', 10), bg=COLORS['secondary_dark'], fg='#dff5e8').pack(anchor='w', pady=(3, 0))

        helper_frame = tk.Frame(treatment_card, bg='#eef6fb')
        helper_frame.pack(fill='x', padx=16, pady=(16, 10))
        self.treatment_helper_label = tk.Label(helper_frame, text="🩺 Enter patient ID, choose a doctor, and add concise treatment notes.",
            font=('Segoe UI', 10, 'bold'), bg='white', fg=COLORS['text'], padx=16, pady=10)
        self.treatment_helper_label.pack(side='left')

        form_card = tk.Frame(treatment_card, bg='white', relief='flat', bd=0)
        form_card.pack(fill='both', expand=True, padx=16, pady=(0, 10))
        form_frame = tk.Frame(form_card, bg='white')
        form_frame.pack(fill='x', pady=18, padx=18)
        form_frame.grid_columnconfigure(1, weight=1)

        tk.Label(form_frame, text="🔎 Patient", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, pady=10, sticky='w')
        self.treatment_pid_var = tk.StringVar()
        self.treatment_pid_combo = ttk.Combobox(
            form_frame,
            textvariable=self.treatment_pid_var,
            width=28,
            font=('Segoe UI', 11),
            state='normal',
            postcommand=self.update_treatment_patient_dropdown
        )
        self.treatment_pid_combo.grid(row=0, column=1, pady=10, padx=(14, 0), sticky='ew')
        ModernButton(form_frame, text="Search", command=self.search_treatment_patients, color='info').grid(row=0, column=2, padx=8, pady=10)

        tk.Label(form_frame, text="💊 Treatment Notes", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=1, column=0, pady=10, sticky='nw')
        self.treatment_desc = tk.Text(form_frame, height=6, width=35, font=('Segoe UI', 11), relief='solid', bd=1,
                                      bg='#f8fbfd', wrap='word', padx=10, pady=10, insertbackground=COLORS['primary'])
        self.treatment_desc.grid(row=1, column=1, pady=10, padx=(14, 0), sticky='ew')

        tk.Label(form_frame, text="👨‍⚕️ Doctor", bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=2, column=0, pady=10, sticky='w')
        self.treatment_doctor_var = tk.StringVar()
        self.treatment_doctor_combo = ttk.Combobox(form_frame, textvariable=self.treatment_doctor_var,
                                                   font=('Segoe UI', 11), state='readonly')
        self.treatment_doctor_combo.grid(row=2, column=1, pady=10, padx=(14, 0), sticky='ew')
        self.update_treatment_doctor_dropdown()

        button_frame = tk.Frame(treatment_card, bg='#eef6fb')
        button_frame.pack(pady=(4, 18))
        ModernButton(button_frame, text="💊 Record Treatment", command=self.add_treatment, 
                    color='secondary').pack(side='left', padx=5)
        ModernButton(button_frame, text="↩️ Undo Last", command=self.undo_treatment, 
                    color='warning').pack(side='left', padx=5)
        ModernButton(button_frame, text="↪️ Redo Last", command=self.redo_treatment, 
                    color='info').pack(side='left', padx=5)
        
        # Right panel - View history
        history_card = tk.Frame(right_frame, bg='#eef6fb', relief='flat', bd=1)
        history_card.pack(fill='both', expand=True, padx=10, pady=10)

        history_banner = tk.Frame(history_card, bg=COLORS['primary'], height=88)
        history_banner.pack(fill='x')
        history_banner.pack_propagate(False)
        tk.Label(history_banner, text="🧾", font=('Segoe UI', 26), bg=COLORS['primary'], fg='white').pack(side='left', padx=(18, 10), pady=18)

        history_banner_text = tk.Frame(history_banner, bg=COLORS['primary'])
        history_banner_text.pack(side='left', pady=16)
        tk.Label(history_banner_text, text="PATIENT TREATMENT HISTORY", font=('Segoe UI', 16, 'bold'),
                bg=COLORS['primary'], fg='white').pack(anchor='w')
        tk.Label(history_banner_text, text="Review one patient or browse the complete treatment register",
                font=('Segoe UI', 10), bg=COLORS['primary'], fg=COLORS['light_bg']).pack(anchor='w', pady=(3, 0))

        search_card = tk.Frame(history_card, bg='white', relief='flat', bd=0)
        search_card.pack(fill='x', padx=16, pady=(16, 10))
        search_frame = tk.Frame(search_card, bg='white')
        search_frame.pack(fill='x', padx=14, pady=14)
        tk.Label(search_frame, text="🔎 Patient", bg='white', fg=COLORS['text'], font=('Segoe UI', 11, 'bold')).pack(side='left', padx=(0, 8))
        self.view_history_var = tk.StringVar()
        self.view_history_combo = ttk.Combobox(
            search_frame,
            textvariable=self.view_history_var,
            width=24,
            font=('Segoe UI', 11),
            state='normal',
            postcommand=self.update_history_patient_dropdown
        )
        self.view_history_combo.pack(side='left', padx=5)
        ModernButton(search_frame, text="🔎 Show Patient", command=self.show_treatment_history,
                    color='info').pack(side='left', padx=5)
        ModernButton(search_frame, text="🗂 Show All", command=self.show_all_treatment_history,
                    color='secondary').pack(side='left', padx=5)
        ModernButton(search_frame, text="🖨 Export / Print", command=self.export_treatment_history_report,
                    color='primary').pack(side='left', padx=5)

        stats_frame = tk.Frame(history_card, bg='#eef6fb')
        stats_frame.pack(fill='x', padx=16, pady=(0, 10))
        self.history_total_label = tk.Label(stats_frame, text="📋 Records: 0", font=('Segoe UI', 10, 'bold'),
                                            bg='white', fg=COLORS['primary'], padx=16, pady=10)
        self.history_total_label.pack(side='left', padx=(0, 10))
        self.history_patient_label = tk.Label(stats_frame, text="👤 Patient: None", font=('Segoe UI', 10, 'bold'),
                                              bg='white', fg=COLORS['text'], padx=16, pady=10)
        self.history_patient_label.pack(side='left', padx=(0, 10))
        self.history_latest_label = tk.Label(stats_frame, text="🕒 Latest: No record selected", font=('Segoe UI', 10, 'bold'),
                                             bg='white', fg=COLORS['gray_dark'], padx=16, pady=10)
        self.history_latest_label.pack(side='left')

        self.history_display = scrolledtext.ScrolledText(history_card, height=18, width=55, font=('Segoe UI', 10),
                                                         bg='#f8fbfd', fg=COLORS['text'], relief='flat', bd=0,
                                                         wrap='word', padx=18, pady=18, insertbackground=COLORS['primary'])
        self.history_display.pack(pady=(0, 16), padx=16, fill='both', expand=True)
        self.configure_history_display()
        self.render_empty_history_state()

    def create_settings_tab(self):
        """Create the system settings tab for theme and preferences."""
        self.settings_tab = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.settings_tab, text="⚙️ Settings")

        settings_canvas = tk.Canvas(self.settings_tab, bg=COLORS['light_bg'], highlightthickness=0)
        settings_scrollbar = ttk.Scrollbar(self.settings_tab, orient='vertical', command=settings_canvas.yview)
        settings_canvas.configure(yscrollcommand=settings_scrollbar.set)
        settings_scrollbar.pack(side='right', fill='y')
        settings_canvas.pack(side='left', fill='both', expand=True)

        settings_container = tk.Frame(settings_canvas, bg=COLORS['light_bg'])
        settings_window = settings_canvas.create_window((0, 0), window=settings_container, anchor='nw')

        def _on_settings_configure(event):
            settings_canvas.configure(scrollregion=settings_canvas.bbox('all'))
        settings_container.bind('<Configure>', _on_settings_configure)

        def _on_canvas_resize(event):
            settings_canvas.itemconfig(settings_window, width=event.width)
        settings_canvas.bind('<Configure>', _on_canvas_resize)

        def _on_mousewheel(event):
            settings_canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        settings_canvas.bind_all('<MouseWheel>', _on_mousewheel)

        settings_card = tk.Frame(settings_container, bg=COLORS['white'], relief='flat', bd=0)
        settings_card.pack(fill='both', expand=True, padx=16, pady=16)

        banner = tk.Frame(settings_card, bg=COLORS['primary'], height=86)
        banner.pack(fill='x')
        banner.pack_propagate(False)
        tk.Label(banner, text="⚙️", font=('Segoe UI', 28), bg=COLORS['primary'], fg='white').pack(side='left', padx=(18, 10), pady=18)
        banner_text = tk.Frame(banner, bg=COLORS['primary'])
        banner_text.pack(side='left', pady=18)
        tk.Label(banner_text, text="SYSTEM SETTINGS", font=('Segoe UI', 16, 'bold'),
                 bg=COLORS['primary'], fg='white').pack(anchor='w')
        tk.Label(banner_text, text="Customize startup behavior, backup preferences, and accessibility settings.",
                 font=('Segoe UI', 10), bg=COLORS['primary'], fg=COLORS['light_bg']).pack(anchor='w', pady=(4, 0))

        form_frame = tk.Frame(settings_card, bg=COLORS['white'])
        form_frame.pack(fill='both', expand=True, padx=24, pady=24)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=2)

        tk.Label(form_frame, text="🎨 Theme", bg=COLORS['white'], fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, sticky='w', padx=8, pady=8)
        self.theme_option_light = tk.Radiobutton(form_frame, text="Light Theme", variable=self.theme_mode_var, value='light',
                                                bg=COLORS['white'], fg=COLORS['text'], anchor='w', font=('Segoe UI', 10),
                                                activebackground=COLORS['white'], selectcolor=COLORS['light_bg'], command=self.change_theme)
        self.theme_option_light.grid(row=0, column=1, sticky='w', padx=8, pady=4)
        self.theme_option_dark = tk.Radiobutton(form_frame, text="Dark Theme", variable=self.theme_mode_var, value='dark',
                                               bg=COLORS['white'], fg=COLORS['text'], anchor='w', font=('Segoe UI', 10),
                                               activebackground=COLORS['white'], selectcolor=COLORS['light_bg'], command=self.change_theme)
        self.theme_option_dark.grid(row=1, column=1, sticky='w', padx=8, pady=4)

        tk.Label(form_frame, text="🚀 Startup Tab", bg=COLORS['white'], fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=2, column=0, sticky='w', padx=8, pady=8)
        startup_options = [
            'Patient Registration', 'Edit Patients', 'Patient Directory', 'Doctors',
            'Triage Queue', 'Appointments', 'Treatment History', 'Billing',
            'Hospital Operations', 'Lab Orders', 'Pharmacy Inventory', 'Insurance Claims', 'Patient Documents',
            'Department Routing', 'Search Patient', 'Settings'
        ]
        self.startup_choice = ttk.Combobox(form_frame, textvariable=self.startup_tab_var, values=startup_options, state='readonly')
        self.startup_choice.grid(row=2, column=1, sticky='we', padx=8, pady=4)
        self.startup_choice.bind('<<ComboboxSelected>>', lambda _: self.change_startup_tab())

        tk.Label(form_frame, text="💾 Auto Backup", bg=COLORS['white'], fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=3, column=0, sticky='w', padx=8, pady=8)
        self.auto_backup_toggle = tk.Checkbutton(form_frame, text="Backup database on exit", variable=self.auto_backup_var,
                                                 bg=COLORS['white'], fg=COLORS['text'], anchor='w', font=('Segoe UI', 10),
                                                 selectcolor=COLORS['light_bg'], activebackground=COLORS['white'], command=self.change_auto_backup)
        self.auto_backup_toggle.grid(row=3, column=1, sticky='w', padx=8, pady=4)

        tk.Label(form_frame, text="🔠 Font Size", bg=COLORS['white'], fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=4, column=0, sticky='w', padx=8, pady=8)
        font_sizes = ['10', '12', '14', '16']
        self.font_size_choice = ttk.Combobox(form_frame, textvariable=self.font_size_var, values=font_sizes, state='readonly')
        self.font_size_choice.grid(row=4, column=1, sticky='we', padx=8, pady=4)
        self.font_size_choice.bind('<<ComboboxSelected>>', lambda _: self.change_font_size())

        tk.Label(form_frame, text="⚙️ Current Settings", bg=COLORS['white'], fg=COLORS['primary'], font=('Segoe UI', 11, 'bold')).grid(row=5, column=0, sticky='w', padx=8, pady=16)
        self.current_settings_label = tk.Label(form_frame, text=f"Theme: {self.active_theme.title()} · Font: {self.font_size_var.get()} · Startup: {self.startup_tab_var.get()}",
                                              bg=COLORS['white'], fg=COLORS['text'], font=('Segoe UI', 10), wraplength=520, justify='left')
        self.current_settings_label.grid(row=5, column=1, sticky='w', padx=8, pady=16)

        button_frame = tk.Frame(settings_card, bg=COLORS['white'])
        button_frame.pack(fill='x', padx=24, pady=(0, 10))
        ModernButton(button_frame, text="Apply Theme", command=self.change_theme, color='secondary').pack(side='left', padx=6)
        ModernButton(button_frame, text="Refresh UI", command=lambda: self.apply_theme_to_widget(self.root), color='info').pack(side='left', padx=6)

        if self.current_user and self.current_user.get('role') == 'Admin':
            admin_section = tk.LabelFrame(settings_card, text="👥 User Management", bg='#f8fbfd', fg=COLORS['primary'], font=('Segoe UI', 14, 'bold'), relief='groove', bd=1, labelanchor='n')
            admin_section.pack(fill='both', padx=24, pady=(10, 16), expand=True)

            admin_form = tk.Frame(admin_section, bg='#f8fbfd')
            admin_form.pack(fill='x', padx=16, pady=16)
            admin_form.grid_columnconfigure(1, weight=1)

            tk.Label(admin_form, text="Username", bg='#f8fbfd', fg=COLORS['text'], font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=8, pady=4)
            self.new_user_username_var = tk.StringVar()
            tk.Entry(admin_form, textvariable=self.new_user_username_var, font=('Segoe UI', 10), bd=1, relief='solid').grid(row=0, column=1, sticky='ew', padx=8, pady=4)

            tk.Label(admin_form, text="Password", bg='#f8fbfd', fg=COLORS['text'], font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky='w', padx=8, pady=4)
            self.new_user_password_var = tk.StringVar()
            tk.Entry(admin_form, textvariable=self.new_user_password_var, font=('Segoe UI', 10), bd=1, relief='solid', show='*').grid(row=1, column=1, sticky='ew', padx=8, pady=4)

            tk.Label(admin_form, text="Role", bg='#f8fbfd', fg=COLORS['text'], font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky='w', padx=8, pady=4)
            self.new_user_role_var = tk.StringVar(value='Receptionist')
            ttk.Combobox(admin_form, textvariable=self.new_user_role_var, values=USER_ROLES, state='readonly', font=('Segoe UI', 10)).grid(row=2, column=1, sticky='ew', padx=8, pady=4)

            tk.Button(admin_form, text="Create User", command=self.create_user_account, bg=COLORS['secondary'], fg='white', font=('Segoe UI', 10, 'bold'), bd=0, padx=16, pady=8, cursor='hand2').grid(row=3, column=1, sticky='e', padx=8, pady=(12, 4))

            tk.Label(admin_section, text="Existing Users", bg='#f8fbfd', fg=COLORS['text'], font=('Segoe UI', 11, 'bold')).pack(anchor='w', padx=16, pady=(10, 4))
            self.user_listbox = scrolledtext.ScrolledText(admin_section, height=8, font=('Segoe UI', 10), bg='white', fg=COLORS['text'], relief='solid', bd=1)
            self.user_listbox.pack(fill='both', padx=16, pady=(0, 16), expand=True)
            self.user_listbox.config(state='disabled')
            self.refresh_user_list()
        else:
            tk.Label(settings_card, text="User management is available to Admin accounts only.", bg=COLORS['white'], fg=COLORS['gray_dark'], font=('Segoe UI', 10), wraplength=600, justify='left').pack(fill='x', padx=24, pady=(0, 16))

        note_label = tk.Label(settings_card, text="Theme changes and startup preferences are saved and will persist when the app restarts.",
                              bg=COLORS['white'], fg=COLORS['gray_dark'], font=('Segoe UI', 10), wraplength=600, justify='left')
        note_label.pack(fill='x', padx=24, pady=(0, 16))

    def create_routing_tab(self):
        """Department routing using graph"""
        self.routing_tab = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.routing_tab, text="🗺️ Department Routing")
        
        frame = tk.Frame(self.routing_tab, bg=COLORS['light_bg'])
        frame.pack(pady=20, padx=20, fill='both', expand=True)

        route_card = tk.Frame(frame, bg='#eef6fb', relief='flat', bd=1)
        route_card.pack(fill='both', expand=True, padx=10, pady=10)

        banner = tk.Frame(route_card, bg=COLORS['primary'], height=88)
        banner.pack(fill='x')
        banner.pack_propagate(False)
        tk.Label(banner, text="🗺️", font=('Segoe UI', 26), bg=COLORS['primary'], fg='white').pack(side='left', padx=(18, 10), pady=18)
        banner_text = tk.Frame(banner, bg=COLORS['primary'])
        banner_text.pack(side='left', pady=16)
        tk.Label(banner_text, text="DEPARTMENT ROUTING", font=('Segoe UI', 16, 'bold'),
                 bg=COLORS['primary'], fg='white').pack(anchor='w')
        tk.Label(banner_text, text="Find the quickest route between two departments for staff or patient movement",
                 font=('Segoe UI', 10), bg=COLORS['primary'], fg=COLORS['light_bg']).pack(anchor='w', pady=(3, 0))

        input_card = tk.Frame(route_card, bg='white', relief='flat', bd=0)
        input_card.pack(pady=16, padx=16, fill='x')
        input_inner = tk.Frame(input_card, bg='white')
        input_inner.pack(pady=16, padx=16, fill='x')
        
        tk.Label(input_inner, text="📍 From Department", bg='white', font=('Segoe UI', 11, 'bold'), fg=COLORS['primary']).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.from_dept = ttk.Combobox(input_inner, values=self.hospital_map.get_all_departments(), 
                                      width=30, font=('Segoe UI', 10))
        self.from_dept.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(input_inner, text="🎯 To Department", bg='white', font=('Segoe UI', 11, 'bold'), fg=COLORS['primary']).grid(row=0, column=2, padx=10, pady=10, sticky='w')
        self.to_dept = ttk.Combobox(input_inner, values=self.hospital_map.get_all_departments(), 
                                    width=30, font=('Segoe UI', 10))
        self.to_dept.grid(row=0, column=3, padx=10, pady=10)
        
        ModernButton(input_inner, text="🗺️ Find Shortest Path", command=self.find_shortest_path, 
                    color='secondary').grid(row=0, column=4, padx=20)
        
        self.path_result = scrolledtext.ScrolledText(route_card, height=12, width=90, font=('Segoe UI', 10),
                                                     bg='#f8fbfd', fg=COLORS['text'], relief='flat', bd=0,
                                                     padx=16, pady=16, wrap='word')
        self.path_result.pack(pady=(0, 14), padx=16, fill='both', expand=True)
        self.configure_path_display()
        
        info_frame = tk.Frame(route_card, bg='#eef6fb')
        info_frame.pack(pady=(0, 14))
        tk.Label(info_frame, text="📍 Available Departments:", bg='#eef6fb', 
                font=('Segoe UI', 10, 'bold')).pack()
        dept_list = " → ".join(self.hospital_map.get_all_departments())
        tk.Label(info_frame, text=dept_list, bg='#eef6fb', wraplength=700, 
                font=('Segoe UI', 9), fg=COLORS['gray_dark']).pack()
    
    def create_search_tab(self):
        """Search for patient records"""
        self.search_tab = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.search_tab, text="🔍 Search Patient")
        
        frame = tk.Frame(self.search_tab, bg=COLORS['light_bg'])
        frame.pack(fill='both', expand=True, pady=20, padx=20)

        search_shell = tk.Frame(frame, bg='#eef6fb', relief='flat', bd=1)
        search_shell.pack(fill='both', expand=True, padx=10, pady=10)

        banner = tk.Frame(search_shell, bg=COLORS['info_dark'], height=88)
        banner.pack(fill='x')
        banner.pack_propagate(False)
        tk.Label(banner, text="🔍", font=('Segoe UI', 26), bg=COLORS['info_dark'], fg='white').pack(side='left', padx=(18, 10), pady=18)
        banner_text = tk.Frame(banner, bg=COLORS['info_dark'])
        banner_text.pack(side='left', pady=16)
        tk.Label(banner_text, text="SEARCH PATIENT RECORD", font=('Segoe UI', 16, 'bold'),
                 bg=COLORS['info_dark'], fg='white').pack(anchor='w')
        tk.Label(banner_text, text="Open a quick patient summary with appointments and recent treatment information",
                 font=('Segoe UI', 10), bg=COLORS['info_dark'], fg='#dbeef8').pack(anchor='w', pady=(3, 0))

        search_card = tk.Frame(search_shell, bg='white', relief='flat', bd=0)
        search_card.pack(pady=16, padx=16, fill='x')
        search_inner = tk.Frame(search_card, bg='white')
        search_inner.pack(pady=16, padx=16, fill='x')
        
        tk.Label(search_inner, text="🔎 Patient ID / Name", bg='white', 
                font=('Segoe UI', 12, 'bold'), fg=COLORS['primary']).pack(side='left', padx=10)
        self.search_var = tk.StringVar()
        self.search_combo = ttk.Combobox(
            search_inner,
            textvariable=self.search_var,
            width=30,
            font=('Segoe UI', 12),
            state='normal',
            postcommand=self.update_search_patient_dropdown
        )
        self.search_combo.pack(side='left', padx=10)
        ModernButton(search_inner, text="🔍 Search", command=self.search_patient, 
                    color='info').pack(side='left', padx=10)
        ModernButton(search_inner, text="🖨 Export / Print", command=self.export_patient_record_report,
                    color='primary').pack(side='left', padx=10)

        self.search_result = scrolledtext.ScrolledText(search_shell, height=20, width=90, font=('Segoe UI', 10),
                                                       bg='#f8fbfd', fg=COLORS['text'], relief='flat', bd=0,
                                                       padx=16, pady=16, wrap='word')
        self.search_result.pack(pady=(0, 16), padx=16, fill='both', expand=True)
        self.configure_search_display()

    def configure_history_display(self):
        """Configure styled tags for the treatment history viewer."""
        self.history_display.tag_configure("section_title", font=('Segoe UI', 15, 'bold'), foreground=COLORS['primary'])
        self.history_display.tag_configure("section_subtitle", font=('Segoe UI', 10), foreground=COLORS['gray_dark'])
        self.history_display.tag_configure("record_badge", font=('Segoe UI', 9, 'bold'), foreground='white', background=COLORS['secondary_dark'])
        self.history_display.tag_configure("record_title", font=('Segoe UI', 11, 'bold'), foreground=COLORS['text'])
        self.history_display.tag_configure("meta", font=('Segoe UI', 10), foreground=COLORS['info_dark'])
        self.history_display.tag_configure("treatment", font=('Segoe UI', 10), foreground=COLORS['text'], lmargin1=18, lmargin2=18, spacing1=4, spacing3=10)
        self.history_display.tag_configure("divider", foreground=COLORS['border'])
        self.history_display.tag_configure("empty_icon", font=('Segoe UI', 30), foreground=COLORS['gray'])
        self.history_display.tag_configure("empty_title", font=('Segoe UI', 14, 'bold'), foreground=COLORS['primary'])
        self.history_display.tag_configure("empty_text", font=('Segoe UI', 10), foreground=COLORS['gray_dark'], justify='center')

    def update_history_summary(self, total_records=0, patient_label="None", latest_label="No record selected"):
        """Update the small summary cards above the history viewer."""
        self.history_total_label.config(text=f"📋 Records: {total_records}")
        self.history_patient_label.config(text=f"👤 Patient: {patient_label}")
        self.history_latest_label.config(text=f"🕒 Latest: {latest_label}")

    def render_empty_history_state(self):
        """Render an empty state when no history is selected."""
        self.history_display.delete(1.0, tk.END)
        self.history_display.insert(tk.END, "\n\n🩺\n", "empty_icon")
        self.history_display.insert(tk.END, "Treatment history ready\n", "empty_title")
        self.history_display.insert(tk.END, "Search by patient ID to view a single patient record,\nor use Show All to browse the full treatment register.", "empty_text")
        self.update_history_summary()

    def render_history_entries(self, heading, subtitle, entries):
        """Render styled treatment entries inside the history viewer."""
        self.history_display.delete(1.0, tk.END)
        self.history_display.insert(tk.END, f"{heading}\n", "section_title")
        self.history_display.insert(tk.END, f"{subtitle}\n\n", "section_subtitle")

        for index, entry in enumerate(entries, 1):
            self.history_display.insert(tk.END, f"  RECORD {index}  ", "record_badge")
            self.history_display.insert(tk.END, "\n")
            self.history_display.insert(tk.END, f"📅 {entry['date']}\n", "record_title")
            self.history_display.insert(tk.END, f"👨‍⚕️ Doctor: {entry['doctor']}\n", "meta")
            self.history_display.insert(tk.END, f"💊 Treatment Notes:\n{entry['treatment'].strip()}\n", "treatment")
            if index != len(entries):
                self.history_display.insert(tk.END, "─" * 64 + "\n\n", "divider")

    def show_all_treatment_history(self):
        """Show all treatment records across patients with a richer display."""
        all_histories = self.patient_treatments.get_all_histories()
        entries = []
        for patient_id, treatments in all_histories.items():
            for treatment in treatments:
                entries.append({
                    'patient_id': patient_id,
                    'date': treatment['date'],
                    'doctor': treatment['doctor'],
                    'treatment': treatment['treatment']
                })

        if not entries:
            self.render_empty_history_state()
            self.update_status("No treatment history available")
            return

        entries.sort(key=lambda item: item['date'], reverse=True)
        display_entries = []
        for item in entries:
            display_entries.append({
                'date': f"{item['date']}  •  Patient {item['patient_id']}",
                'doctor': item['doctor'],
                'treatment': item['treatment']
            })

        latest = entries[0]['date']
        self.render_history_entries(
            "All Treatment Records",
            f"Showing {len(entries)} recorded treatments across {len(all_histories)} patient file(s).",
            display_entries
        )
        self.update_history_summary(len(entries), "All Patients", latest)
        self.update_status("Showing all treatment history")

    def configure_schedule_display(self):
        """Apply light formatting to the weekly schedule output."""
        self.schedule_display.tag_configure("schedule_title", font=('Segoe UI', 14, 'bold'), foreground=COLORS['primary'])
        self.schedule_display.tag_configure("schedule_day", font=('Segoe UI', 11, 'bold'), foreground=COLORS['info_dark'])
        self.schedule_display.tag_configure("schedule_body", font=('Consolas', 9), foreground=COLORS['text'])

    def configure_path_display(self):
        """Apply light formatting to the routing result output."""
        self.path_result.tag_configure("path_title", font=('Segoe UI', 14, 'bold'), foreground=COLORS['primary'])
        self.path_result.tag_configure("path_meta", font=('Segoe UI', 11, 'bold'), foreground=COLORS['info_dark'])
        self.path_result.tag_configure("path_route", font=('Segoe UI', 11), foreground=COLORS['text'], spacing1=4, spacing3=6)
        self.path_result.tag_configure("path_empty", font=('Segoe UI', 11), foreground=COLORS['gray_dark'])

    def configure_search_display(self):
        """Apply light formatting to the patient search result output."""
        self.search_result.tag_configure("search_title", font=('Segoe UI', 14, 'bold'), foreground=COLORS['primary'])
        self.search_result.tag_configure("search_label", font=('Segoe UI', 10, 'bold'), foreground=COLORS['info_dark'])
        self.search_result.tag_configure("search_value", font=('Segoe UI', 10), foreground=COLORS['text'])
        self.search_result.tag_configure("search_section", font=('Segoe UI', 11, 'bold'), foreground=COLORS['primary'], spacing1=8)
        self.search_result.tag_configure("search_empty", font=('Segoe UI', 10), foreground=COLORS['gray_dark'])

    def configure_billing_display(self):
        """Apply light formatting to billing details."""
        self.billing_display.tag_configure("billing_title", font=('Segoe UI', 14, 'bold'), foreground=COLORS['primary'])
        self.billing_display.tag_configure("billing_label", font=('Segoe UI', 10, 'bold'), foreground=COLORS['info_dark'])
        self.billing_display.tag_configure("billing_value", font=('Segoe UI', 10), foreground=COLORS['text'])
        self.billing_display.tag_configure("billing_note", font=('Segoe UI', 10), foreground=COLORS['gray_dark'])
        self.billing_display.tag_configure("billing_paid", font=('Segoe UI', 10, 'bold'), foreground=COLORS['secondary_dark'])
        self.billing_display.tag_configure("billing_unpaid", font=('Segoe UI', 10, 'bold'), foreground=COLORS['danger'])

    def configure_doctor_table_style(self):
        """Apply light styling to the doctor directory table."""
        style = ttk.Style()
        style.configure(
            "DoctorDirectory.Treeview",
            background='white',
            fieldbackground='white',
            foreground=COLORS['text'],
            rowheight=30,
            font=('Segoe UI', 10),
            borderwidth=0
        )
        style.map("DoctorDirectory.Treeview", background=[('selected', '#d7ebf7')], foreground=[('selected', COLORS['text'])])
        style.configure(
            "DoctorDirectory.Treeview.Heading",
            background='#dbeaf4',
            foreground=COLORS['primary'],
            font=('Segoe UI', 10, 'bold'),
            relief='flat',
            padding=(8, 8)
        )
        style.map(
            "DoctorDirectory.Treeview.Heading",
            background=[('active', '#cfe2ef')],
            foreground=[('active', COLORS['primary'])]
        )

    def configure_patient_directory_table_style(self):
        """Apply light styling to the patient directory table."""
        style = ttk.Style()
        style.configure(
            "PatientDirectory.Treeview",
            background='white',
            fieldbackground='white',
            foreground=COLORS['text'],
            rowheight=30,
            font=('Segoe UI', 10),
            borderwidth=0
        )
        style.map("PatientDirectory.Treeview", background=[('selected', '#d7ebf7')], foreground=[('selected', COLORS['text'])])
        style.configure(
            "PatientDirectory.Treeview.Heading",
            background='#dbeaf4',
            foreground=COLORS['primary'],
            font=('Segoe UI', 10, 'bold'),
            relief='flat',
            padding=(8, 8)
        )
        style.map(
            "PatientDirectory.Treeview.Heading",
            background=[('active', '#cfe2ef')],
            foreground=[('active', COLORS['primary'])]
        )

    def configure_edit_patient_table_style(self):
        """Apply light styling to the edit patient table."""
        style = ttk.Style()
        style.configure(
            "EditPatient.Treeview",
            background='white',
            fieldbackground='white',
            foreground=COLORS['text'],
            rowheight=30,
            font=('Segoe UI', 10),
            borderwidth=0
        )
        style.map("EditPatient.Treeview", background=[('selected', '#d7ebf7')], foreground=[('selected', COLORS['text'])])
        style.configure(
            "EditPatient.Treeview.Heading",
            background='#dbeaf4',
            foreground=COLORS['primary'],
            font=('Segoe UI', 10, 'bold'),
            relief='flat',
            padding=(8, 8)
        )
        style.map(
            "EditPatient.Treeview.Heading",
            background=[('active', '#cfe2ef')],
            foreground=[('active', COLORS['primary'])]
        )
    
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

    def generate_doctor_id(self):
        """Generate the next doctor id"""
        self.last_doctor_number += 1
        return f"{self.last_doctor_number:03d}"

    def update_doctor_id_display(self):
        """Show the next doctor id without incrementing"""
        if hasattr(self, 'doctor_id_entry'):
            next_id = f"{self.last_doctor_number + 1:03d}"
            self.doctor_id_entry.configure(state='normal')
            self.doctor_id_entry.delete(0, tk.END)
            self.doctor_id_entry.insert(0, next_id)
            self.doctor_id_entry.configure(state='readonly')
    
    def validate_contact(self, contact):
        """Validate contact number (10 digits)"""
        return contact.isdigit() and len(contact) == 10

    def sanitize_filename(self, text):
        """Create a safe filename from a label"""
        clean = re.sub(r'[^A-Za-z0-9._-]+', '_', text.strip())
        return clean.strip('_') or "report"

    def normalize_export_text(self, content, ascii_only=False):
        """Normalize UI text for export formats"""
        replacements = {
            "→": "->",
            "•": "-",
            "✓": "[OK]",
            "✗": "[X]",
            "⚠": "[!]",
            "📊": "[Stats]",
            "📅": "[Date]",
            "📞": "[Contact]",
            "🆔": "[ID]",
            "👤": "[Name]",
            "🩸": "[Blood]",
            "💊": "[Treatment]",
            "👨‍⚕️": "[Doctor]",
            "🚑": "[Triage]",
            "🚨": "[Emergency]",
            "📍": "[From]",
            "🎯": "[To]",
            "🚶": "[Route]",
            "📏": "[Distance]",
            "⏱️": "[Time]",
            "🏥": "[Hospital]",
            "✨": "[Features]",
            "🗄️": "[Database]"
        }

        normalized = content.replace("\r\n", "\n")
        for old, new in replacements.items():
            normalized = normalized.replace(old, new)

        if ascii_only:
            normalized = normalized.encode("ascii", "ignore").decode("ascii")

        return normalized

    def write_text_file(self, filepath, content):
        """Write plain text export"""
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

    def write_pdf_file(self, filepath, title, content):
        """Write a styled PDF report without external libraries"""
        normalized_title = self.normalize_export_text(title, ascii_only=True)
        normalized_content = self.normalize_export_text(content, ascii_only=True)

        page_width = 595
        page_height = 842
        margin = 42
        content_left = 56
        content_right = page_width - 56
        header_height = 86
        footer_height = 34
        body_top = page_height - header_height - 34
        body_bottom = margin + footer_height + 12
        body_width = content_right - content_left
        line_height = 15
        chars_per_line = 84

        def escape_pdf_text(text):
            return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

        def wrap_line(text, limit):
            words = text.split()
            if not words:
                return [""]

            wrapped = []
            current = words[0]

            for word in words[1:]:
                candidate = f"{current} {word}"
                if len(candidate) <= limit:
                    current = candidate
                else:
                    wrapped.append(current)
                    current = word

            wrapped.append(current)
            return wrapped

        formatted_lines = []
        for raw_line in normalized_content.splitlines():
            stripped = raw_line.strip()

            if not stripped:
                formatted_lines.append({"text": "", "style": "spacer"})
                continue

            if set(stripped) == {"="} or set(stripped) == {"-"}:
                formatted_lines.append({"text": "", "style": "divider"})
                continue

            is_heading = stripped == stripped.upper() and any(char.isalpha() for char in stripped) and len(stripped) <= 48
            wrapped_lines = wrap_line(stripped, chars_per_line)

            for index, wrapped in enumerate(wrapped_lines):
                style = "heading" if is_heading and index == 0 else "body"
                formatted_lines.append({"text": wrapped, "style": style})

        if not formatted_lines:
            formatted_lines = [{"text": "No report content available.", "style": "body"}]

        pages = []
        current_page = []
        current_y = body_top

        for item in formatted_lines:
            if item["style"] == "spacer":
                required_height = 8
            elif item["style"] == "divider":
                required_height = 12
            elif item["style"] == "heading":
                required_height = 20
            else:
                required_height = line_height

            if current_page and current_y - required_height < body_bottom:
                pages.append(current_page)
                current_page = []
                current_y = body_top

            current_page.append(item)
            current_y -= required_height

        if current_page:
            pages.append(current_page)

        objects = []

        def add_object(body):
            objects.append(body)
            return len(objects)

        font_obj = add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
        bold_font_obj = add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
        page_ids = []
        content_ids = []

        generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        for page_number, page_lines in enumerate(pages, start=1):
            content_stream = [
                "q",
                "0.17 0.37 0.54 rg",
                f"{margin} {page_height - margin - header_height} {page_width - (margin * 2)} {header_height} re f",
                "0.93 0.96 0.98 rg",
                f"{margin} {body_bottom - 12} {page_width - (margin * 2)} {body_top - body_bottom + 28} re f",
                "0.80 0.87 0.92 RG",
                "1 w",
                f"{margin} {body_bottom - 12} {page_width - (margin * 2)} {body_top - body_bottom + 28} re S",
                "BT",
                "1 1 1 rg",
                f"/F2 20 Tf 1 0 0 1 {content_left} {page_height - margin - 30} Tm",
                f"({escape_pdf_text('MediStruct')}) Tj",
                f"/F1 10 Tf 1 0 0 1 {content_left} {page_height - margin - 48} Tm",
                f"({escape_pdf_text(normalized_title)}) Tj",
                f"1 0 0 1 {content_left} {page_height - margin - 64} Tm",
                f"(Generated on: {escape_pdf_text(generated_at)}) Tj",
                "0.17 0.37 0.54 rg",
                f"/F1 9 Tf 1 0 0 1 {page_width - 118} {page_height - margin - 64} Tm",
                f"(Page {page_number} of {len(pages)}) Tj",
                "ET"
            ]

            current_y = body_top
            for item in page_lines:
                if item["style"] == "spacer":
                    current_y -= 8
                    continue

                if item["style"] == "divider":
                    line_y = current_y - 4
                    content_stream.extend([
                        "0.78 0.84 0.89 RG",
                        "0.8 w",
                        f"{content_left} {line_y} m {content_right} {line_y} l S"
                    ])
                    current_y -= 12
                    continue

                if item["style"] == "heading":
                    content_stream.extend([
                        "BT",
                        "0.17 0.37 0.54 rg",
                        f"/F2 12 Tf 1 0 0 1 {content_left} {current_y} Tm",
                        f"({escape_pdf_text(item['text'])}) Tj",
                        "ET"
                    ])
                    current_y -= 20
                    continue

                content_stream.extend([
                    "BT",
                    "0.16 0.19 0.24 rg",
                    f"/F1 10.5 Tf 1 0 0 1 {content_left} {current_y} Tm",
                    f"({escape_pdf_text(item['text'])}) Tj",
                    "ET"
                ])
                current_y -= line_height

            content_stream.extend([
                "BT",
                "0.45 0.50 0.54 rg",
                f"/F1 9 Tf 1 0 0 1 {content_left} {margin - 2} Tm",
                f"(Confidential hospital report - {escape_pdf_text(normalized_title)}) Tj",
                "ET",
                "Q"
            ])

            stream_text = "\n".join(content_stream)
            content_id = add_object(f"<< /Length {len(stream_text.encode('latin-1'))} >>\nstream\n{stream_text}\nendstream")
            content_ids.append(content_id)
            page_ids.append(add_object(""))

        pages_obj = add_object("")
        catalog_obj = add_object(f"<< /Type /Catalog /Pages {pages_obj} 0 R >>")

        for index, page_id in enumerate(page_ids):
            objects[page_id - 1] = (
                f"<< /Type /Page /Parent {pages_obj} 0 R /MediaBox [0 0 {page_width} {page_height}] "
                f"/Resources << /Font << /F1 {font_obj} 0 R /F2 {bold_font_obj} 0 R >> >> /Contents {content_ids[index]} 0 R >>"
            )

        kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
        objects[pages_obj - 1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>"

        pdf_parts = ["%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"]
        offsets = []
        byte_count = len(pdf_parts[0].encode("latin-1"))

        for obj_id, body in enumerate(objects, start=1):
            offsets.append(byte_count)
            chunk = f"{obj_id} 0 obj\n{body}\nendobj\n"
            pdf_parts.append(chunk)
            byte_count += len(chunk.encode("latin-1"))

        xref_offset = byte_count
        xref = [f"xref\n0 {len(objects) + 1}\n", "0000000000 65535 f \n"]
        xref.extend(f"{offset:010d} 00000 n \n" for offset in offsets)
        trailer = (
            f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_obj} 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF"
        )
        pdf_parts.extend(xref)
        pdf_parts.append(trailer)

        with open(filepath, "wb") as file:
            file.write("".join(pdf_parts).encode("latin-1"))

    def write_docx_file(self, filepath, title, content):
        """Write a minimal DOCX file without external libraries"""
        normalized_title = self.normalize_export_text(title)
        normalized_content = self.normalize_export_text(content)

        paragraphs = [normalized_title, ""]
        paragraphs.extend(normalized_content.splitlines() or [""])

        document_lines = []
        for line in paragraphs:
            safe_text = escape(line)
            document_lines.append(
                "<w:p><w:r><w:t xml:space=\"preserve\">"
                f"{safe_text}"
                "</w:t></w:r></w:p>"
            )

        document_xml = (
            "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
            "<w:document xmlns:wpc=\"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas\" "
            "xmlns:mc=\"http://schemas.openxmlformats.org/markup-compatibility/2006\" "
            "xmlns:o=\"urn:schemas-microsoft-com:office:office\" "
            "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\" "
            "xmlns:m=\"http://schemas.openxmlformats.org/officeDocument/2006/math\" "
            "xmlns:v=\"urn:schemas-microsoft-com:vml\" "
            "xmlns:wp14=\"http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing\" "
            "xmlns:wp=\"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing\" "
            "xmlns:w10=\"urn:schemas-microsoft-com:office:word\" "
            "xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\" "
            "xmlns:w14=\"http://schemas.microsoft.com/office/word/2010/wordml\" "
            "xmlns:wpg=\"http://schemas.microsoft.com/office/word/2010/wordprocessingGroup\" "
            "xmlns:wpi=\"http://schemas.microsoft.com/office/word/2010/wordprocessingInk\" "
            "xmlns:wne=\"http://schemas.microsoft.com/office/word/2006/wordml\" "
            "xmlns:wps=\"http://schemas.microsoft.com/office/word/2010/wordprocessingShape\" "
            "mc:Ignorable=\"w14 wp14\">"
            "<w:body>"
            + "".join(document_lines) +
            "<w:sectPr><w:pgSz w:w=\"12240\" w:h=\"15840\"/><w:pgMar w:top=\"1440\" w:right=\"1440\" "
            "w:bottom=\"1440\" w:left=\"1440\" w:header=\"708\" w:footer=\"708\" w:gutter=\"0\"/></w:sectPr>"
            "</w:body></w:document>"
        )

        content_types_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>"""

        rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

        with zipfile.ZipFile(filepath, "w", zipfile.ZIP_DEFLATED) as docx_file:
            docx_file.writestr("[Content_Types].xml", content_types_xml)
            docx_file.writestr("_rels/.rels", rels_xml)
            docx_file.writestr("word/document.xml", document_xml)

    def save_report_to_file(self, title, content, default_name):
        """Save report content as TXT, PDF, or DOCX"""
        if not content.strip():
            SilentMessageBox.show_warning("Nothing to Export", "No content available to export.", self.root)
            return None

        filename = filedialog.asksaveasfilename(
            parent=self.root,
            title="Export Report",
            defaultextension=".pdf",
            initialfile=self.sanitize_filename(default_name),
            filetypes=[
                ("PDF file", "*.pdf"),
                ("Word document", "*.docx"),
                ("Text file", "*.txt")
            ]
        )

        if not filename:
            return None

        extension = os.path.splitext(filename)[1].lower()
        try:
            if extension == ".pdf":
                self.write_pdf_file(filename, title, content)
            elif extension == ".docx":
                self.write_docx_file(filename, title, content)
            else:
                self.write_text_file(filename, self.normalize_export_text(content))

            return filename
        except Exception as e:
            SilentMessageBox.show_error("Export Failed", f"❌ Could not export file:\n{e}", self.root)
            return None

    def print_exported_file(self, filepath):
        """Send an exported file to the system print command on Windows"""
        try:
            if sys.platform == "win32":
                os.startfile(filepath, "print")
                self.update_status(f"Sent to printer: {os.path.basename(filepath)}")
                return True

            SilentMessageBox.show_info("Print Not Supported", "Printing is currently supported on Windows only.", self.root)
            return False
        except Exception as e:
            SilentMessageBox.show_error("Print Failed", f"❌ Could not print file:\n{e}", self.root)
            return False

    def export_report(self, title, content, default_name, offer_print=True):
        """Export current screen content and optionally print it"""
        filepath = self.save_report_to_file(title, content, default_name)
        if not filepath:
            return

        self.update_status(f"Exported report: {os.path.basename(filepath)}")

        if offer_print and SilentMessageBox.ask_question("Print Report", "File exported successfully.\n\nPrint it now?", self.root):
            self.print_exported_file(filepath)
        else:
            SilentMessageBox.show_info("Export Complete", f"✅ Report saved to:\n{filepath}", self.root)

    def get_text_widget_content(self, widget):
        """Read content from text-based widgets"""
        return widget.get(1.0, tk.END).strip()
    
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
        if hasattr(self, 'update_edit_patient_list'):
            self.update_edit_patient_list()
        if hasattr(self, 'update_doctor_list_display'):
            self.update_doctor_list_display()
        self.update_queue_display()
        self.update_schedule_display()
        if hasattr(self, 'update_billing_display'):
            self.update_billing_display()
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
                    f"✅ Patient {name} registered successfully!\n\n🆔 Patient ID: {patient_id}\n💾 Saved securely", self.root)
                
                self.clear_registration_form()
                self.update_patient_list_display()
                if hasattr(self, 'update_edit_patient_list'):
                    self.update_edit_patient_list()
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

    def update_edit_patient_list(self):
        """Show patients available for editing"""
        patients = self.patient_db.get_all()
        for item in self.edit_patient_display.get_children():
            self.edit_patient_display.delete(item)

        if not patients:
            return

        for index, patient in enumerate(patients):
            self.edit_patient_display.insert(
                '',
                'end',
                values=(
                    patient.patient_id,
                    patient.name,
                    patient.contact,
                    patient.blood_group
                ),
                tags=('evenrow' if index % 2 == 0 else 'oddrow',)
            )
        self.edit_patient_display.tag_configure('evenrow', background='white')
        self.edit_patient_display.tag_configure('oddrow', background='#f4f9fc')

    def get_edit_patient_id(self):
        """Return the selected patient ID from the edit dropdown."""
        selected_value = self.edit_patient_id_var.get().strip()
        if ' - ' in selected_value:
            return selected_value.split(' - ', 1)[0].upper()
        return selected_value.upper()

    def update_edit_patient_dropdown(self, patients=None):
        """Populate the edit patient dropdown with patient IDs and names."""
        patients = patients if patients is not None else self.patient_db.get_all()
        sorted_patients = sorted(patients, key=lambda p: p.patient_id)
        self.edit_pid_combo['values'] = [f"{p.patient_id} - {p.name}" for p in sorted_patients]

    def search_edit_patients(self):
        """Search patients by ID or name for the edit dropdown."""
        search_term = self.edit_patient_search_entry.get().strip()
        if not search_term:
            self.update_edit_patient_dropdown()
            return

        matches = [
            patient for patient in self.patient_db.get_all()
            if search_term.lower() in patient.patient_id.lower() or search_term.lower() in patient.name.lower()
        ]
        self.update_edit_patient_dropdown(matches)
        if matches:
            self.edit_patient_id_var.set(f"{matches[0].patient_id} - {matches[0].name}")
            self.update_status(f"Found {len(matches)} patient(s); selected first match.")
        else:
            self.edit_patient_id_var.set("")
            SilentMessageBox.show_error("No patient", f"❌ No patient found for '{search_term}'.", self.root)

    def load_patient_for_edit(self):
        """Load an existing patient into the edit form"""
        pid = self.get_edit_patient_id()
        if not pid:
            SilentMessageBox.show_error("Error", "❌ Select or enter Patient ID to load!", self.root)
            return

        patient = self.patient_db.lookup(pid)
        if not patient:
            SilentMessageBox.show_error("Error", f"❌ Patient {pid} not found!", self.root)
            return

        self.edit_name_entry.delete(0, tk.END)
        self.edit_name_entry.insert(0, patient.name)
        self.edit_age_entry.delete(0, tk.END)
        self.edit_age_entry.insert(0, patient.age)
        self.edit_contact_entry.delete(0, tk.END)
        self.edit_contact_entry.insert(0, patient.contact)
        self.edit_blood_group_var.set(patient.blood_group)
        self.edit_allergies_entry.delete(0, tk.END)
        self.edit_allergies_entry.insert(0, patient.allergies)
        self.update_status(f"Loaded patient {pid} for editing")

    def open_edit_patient_from_directory(self):
        """Open the edit patient tab from the patient directory toolbar."""
        search_term = self.patient_search_entry.get().strip()
        self.notebook.select(self.edit_patient_tab)

        if not search_term:
            self.edit_pid_combo.focus()
            return

        patient = self.patient_db.lookup(search_term.upper())
        if not patient:
            matches = [p for p in self.patient_db.get_all() if search_term.lower() in p.name.lower()]
            if len(matches) == 1:
                patient = matches[0]

        if patient:
            self.edit_patient_id_var.set(f"{patient.patient_id} - {patient.name}")
            self.load_patient_for_edit()
        else:
            self.edit_patient_id_var.set(search_term.upper())
            self.edit_pid_combo.focus()

    def save_patient_changes(self):
        """Save edited patient details"""
        pid = self.get_edit_patient_id()
        name = self.edit_name_entry.get().strip()
        age = self.edit_age_entry.get().strip()
        contact = self.edit_contact_entry.get().strip()
        blood_group = self.edit_blood_group_var.get().strip()
        allergies = self.edit_allergies_entry.get().strip()

        if not pid or not name or not age or not contact or not blood_group:
            SilentMessageBox.show_error("Error", "❌ Load a patient and fill all required fields!", self.root)
            return
        if not age.isdigit() or int(age) < 0 or int(age) > 150:
            SilentMessageBox.show_error("Error", "❌ Please enter a valid age (0-150)!", self.root)
            return
        if not self.validate_contact(contact):
            SilentMessageBox.show_error("Error", "❌ Contact must be exactly 10 digits!", self.root)
            return

        patient = PatientRecord(pid, name, age, contact, blood_group, allergies)
        self.patient_db.insert(patient)
        if self.db.update_patient(pid, name, age, contact, blood_group, allergies):
            SilentMessageBox.show_info("Saved", f"✅ Patient {pid} updated successfully.", self.root)
            self.update_edit_patient_list()
            self.update_patient_list_display()
            self.update_status(f"Updated patient {pid}")
        else:
            SilentMessageBox.show_error("Error", "❌ Failed to update patient record.", self.root)

    def clear_edit_patient_form(self):
        """Clear the edit patient form"""
        self.edit_patient_id_var.set("")
        if hasattr(self, 'edit_patient_search_entry'):
            self.edit_patient_search_entry.delete(0, tk.END)
        self.edit_name_entry.delete(0, tk.END)
        self.edit_age_entry.delete(0, tk.END)
        self.edit_contact_entry.delete(0, tk.END)
        self.edit_blood_group_var.set("")
        self.edit_allergies_entry.delete(0, tk.END)

    def update_doctor_list_display(self, doctors=None):
        """Refresh doctor directory"""
        doctors = doctors if doctors is not None else self.db.get_all_doctors()
        for item in self.doctor_display.get_children():
            self.doctor_display.delete(item)

        for index, doctor in enumerate(doctors):
            self.doctor_display.insert(
                '',
                'end',
                values=(
                    doctor['doctor_id'],
                    doctor['name'],
                    doctor['specialty'] or 'Not set',
                    doctor['contact'] or 'Not set',
                    doctor['availability'] or 'Not set'
                ),
                tags=('evenrow' if index % 2 == 0 else 'oddrow',)
            )

        self.doctor_display.tag_configure('evenrow', background='white')
        self.doctor_display.tag_configure('oddrow', background='#f4f9fc')

    def update_treatment_doctor_dropdown(self):
        """Load doctor names into the treatment form dropdown."""
        doctors = self.db.get_all_doctors()
        doctor_values = [f"{doctor['name']} ({doctor['specialty']})" for doctor in doctors]
        self.treatment_doctor_combo['values'] = doctor_values
        if doctor_values:
            self.treatment_doctor_combo.set(doctor_values[0])
        else:
            self.treatment_doctor_combo.set("")

    def search_doctors_display(self):
        """Search doctor directory"""
        search_term = self.doctor_search_entry.get().strip()
        if not search_term:
            self.update_doctor_list_display()
            return
        self.update_doctor_list_display(self.db.search_doctors(search_term))

    def save_doctor_record(self):
        """Save doctor details"""
        doctor_id = self.generate_doctor_id()
        name = self.doctor_name_entry.get().strip()
        specialty = self.doctor_specialty_entry.get().strip()
        contact = self.doctor_contact_entry.get().strip()
        availability = self.doctor_availability_entry.get().strip()

        if not name or not specialty:
            self.last_doctor_number -= 1
            SilentMessageBox.show_error("Error", "❌ Name and specialty are required!", self.root)
            return

        if self.db.save_doctor(doctor_id, name, specialty, contact, availability):
            SilentMessageBox.show_info("Saved", f"✅ Doctor {name} saved successfully.", self.root)
            self.clear_doctor_form()
            self.update_doctor_list_display()
            if hasattr(self, 'update_treatment_doctor_dropdown'):
                self.update_treatment_doctor_dropdown()
            self.update_status(f"Saved doctor {doctor_id}")
        else:
            self.last_doctor_number -= 1
            SilentMessageBox.show_error("Error", "❌ Failed to save doctor record.", self.root)

    def clear_doctor_form(self):
        """Clear doctor management inputs"""
        self.doctor_name_entry.delete(0, tk.END)
        self.doctor_specialty_entry.delete(0, tk.END)
        self.doctor_contact_entry.delete(0, tk.END)
        self.doctor_availability_entry.delete(0, tk.END)
        self.update_doctor_id_display()

    def update_billing_display(self, bills=None):
        """Refresh billing list and summary"""
        bills = bills if bills is not None else self.db.get_all_bills()
        self.bill_listbox.delete(0, tk.END)
        self.billing_display.delete(1.0, tk.END)
        self.bill_index_map = []

        if not bills:
            self.billing_display.insert(tk.END, "No billing records available yet.")
            self.bill_selected_label.config(text="Selected Bill ID: None")
            self.selected_bill_id_var.set("")
            return

        total_outstanding = 0.0
        for bill in bills:
            is_paid = bill['status'] == 'Paid'
            status_icon = "✅" if is_paid else "🕒"
            status_text = "Paid" if is_paid else "Unpaid"
            label = f"{status_icon}  {bill['id']}  {bill['patient_id']}  {bill['service']}  KES {bill['amount']:.2f}  [{status_text}]"
            self.bill_listbox.insert(tk.END, label)
            index = self.bill_listbox.size() - 1
            self.bill_index_map.append(str(bill['id']))
            self.bill_listbox.itemconfig(
                index,
                fg=COLORS['secondary_dark'] if is_paid else COLORS['danger'],
                bg='#f8fbfd'
            )
            if bill['status'] != 'Paid':
                total_outstanding += float(bill['amount'])

        self.billing_display.insert(tk.END, "Billing Summary\n\n", "billing_title")
        self.billing_display.insert(tk.END, "Total Bills: ", "billing_label")
        self.billing_display.insert(tk.END, f"{len(bills)}\n", "billing_value")
        self.billing_display.insert(tk.END, "Outstanding Balance: ", "billing_label")
        self.billing_display.insert(tk.END, f"KES {total_outstanding:.2f}\n\n", "billing_value")
        self.billing_display.insert(tk.END, "Select a bill from the list to view details or mark it as paid.", "billing_note")

    def update_billing_patient_dropdown(self, patients=None):
        """Load patient list into the billing patient dropdown."""
        patients = patients if patients is not None else self.patient_db.get_all()
        sorted_patients = sorted(patients, key=lambda p: p.patient_id)
        values = [f"{patient.patient_id} - {patient.name}" for patient in sorted_patients]
        self.bill_patient_id_combo['values'] = values

    def search_billing_patients(self):
        """Search patients by name or ID for the billing dropdown."""
        search_term = self.bill_patient_id_var.get().strip()
        if not search_term:
            self.update_billing_patient_dropdown()
            return

        matches = [
            patient for patient in self.patient_db.get_all()
            if search_term.lower() in patient.patient_id.lower() or search_term.lower() in patient.name.lower()
        ]
        self.update_billing_patient_dropdown(matches)
        if matches:
            first_value = f"{matches[0].patient_id} - {matches[0].name}"
            self.bill_patient_id_var.set(first_value)
            self.update_status(f"Found {len(matches)} patient(s); selected first match.")
        else:
            self.bill_patient_id_var.set("")
            SilentMessageBox.show_error("No patient", f"❌ No patient found for '{search_term}'.", self.root)

    def filter_billing_display(self):
        """Filter bills by patient id or patient name"""
        search_term = self.bill_filter_entry.get().strip().lower()
        bills = self.db.get_all_bills()
        if search_term:
            bills = [bill for bill in bills if search_term in bill['patient_id'].lower() or search_term in bill['patient_name'].lower()]
        self.update_billing_display(bills)

    def on_bill_select(self, event=None):
        """Show selected bill details"""
        selection = self.bill_listbox.curselection()
        if not selection:
            return

        selected_index = selection[0]
        if not hasattr(self, 'bill_index_map') or selected_index >= len(self.bill_index_map):
            return
        bill_id = self.bill_index_map[selected_index]
        self.selected_bill_id_var.set(bill_id)
        self.bill_selected_label.config(text=f"Selected Bill ID: {bill_id}")

        bill = next((item for item in self.db.get_all_bills() if str(item['id']) == bill_id), None)
        if not bill:
            return

        details = (
            (
                ("Bill ID", bill['id']),
                ("Patient", f"{bill['patient_name']} ({bill['patient_id']})"),
                ("Service", bill['service']),
                ("Amount", f"KES {bill['amount']:.2f}"),
                ("Status", bill['status']),
                ("Created", bill['created_date']),
                ("Paid", bill['paid_date'] or 'Not yet paid'),
                ("Notes", bill['notes'] or 'None')
            )
        )
        self.billing_display.delete(1.0, tk.END)
        self.billing_display.insert(tk.END, "Bill Details\n\n", "billing_title")
        for label, value in details:
            self.billing_display.insert(tk.END, f"{label}: ", "billing_label")
            if label == "Status":
                status_tag = "billing_paid" if str(value) == "Paid" else "billing_unpaid"
                self.billing_display.insert(tk.END, f"{value}\n", status_tag)
            else:
                self.billing_display.insert(tk.END, f"{value}\n", "billing_value")

    def get_billing_patient_id(self):
        """Return the patient ID selected in the billing patient dropdown."""
        patient_value = self.bill_patient_id_var.get().strip()
        if ' - ' in patient_value:
            return patient_value.split(' - ', 1)[0].upper()
        return patient_value.upper()

    def create_bill_record(self):
        """Create a bill for a patient"""
        patient_id = self.get_billing_patient_id()
        service = self.bill_service_entry.get().strip()
        amount_text = self.bill_amount_entry.get().strip()
        notes = self.bill_notes_text.get(1.0, tk.END).strip()

        if not patient_id or not service or not amount_text:
            SilentMessageBox.show_error("Error", "❌ Patient ID, service, and amount are required!", self.root)
            return

        patient = self.patient_db.lookup(patient_id)
        if not patient:
            SilentMessageBox.show_error("Error", f"❌ Patient {patient_id} not found!", self.root)
            return

        try:
            amount = float(amount_text)
        except ValueError:
            SilentMessageBox.show_error("Error", "❌ Amount must be a valid number!", self.root)
            return

        if amount <= 0:
            SilentMessageBox.show_error("Error", "❌ Amount must be greater than zero!", self.root)
            return

        if self.db.save_bill(patient_id, patient.name, service, amount, notes):
            SilentMessageBox.show_info("Saved", f"✅ Bill created for {patient.name}.", self.root)
            self.clear_billing_form()
            self.update_billing_display()
            self.update_status(f"Created bill for {patient.name}")
        else:
            SilentMessageBox.show_error("Error", "❌ Failed to create bill.", self.root)

    def mark_selected_bill_paid(self):
        """Mark the selected bill as paid"""
        bill_id = self.selected_bill_id_var.get().strip()
        if not bill_id:
            SilentMessageBox.show_error("Error", "❌ Select a bill from the list first!", self.root)
            return

        if self.db.mark_bill_paid(bill_id):
            SilentMessageBox.show_info("Updated", f"✅ Bill #{bill_id} marked as paid.", self.root)
            self.update_billing_display()
            self.bill_selected_label.config(text=f"Selected Bill ID: {bill_id}")
            self.selected_bill_id_var.set(bill_id)
            self.update_status(f"Bill {bill_id} marked as paid")
        else:
            SilentMessageBox.show_error("Error", "❌ Failed to update bill payment.", self.root)

    def clear_billing_form(self):
        """Clear billing inputs"""
        self.bill_patient_id_var.set("")
        self.bill_service_entry.delete(0, tk.END)
        self.bill_amount_entry.delete(0, tk.END)
        self.bill_notes_text.delete(1.0, tk.END)
    
    def update_patient_list_display(self):
        """Update the patient directory display"""
        patients = self.patient_db.get_all()
        self.render_patient_directory(patients)
        self.patient_stats_label.config(text=f"📊 Total Patients Registered: {len(patients)}")

    def export_patient_directory_report(self):
        """Export the patient directory currently shown on screen"""
        rows = []
        header = f"{'Patient ID':<12} {'Name':<28} {'Age':<5} {'Contact':<16} {'Blood':<8} {'Allergies':<24}"
        rows.append(header)
        rows.append("=" * len(header))
        for item in self.patient_list_display.get_children():
            values = self.patient_list_display.item(item, 'values')
            rows.append(
                f"{values[0]:<12} {values[1][:28]:<28} {values[2]:<5} {values[3][:16]:<16} {values[4]:<8} {values[5][:24]:<24}"
            )
        content = "\n".join(rows) if rows else "No patients in directory."
        self.export_report("Patient Directory Report", content, "patient_directory_report")
    
    def search_in_patient_list(self):
        """Search patient in the list"""
        search_term = self.patient_search_entry.get().strip().lower()
        if not search_term:
            self.update_patient_list_display()
            return
        
        patients = self.patient_db.get_all()
        filtered = [p for p in patients if search_term in p.name.lower() or search_term in p.patient_id.lower()]
        
        self.render_patient_directory(filtered, search_term)
        self.patient_stats_label.config(text=f"Total Patients: {len(patients)} | Showing: {len(filtered)}")

    def render_patient_directory(self, patients, search_term=""):
        """Render the patient directory in a styled table layout."""
        for item in self.patient_list_display.get_children():
            self.patient_list_display.delete(item)

        for index, patient in enumerate(patients):
            self.patient_list_display.insert(
                '',
                'end',
                values=(
                    patient.patient_id,
                    patient.name,
                    patient.age,
                    patient.contact or 'Not set',
                    patient.blood_group or 'Not set',
                    patient.allergies or 'None recorded'
                ),
                tags=('evenrow' if index % 2 == 0 else 'oddrow',)
            )

        self.patient_list_display.tag_configure('evenrow', background='white')
        self.patient_list_display.tag_configure('oddrow', background='#f4f9fc')
    
    def add_to_triage(self):
        """Add patient to triage queue with database"""
        pid = self.get_triage_patient_id()
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
        self.triage_patient_id_var.set("")
        if hasattr(self, 'triage_patient_search_entry'):
            self.triage_patient_search_entry.delete(0, tk.END)
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

    def export_triage_report(self):
        """Export the triage queue currently shown on screen"""
        content = self.get_text_widget_content(self.queue_display)
        self.export_report("Triage Queue Report", content, "triage_queue_report")
    
    def book_appointment(self):
        """Book an appointment with database"""
        pid = self.resolve_patient_id(self.appt_patient_id_var.get())
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
        schedule_text = self.calendar.display_week_schedule()
        self.schedule_display.insert(tk.END, "Weekly Appointment Schedule\n", "schedule_title")
        self.schedule_display.insert(tk.END, "\n")
        for line in schedule_text.splitlines():
            stripped = line.strip()
            if not stripped:
                self.schedule_display.insert(tk.END, "\n")
            elif stripped.endswith(":") and not set(stripped) <= {"=", "-"}:
                self.schedule_display.insert(tk.END, f"{line}\n", "schedule_day")
            else:
                self.schedule_display.insert(tk.END, f"{line}\n", "schedule_body")

    def export_appointments_report(self):
        """Export the appointment schedule currently shown on screen"""
        content = self.get_text_widget_content(self.schedule_display)
        self.export_report("Appointments Schedule Report", content, "appointments_schedule_report")
    
    def add_treatment(self):
        """Add treatment record with database"""
        pid = self.resolve_patient_id(self.treatment_pid_var.get())
        treatment = self.treatment_desc.get(1.0, tk.END).strip()
        doctor_selection = self.treatment_doctor_var.get().strip()
        doctor = doctor_selection.split(" (")[0] if doctor_selection else ""
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
        self.treatment_pid_var.set("")
        self.treatment_desc.delete(1.0, tk.END)
        if self.treatment_doctor_combo['values']:
            self.treatment_doctor_combo.current(0)
        else:
            self.treatment_doctor_combo.set("")
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
        pid = self.resolve_patient_id(self.view_history_var.get())
        if not pid:
            SilentMessageBox.show_error("Error", "❌ Enter Patient ID or name!", self.root)
            return
        
        history = self.patient_treatments.get_history(pid)

        if history:
            patient = self.patient_db.lookup(pid)
            patient_label = patient.name if patient else pid
            latest = history[-1]['date']
            self.render_history_entries(
                f"Treatment History for {pid}",
                f"Patient: {patient_label}  •  {len(history)} treatment record(s) found",
                history
            )
            self.update_history_summary(len(history), patient_label, latest)
            self.update_status(f"Showing treatment history for {pid}")
        else:
            self.history_display.delete(1.0, tk.END)
            self.history_display.insert(tk.END, "\n\n🗂\n", "empty_icon")
            self.history_display.insert(tk.END, f"No records found for {pid}\n", "empty_title")
            self.history_display.insert(tk.END, "This patient does not have treatment notes yet.\nRecord a treatment on the left, then reopen the history view.", "empty_text")
            self.update_history_summary(0, pid, "No record available")
            self.update_status(f"No treatment history found for {pid}")

    def export_treatment_history_report(self):
        """Export the current treatment history view"""
        pid = self.view_history_var.get().strip() or "patient"
        content = self.get_text_widget_content(self.history_display)
        self.export_report("Treatment History Report", content, f"treatment_history_{pid.lower()}")
    
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
            self.path_result.insert(tk.END, "Shortest Path Result\n\n", "path_title")
            self.path_result.insert(tk.END, f"📍 From: {start}\n", "path_meta")
            self.path_result.insert(tk.END, f"🎯 To: {end}\n\n", "path_meta")
            self.path_result.insert(tk.END, f"🚶 Route: {' → '.join(path)}\n\n", "path_route")
            self.path_result.insert(tk.END, f"📏 Total distance: {distance} units\n", "path_route")
            self.path_result.insert(tk.END, f"⏱️ Estimated walking time: {distance * 2} minutes\n", "path_route")
            self.update_status(f"Path found from {start} to {end}")
        else:
            self.path_result.insert(tk.END, f"No path found from {start} to {end}", "path_empty")
            self.update_status("No path found")
    
    def search_patient(self):
        """Search for patient by ID or name"""
        search_term = self.search_var.get().strip()
        
        if not search_term:
            SilentMessageBox.show_error("Error", "❌ Enter Patient ID or name!", self.root)
            return

        pid = self.resolve_patient_id(search_term)
        patient = self.patient_db.lookup(pid)

        if not patient:
            patients = self.patient_db.get_all()
            matches = [p for p in patients if search_term.lower() in p.name.lower()]

            if len(matches) == 1:
                patient = matches[0]
                pid = patient.patient_id
            elif len(matches) > 1:
                self.search_result.delete(1.0, tk.END)
                self.search_result.insert(tk.END, "Multiple Patients Found\n\n", "search_title")
                self.search_result.insert(tk.END, "Please refine the name or use a Patient ID.\n\n", "search_empty")
                for match in matches[:10]:
                    self.search_result.insert(tk.END, f"{match.patient_id}: ", "search_label")
                    self.search_result.insert(tk.END, f"{match.name}\n", "search_value")
                self.update_status(f"Found {len(matches)} matching patients")
                return
        
        self.search_result.delete(1.0, tk.END)
        
        if patient:
            self.search_result.insert(tk.END, "Patient Details\n\n", "search_title")
            details = [
                ("🆔 Patient ID", patient.patient_id),
                ("👤 Name", patient.name),
                ("📅 Age", patient.age),
                ("📞 Contact", patient.contact),
                ("🩸 Blood Group", patient.blood_group),
                ("⚠️ Allergies", patient.allergies),
            ]
            for label, value in details:
                self.search_result.insert(tk.END, f"{label}: ", "search_label")
                self.search_result.insert(tk.END, f"{value}\n", "search_value")
            
            # Get appointments from database
            appointments = self.db.get_patient_appointments(pid)
            if appointments:
                self.search_result.insert(tk.END, f"\nAppointments\n", "search_section")
                for appt in appointments:
                    self.search_result.insert(tk.END, f"• {appt[0]} at {appt[1]}\n", "search_value")
            else:
                self.search_result.insert(tk.END, f"\nAppointments\n", "search_section")
                self.search_result.insert(tk.END, "None scheduled\n", "search_empty")
            
            # Get treatment history
            treatments = self.patient_treatments.get_history(pid)
            if treatments:
                self.search_result.insert(tk.END, f"\nRecent Treatments\n", "search_section")
                for t in treatments[-3:]:
                    self.search_result.insert(tk.END, f"• {t['date'][:10]}: {t['treatment'][:50]}\n", "search_value")
            
            self.update_status(f"Found patient: {patient.name}")
        else:
            self.search_result.insert(tk.END, f"No patient found for '{search_term}'.\n\n", "search_title")
            self.search_result.insert(tk.END, "Try a Patient ID, full name, or part of the name.", "search_empty")
            self.update_status(f"No patient found for {search_term}")

    def export_patient_record_report(self):
        """Export the current patient search result"""
        pid = self.search_var.get().strip().upper() or "patient_record"
        content = self.get_text_widget_content(self.search_result)
        self.export_report("Patient Record Report", content, f"patient_record_{pid.lower()}")
    
    def show_about(self):
        """Show about dialog"""
        SilentMessageBox.show_info("About MediStruct", 
            "🏥 MEDISTRUCT\n\nVersion 4.0\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n📊 DATA STRUCTURES IMPLEMENTED:\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n✓ Hash Table     → Patient Records (O(1) lookup)\n✓ Priority Queue → Triage System (Emergency first)\n✓ Array          → Appointment Calendar (7x10 grid)\n✓ Stack          → Treatment History (Undo/Redo)\n✓ Graph          → Department Routing (Shortest path)\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n🗄️ DATABASE FEATURES:\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n• SQLite Database (medistruct.db)\n• Auto-save on close\n• Data persists after PC restart\n• Multi-user ready\n• Backup capability\n\n✨ OTHER FEATURES:\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n• Auto-increment Patient IDs (KGH001, KGH002...)\n• Contact number validation (10 digits)\n• Blood group dropdown selection\n• Separate Patient Directory tab\n• Doctor management module\n• Billing and payments module\n• Patient record editing module\n• Silent message boxes (no Windows sound)", self.root)


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = HospitalApp(root)
    app.show_startup_splash()
    root.mainloop()
