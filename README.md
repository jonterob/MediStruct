# 🏥 Kerugoya Hospital Management System

## 📌 Project Overview
An application for Kerugoya Hospital that manages patient registration, triage queue, appointments, treatment history and department routing using **five different data structures** with SQLite database persistence.

---

## 📊 Data Structures Implemented

| Data Structure | Purpose | Complexity |
|---------------|--------|------------|
| Hash Table | Patient records storage (fast lookup) | O(1) avg |
| Priority Queue | Triage system (Emergency first) | O(log n) |
| 2D Array | Appointment calendar (7×10 grid) | O(1) |
| Stack | Treatment history (Undo/Redo) | O(1) |
| Graph | Department routing (Shortest path) | O(V²) |

---

## ✨ Key Features

### 1. Patient Registration
- ✅ Auto-increment IDs (KGH001, KGH002...)
- ✅ Contact validation (10 digits)
- ✅ Blood group selection
- ✅ SQLite database persistence

---

### 2. Triage Queue
- 🔴 Emergency (Priority 1)
- 🟡 Serious (Priority 2)
- 🟢 Minor (Priority 3)
- ✅ Priority-based processing
- 🎨 Color-coded display

---

### 3. Appointment Calendar
- 📅 7 days × 10 slots (8AM–5PM)
- ⏱️ Slot availability checking
- 📊 Visual weekly schedule

---

### 4. Treatment History
- 🔄 Undo/Redo functionality
- 👨‍⚕️ Doctor attribution
- 🕒 Timestamp tracking

---

### 5. Department Routing
- 🧭 Shortest path using Dijkstra's Algorithm
- 🏥 8 hospital departments connected
- ⏳ Distance and time estimation

---

## 🗄️ Database Schema

**Tables:**
- patients  
- triage_queue  
- appointments  
- treatments  
- system_settings  

**Features:**
- 💾 Auto-save on close  
- 🔄 Backup & restore support  
- 🔐 Persistent data storage  

---

## 🚀 Quick Start

### Requirements
- Python 3.7+
- Tkinter (comes pre-installed with Python)

### Run the Application

## 📁 File Structure


kerugoya_hospital_system/
├── main.py # Main application
├── database.py # SQLite operations
├── hash_table.py # Hash table for patients
├── priority_queue.py # Priority queue for triage
├── appointment_calendar.py # 2D array calendar
├── treatment_stack.py # Stack for undo/redo
├── hospital_graph.py # Graph for routing
└── kerugoya_hospital.db # Database (auto-created)
