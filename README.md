# Smart Attendance & Workforce Analytics Dashboard

A modern **Flask-based HR Management System** that provides employee management, attendance tracking, department management, workforce analytics, and interactive reporting. The application is designed to help organizations monitor employee attendance, manage HR operations, and gain actionable insights through visual dashboards.

---

## Features

### Authentication

* Secure login system
* Password hashing using Werkzeug
* Session management with Flask-Login
* Role-based user support

### Dashboard

* Real-time attendance overview
* Employee statistics
* Department-wise employee distribution
* Interactive charts using Chart.js
* HR analytics overview

### Employee Management

* Add new employees
* Edit employee information
* Delete employees
* Search employees
* Department assignment
* Shift information
* Salary management

### Department Management

* Create departments
* Update department details
* Department descriptions
* Employee count per department

### Attendance Management

* Daily attendance records
* Check-in and check-out times
* Attendance status

  * Present
  * Late
  * Absent
* Attendance history
* Attendance percentage calculation

### Reports & Analytics

* Overall attendance statistics
* Monthly attendance reports
* Yearly attendance reports
* Attendance charts
* Department analytics
* Workforce performance insights

---

## Technologies Used

### Backend

* Python 3.x
* Flask
* Flask-SQLAlchemy
* Flask-Login
* SQLAlchemy
* Werkzeug

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript
* Chart.js
* Font Awesome

### Database

* SQLite

---

## Project Structure

```text
Smart Attendance & HR Analytics Dashboard/
│
├── app/
│   ├── auth/
│   ├── dashboard/
│   ├── employees/
│   ├── departments/
│   ├── attendance/
│   ├── reports/
│   ├── models/
│   ├── templates/
│   ├── static/
│   ├── extensions.py
│   └── __init__.py
│
├── instance/
│   └── hr.db
│
├── run.py
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/smart-attendance-dashboard.git
cd smart-attendance-dashboard
```

### 2. Create a virtual environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database

The project uses SQLite by default.

```python
SQLALCHEMY_DATABASE_URI = "sqlite:///hr.db"
```

### 5. Run the application

```bash
python run.py
```

Open:

```
http://127.0.0.1:5000
```

---

## Default Login

Example administrator account:

```
Email:
admin@hrinsight.com

Password:
admin123
```

*(Update these credentials according to your database.)*

---

## Dashboard Modules

* Employee Statistics
* Today's Attendance Overview
* Employees per Department
* Attendance Summary
* Workforce Analytics

---

## Reports

### Dashboard Report

Displays:

* Total Records
* Present Employees
* Late Employees
* Absent Employees
* Overall Attendance Percentage

### Monthly Report

* Monthly attendance summary
* Attendance chart
* Attendance history
* Attendance percentage

### Yearly Report

* Annual attendance summary
* Trend visualization
* Performance analytics

---

## Database Tables

### Users

* id
* username
* email
* password_hash
* role
* is_active_user
* created_at

### Employees

* employee_code
* first_name
* last_name
* email
* phone
* gender
* date_of_birth
* joining_date
* designation
* salary
* address
* status
* shift
* department_id

### Departments

* department_name
* department_code
* description

### Attendance

* employee_id
* date
* check_in
* check_out
* status

---

## Security Features

* Password hashing
* User authentication
* Session management
* Protected routes
* SQLAlchemy ORM protection against SQL Injection

---

## Future Enhancements

* Face Recognition Attendance
* QR Code Attendance
* Leave Management
* Payroll Module
* Email Notifications
* Employee Performance Analytics
* Export Reports to PDF and Excel
* REST API
* Role-based Access Control
* Multi-branch Management

---

## Author

**Ishan Shridhar**

Cybersecurity Engineer | Python Developer | Flask Developer

---

## License

This project is developed for academic and educational purposes. Feel free to modify and extend it for learning or personal use.
