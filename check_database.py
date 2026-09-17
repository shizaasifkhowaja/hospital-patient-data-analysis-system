import sqlite3

connection = sqlite3.connect("hospital.db")
cursor = connection.cursor()

tables = [
    "patients",
    "demographics",
    "departments",
    "doctors",
    "staff",
    "appointments",
    "rooms",
    "admissions",
    "medical_history",
    "allergies",
    "surgeries",
    "medical_records",
    "vital_signs",
    "lab_tests",
    "scans",
    "medications",
    "prescriptions",
    "prescription_items",
    "pharmacy_history",
    "discharge_records",
    "hospital_services",
    "service_records",
    "bills",
    "bill_items",
    "payments",
    "welfare_assistance",
    "follow_ups",
    "notifications"
]

print("HOSPITAL DATABASE DATA CHECK")
print("-" * 40)

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]

    print(f"{table:<25} {count} records")

connection.close()