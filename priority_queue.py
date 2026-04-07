# priority_queue.py
# Priority Queue for Triage System with Color Support

class TriagePatient:
    """Represents a patient in the triage queue"""
    
    def __init__(self, patient_id, name, condition, priority):
        """
        Initialize a triage patient
        
        Args:
            patient_id (str): Unique patient identifier
            name (str): Patient's full name
            condition (str): Medical condition description
            priority (int): 1=Emergency, 2=Serious, 3=Minor
        """
        self.patient_id = patient_id
        self.name = name
        self.condition = condition
        self.priority = priority  # 1=Emergency, 2=Serious, 3=Minor
        self.wait_time = 0
        self.arrival_time = None  # Will be set when added to queue
        self.notes = ""
    
    def __str__(self):
        """String representation without colors"""
        priority_text = {1: "EMERGENCY", 2: "SERIOUS", 3: "MINOR"}
        return f"[{priority_text[self.priority]}] {self.name} - {self.condition}"
    
    def get_priority_text(self):
        """Get priority text with emoji"""
        return {
            1: "🔴 EMERGENCY",
            2: "🟡 SERIOUS", 
            3: "🟢 MINOR"
        }[self.priority]
    
    def get_priority_color(self):
        """Get hex color code for priority"""
        return {
            1: "#e74c3c",  # Red for emergency
            2: "#f39c12",  # Orange for serious
            3: "#27ae60"   # Green for minor
        }[self.priority]
    
    def get_priority_bg_color(self):
        """Get background color for priority"""
        return {
            1: "#fde5e5",  # Light red
            2: "#fef3e0",  # Light orange
            3: "#e8f5e9"   # Light green
        }[self.priority]
    
    def get_priority_icon(self):
        """Get priority icon"""
        return {
            1: "🚨",
            2: "⚠️",
            3: "ℹ️"
        }[self.priority]
    
    def get_formatted_display(self, index=None):
        """
        Get formatted display string for list view
        
        Args:
            index (int, optional): Position in queue
            
        Returns:
            dict: Contains formatted text and color information
        """
        priority_info = {
            1: {"text": "EMERGENCY", "icon": "🔴", "color": "#e74c3c"},
            2: {"text": "SERIOUS", "icon": "🟡", "color": "#f39c12"},
            3: {"text": "MINOR", "icon": "🟢", "color": "#27ae60"}
        }[self.priority]
        
        result = {
            "priority_text": priority_info["text"],
            "priority_icon": priority_info["icon"],
            "priority_color": priority_info["color"],
            "patient_id": self.patient_id,
            "name": self.name,
            "condition": self.condition,
            "wait_time": self.wait_time
        }
        
        if index:
            result["index"] = index
        
        return result
    
    def update_wait_time(self):
        """Update waiting time (to be called periodically)"""
        self.wait_time += 1
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "condition": self.condition,
            "priority": self.priority,
            "wait_time": self.wait_time,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        patient = cls(
            data["patient_id"],
            data["name"],
            data["condition"],
            data["priority"]
        )
        patient.wait_time = data.get("wait_time", 0)
        patient.notes = data.get("notes", "")
        return patient


class PriorityQueue:
    """Priority queue implementation for triage management"""
    
    def __init__(self):
        self.queue = []  # Will store (priority, patient, timestamp)
        self.history = []  # Store served patients for history
        self.max_size = 100  # Maximum queue size
    
    def enqueue(self, patient):
        """
        Add patient to queue with priority
        
        Args:
            patient (TriagePatient): Patient to add
            
        Returns:
            bool: True if successful, False if queue is full
        """
        if self.size() >= self.max_size:
            return False
        
        from datetime import datetime
        patient.arrival_time = datetime.now()
        # Add to queue as tuple (priority, patient, timestamp)
        self.queue.append((patient.priority, patient, patient.arrival_time))
        # Sort by priority (lower number = higher priority)
        # For same priority, earlier arrival time gets higher priority
        self.queue.sort(key=lambda x: (x[0], x[2]))
        return True
    
    def dequeue(self):
        """
        Remove and return highest priority patient
        
        Returns:
            TriagePatient or None: Next patient to serve
        """
        if self.queue:
            priority, patient, timestamp = self.queue.pop(0)
            # Add to history
            from datetime import datetime
            self.history.append({
                "patient": patient,
                "served_time": datetime.now(),
                "wait_time": patient.wait_time
            })
            return patient
        return None
    
    def peek(self):
        """
        See next patient without removing
        
        Returns:
            TriagePatient or None: Next patient to serve
        """
        if self.queue:
            return self.queue[0][1]
        return None
    
    def is_empty(self):
        """Check if queue is empty"""
        return len(self.queue) == 0
    
    def size(self):
        """Get current queue size"""
        return len(self.queue)
    
    def get_all(self):
        """Get all patients in queue"""
        return [patient for _, patient, _ in self.queue]
    
    def get_all_with_priority(self):
        """Get all patients with their priority levels"""
        return [(priority, patient) for priority, patient, _ in self.queue]
    
    def remove_patient(self, patient_id):
        """
        Remove specific patient from queue
        
        Args:
            patient_id (str): ID of patient to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        for i, (_, patient, _) in enumerate(self.queue):
            if patient.patient_id == patient_id:
                self.queue.pop(i)
                return True
        return False
    
    def get_patient_position(self, patient_id):
        """
        Get position of patient in queue (1-based)
        
        Args:
            patient_id (str): ID of patient to find
            
        Returns:
            int: Position (1-based) or -1 if not found
        """
        for i, (_, patient, _) in enumerate(self.queue):
            if patient.patient_id == patient_id:
                return i + 1
        return -1
    
    def update_wait_times(self):
        """Update wait times for all patients in queue"""
        for _, patient, _ in self.queue:
            patient.update_wait_time()
    
    def get_statistics(self):
        """
        Get queue statistics
        
        Returns:
            dict: Statistics about current queue
        """
        patients = self.get_all()
        stats = {
            "total": len(patients),
            "emergency": sum(1 for p in patients if p.priority == 1),
            "serious": sum(1 for p in patients if p.priority == 2),
            "minor": sum(1 for p in patients if p.priority == 3),
            "max_wait_time": max([p.wait_time for p in patients]) if patients else 0,
            "avg_wait_time": sum([p.wait_time for p in patients]) / len(patients) if patients else 0
        }
        return stats
    
    def clear(self):
        """Clear all patients from queue"""
        self.queue.clear()
    
    def get_queue_display_data(self):
        """
        Get formatted data for display with colors
        
        Returns:
            list: List of dictionaries with display information
        """
        display_data = []
        for i, (_, patient, _) in enumerate(self.queue, 1):
            data = patient.get_formatted_display(i)
            display_data.append(data)
        return display_data
    
    def get_history(self, limit=50):
        """
        Get recently served patients
        
        Args:
            limit (int): Maximum number of history entries to return
            
        Returns:
            list: History of served patients
        """
        return self.history[-limit:]
    
    def get_priority_summary(self):
        """
        Get priority summary string for display
        
        Returns:
            str: Formatted priority summary
        """
        stats = self.get_statistics()
        if stats["total"] == 0:
            return "Queue is empty"
        
        return (f"📊 Total: {stats['total']} | "
                f"🔴 Emergency: {stats['emergency']} | "
                f"🟡 Serious: {stats['serious']} | "
                f"🟢 Minor: {stats['minor']}")
    
    def to_dict(self):
        """Convert entire queue to dictionary for saving"""
        return {
            "queue": [patient.to_dict() for _, patient, _ in self.queue],
            "history": [
                {
                    "patient": h["patient"].to_dict(),
                    "served_time": str(h["served_time"]),
                    "wait_time": h["wait_time"]
                }
                for h in self.history
            ]
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create queue from saved dictionary"""
        queue = cls()
        for patient_data in data.get("queue", []):
            patient = TriagePatient.from_dict(patient_data)
            queue.enqueue(patient)
        
        # Load history (simplified - would need proper datetime parsing)
        for history_data in data.get("history", []):
            patient = TriagePatient.from_dict(history_data["patient"])
            queue.history.append({
                "patient": patient,
                "served_time": None,  # Would parse datetime here
                "wait_time": history_data["wait_time"]
            })
        
        return queue
    
    def __str__(self):
        """String representation of queue"""
        if self.is_empty():
            return "Queue is empty"
        
        result = "=" * 60 + "\n"
        result += "TRIAGE QUEUE (Emergency First)\n"
        result += "=" * 60 + "\n\n"
        
        for i, (_, patient, _) in enumerate(self.queue, 1):
            result += f"{i}. {patient.get_priority_text()} | {patient.name} - {patient.condition}\n"
            if patient.wait_time > 0:
                result += f"   ⏱️ Waiting: {patient.wait_time} minutes\n"
        
        result += "\n" + "=" * 60 + "\n"
        result += self.get_priority_summary()
        
        return result


# Example usage and testing
if __name__ == "__main__":
    # Test the priority queue
    print("Testing Priority Queue System...")
    print("-" * 40)
    
    # Create queue
    triage_queue = PriorityQueue()
    
    # Add sample patients
    patient1 = TriagePatient("KGH001", "John Mwangi", "Chest pain", 1)  # Emergency
    patient2 = TriagePatient("KGH002", "Mary Wanjiku", "Fever", 3)       # Minor
    patient3 = TriagePatient("KGH003", "Peter Otieno", "Broken arm", 2)  # Serious
    patient4 = TriagePatient("KGH004", "Grace Akinyi", "Difficulty breathing", 1)  # Emergency
    
    triage_queue.enqueue(patient1)
    triage_queue.enqueue(patient2)
    triage_queue.enqueue(patient3)
    triage_queue.enqueue(patient4)
    
    # Display queue
    print(triage_queue)
    print("\n" + "-" * 40)
    
    # Get display data for colored UI
    print("\nDisplay data for colored UI:")
    for data in triage_queue.get_queue_display_data():
        print(f"Position {data['index']}: {data['priority_icon']} {data['priority_text']} - "
              f"{data['name']} ({data['condition']})")
    
    print("\n" + "-" * 40)
    
    # Serve patients
    print("\nServing patients:")
    while not triage_queue.is_empty():
        patient = triage_queue.dequeue()
        print(f"Now serving: {patient}")
    
    print("\n" + "-" * 40)
    print(f"Queue empty: {triage_queue.is_empty()}")
    print(f"Queue size: {triage_queue.size()}")
    
    # Test statistics
    print("\nStatistics for empty queue:")
    print(triage_queue.get_statistics())