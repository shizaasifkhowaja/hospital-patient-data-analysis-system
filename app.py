from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)
app.json.sort_keys = False

DATABASE = "hospital.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def rows_to_list(rows):
    return [dict(row) for row in rows]


@app.route("/")
def home():
    return "Hospital Patient Portal Backend is Running!"


@app.route("/patients")
def get_patients():
    connection = get_db_connection()

    patients = connection.execute("""
        SELECT *
        FROM patients
        ORDER BY patient_id
    """).fetchall()

    connection.close()

    return jsonify(rows_to_list(patients))


@app.route("/patient/<int:patient_id>")
def get_patient(patient_id):
    connection = get_db_connection()

    patient = connection.execute("""
        SELECT *
        FROM patients
        WHERE patient_id = ?
    """, (patient_id,)).fetchone()

    if patient is None:
        connection.close()
        return jsonify({
            "error": "Patient not found"
        }), 404

    demographics = connection.execute("""
        SELECT *
        FROM demographics
        WHERE patient_id = ?
    """, (patient_id,)).fetchone()

    medical_history = connection.execute("""
        SELECT *
        FROM medical_history
        WHERE patient_id = ?
        ORDER BY diagnosis_date DESC
    """, (patient_id,)).fetchall()

    allergies = connection.execute("""
        SELECT *
        FROM allergies
        WHERE patient_id = ?
        ORDER BY allergy_id
    """, (patient_id,)).fetchall()

    appointments = connection.execute("""
        SELECT
            a.appointment_id,
            a.appointment_date,
            a.appointment_time,
            a.reason,
            a.status,
            a.notes,
            d.doctor_id,
            d.doctor_code,
            d.first_name AS doctor_first_name,
            d.last_name AS doctor_last_name,
            d.specialization,
            dep.department_id,
            dep.department_name,
            dep.location AS department_location
        FROM appointments a
        JOIN doctors d
            ON a.doctor_id = d.doctor_id
        JOIN departments dep
            ON d.department_id = dep.department_id
        WHERE a.patient_id = ?
        ORDER BY a.appointment_date DESC,
                 a.appointment_time DESC
    """, (patient_id,)).fetchall()

    admissions = connection.execute("""
        SELECT
            a.admission_id,
            a.admission_date,
            a.discharge_date,
            a.admission_reason,
            a.status,
            a.notes,
            d.doctor_id,
            d.doctor_code,
            d.first_name AS doctor_first_name,
            d.last_name AS doctor_last_name,
            d.specialization,
            r.room_id,
            r.ward_name,
            r.room_number,
            r.bed_number,
            r.room_type,
            r.daily_charge,
            r.status AS room_status
        FROM admissions a
        JOIN doctors d
            ON a.doctor_id = d.doctor_id
        LEFT JOIN rooms r
            ON a.room_id = r.room_id
        WHERE a.patient_id = ?
        ORDER BY a.admission_date DESC
    """, (patient_id,)).fetchall()

    surgeries = connection.execute("""
        SELECT
            s.*,
            d.doctor_code,
            d.first_name AS doctor_first_name,
            d.last_name AS doctor_last_name,
            d.specialization
        FROM surgeries s
        LEFT JOIN doctors d
            ON s.doctor_id = d.doctor_id
        WHERE s.patient_id = ?
        ORDER BY s.surgery_date DESC
    """, (patient_id,)).fetchall()

    medical_records = connection.execute("""
        SELECT
            m.*,
            d.doctor_code,
            d.first_name AS doctor_first_name,
            d.last_name AS doctor_last_name,
            d.specialization
        FROM medical_records m
        LEFT JOIN doctors d
            ON m.doctor_id = d.doctor_id
        WHERE m.patient_id = ?
        ORDER BY m.record_date DESC
    """, (patient_id,)).fetchall()

    vital_signs = connection.execute("""
        SELECT
            v.*,
            s.staff_code,
            s.first_name AS staff_first_name,
            s.last_name AS staff_last_name,
            s.role AS staff_role
        FROM vital_signs v
        LEFT JOIN staff s
            ON v.recorded_by = s.staff_id
        WHERE v.patient_id = ?
        ORDER BY v.recorded_date DESC
    """, (patient_id,)).fetchall()

    lab_tests = connection.execute("""
        SELECT
            l.*,
            d.doctor_code,
            d.first_name AS doctor_first_name,
            d.last_name AS doctor_last_name,
            d.specialization
        FROM lab_tests l
        LEFT JOIN doctors d
            ON l.doctor_id = d.doctor_id
        WHERE l.patient_id = ?
        ORDER BY l.test_date DESC
    """, (patient_id,)).fetchall()

    scans = connection.execute("""
        SELECT
            s.*,
            d.doctor_code,
            d.first_name AS doctor_first_name,
            d.last_name AS doctor_last_name,
            d.specialization
        FROM scans s
        LEFT JOIN doctors d
            ON s.doctor_id = d.doctor_id
        WHERE s.patient_id = ?
        ORDER BY s.scan_date DESC
    """, (patient_id,)).fetchall()

    prescriptions = connection.execute("""
        SELECT
            p.*,
            d.doctor_code,
            d.first_name AS doctor_first_name,
            d.last_name AS doctor_last_name,
            d.specialization
        FROM prescriptions p
        JOIN doctors d
            ON p.doctor_id = d.doctor_id
        WHERE p.patient_id = ?
        ORDER BY p.prescription_date DESC
    """, (patient_id,)).fetchall()

    prescription_items = connection.execute("""
        SELECT
            pi.*,
            p.prescription_date,
            p.status AS prescription_status,
            m.medication_name,
            m.dosage_form,
            m.strength,
            m.manufacturer,
            m.unit_price
        FROM prescription_items pi
        JOIN prescriptions p
            ON pi.prescription_id = p.prescription_id
        JOIN medications m
            ON pi.medication_id = m.medication_id
        WHERE p.patient_id = ?
        ORDER BY p.prescription_date DESC
    """, (patient_id,)).fetchall()

    pharmacy_history = connection.execute("""
        SELECT
            ph.*,
            m.medication_name,
            m.dosage_form,
            m.strength,
            m.manufacturer
        FROM pharmacy_history ph
        JOIN medications m
            ON ph.medication_id = m.medication_id
        WHERE ph.patient_id = ?
        ORDER BY ph.dispensing_date DESC
    """, (patient_id,)).fetchall()

    discharge_records = connection.execute("""
        SELECT *
        FROM discharge_records
        WHERE patient_id = ?
        ORDER BY discharge_date DESC
    """, (patient_id,)).fetchall()

    service_records = connection.execute("""
        SELECT
            sr.*,
            hs.service_name,
            hs.category,
            hs.default_charge
        FROM service_records sr
        JOIN hospital_services hs
            ON sr.service_id = hs.service_id
        WHERE sr.patient_id = ?
        ORDER BY sr.service_date DESC
    """, (patient_id,)).fetchall()

    bills = connection.execute("""
        SELECT *
        FROM bills
        WHERE patient_id = ?
        ORDER BY bill_date DESC
    """, (patient_id,)).fetchall()

    bill_items = connection.execute("""
        SELECT
            bi.*,
            b.bill_date,
            b.discount,
            hs.service_name,
            hs.category
        FROM bill_items bi
        JOIN bills b
            ON bi.bill_id = b.bill_id
        LEFT JOIN hospital_services hs
            ON bi.service_id = hs.service_id
        WHERE b.patient_id = ?
        ORDER BY b.bill_date DESC
    """, (patient_id,)).fetchall()

    payments = connection.execute("""
        SELECT
            p.*,
            b.bill_date,
            b.discount
        FROM payments p
        JOIN bills b
            ON p.bill_id = b.bill_id
        WHERE p.patient_id = ?
        ORDER BY p.payment_date DESC
    """, (patient_id,)).fetchall()

    welfare_assistance = connection.execute("""
        SELECT
            w.*,
            b.bill_date,
            s.staff_code,
            s.first_name AS staff_first_name,
            s.last_name AS staff_last_name,
            s.role AS staff_role
        FROM welfare_assistance w
        LEFT JOIN bills b
            ON w.bill_id = b.bill_id
        LEFT JOIN staff s
            ON w.approved_by = s.staff_id
        WHERE w.patient_id = ?
        ORDER BY w.assistance_date DESC
    """, (patient_id,)).fetchall()

    follow_ups = connection.execute("""
        SELECT
            f.*,
            d.doctor_code,
            d.first_name AS doctor_first_name,
            d.last_name AS doctor_last_name,
            d.specialization
        FROM follow_ups f
        JOIN doctors d
            ON f.doctor_id = d.doctor_id
        WHERE f.patient_id = ?
        ORDER BY f.follow_up_date DESC
    """, (patient_id,)).fetchall()

    notifications = connection.execute("""
        SELECT
            n.*,
            s.staff_code,
            s.first_name AS staff_first_name,
            s.last_name AS staff_last_name,
            s.role AS staff_role
        FROM notifications n
        LEFT JOIN staff s
            ON n.staff_id = s.staff_id
        WHERE n.patient_id = ?
        ORDER BY n.created_at DESC
    """, (patient_id,)).fetchall()

    patient_data = {
        "patient": dict(patient),
        "demographics": dict(demographics) if demographics else None,
        "medical_history": rows_to_list(medical_history),
        "allergies": rows_to_list(allergies),
        "appointments": rows_to_list(appointments),
        "admissions": rows_to_list(admissions),
        "surgeries": rows_to_list(surgeries),
        "medical_records": rows_to_list(medical_records),
        "vital_signs": rows_to_list(vital_signs),
        "lab_tests": rows_to_list(lab_tests),
        "scans": rows_to_list(scans),
        "prescriptions": rows_to_list(prescriptions),
        "prescription_items": rows_to_list(prescription_items),
        "pharmacy_history": rows_to_list(pharmacy_history),
        "discharge_records": rows_to_list(discharge_records),
        "service_records": rows_to_list(service_records),
        "bills": rows_to_list(bills),
        "bill_items": rows_to_list(bill_items),
        "payments": rows_to_list(payments),
        "welfare_assistance": rows_to_list(welfare_assistance),
        "follow_ups": rows_to_list(follow_ups),
        "notifications": rows_to_list(notifications)
    }

    return render_template(
        "patient_detail.html",
        patient=patient_data["patient"],
        demographics=patient_data["demographics"],
        medical_history=patient_data["medical_history"],
        allergies=patient_data["allergies"],
        appointments=patient_data["appointments"],
        admissions=patient_data["admissions"],
        surgeries=patient_data["surgeries"],
        medical_records=patient_data["medical_records"],
        vital_signs=patient_data["vital_signs"],
        lab_tests=patient_data["lab_tests"],
        scans=patient_data["scans"],
        prescriptions=patient_data["prescriptions"],
        prescription_items=patient_data["prescription_items"],
        pharmacy_history=patient_data["pharmacy_history"],
        discharge_records=patient_data["discharge_records"],
        service_records=patient_data["service_records"],
        bills=patient_data["bills"],
        bill_items=patient_data["bill_items"],
        payments=patient_data["payments"],
        welfare_assistance=patient_data["welfare_assistance"],
        follow_ups=patient_data["follow_ups"],
        notifications=patient_data["notifications"]
    )


@app.route("/dashboard")
def dashboard():
    connection = get_db_connection()

    total_patients = connection.execute("""
        SELECT COUNT(*) AS total
        FROM patients
    """).fetchone()["total"]

    total_appointments = connection.execute("""
        SELECT COUNT(*) AS total
        FROM appointments
    """).fetchone()["total"]

    total_admissions = connection.execute("""
        SELECT COUNT(*) AS total
        FROM admissions
    """).fetchone()["total"]

    pending_bills = connection.execute("""
        SELECT COUNT(*) AS total
        FROM bills b
        WHERE (
            SELECT COALESCE(SUM(amount), 0)
            FROM bill_items bi
            WHERE bi.bill_id = b.bill_id
        ) - b.discount
        >
        (
            SELECT COALESCE(SUM(amount), 0)
            FROM payments p
            WHERE p.bill_id = b.bill_id
            AND p.status = 'Completed'
        )
    """).fetchone()["total"]

    connection.close()

    return render_template(
        "dashboard.html",
        total_patients=total_patients,
        total_appointments=total_appointments,
        total_admissions=total_admissions,
        pending_bills=pending_bills
    )


@app.route("/patients-page")
def patients_page():
    connection = get_db_connection()

    patients = connection.execute("""
        SELECT *
        FROM patients
        ORDER BY patient_id
    """).fetchall()

    connection.close()

    return render_template(
        "patients.html",
        patients=patients
    )


@app.route("/appointments-page")
def appointments_page():
    connection = get_db_connection()

    appointments = connection.execute("""
        SELECT
            a.appointment_id,
            a.patient_id,
            a.doctor_id,
            a.appointment_date,
            a.appointment_time,
            a.reason,
            a.status,
            a.notes,
            p.first_name AS patient_first_name,
            p.last_name AS patient_last_name,
            d.first_name AS doctor_first_name,
            d.last_name AS doctor_last_name,
            d.specialization
        FROM appointments a
        JOIN patients p
            ON a.patient_id = p.patient_id
        JOIN doctors d
            ON a.doctor_id = d.doctor_id
        ORDER BY a.appointment_id ASC
    """).fetchall()

    connection.close()

    return render_template(
        "appointments.html",
        appointments=appointments
    )


if __name__ == "__main__":
    app.run(debug=True)