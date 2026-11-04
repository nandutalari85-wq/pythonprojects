# Agricultural Crop Production Analysis System

> **Academic Level:** B.Tech in Artificial Intelligence & Machine Learning (AIML) Capstone / Major Project  
> **Target Audience:** College Students, Beginners, Evaluators, and Viva Examiners  
> **Status:** Fully functional, tested (35 automated tests passing), and production-ready.

---

## 🌾 Project Overview

The **Agricultural Crop Production Analysis System** is a complete, full-stack web application designed to help agricultural researchers, planners, and students analyze multi-year crop production records, regional yields, and climatic variations.

### Key Highlights
- **Interactive Web Dashboard:** Real-time Key Performance Indicators (KPIs), multi-parameter filters (Crop, Region, Year), and summary tables.
- **Relational Integrity (MySQL 3NF):** Three normalized tables (`regions`, `crops`, `crop_records`) with composite unique constraints (`UNIQUE(crop_id, region_id, year)`) and cascading deletions.
- **Batch CSV Ingestion Engine:** Validates uploaded datasets row-by-row, detects duplicate records and invalid values (negative areas, non-numeric years), and provides a clear breakdown of accepted vs. rejected rows.
- **Statistical Analytics (Pandas & NumPy):** Automated calculations for yield per unit area ($\text{Yield} = \frac{\text{Production}}{\text{Area}}$), Year-over-Year (YoY) absolute and percentage changes, crop summaries, and rainfall correlation with academic caveats.
- **Publication-Grade Matplotlib Charts:** Automated generation of 4 high-resolution visual charts with one-click download buttons.
- **Standards-Compliant REST APIs:** JSON endpoints for health checks, crops, regions, filtered records, and analytical trends.
- **Automated Test Suite:** 35 comprehensive `pytest` unit and integration tests passing with 100% success rate.

---

## 🛠️ Technology Stack

| Component | Technology | Version | Purpose |
|---|---|---|---|
| **Programming Language** | Python | 3.11+ / 3.14 | Core application logic and data pipelines |
| **Web Framework** | Flask | 3.1.3 | Web routing, sessions, templates, and REST APIs |
| **Database** | MySQL | 8.0+ | Relational data persistence and ACID transactions |
| **ORM & Driver** | Flask-SQLAlchemy & PyMySQL | 3.1.1 / 1.2.3 | Object-relational mapping and connection pooling |
| **Data Processing** | Pandas & NumPy | 3.1.0 / 2.5.4 | Mathematical aggregation, vectorization, and statistics |
| **Data Visualization** | Matplotlib (Agg backend) | 3.11.2 | Automated generation of publication-ready PNG charts |
| **Frontend UI** | HTML5, CSS3, Bootstrap 5.3, Jinja2 | Modern | Clean, responsive, mobile-ready dashboard |
| **Testing Framework** | pytest | 9.2.0 | Automated unit and integration testing |

---

## 📁 Project Directory Structure

```
c:\Agriculture project\
├── app/
│   ├── __init__.py          # Flask application factory, error handlers, Jinja filters
│   ├── config.py            # Development, Production, and Testing configurations
│   ├── models.py            # SQLAlchemy models: Region, Crop, CropRecord
│   ├── forms.py             # Server-side validation logic for CRUD operations
│   ├── analysis.py          # Pandas & NumPy statistical engine (yields, YoY, correlation)
│   ├── charts.py            # Headless Matplotlib chart generation (Agg backend)
│   ├── csv_importer.py      # Robust CSV validation, error tracking, batch import
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py          # Dashboard, CRUD operations, chart download routes
│   │   ├── upload.py        # CSV upload, preview report, template download
│   │   └── api.py           # REST API endpoints (/api/health, /api/crops, etc.)
│   ├── static/
│   │   ├── css/style.css    # Custom responsive styling and theme rules
│   │   ├── js/main.js       # Auto-dismissing alerts and file input listeners
│   │   └── charts/          # Generated Matplotlib chart images (.png)
│   └── templates/
│       ├── base.html        # Shared base template with navigation and footer
│       ├── dashboard.html   # Main analytical dashboard with charts and tables
│       ├── records/         # Records listing, form (add/edit), and detail views
│       ├── crops/           # Crops catalog and management view
│       ├── regions/         # Regions management view
│       ├── upload.html      # CSV upload page with column specifications
│       ├── upload_result.html # Ingestion report (accepted vs. rejected rows)
│       └── errors/          # Custom 404 and 500 error pages
├── data/
│   ├── crop_production_synthetic.csv      # 75 synthetic records (5 crops, 3 regions, 5 yrs)
│   ├── crop_production_invalid_sample.csv # Test dataset with deliberate errors
│   └── crop_production_template.csv       # Clean downloadable template
├── database/
│   ├── schema.sql           # MySQL DDL script with foreign keys and indexes
│   ├── seed.sql             # SQL script to populate MySQL directly
│   └── init_db.py           # Python CLI database initializer and seeder
├── docs/
│   ├── PROJECT_REPORT.md             # Academic report (Abstract, Objectives, 3NF, ER)
│   ├── DEMONSTRATION_SCRIPT.md       # Timed 8-12 minute college presentation script
│   ├── PRESENTATION_OUTLINE.md       # 14-slide presentation deck outline
│   └── VIVA_QUESTIONS_AND_ANSWERS.md # 20 likely viva voce questions with answers
├── tests/
│   ├── conftest.py          # Pytest fixtures (in-memory SQLite, test client)
│   ├── test_models.py       # Model CRUD and constraint tests
│   ├── test_analysis.py     # Pandas & NumPy analysis and yield calculation tests
│   ├── test_csv_importer.py # CSV validation and error detection tests
│   ├── test_charts.py       # Matplotlib chart generation tests
│   ├── test_routes.py       # Web UI route tests
│   └── test_api.py          # REST API endpoint tests
├── .env.example             # Example environment variable file
├── .env                     # Active environment configuration
├── requirements.txt         # Compatible Python dependencies
├── run.py                   # Application entry point
└── README.md                # This setup and user guide
```

---

## 🚀 Beginner-Friendly Windows Setup Guide

Follow these exact step-by-step instructions in Windows **PowerShell** or **Command Prompt (CMD)**.

### Step 1: Install Required Software
Before starting, ensure you have:
1. **Python 3.11+** installed (Download from [python.org](https://www.python.org/downloads/)).
   > ⚠️ During installation, check the box: **"Add python.exe to PATH"**.
2. **MySQL Community Server 8.0** installed (Download from [mysql.com](https://dev.mysql.com/downloads/installer/)).
   - Note down the `root` password you configured during installation.

---

### Step 2: Create the MySQL Database

1. Open your **MySQL Command Line Client** or **Windows PowerShell**:
```powershell
mysql -u root -p
```
*(Enter your MySQL root password when prompted)*

2. In the MySQL prompt, create the database:
```sql
CREATE DATABASE IF NOT EXISTS crop_analysis_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

---

### Step 3: Configure Environment Variables

1. Open the project folder in your terminal:
```powershell
cd "c:\Agriculture project"
```

2. Open the `.env` file in Notepad or VS Code:
```powershell
notepad .env
```

3. Update your MySQL database credentials:
```ini
SECRET_KEY=college-project-agricultural-analysis-secure-key-2026
FLASK_ENV=development
FLASK_DEBUG=1
MAX_CONTENT_LENGTH=5242880

# MySQL Database Settings
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD_HERE
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=crop_analysis_db

# Set to false to use MySQL. (Set to true if testing without MySQL running)
USE_SQLITE=false
```
Save and close the file.

---

### Step 4: Create Virtual Environment & Install Dependencies

1. Create a Python virtual environment:
```powershell
python -m venv venv
```

2. Activate the virtual environment:
- In **PowerShell**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  *(If PowerShell displays an execution policy error, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*
- In **Command Prompt (CMD)**:
  ```cmd
  venv\Scripts\activate.bat
  ```

3. Install required packages:
```powershell
pip install -r requirements.txt
```

---

### Step 5: Initialize and Seed the Database

Run our automated database initializer script:
```powershell
python database/init_db.py
```

**Expected Output:**
```
======================================================================
Agricultural Crop Production Analysis System - Database Initializer
======================================================================
>> Target Database URI: mysql+pymysql://root:***@127.0.0.1:3306/crop_analysis_db
>> Dropping existing tables (clean reset)...
>> Creating database tables according to schema...
>> Tables created: regions, crops, crop_records.
>> Ingesting synthetic records from: crop_production_synthetic.csv...
>> Valid rows detected: 75 | Rejected: 0

----------------------------------------------------------------------
>> SUCCESS: Database populated successfully!
>> - Crops Registered:    5
>> - Regions Registered:  3
>> - Observation Records: 75
----------------------------------------------------------------------
```

*(Note: If your MySQL service is not running, you can set `USE_SQLITE=true` in `.env` to run with SQLite instantly).*

---

### Step 6: Start the Flask Application

Start the web server:
```powershell
python run.py
```

**Output:**
```
>> Database tables verified and ready.
>> Agricultural Crop Production Analysis System running at: http://127.0.0.1:5000/
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

## 🖥️ Using the Application

### 1. Main Dashboard (`/`)
- View system-wide KPIs: Total observations, crops monitored, regions covered, total production, and average productivity.
- Explore 4 automatically generated visual charts:
  - Annual Production Trend (Line chart)
  - Regional Output Comparison (Bar chart)
  - Crop-wise Yield Comparison (Tonnes / Hectare)
  - Rainfall vs. Production Scatter Analysis (with correlation trendline)
- Filter observations by specific Crop, Region, or Year.

### 2. Crop Production Records (`/records`)
- Browse all observation records with pagination.
- Add new records with server-side validation (`/records/add`).
- View comprehensive details for any record (`/records/<id>`).
- Edit records (`/records/<id>/edit`) or delete them (`/records/<id>/delete`).

### 3. Master Entity Management
- **Crops Catalog (`/crops`):** Add, update, or remove crops and assign taxonomic categories (Cereal, Pulse, Cash Crop, Oilseed).
- **Regions Catalog (`/regions`):** Add, update, or remove geographical zones and specify agro-climatic conditions.

### 4. CSV Dataset Upload (`/upload`)
- Download the pre-formatted CSV template (`/download-template`).
- Upload a new CSV dataset.
- The validator inspects the file and provides a **Validation Report**:
  - Displays count of accepted vs. rejected rows.
  - Lists every rejected row with specific diagnostic reasons (e.g. negative area, missing crop name, duplicate entry).
  - Users can review the accepted rows and click **"Confirm & Import Valid Rows"** to commit them into MySQL within an atomic transaction.

---

## 🧪 Running Automated Tests

Run the full automated test suite using `pytest`:
```powershell
pytest -v
```

**Expected Result:**
```
============================= test session starts =============================
platform win32 -- Python 3.14.x, pytest-9.2.0
collected 35 items

tests/test_analysis.py::test_empty_analysis_engine PASSED                [  2%]
tests/test_analysis.py::test_kpi_calculations PASSED                     [  5%]
tests/test_analysis.py::test_crop_summary_statistics PASSED              [  8%]
tests/test_analysis.py::test_annual_trends_and_yoy_changes PASSED        [ 11%]
tests/test_analysis.py::test_rainfall_correlation_with_sufficient_data PASSED [ 14%]
tests/test_analysis.py::test_rainfall_correlation_insufficient_data PASSED [ 17%]
tests/test_api.py::test_api_health PASSED                                [ 20%]
tests/test_api.py::test_api_crops PASSED                                 [ 22%]
tests/test_api.py::test_api_regions PASSED                               [ 25%]
tests/test_api.py::test_api_records_filtered PASSED                      [ 28%]
tests/test_api.py::test_api_analysis_summary PASSED                      [ 31%]
tests/test_api.py::test_api_analysis_trends PASSED                       [ 34%]
tests/test_charts.py::test_chart_generation PASSED                       [ 37%]
tests/test_charts.py::test_chart_generation_empty_data PASSED            [ 40%]
tests/test_csv_importer.py::test_valid_csv_parsing PASSED                [ 42%]
tests/test_csv_importer.py::test_missing_required_headers PASSED         [ 45%]
tests/test_csv_importer.py::test_empty_csv_file PASSED                   [ 48%]
tests/test_csv_importer.py::test_row_level_validation_errors PASSED      [ 51%]
tests/test_csv_importer.py::test_duplicate_row_detection PASSED          [ 54%]
tests/test_models.py::test_create_crop_and_region PASSED                 [ 57%]
tests/test_models.py::test_crop_record_yield_property PASSED             [ 60%]
tests/test_models.py::test_unique_constraint_crop_region_year PASSED     [ 62%]
tests/test_models.py::test_cascade_delete PASSED                         [ 65%]
tests/test_models.py::test_model_to_dict_serialization PASSED            [ 68%]
tests/test_routes.py::test_dashboard_route PASSED                        [ 71%]
tests/test_routes.py::test_records_list_route PASSED                     [ 74%]
tests/test_routes.py::test_add_record_valid PASSED                       [ 77%]
tests/test_routes.py::test_add_record_duplicate_validation PASSED        [ 80%]
tests/test_routes.py::test_record_detail_and_edit PASSED                 [ 82%]
tests/test_routes.py::test_record_delete PASSED                          [ 85%]
tests/test_crops_management_routes PASSED                                [ 88%]
tests/test_regions_management_routes PASSED                              [ 91%]
tests/test_download_template PASSED                                      [ 94%]
tests/test_upload_csv_flow PASSED                                        [ 97%]
tests/test_routes.py::test_404_not_found PASSED                          [100%]

============================= 35 passed in 4.78s ==============================
```

---

## 📡 REST API Reference

The application exposes RESTful JSON endpoints:

| Endpoint | Method | Description | Sample Output |
|---|---|---|---|
| `/api/health` | GET | System and DB health check | `{"status": "healthy", "database": "connected"}` |
| `/api/crops` | GET | List of registered crops | `{"status": "success", "count": 5, "data": [...]}` |
| `/api/regions` | GET | List of registered regions | `{"status": "success", "count": 3, "data": [...]}` |
| `/api/records` | GET | Filter records (`?crop_id=1&year=2023`) | `{"status": "success", "count": 15, "data": [...]}` |
| `/api/analysis/summary`| GET | KPIs, crop/region summaries | `{"status": "success", "kpis": {...}}` |
| `/api/analysis/trends` | GET | Multi-year trends and YoY changes | `{"status": "success", "trends": [...]}` |

---

## ❓ Troubleshooting Common Errors

### 1. `Can't connect to MySQL server on '127.0.0.1'`
- **Cause:** MySQL service is stopped or not running.
- **Solution (PowerShell as Administrator):**
  ```powershell
  net start MySQL80
  ```
- **Alternative:** Set `USE_SQLITE=true` in your `.env` file to immediately test the system with SQLite.

### 2. `Access denied for user 'root'@'localhost'`
- **Cause:** Incorrect MySQL root password in `.env`.
- **Solution:** Verify the password used during MySQL Server installation and update `DB_PASSWORD=your_password` in `.env`.

### 3. `Execution of scripts is disabled on this system` (PowerShell)
- **Cause:** Windows PowerShell default execution policy.
- **Solution:** Run the following command in PowerShell:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```

### 4. `Port 5000 is in use`
- **Cause:** Another process is running on port 5000.
- **Solution:** In PowerShell, run the app on a custom port:
  ```powershell
  $env:PORT="5050"; python run.py
  ```

---

## 🎓 Academic Documentation Links

For your college presentation, project report, and viva exam, refer to the detailed documents in the `docs/` folder:
- [Academic Project Report (`docs/PROJECT_REPORT.md`)](file:///c:/Agriculture%20project/docs/PROJECT_REPORT.md)
- [Demonstration Script (`docs/DEMONSTRATION_SCRIPT.md`)](file:///c:/Agriculture%20project/docs/DEMONSTRATION_SCRIPT.md)
- [Presentation Slides Outline (`docs/PRESENTATION_OUTLINE.md`)](file:///c:/Agriculture%20project/docs/PRESENTATION_OUTLINE.md)
- [15+ Viva Questions & Answers (`docs/VIVA_QUESTIONS_AND_ANSWERS.md`)](file:///c:/Agriculture%20project/docs/VIVA_QUESTIONS_AND_ANSWERS.md)

---

## 📜 Academic Declaration

This project utilizes synthetic agricultural datasets generated strictly for undergraduate educational demonstration, algorithmic testing, and viva voce examination. It does not claim to represent official governmental or census agricultural records.
