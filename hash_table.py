# Hash Table for Patient Records
class PatientRecord:
    def __init__(self, patient_id, name, age, contact, blood_group, allergies):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.contact = contact
        self.blood_group = blood_group
        self.allergies = allergies
        self.treatment_history = []
    
    def __str__(self):
        return f"ID: {self.patient_id} | Name: {self.name} | Age: {self.age} | Blood: {self.blood_group}"

class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [None] * size
        self.count = 0
    
    def _hash(self, key):
        # Simple hash function
        return sum(ord(c) for c in key) % self.size
    
    def insert(self, patient):
        index = self._hash(patient.patient_id)
        original_index = index
        
        while self.table[index] is not None:
            if self.table[index].patient_id == patient.patient_id:
                # Update existing
                self.table[index] = patient
                return True
            index = (index + 1) % self.size
            if index == original_index:
                # Table full
                return False
        
        self.table[index] = patient
        self.count += 1
        return True
    
    def lookup(self, patient_id):
        index = self._hash(patient_id)
        original_index = index
        
        while self.table[index] is not None:
            if self.table[index].patient_id == patient_id:
                return self.table[index]
            index = (index + 1) % self.size
            if index == original_index:
                break
        return None
    
    def delete(self, patient_id):
        index = self._hash(patient_id)
        original_index = index
        
        while self.table[index] is not None:
            if self.table[index].patient_id == patient_id:
                self.table[index] = None
                self.count -= 1
                return True
            index = (index + 1) % self.size
            if index == original_index:
                break
        return False
    
    def get_all(self):
        return [p for p in self.table if p is not None]
    
    def __len__(self):
        return self.count# Hash Table for Patient Records
class PatientRecord:
    def __init__(self, patient_id, name, age, contact, blood_group, allergies):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.contact = contact
        self.blood_group = blood_group
        self.allergies = allergies
        self.treatment_history = []
    
    def __str__(self):
        return f"ID: {self.patient_id} | Name: {self.name} | Age: {self.age} | Blood: {self.blood_group}"

class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [None] * size
        self.count = 0
    
    def _hash(self, key):
        # Simple hash function
        return sum(ord(c) for c in key) % self.size
    
    def insert(self, patient):
        index = self._hash(patient.patient_id)
        original_index = index
        
        while self.table[index] is not None:
            if self.table[index].patient_id == patient.patient_id:
                # Update existing
                self.table[index] = patient
                return True
            index = (index + 1) % self.size
            if index == original_index:
                # Table full
                return False
        
        self.table[index] = patient
        self.count += 1
        return True
    
    def lookup(self, patient_id):
        index = self._hash(patient_id)
        original_index = index
        
        while self.table[index] is not None:
            if self.table[index].patient_id == patient_id:
                return self.table[index]
            index = (index + 1) % self.size
            if index == original_index:
                break
        return None
    
    def delete(self, patient_id):
        index = self._hash(patient_id)
        original_index = index
        
        while self.table[index] is not None:
            if self.table[index].patient_id == patient_id:
                self.table[index] = None
                self.count -= 1
                return True
            index = (index + 1) % self.size
            if index == original_index:
                break
        return False
    
    def get_all(self):
        return [p for p in self.table if p is not None]
    
    def __len__(self):
        return self.count