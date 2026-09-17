import sqlite3
connection = sqlite3.connect("hospital.db")
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

cursor.executemany("""
INSERT OR IGNORE INTO patients
(patient_code, first_name, last_name, date_of_birth, phone, email, address,
 emergency_contact_name, emergency_contact_phone)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    ("P001", "Ali", "Khan", "1981-05-12", "03001234001", "ali.khan@email.com", "Karachi", "Usman Khan", "03001234011"),
    ("P002", "Shiza", "Ashal", "1998-08-21","03005688642","shiza.ashal@gmail.com", "karachi","ashal hussain","0367418638"),
    ("P003", "Hassan", "Raza", "1975-02-17", "03001234003", "hassan.raza@email.com", "Karachi", "Bilal Raza", "03001234013"),
    ("P004", "Ayesha", "Malik", "2002-11-09", "03001234004", "ayesha.malik@email.com", "Karachi", "Mariam Malik", "03001234014"),
    ("P005", "Hamza", "Siddiqui", "1968-07-24", "03001234005", "hamza.siddiqui@email.com", "Karachi", "Faisal Siddiqui", "03001234015"),
    ("P006", "Mariam", "Hussain", "1989-03-30", "03001234006", "mariam.hussain@email.com", "Karachi", "Nadia Hussain", "03001234016"),
    ("P007", "Usman", "Qureshi", "1995-12-14", "03001234007", "usman.qureshi@email.com", "Karachi", "Ahmed Qureshi", "03001234017"),
    ("P008", "Fatima", "Ali", "1959-09-05", "03001234008", "fatima.ali@email.com", "Karachi", "Zain Ali", "03001234018"),
    ("P009", "Bilal", "Shah", "1986-06-18", "03001234009", "bilal.shah@email.com", "Karachi", "Sadia Shah", "03001234019"),
    ("P010", "Sana", "Farooq", "2010-01-27", "03001234010", "sana.farooq@email.com", "Karachi", "Omar Farooq", "03001234020")
])

patient_ids = {}

cursor.execute("SELECT patient_id, patient_code FROM patients")

for patient_id, patient_code in cursor.fetchall():
    patient_ids[patient_code] = patient_id

cursor.executemany("""
INSERT OR IGNORE INTO demographics
(patient_id, gender, blood_group, marital_status, nationality, occupation)
VALUES (?, ?, ?, ?, ?, ?)
""", [
    (patient_ids["P001"], "Male", "B+", "Married", "Pakistani", "Businessman"),
    (patient_ids["P002"], "Female", "A+", "Single", "Pakistani", "Student"),
    (patient_ids["P003"], "Male", "O+", "Married", "Pakistani", "Engineer"),
    (patient_ids["P004"], "Female", "B+", "Single", "Pakistani", "Student"),
    (patient_ids["P005"], "Male", "O-", "Married", "Pakistani", "Retired"),
    (patient_ids["P006"], "Female", "A-", "Married", "Pakistani", "Teacher"),
    (patient_ids["P007"], "Male", "AB+", "Single", "Pakistani", "Software Developer"),
    (patient_ids["P008"], "Female", "B-", "Widowed", "Pakistani", "Retired"),
    (patient_ids["P009"], "Male", "A+", "Married", "Pakistani", "Accountant"),
    (patient_ids["P010"], "Female", "O+", "Single", "Pakistani", "Student")
])

cursor.executemany("""
INSERT OR IGNORE INTO departments
(department_code, department_name, location, phone)
VALUES (?, ?, ?, ?)
""", [
    ("DEP001", "Cardiology", "Block A", "021-1111111"),
    ("DEP002", "Neurology", "Block A", "021-1111112"),
    ("DEP003", "General Medicine", "Block B", "021-1111113"),
    ("DEP004", "Orthopedics", "Block B", "021-1111114"),
    ("DEP005", "Pediatrics", "Block C", "021-1111115"),
    ("DEP006", "Dermatology", "Block C", "021-1111116"),
    ("DEP007", "Emergency", "Block D", "021-1111117"),
    ("DEP008", "Radiology", "Block D", "021-1111118"),
    ("DEP009", "Pathology", "Block E", "021-1111119")
])

department_ids = {}

cursor.execute("SELECT department_id, department_code FROM departments")

for department_id, department_code in cursor.fetchall():
    department_ids[department_code] = department_id

cursor.executemany("""
INSERT OR IGNORE INTO doctors
(doctor_code, first_name, last_name, specialization, phone, email, department_id)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", [
    ("DOC001", "Ahmed", "Khan", "Cardiologist", "03001234567", "ahmed.khan@hospital.com", department_ids["DEP001"]),
    ("DOC002", "Sara", "Malik", "Neurologist", "03001234568", "sara.malik@hospital.com", department_ids["DEP002"]),
    ("DOC003", "Usman", "Ali", "General Physician", "03001234569", "usman.ali@hospital.com", department_ids["DEP003"]),
    ("DOC004", "Ayesha", "Raza", "Orthopedic Surgeon", "03001234570", "ayesha.raza@hospital.com", department_ids["DEP004"]),
    ("DOC005", "Hassan", "Ahmed", "Pediatrician", "03001234571", "hassan.ahmed@hospital.com", department_ids["DEP005"]),
    ("DOC006", "Mariam", "Shah", "Dermatologist", "03001234572", "mariam.shah@hospital.com", department_ids["DEP006"]),
    ("DOC007", "Bilal", "Hussain", "Emergency Physician", "03001234573", "bilal.hussain@hospital.com", department_ids["DEP007"]),
    ("DOC008", "Fatima", "Siddiqui", "Radiologist", "03001234574", "fatima.siddiqui@hospital.com", department_ids["DEP008"]),
    ("DOC009", "Hamza", "Qureshi", "Pathologist", "03001234575", "hamza.qureshi@hospital.com", department_ids["DEP009"])
])

doctor_ids = {}

cursor.execute("SELECT doctor_id, doctor_code FROM doctors")

for doctor_id, doctor_code in cursor.fetchall():
    doctor_ids[doctor_code] = doctor_id

cursor.executemany("""
INSERT OR IGNORE INTO staff
(staff_code, first_name, last_name, role, phone, email, department_id)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", [
    ("STF001", "Nadia", "Khan", "Receptionist", "03001234601", "nadia.khan@hospital.com", department_ids["DEP003"]),
    ("STF002", "Sana", "Ahmed", "Nurse", "03001234602", "sana.ahmed@hospital.com", department_ids["DEP003"]),
    ("STF003", "Omar", "Farooq", "Lab Technician", "03001234603", "omar.farooq@hospital.com", department_ids["DEP009"]),
    ("STF004", "Hira", "Aslam", "Pharmacist", "03001234604", "hira.aslam@hospital.com", department_ids["DEP009"]),
    ("STF005", "Danish", "Iqbal", "Nurse", "03001234605", "danish.iqbal@hospital.com", department_ids["DEP001"])
])

staff_ids = {}

cursor.execute("SELECT staff_id, staff_code FROM staff")

for staff_id, staff_code in cursor.fetchall():
    staff_ids[staff_code] = staff_id

cursor.executemany("""
INSERT INTO appointments
(patient_id, doctor_id, appointment_date, appointment_time, reason, status, notes)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", [
    (patient_ids["P001"], doctor_ids["DOC001"], "2026-09-05", "10:00", "Chest pain", "Scheduled", None),
    (patient_ids["P002"], doctor_ids["DOC002"], "2026-09-05", "11:00", "Headache", "Scheduled", None),
    (patient_ids["P003"], doctor_ids["DOC003"], "2026-09-06", "09:30", "Fever", "Completed", "Follow-up required"),
    (patient_ids["P004"], doctor_ids["DOC005"], "2026-09-06", "12:00", "Routine checkup", "Scheduled", None),
    (patient_ids["P005"], doctor_ids["DOC001"], "2026-09-07", "10:30", "Blood pressure review", "Completed", None),
    (patient_ids["P006"], doctor_ids["DOC006"], "2026-09-07", "14:00", "Skin condition", "Scheduled", None),
    (patient_ids["P007"], doctor_ids["DOC003"], "2026-09-08", "11:30", "Back pain", "Scheduled", None),
    (patient_ids["P008"], doctor_ids["DOC001"], "2026-09-08", "15:00", "Heart checkup", "Completed", None),
    (patient_ids["P009"], doctor_ids["DOC004"], "2026-09-09", "13:00", "Knee pain", "Scheduled", None),
    (patient_ids["P010"], doctor_ids["DOC005"], "2026-09-09", "09:00", "Routine pediatric visit", "Completed", None)
])

cursor.executemany("""
INSERT OR IGNORE INTO rooms
(ward_name, room_number, bed_number, room_type, daily_charge, status)
VALUES (?, ?, ?, ?, ?, ?)
""", [
    ("General Ward", "G101", "1", "General", 3000, "Available"),
    ("General Ward", "G101", "2", "General", 3000, "Available"),
    ("Cardiac Ward", "C201", "1", "Private", 7000, "Available"),
    ("Cardiac Ward", "C201", "2", "Private", 7000, "Available"),
    ("Neurology Ward", "N301", "1", "Private", 6000, "Available"),
    ("Pediatric Ward", "P401", "1", "Pediatric", 4000, "Available"),
    ("Emergency Ward", "E501", "1", "Emergency", 5000, "Available"),
    ("Emergency Ward", "E501", "2", "Emergency", 5000, "Available")
])

room_ids = {}

cursor.execute("SELECT room_id, room_number, bed_number FROM rooms")

for room_id, room_number, bed_number in cursor.fetchall():
    room_ids[(room_number, bed_number)] = room_id

cursor.execute("""
SELECT admission_id
FROM admissions
""")

existing_admissions = cursor.fetchall()

if not existing_admissions:
    cursor.executemany("""
    INSERT INTO admissions
    (patient_id, doctor_id, room_id, admission_date, discharge_date,
     admission_reason, status, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (patient_ids["P001"], doctor_ids["DOC001"], room_ids[("C201", "1")], "2026-08-28", "2026-08-31", "Chest pain and cardiac evaluation", "Discharged", "Stable"),
        (patient_ids["P003"], doctor_ids["DOC003"], room_ids[("G101", "1")], "2026-08-30", None, "High fever", "Admitted", "Under observation"),
        (patient_ids["P005"], doctor_ids["DOC001"], room_ids[("C201", "2")], "2026-08-25", "2026-08-29", "Hypertension", "Discharged", "Stable"),
        (patient_ids["P008"], doctor_ids["DOC001"], room_ids[("G101", "2")], "2026-08-27", "2026-08-30", "Cardiac monitoring", "Discharged", "Stable")
    ])

admission_ids = {}

cursor.execute("SELECT admission_id, patient_id FROM admissions")

for admission_id, patient_id in cursor.fetchall():
    admission_ids[patient_id] = admission_id

cursor.execute("SELECT COUNT(*) FROM medical_history")

if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO medical_history
    (patient_id, condition_name, diagnosis_date, treatment, status, notes)
    VALUES (?, ?, ?, ?, ?, ?)
    """, [
        (patient_ids["P001"], "Hypertension", "2020-04-15", "Medication and lifestyle management", "Ongoing", "Regular monitoring required"),
        (patient_ids["P001"], "High Cholesterol", "2021-06-20", "Diet and medication", "Ongoing", None),
        (patient_ids["P003"], "Asthma", "2015-09-10", "Inhaler", "Ongoing", None),
        (patient_ids["P005"], "Hypertension", "2012-03-11", "Antihypertensive medication", "Ongoing", "Regular BP monitoring"),
        (patient_ids["P006"], "Migraine", "2018-01-25", "Medication as required", "Ongoing", None),
        (patient_ids["P008"], "Diabetes", "2010-05-18", "Medication and diet control", "Ongoing", None),
        (patient_ids["P009"], "Back Pain", "2022-07-09", "Physiotherapy", "Improved", None)
    ])

cursor.execute("SELECT COUNT(*) FROM allergies")

if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO allergies
    (patient_id, allergen, reaction, severity, notes)
    VALUES (?, ?, ?, ?, ?)
    """, [
        (patient_ids["P001"], "Penicillin", "Skin rash", "Moderate", "Avoid penicillin-based medicines"),
        (patient_ids["P003"], "Dust", "Sneezing", "Mild", None),
        (patient_ids["P006"], "Peanuts", "Skin reaction", "Severe", "Avoid peanut products"),
        (patient_ids["P009"], "Aspirin", "Stomach discomfort", "Moderate", None)
    ])

cursor.execute("SELECT COUNT(*) FROM surgeries")

if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO surgeries
    (patient_id, doctor_id, surgery_name, surgery_date,
     hospital_name, outcome, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [
        (patient_ids["P004"], doctor_ids["DOC004"], "Appendectomy", "2022-05-10", "City Hospital", "Successful", None),
        (patient_ids["P009"], doctor_ids["DOC004"], "Knee Arthroscopy", "2024-02-15", "City Hospital", "Successful", "Physiotherapy recommended")
    ])

cursor.execute("SELECT COUNT(*) FROM medical_records")

if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO medical_records
    (patient_id, doctor_id, admission_id, record_date,
     diagnosis, treatment, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [
        (patient_ids["P001"], doctor_ids["DOC001"], admission_ids[patient_ids["P001"]], "2026-08-28", "Chest pain", "Cardiac monitoring", "ECG and blood tests ordered"),
        (patient_ids["P003"], doctor_ids["DOC003"], admission_ids[patient_ids["P003"]], "2026-08-30", "Fever", "Fluids and medication", "Patient under observation"),
        (patient_ids["P005"], doctor_ids["DOC001"], admission_ids[patient_ids["P005"]], "2026-08-25", "Hypertension", "Blood pressure management", "BP monitored regularly"),
        (patient_ids["P008"], doctor_ids["DOC001"], admission_ids[patient_ids["P008"]], "2026-08-27", "Cardiac monitoring", "Observation and medication", "Stable condition")
    ])

cursor.execute("SELECT COUNT(*) FROM vital_signs")

if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO vital_signs
    (patient_id, recorded_by, recorded_date, temperature,
     systolic_bp, diastolic_bp, heart_rate, respiratory_rate,
     oxygen_saturation, weight, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (patient_ids["P001"], staff_ids["STF005"], "2026-08-28", 36.8, 145, 92, 88, 18, 97.0, 78.5, "Blood pressure elevated"),
        (patient_ids["P003"], staff_ids["STF002"], "2026-08-30", 38.5, 125, 80, 96, 20, 96.0, 70.2, "Fever recorded"),
        (patient_ids["P005"], staff_ids["STF005"], "2026-08-25", 36.7, 155, 95, 82, 18, 98.0, 82.0, "Hypertension"),
        (patient_ids["P008"], staff_ids["STF005"], "2026-08-27", 36.6, 130, 84, 76, 17, 98.0, 68.4, "Stable")
    ])

cursor.execute("SELECT COUNT(*) FROM lab_tests")

if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO lab_tests
    (patient_id, doctor_id, test_name, test_date, result,
     unit, reference_range, status, remarks)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (patient_ids["P001"], doctor_ids["DOC001"], "CBC", "2026-08-28", "Normal", None, "See reference report", "Normal", None),
        (patient_ids["P001"], doctor_ids["DOC001"], "Blood Glucose", "2026-08-28", "118", "mg/dL", "70-99", "High", "Fasting"),
        (patient_ids["P003"], doctor_ids["DOC003"], "CBC", "2026-08-30", "WBC 13.2", "x10^9/L", "4-11", "High", "Elevated WBC"),
        (patient_ids["P005"], doctor_ids["DOC001"], "Lipid Profile", "2026-08-25", "LDL 145", "mg/dL", "<100", "High", "Follow-up advised"),
        (patient_ids["P008"], doctor_ids["DOC001"], "HbA1c", "2026-08-27", "6.8", "%", "4-5.6", "High", "Diabetes monitoring"),
        (patient_ids["P010"], doctor_ids["DOC005"], "Blood Glucose", "2026-09-01", "92", "mg/dL", "70-99", "Normal", None)
    ])

cursor.execute("SELECT COUNT(*) FROM scans")

if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO scans
    (patient_id, doctor_id, scan_type, scan_date, body_part,
     findings, impression, remarks)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (patient_ids["P001"], doctor_ids["DOC001"], "Echocardiogram", "2026-08-28", "Heart", "Normal chamber size", "No significant abnormality", None),
        (patient_ids["P003"], doctor_ids["DOC003"], "Chest X-Ray", "2026-08-30", "Chest", "No focal consolidation", "No acute findings", None),
        (patient_ids["P005"], doctor_ids["DOC001"], "Echocardiogram", "2026-08-25", "Heart", "Mild left ventricular hypertrophy", "Clinical correlation advised", None),
        (patient_ids["P009"], doctor_ids["DOC004"], "Knee X-Ray", "2026-09-01", "Right Knee", "Mild joint space narrowing", "Early degenerative changes", None)
    ])

cursor.executemany("""
INSERT OR IGNORE INTO medications
(medication_name, dosage_form, strength, manufacturer, unit_price)
VALUES (?, ?, ?, ?, ?)
""", [
    ("Paracetamol", "Tablet", "500 mg", "Pharma A", 20),
    ("Amoxicillin", "Capsule", "500 mg", "Pharma B", 35),
    ("Amlodipine", "Tablet", "5 mg", "Pharma C", 25),
    ("Metformin", "Tablet", "500 mg", "Pharma D", 18),
    ("Atorvastatin", "Tablet", "20 mg", "Pharma E", 30),
    ("Salbutamol", "Inhaler", "100 mcg", "Pharma F", 450),
    ("Omeprazole", "Capsule", "20 mg", "Pharma G", 15),
    ("Ibuprofen", "Tablet", "400 mg", "Pharma H", 22)
])

medication_ids = {}

cursor.execute("SELECT medication_id, medication_name FROM medications")

for medication_id, medication_name in cursor.fetchall():
    medication_ids[medication_name] = medication_id

cursor.execute("SELECT COUNT(*) FROM prescriptions")

if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO prescriptions
    (patient_id, doctor_id, prescription_date, instructions, status)
    VALUES (?, ?, ?, ?, ?)
    """, [
        (patient_ids["P001"], doctor_ids["DOC001"], "2026-08-28", "Take medicines as prescribed", "Active"),
        (patient_ids["P003"], doctor_ids["DOC003"], "2026-08-30", "Complete the prescribed course", "Active"),
        (patient_ids["P005"], doctor_ids["DOC001"], "2026-08-25", "Take daily and monitor BP", "Active"),
        (patient_ids["P008"], doctor_ids["DOC001"], "2026-08-27", "Take with meals", "Active")
    ])

prescription_ids = []

cursor.execute("SELECT prescription_id FROM prescriptions ORDER BY prescription_id")

for row in cursor.fetchall():
    prescription_ids.append(row[0])

cursor.execute("SELECT COUNT(*) FROM prescription_items")

if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO prescription_items
    (prescription_id, medication_id, dosage, frequency,
     duration, quantity, instructions)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [
        (prescription_ids[0], medication_ids["Amlodipine"], "5 mg", "Once daily", "30 days", 30, "After breakfast"),
        (prescription_ids[0], medication_ids["Atorvastatin"], "20 mg", "Once daily", "30 days", 30, "At night"),
        (prescription_ids[1], medication_ids["Paracetamol"], "500 mg", "Twice daily", "5 days", 10, "After meals"),
        (prescription_ids[1], medication_ids["Omeprazole"], "20 mg", "Once daily", "5 days", 5, "Before breakfast"),
        (prescription_ids[2], medication_ids["Amlodipine"], "5 mg", "Once daily", "30 days", 30, "After breakfast"),
        (prescription_ids[3], medication_ids["Metformin"], "500 mg", "Twice daily", "30 days", 60, "With meals")
    ])

prescription_item_ids = []

cursor.execute("""
SELECT prescription_item_id
FROM prescription_items
ORDER BY prescription_item_id
""")

for row in cursor.fetchall():
    prescription_item_ids.append(row[0])

cursor.execute("SELECT COUNT(*) FROM pharmacy_history")

if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO pharmacy_history
    (patient_id, prescription_item_id, medication_id,
     dispensing_date, quantity, amount, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [
        (patient_ids["P001"], prescription_item_ids[0], medication_ids["Amlodipine"], "2026-08-28", 30, 750, "Dispensed"),
        (patient_ids["P001"], prescription_item_ids[1], medication_ids["Atorvastatin"], "2026-08-28", 30, 900, "Dispensed"),
        (patient_ids["P003"], prescription_item_ids[2], medication_ids["Paracetamol"], "2026-08-30", 10, 200, "Dispensed"),
        (patient_ids["P003"], prescription_item_ids[3], medication_ids["Omeprazole"], "2026-08-30", 5, 75, "Dispensed"),
        (patient_ids["P005"], prescription_item_ids[4], medication_ids["Amlodipine"], "2026-08-25", 30, 750, "Dispensed"),
        (patient_ids["P008"], prescription_item_ids[5], medication_ids["Metformin"], "2026-08-27", 60, 1080, "Dispensed")
    ])

cursor.execute("SELECT COUNT(*) FROM discharge_records")

if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO discharge_records
    (patient_id, admission_id, discharge_date, final_diagnosis,
     discharge_condition, instructions, follow_up_date)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [
        (patient_ids["P001"], admission_ids[patient_ids["P001"]], "2026-08-31", "Chest pain under evaluation", "Stable", "Continue medication and follow-up", "2026-09-10"),
        (patient_ids["P005"], admission_ids[patient_ids["P005"]], "2026-08-29", "Hypertension", "Stable", "Continue BP medication", "2026-09-12"),
        (patient_ids["P008"], admission_ids[patient_ids["P008"]], "2026-08-30", "Cardiac monitoring", "Stable", "Continue regular monitoring", "2026-09-15")
    ])

cursor.executemany("""
INSERT OR IGNORE INTO hospital_services
(service_name, category, default_charge)
VALUES (?, ?, ?)
""", [
    ("Doctor Consultation", "Consultation", 2000),
    ("General Room", "Room", 3000),
    ("Private Room", "Room", 7000),
    ("CBC", "Laboratory", 1500),
    ("Blood Glucose", "Laboratory", 800),
    ("Lipid Profile", "Laboratory", 2500),
    ("HbA1c", "Laboratory", 1800),
    ("Chest X-Ray", "Radiology", 2000),
    ("Knee X-Ray", "Radiology", 2000),
    ("Echocardiogram", "Radiology", 5000),
    ("Medication", "Pharmacy", 0),
    ("General Treatment", "Treatment", 3000)
])

service_ids = {}

cursor.execute("SELECT service_id, service_name FROM hospital_services")

for service_id, service_name in cursor.fetchall():
    service_ids[service_name] = service_id

cursor.execute("SELECT COUNT(*) FROM service_records")

if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO service_records
    (patient_id, service_id, admission_id, service_date,
     quantity, charge, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [
        (patient_ids["P001"], service_ids["Doctor Consultation"], admission_ids[patient_ids["P001"]], "2026-08-28", 1, 2000, None),
        (patient_ids["P001"], service_ids["CBC"], admission_ids[patient_ids["P001"]], "2026-08-28", 1, 1500, None),
        (patient_ids["P001"], service_ids["Echocardiogram"], admission_ids[patient_ids["P001"]], "2026-08-28", 1, 5000, None),
        (patient_ids["P003"], service_ids["Doctor Consultation"], admission_ids[patient_ids["P003"]], "2026-08-30", 1, 2000, None),
        (patient_ids["P003"], service_ids["CBC"], admission_ids[patient_ids["P003"]], "2026-08-30", 1, 1500, None),
        (patient_ids["P003"], service_ids["Chest X-Ray"], admission_ids[patient_ids["P003"]], "2026-08-30", 1, 2000, None),
        (patient_ids["P005"], service_ids["Doctor Consultation"], admission_ids[patient_ids["P005"]], "2026-08-25", 1, 2000, None),
        (patient_ids["P005"], service_ids["Lipid Profile"], admission_ids[patient_ids["P005"]], "2026-08-25", 1, 2500, None),
        (patient_ids["P005"], service_ids["Echocardiogram"], admission_ids[patient_ids["P005"]], "2026-08-25", 1, 5000, None),
        (patient_ids["P008"], service_ids["Doctor Consultation"], admission_ids[patient_ids["P008"]], "2026-08-27", 1, 2000, None),
        (patient_ids["P008"], service_ids["HbA1c"], admission_ids[patient_ids["P008"]], "2026-08-27", 1, 1800, None),
        (patient_ids["P008"], service_ids["Echocardiogram"], admission_ids[patient_ids["P008"]], "2026-08-27", 1, 5000, None)
    ])

cursor.execute("SELECT COUNT(*) FROM bills")

if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO bills
    (patient_id, admission_id, bill_date, discount)
    VALUES (?, ?, ?, ?)
    """, [
        (patient_ids["P001"], admission_ids[patient_ids["P001"]], "2026-08-31", 500),
        (patient_ids["P003"], admission_ids[patient_ids["P003"]], "2026-08-30", 0),
        (patient_ids["P005"], admission_ids[patient_ids["P005"]], "2026-08-29", 1000),
        (patient_ids["P008"], admission_ids[patient_ids["P008"]], "2026-08-30", 500)
    ])

bill_ids = []

cursor.execute("SELECT bill_id FROM bills ORDER BY bill_id")

for row in cursor.fetchall():
    bill_ids.append(row[0])

cursor.execute("SELECT COUNT(*) FROM bill_items")

if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO bill_items
    (bill_id, service_id, description, quantity, unit_price, amount)
    VALUES (?, ?, ?, ?, ?, ?)
    """, [
        (bill_ids[0], service_ids["Doctor Consultation"], "Doctor Consultation", 1, 2000, 2000),
        (bill_ids[0], service_ids["General Room"], "Room Charges", 3, 3000, 9000),
        (bill_ids[0], service_ids["CBC"], "CBC", 1, 1500, 1500),
        (bill_ids[0], service_ids["Echocardiogram"], "Echocardiogram", 1, 5000, 5000),
        (bill_ids[1], service_ids["Doctor Consultation"], "Doctor Consultation", 1, 2000, 2000),
        (bill_ids[1], service_ids["General Room"], "Room Charges", 1, 3000, 3000),
        (bill_ids[1], service_ids["CBC"], "CBC", 1, 1500, 1500),
        (bill_ids[1], service_ids["Chest X-Ray"], "Chest X-Ray", 1, 2000, 2000),
        (bill_ids[2], service_ids["Doctor Consultation"], "Doctor Consultation", 1, 2000, 2000),
        (bill_ids[2], service_ids["Private Room"], "Room Charges", 4, 7000, 28000),
        (bill_ids[2], service_ids["Lipid Profile"], "Lipid Profile", 1, 2500, 2500),
        (bill_ids[2], service_ids["Echocardiogram"], "Echocardiogram", 1, 5000, 5000),
        (bill_ids[3], service_ids["Doctor Consultation"], "Doctor Consultation", 1, 2000, 2000),
        (bill_ids[3], service_ids["General Room"], "Room Charges", 3, 3000, 9000),
        (bill_ids[3], service_ids["HbA1c"], "HbA1c", 1, 1800, 1800),
        (bill_ids[3], service_ids["Echocardiogram"], "Echocardiogram", 1, 5000, 5000)
    ])

cursor.execute("SELECT COUNT(*) FROM payments")

if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO payments
    (bill_id, patient_id, payment_date, amount, payment_method, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, [
        (bill_ids[0], patient_ids["P001"], "2026-08-31", 10000, "Cash", "Completed"),
        (bill_ids[1], patient_ids["P003"], "2026-08-30", 5000, "Card", "Completed"),
        (bill_ids[2], patient_ids["P005"], "2026-08-29", 15000, "Bank Transfer", "Completed"),
        (bill_ids[3], patient_ids["P008"], "2026-08-30", 8000, "Cash", "Completed")
    ])

cursor.execute("SELECT COUNT(*) FROM welfare_assistance")

if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO welfare_assistance
    (patient_id, bill_id, assistance_date, assistance_type,
     amount, reason, approved_by)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [
        (patient_ids["P001"], bill_ids[0], "2026-08-31", "Hospital Welfare", 2000, "Financial assistance", staff_ids["STF001"]),
        (patient_ids["P003"], bill_ids[1], "2026-08-30", "Charity Assistance", 1500, "Financial assistance", staff_ids["STF001"]),
        (patient_ids["P008"], bill_ids[3], "2026-08-30", "Hospital Welfare", 1000, "Financial assistance", staff_ids["STF001"])
    ])

cursor.execute("SELECT COUNT(*) FROM follow_ups")

if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO follow_ups
    (patient_id, doctor_id, follow_up_date, reason, status, notes)
    VALUES (?, ?, ?, ?, ?, ?)
    """, [
        (patient_ids["P001"], doctor_ids["DOC001"], "2026-09-10", "Cardiac follow-up", "Scheduled", None),
        (patient_ids["P005"], doctor_ids["DOC001"], "2026-09-12", "Blood pressure review", "Scheduled", None),
        (patient_ids["P008"], doctor_ids["DOC001"], "2026-09-15", "Cardiac monitoring", "Scheduled", None),
        (patient_ids["P003"], doctor_ids["DOC003"], "2026-09-07", "Fever follow-up", "Scheduled", None)
    ])

cursor.execute("SELECT COUNT(*) FROM notifications")

if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO notifications
    (patient_id, staff_id, title, message, notification_type, is_read)
    VALUES (?, ?, ?, ?, ?, ?)
    """, [
        (patient_ids["P001"], None, "Lab Result Available", "Your laboratory results are available in the patient portal.", "Lab", 0),
        (patient_ids["P001"], None, "Follow-up Appointment", "Your cardiac follow-up appointment is scheduled.", "Appointment", 0),
        (patient_ids["P003"], None, "Admission Update", "Your current admission record has been updated.", "Admission", 0),
        (patient_ids["P005"], None, "Payment Reminder", "There is a remaining balance on your hospital bill.", "Billing", 0),
        (None, staff_ids["STF001"], "New Patient Record", "A new patient record is available for review.", "System", 0)
    ])

 
connection.commit()
connection.close()