CHEMICAL EQUIPMENT PARAMETER VISUALIZER

A full-stack, multi-platform application for analyzing and visualizing chemical equipment datasets using CSV files.

PROJECT OVERVIEW
The Chemical Equipment Parameter Visualizer allows users to upload CSV datasets, analyze equipment parameters,
visualize trends using charts, and generate professional PDF reports. The system is powered by a shared backend
that supports both a web dashboard and a desktop application.

KEY FEATURES

Authentication
- User signup and login
- Token-based authentication
- User-specific dataset history

Dataset Management
- CSV-only file uploads
- Dataset validation
- Clickable dataset history
- Summary reload on history selection

Data Analysis
- Total record count
- Average, minimum, and maximum values
- Equipment type distribution
- Separate chart views:
  - Average Parameters (Bar Chart)
  - Type Distribution (Pie Chart with percentages)

PDF Report Generation
- Downloadable PDF reports
- Includes dataset overview, statistics, charts, and distributions

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

REPOSITORY STRUCTURE

chemical-equipment-parameter-visualizer/
│
├── backend/
│   ├── chemical_backend/
│   ├── api/
│   ├── manage.py
│   ├── requirements.txt
│
├── web-frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│
├── desktop-app/
│   └── desktop_app.py
│
├── sample-data/
│   └── sample_equipment_data.csv
│
├── .gitignore
└── README.md

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
