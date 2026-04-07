# treatment_stack.py
# Stack for Treatment History (Undo/Redo functionality)

class TreatmentStack:
    def __init__(self):
        self.undo_stack = []  # For actions that can be undone
        self.redo_stack = []  # For actions that can be redone
    
    def add_treatment(self, patient_id, treatment, doctor, date):
        """Add a new treatment record"""
        action = {
            "type": "add_treatment",
            "patient_id": patient_id,
            "treatment": treatment,
            "doctor": doctor,
            "date": date
        }
        self.undo_stack.append(action)
        self.redo_stack.clear()  # Clear redo when new action added
        return f"Treatment recorded: {treatment}"
    
    def undo(self):
        """Undo last treatment addition"""
        if self.undo_stack:
            action = self.undo_stack.pop()
            self.redo_stack.append(action)
            return f"Undid: {action['treatment']} for patient {action['patient_id']}"
        return "Nothing to undo"
    
    def redo(self):
        """Redo previously undone treatment"""
        if self.redo_stack:
            action = self.redo_stack.pop()
            self.undo_stack.append(action)
            return f"Redid: {action['treatment']} for patient {action['patient_id']}"
        return "Nothing to redo"
    
    def get_history(self):
        """Get all treatments in order"""
        return self.undo_stack.copy()


class PatientTreatmentHistory:
    def __init__(self):
        self.histories = {}  # patient_id -> list of treatments
    
    def add_treatment(self, patient_id, treatment, doctor, date):
        if patient_id not in self.histories:
            self.histories[patient_id] = []
        self.histories[patient_id].append({
            "treatment": treatment,
            "doctor": doctor,
            "date": date
        })
    
    def get_history(self, patient_id):
        return self.histories.get(patient_id, [])
    
    def __str__(self):
        result = ""
        for pid, treatments in self.histories.items():
            result += f"\nPatient {pid}:\n"
            for t in treatments:
                result += f"  {t['date']} - Dr. {t['doctor']}: {t['treatment']}\n"
        return result