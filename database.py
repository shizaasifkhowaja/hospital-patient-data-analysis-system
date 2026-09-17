import sqlite3

connection = sqlite3.connect("hospital.db")
cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

cursor.executescript("""
CREATE TABLE IF NOT EXISTS patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_code TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    address TEXT,
    emergency_contact_name TEXT,
    emergency_contact_phone TEXT,
    registration_date TEXT NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS demographics (
    demographic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL UNIQUE,
    gender TEXT NOT NULL,
    blood_group TEXT,
    marital_status TEXT,
    nationality TEXT,
    occupation TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_code TEXT NOT NULL UNIQUE,
    department_name TEXT NOT NULL UNIQUE,
    location TEXT,
    phone TEXT
);

CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_code TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    specialization TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    department_id INTEGER NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE IF NOT EXISTS staff (
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff_code TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    role TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    department_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    appointment_date TEXT NOT NULL,
    appointment_time TEXT NOT NULL,
    reason TEXT,
    status TEXT NOT NULL DEFAULT 'Scheduled',
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

CREATE TABLE IF NOT EXISTS rooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ward_name TEXT NOT NULL,
    room_number TEXT NOT NULL,
    bed_number TEXT NOT NULL,
    room_type TEXT,
    daily_charge REAL NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'Available',
    UNIQUE (room_number, bed_number)
);

CREATE TABLE IF NOT EXISTS admissions (
    admission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    room_id INTEGER,
    admission_date TEXT NOT NULL,
    discharge_date TEXT,
    admission_reason TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Admitted',
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);

CREATE TABLE IF NOT EXISTS medical_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    condition_name TEXT NOT NULL,
    diagnosis_date TEXT,
    treatment TEXT,
    status TEXT,
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS allergies (
    allergy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    allergen TEXT NOT NULL,
    reaction TEXT,
    severity TEXT,
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS surgeries (
    surgery_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER,
    surgery_name TEXT NOT NULL,
    surgery_date TEXT,
    hospital_name TEXT,
    outcome TEXT,
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

CREATE TABLE IF NOT EXISTS medical_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER,
    admission_id INTEGER,
    record_date TEXT NOT NULL,
    diagnosis TEXT NOT NULL,
    treatment TEXT,
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY (admission_id) REFERENCES admissions(admission_id)
);

CREATE TABLE IF NOT EXISTS vital_signs (
    vital_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    recorded_by INTEGER,
    recorded_date TEXT NOT NULL,
    temperature REAL,
    systolic_bp INTEGER,
    diastolic_bp INTEGER,
    heart_rate INTEGER,
    respiratory_rate INTEGER,
    oxygen_saturation REAL,
    weight REAL,
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (recorded_by) REFERENCES staff(staff_id)
);

CREATE TABLE IF NOT EXISTS lab_tests (
    lab_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER,
    test_name TEXT NOT NULL,
    test_date TEXT NOT NULL,
    result TEXT,
    unit TEXT,
    reference_range TEXT,
    status TEXT,
    remarks TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

CREATE TABLE IF NOT EXISTS scans (
    scan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER,
    scan_type TEXT NOT NULL,
    scan_date TEXT NOT NULL,
    body_part TEXT,
    findings TEXT,
    impression TEXT,
    remarks TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

CREATE TABLE IF NOT EXISTS medications (
    medication_id INTEGER PRIMARY KEY AUTOINCREMENT,
    medication_name TEXT NOT NULL,
    dosage_form TEXT,
    strength TEXT,
    manufacturer TEXT,
    unit_price REAL NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS prescriptions (
    prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    prescription_date TEXT NOT NULL,
    instructions TEXT,
    status TEXT NOT NULL DEFAULT 'Active',
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

CREATE TABLE IF NOT EXISTS prescription_items (
    prescription_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prescription_id INTEGER NOT NULL,
    medication_id INTEGER NOT NULL,
    dosage TEXT,
    frequency TEXT,
    duration TEXT,
    quantity INTEGER,
    instructions TEXT,
    FOREIGN KEY (prescription_id) REFERENCES prescriptions(prescription_id) ON DELETE CASCADE,
    FOREIGN KEY (medication_id) REFERENCES medications(medication_id)
);

CREATE TABLE IF NOT EXISTS pharmacy_history (
    pharmacy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    prescription_item_id INTEGER,
    medication_id INTEGER NOT NULL,
    dispensing_date TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    amount REAL NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'Dispensed',
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (prescription_item_id) REFERENCES prescription_items(prescription_item_id),
    FOREIGN KEY (medication_id) REFERENCES medications(medication_id)
);

CREATE TABLE IF NOT EXISTS discharge_records (
    discharge_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    admission_id INTEGER NOT NULL UNIQUE,
    discharge_date TEXT NOT NULL,
    final_diagnosis TEXT,
    discharge_condition TEXT,
    instructions TEXT,
    follow_up_date TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (admission_id) REFERENCES admissions(admission_id)
);

CREATE TABLE IF NOT EXISTS hospital_services (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    default_charge REAL NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS service_records (
    service_record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    admission_id INTEGER,
    service_date TEXT NOT NULL DEFAULT CURRENT_DATE,
    quantity INTEGER NOT NULL DEFAULT 1,
    charge REAL NOT NULL DEFAULT 0,
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (service_id) REFERENCES hospital_services(service_id),
    FOREIGN KEY (admission_id) REFERENCES admissions(admission_id)
);

CREATE TABLE IF NOT EXISTS bills (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    admission_id INTEGER,
    bill_date TEXT NOT NULL DEFAULT CURRENT_DATE,
    discount REAL NOT NULL DEFAULT 0,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (admission_id) REFERENCES admissions(admission_id)
);

CREATE TABLE IF NOT EXISTS bill_items (
    bill_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_id INTEGER NOT NULL,
    service_id INTEGER,
    description TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price REAL NOT NULL DEFAULT 0,
    amount REAL NOT NULL DEFAULT 0,
    FOREIGN KEY (bill_id) REFERENCES bills(bill_id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES hospital_services(service_id)
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_id INTEGER NOT NULL,
    patient_id INTEGER NOT NULL,
    payment_date TEXT NOT NULL DEFAULT CURRENT_DATE,
    amount REAL NOT NULL,
    payment_method TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Completed',
    FOREIGN KEY (bill_id) REFERENCES bills(bill_id),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

CREATE TABLE IF NOT EXISTS welfare_assistance (
    welfare_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    bill_id INTEGER,
    assistance_date TEXT NOT NULL DEFAULT CURRENT_DATE,
    assistance_type TEXT,
    amount REAL NOT NULL,
    reason TEXT,
    approved_by INTEGER,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (bill_id) REFERENCES bills(bill_id),
    FOREIGN KEY (approved_by) REFERENCES staff(staff_id)
);

CREATE TABLE IF NOT EXISTS follow_ups (
    follow_up_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    follow_up_date TEXT NOT NULL,
    reason TEXT,
    status TEXT NOT NULL DEFAULT 'Scheduled',
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

CREATE TABLE IF NOT EXISTS notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    staff_id INTEGER,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    notification_type TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_read INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id) ON DELETE CASCADE
);
""")

connection.commit()
connection.close()