# Hospital Patient Data Analysis System

A full-stack hospital patient management and data analysis project built as a semester project.

## About

This project is a hospital-focused system for managing and exploring patient information through a structured database and web-based interface.

It brings patient records, appointments, medical history, laboratory results, prescriptions, billing, and other hospital information into one system, with a dashboard for viewing and analyzing the data.

## Features

* Patient profiles and personal information
* Appointments, admissions, rooms and departments
* Medical history, allergies and surgeries
* Vital signs, laboratory tests and scan records
* Prescriptions and pharmacy history
* Billing, payments and welfare assistance
* Follow-ups and patient notifications
* Dashboard with hospital data insights

## Built With

* Python
* Flask
* SQLite
* HTML
* CSS
* JavaScript

## Database

The system uses a relational SQLite database with separate tables for different areas of hospital information.

The database includes patient records along with demographics, doctors, departments, appointments, admissions, medical history, allergies, surgeries, medical records, vital signs, laboratory tests, scans, prescriptions, pharmacy history, billing, payments, welfare assistance, follow-ups and notifications.

## Project Structure

```text
Hospital Patient Data Analysis System/
│
├── app.py
├── database.py
├── insert_data.py
├── check_database.py
├── hospital.db
│
├── templates/
│   ├── dashboard.html
│   ├── patients.html
│   └── patient_detail.html
│
└── static/
    └── style.css
```

## Running the Project

### 1. Install Flask

```bash
python -m pip install flask
```

### 2. Run the application

```bash
python app.py
```

### 3. Open the application

Open the local Flask address shown in the terminal.

## Current Status

This project is currently being developed as a semester project, with the system being expanded and refined as new hospital features and interface improvements are added.
