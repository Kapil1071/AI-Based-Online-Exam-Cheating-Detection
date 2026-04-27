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
