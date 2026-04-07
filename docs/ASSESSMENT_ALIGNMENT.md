# Lecturer Grading Rubric Alignment

## Purpose
This document maps common software project grading criteria to concrete evidence in MediStruct. It is designed to help lecturers assess technical quality, design reasoning, and implementation completeness quickly.

## Rubric Coverage Matrix

| Criterion | What Was Implemented | Evidence in Project | Performance Indicators |
|---|---|---|---|
| Problem Definition and Scope | Hospital workflow system covering registration, triage, appointments, treatment history, and routing | README project overview and feature sections | Scope is clear, realistic, and cohesive |
| Data Structure Selection and Justification | Five structures chosen to match operational needs: Hash Table, Priority Queue, 2D Array, Stack, Graph | README Why These Data Structures and Summary Table; ARCHITECTURE Why These Five Data Structures | Selection is justified by fit to real workflow and access pattern |
| Correctness of Core Logic | CRUD patient flow, triage ordering, slot collision prevention, treatment recording, shortest path routing | main.py action handlers; database.py methods; structure modules | Feature behavior matches stated requirements |
| Time Complexity Awareness | Complexity notes documented for each structure and algorithmic approach | README Summary Table; MODULES and ARCHITECTURE notes | Student demonstrates computational reasoning |
| OOP and Modularity | Class-based design across UI, persistence, and domain modules | main.py, database.py, hash_table.py, priority_queue.py, appointment_calendar.py, treatment_stack.py, hospital_graph.py | Responsibilities are separated and classes are meaningful |
| Persistence and Data Integrity | SQLite schema with patient, triage, appointment, treatment, and settings tables | DATABASE documentation and database.py implementation | Data survives restart and supports operational continuity |
| UI and Usability | Multi-tab Tkinter interface with workflow-based navigation and feedback dialogs | main.py class HospitalApp and UI components | User can perform all required tasks with clear flow |
| Documentation Quality | Full documentation suite with architecture, modules, user/developer guides, troubleshooting, changelog, and diagrams | docs folder and README documentation index | Documentation is complete, navigable, and consistent |
| Testing and Validation Strategy | Defined priority testing targets and quality focus areas | DEVELOPER_GUIDE testing recommendations | Demonstrates awareness of verification even if full test suite is pending |
| Reflection and Improvement Awareness | Constraints and refactoring opportunities identified | README Current Constraints; DEVELOPER_GUIDE Refactoring Opportunities | Student shows critical evaluation and forward planning |

## Learning Outcome Evidence

1. Apply data structures to real-world systems
- Evidence: structure-to-workflow mapping across triage, appointments, history, and routing.

2. Analyze algorithmic tradeoffs
- Evidence: complexity table and module-level notes describing behavior and costs.

3. Build modular OOP software
- Evidence: class-driven modules and layer separation in architecture documentation.

4. Persist and manage structured data
- Evidence: SQLite schema, CRUD flows, and backup behavior.

5. Communicate technical design professionally
- Evidence: full documentation suite plus architecture/workflow diagrams.

## Suggested Lecturer Marking Notes

- High marks can be awarded where justification, implementation, and documentation are all aligned.
- Distinction-level indicators include clear complexity reasoning, coherent architecture narrative, and traceable rubric evidence.
- Areas for incremental improvement include automated testing and stronger formal validation metrics.

## Quick Access Index

- README: project narrative and summary table
- ARCHITECTURE: structural explanation and diagrams
- MODULES: per-module technical reference
- DATABASE: schema and persistence lifecycle
- USER_GUIDE: operational workflows
- DEVELOPER_GUIDE: maintainability and testing direction
- TROUBLESHOOTING: fault handling and recovery
