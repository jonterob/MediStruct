# Array-based Appointment Calendar (7 days, 8am-5pm)
class AppointmentCalendar:
    def __init__(self):
        # 7 days (Mon-Sun) x 10 slots (8am-5pm, hourly)
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.slots = ["8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
        
        # 2D array: [day][slot] = patient_id or None
        self.calendar = [[None for _ in range(10)] for _ in range(7)]
    
    def book_appointment(self, day_index, slot_index, patient_id, patient_name):
        """Book an appointment"""
        if day_index < 0 or day_index >= 7 or slot_index < 0 or slot_index >= 10:
            return False, "Invalid day or time slot"
        
        if self.calendar[day_index][slot_index] is not None:
            return False, "Slot already booked"
        
        self.calendar[day_index][slot_index] = {"patient_id": patient_id, "patient_name": patient_name}
        return True, f"Appointment booked for {self.days[day_index]} at {self.slots[slot_index]}"
    
    def cancel_appointment(self, day_index, slot_index):
        """Cancel an appointment"""
        if self.calendar[day_index][slot_index] is not None:
            self.calendar[day_index][slot_index] = None
            return True, "Appointment cancelled"
        return False, "No appointment at this slot"
    
    def get_patient_appointments(self, patient_id):
        """Find all appointments for a patient"""
        appointments = []
        for day in range(7):
            for slot in range(10):
                if self.calendar[day][slot] and self.calendar[day][slot]["patient_id"] == patient_id:
                    appointments.append(f"{self.days[day]} at {self.slots[slot]}")
        return appointments
    
    def get_available_slots(self, day_index):
        """Get all available slots for a specific day"""
        available = []
        for slot in range(10):
            if self.calendar[day_index][slot] is None:
                available.append(self.slots[slot])
        return available
    
    def display_week_schedule(self):
        """Show entire week's schedule"""
        schedule = "\n=== WEEKLY APPOINTMENT SCHEDULE ===\n"
        for day in range(7):
            schedule += f"\n{self.days[day]}:\n"
            has_appointments = False
            for slot in range(10):
                if self.calendar[day][slot]:
                    appt = self.calendar[day][slot]
                    schedule += f"  {self.slots[slot]}: {appt['patient_name']} (ID: {appt['patient_id']})\n"
                    has_appointments = True
            if not has_appointments:
                schedule += "  No appointments\n"
        return schedule