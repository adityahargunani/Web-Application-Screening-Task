# ⚗️ Chemical Equipment Parameter Visualizer

A full-stack data visualization system for analyzing chemical equipment datasets using **CSV uploads**, built with:

- **Backend**: Django + Django REST Framework
- **Web Frontend**: React + Chart.js
- **Desktop App**: PyQt5 + Matplotlib

This project allows users to upload datasets, analyze equipment parameters, visualize trends, and generate detailed PDF reports.

---

## 🚀 Features

### 🔐 Authentication
- User signup & login
- Token-based authentication
- Per-user dataset history

### 📁 Dataset Management
- CSV-only file upload
- Last 5 datasets stored per user
- Clickable history with summary loading

### 📊 Data Analysis
- Average, minimum, and maximum values
- Equipment type distribution
- Separate charts for:
  - Average Parameters (Bar Chart)
  - Type Distribution (Pie Chart with %)

### 📄 Reporting
- Auto-generated PDF reports
- Includes:
  - Summary statistics
  - Charts
  - Equipment type distribution

### 💻 Multi-Platform
- Web dashboard (React)
- Desktop application (PyQt5)
- Shared backend APIs

---

## 🧩 Tech Stack

| Layer | Technology |
|-----|------------|
Backend | Django, DRF, SQLite |
Web UI | React, Chart.js |
Desktop | PyQt5, Matplotlib |
Auth | Token Authentication |
Reports | ReportLab + Matplotlib |

---

## 🛠️ Installation & Setup

### 1️⃣ Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver




Multi-Platform Support
- Web dashboard built with React
- Desktop application built with PyQt5
- Shared Django REST backend

SYSTEM ARCHITECTURE

Web Frontend (React)
        |
        | REST API
        v
Backend (Django + DRF)
        ^
        | REST API
Desktop App (PyQt5)

TECHNOLOGY STACK

Backend: Django, Django REST Framework
Database: SQLite
Authentication: Token Authentication
Web Frontend: React, Chart.js
Desktop Application: PyQt5, Matplotlib
Reporting: ReportLab, Matplotlib


SETUP INSTRUCTIONS

Backend Setup
1. Navigate to backend directory
2. Create and activate virtual environment
3. Install dependencies
4. Run migrations
5. Start server

Web Frontend Setup
1. Navigate to web-frontend directory
2. Install dependencies
3. Start development server

Desktop Application Setup
1. Navigate to desktop-app directory
2. Install required Python packages
3. Run desktop_app.py

CSV FILE FORMAT

The application accepts CSV files only.

Example:
equipment_type,flowrate,pressure,temperature
Pump,12.5,5.2,85
Valve,8.1,3.9,60
Reactor,15.0,7.8,120

APPLICATION WORKFLOW

1. User logs in or signs up
2. Uploads CSV dataset
3. Views dataset summary
4. Analyzes charts
5. Selects previous datasets from history
6. Downloads PDF report
7. Optionally uses desktop application

DEMO GUIDELINES

Recommended demo flow:
- Show GitHub repository
- Explain architecture
- Run backend server
- Login and upload dataset
- Show charts and history
- Download PDF report
- Demonstrate desktop app

DESIGN PRINCIPLES

- Clean separation of concerns
- Shared backend for scalability
- Focus on usability
- Scientific data presentation
- Real-world engineering practices

FUTURE ENHANCEMENTS

- Dataset comparison
- Dark mode
- Export charts as images
- Advanced filtering
- User profile management
- Cloud deployment

AUTHOR
Aditya Hargunani

LICENSE
This project is intended for educational and demonstration purposes.
