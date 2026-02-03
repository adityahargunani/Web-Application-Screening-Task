#  Chemical Equipment Parameter Visualizer

A full-stack data visualization system for analyzing chemical equipment datasets using **CSV uploads**, built with:

- **Backend**: Django + Django REST Framework
- **Web Frontend**: React + Chart.js
- **Desktop App**: PyQt5 + Matplotlib

This project allows users to upload datasets, analyze equipment parameters, visualize trends, and generate detailed PDF reports.

---

##  Features

###  Authentication
- User signup & login
- Token-based authentication
- Per-user dataset history

###  Dataset Management
- CSV-only file upload
- Last 5 datasets stored per user
- Clickable history with summary loading

###  Data Analysis
- Average, minimum, and maximum values
- Equipment type distribution
- Separate charts for:
  - Average Parameters (Bar Chart)
  - Type Distribution (Pie Chart with %)

###  Reporting
- Auto-generated PDF reports
- Includes:
  - Summary statistics
  - Charts
  - Equipment type distribution

###  Multi-Platform
- Web dashboard (React)
- Desktop application (PyQt5)
- Shared backend APIs

---

##  Tech Stack

| Layer | Technology |
|-----|------------|
Backend | Django, DRF, SQLite |
Web UI | React, Chart.js |
Desktop | PyQt5, Matplotlib |
Auth | Token Authentication |
Reports | ReportLab + Matplotlib |

---

## Installation & Setup

### Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

#### Backend runs at:      ```bash
```
```bash
http://127.0.0.1:8000

```

###  Web Frontend Setup (React)
```bash
cd web-frontend
npm install
npm start

```
#### Web Application runs at:
```bash
http://localhost:3000

```


