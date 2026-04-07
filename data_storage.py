# data_storage.py
# Save/Load data to file

import json
from datetime import datetime

class DataStorage:
    @staticmethod
    def save_data(patients_list, appointments, filename="hospital_data.json"):
        """Save all data to JSON file"""
        data = {
            "patients": [],
            "appointments": [],
            "saved_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Save patients
        for patient in patients_list:
            data["patients"].append({
                "patient_id": patient.patient_id,
                "name": patient.name,
                "age": patient.age,
                "contact": patient.contact,
                "blood_group": patient.blood_group,
                "allergies": patient.allergies
            })
        
        # Save appointments (simplified)
        for day in range(7):
            for slot in range(10):
                if appointments[day][slot]:
                    data["appointments"].append({
                        "day": day,
                        "slot": slot,
                        "patient_id": appointments[day][slot]["patient_id"],
                        "patient_name": appointments[day][slot]["patient_name"]
                    })
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return f"Data saved to {filename}"
    
    @staticmethod
    def load_data(filename="hospital_data.json"):
        """Load data from JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            return None