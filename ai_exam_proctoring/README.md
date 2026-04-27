# AI Exam Cheating Detection System

## Project Overview

The AI Exam Cheating Detection System is a web-based proctoring system designed to detect suspicious activities during online examinations.

The system uses **computer vision and machine learning** to monitor students through a webcam and detect potential cheating behaviors such as:

- Tab switching
- Looking away from the screen
- Multiple faces in camera
- Phone or book detection
- Window focus loss

The system logs all suspicious events and allows administrators to monitor exam sessions through a dashboard.

---

## Features

### Student Features
- Secure login system
- Start exam session
- Live webcam monitoring
- Tab switching detection
- Copy attempt detection
- Real-time AI behavior monitoring

### Admin Features
- View cheating logs
- Monitor exam sessions
- View evidence images
- Dashboard with recorded suspicious activities

---

## Technologies Used

### Backend
- Flask
- Flask-Login
- Flask-SQLAlchemy

### AI / Computer Vision
- OpenCV
- MediaPipe
- YOLOv8 (Ultralytics)

### Frontend
- HTML
- CSS
- JavaScript

### Database
- SQLite

---

## Project Structure

```
ai_exam_proctoring/
├── app.py                  # Flask application entry point
├── config.py               # Application configuration settings
├── init_db.py              # Database initialization script
├── requirements.txt        # Python dependencies
├── ai_modules/             # AI detection modules (face, gaze, object)
├── database/               # Database models and connection setup
├── models/                 # YOLO model weights
├── routes/                 # Flask route blueprints
├── services/               # Business logic and detection services
├── static/                 # CSS, JS, and captured evidence images
├── templates/              # HTML templates
└── utils/                  # Utility/helper functions
```

---

## Running Locally

### Prerequisites

- **Python 3.9 or higher** — [Download](https://www.python.org/downloads/)
- **Git** — [Download](https://git-scm.com/)
- A **webcam** connected to your machine (required for live proctoring)

---

### 1. Clone the Repository

```bash
git clone https://github.com/Kapil1071/AI-Based-Online-Exam-Cheating-Detection.git
cd AI-Based-Online-Exam-Cheating-Detection/ai_exam_proctoring
```

---

### 2. Create and Activate a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `torch` (PyTorch) is a large package. Installation may take several minutes depending on your internet speed. For GPU support, visit [pytorch.org](https://pytorch.org/get-started/locally/) for the appropriate install command.

---

### 4. Initialize the Database

Run the database initialization script once before starting the app for the first time:

```bash
python init_db.py
```

This creates the SQLite database and a default admin account:

| Role  | Username | Password  |
|-------|----------|-----------|
| Admin | `admin`  | `admin123` |

---

### 5. Run the Application

```bash
python app.py
```

The app will start in production mode by default. To enable debug mode:

**Windows:**
```bash
set FLASK_DEBUG=1
python app.py
```

**macOS / Linux:**
```bash
FLASK_DEBUG=1 python app.py
```

Then open your browser and navigate to:

```
http://127.0.0.1:5000
```

---

### 6. Create a Student Account

Log in as admin and use the admin dashboard to create student accounts, or register a new student directly from the registration page.

---

### Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Make sure the virtual environment is activated and `pip install -r requirements.txt` completed successfully |
| Webcam not detected | Check that your webcam is properly connected and not in use by another application |
| YOLO model missing | The YOLOv8 weights (`yolov8n.pt`) are downloaded automatically by `ultralytics` on first run |
| Port already in use | Change the port: `python app.py` (edit `app.run(port=5001)` in `app.py`) |

---

