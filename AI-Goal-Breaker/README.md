**AI Smart Goal Breaker**

AI Smart Goal Breaker is a web application that uses a Large Language Model (LLM) to automatically break large goals into small, actionable daily tasks.
The application integrates AI with a database-backed task manager to provide intelligent goal planning and real-time progress tracking.

**How It Works**
User enters a goal (e.g., “Learn Python in 30 days”).
The frontend sends the goal to the Flask backend.
The backend:
Saves the goal in MySQL
Calls the GROQ LLM API
Receives 7–10 actionable subtasks
Stores subtasks in the database
The frontend dynamically displays tasks and tracks progress.
When subtasks are completed, overall task progress updates automatically.

**Features**
AI-powered goal breakdown
Automatic subtask generation (7–10 tasks)
Task difficulty levels (easy, medium, hard)
Real-time progress tracking
Automatic parent task status update
Cascade delete for tasks and subtasks
Persistent database storage
Clean REST API architecture

**Task Status Logic**
All subtasks completed → Task = completed
Some subtasks completed → Task = in_progress
No subtasks completed → Task = pending


**Tech Stack**
**Backend**
Flask
SQLAlchemy (ORM)
PyMySQL
Flask-CORS
python-dotenv
Groq SDK (LLM integration)

**Frontend**
HTML
CSS
JavaScript (Fetch API, DOM Manipulation)
Database
MySQL



**Project Structure**
AI-Smart-Goal-Breaker/
│
├── app.py              # Flask backend API
├── config.py           # Environment & DB configuration
├── database.py         # SQLAlchemy engine and session setup
├── models.py           # Task and SubTask models
├── llm_service.py      # LLM integration logic
├── .env                # Environment variables (not included in repo)
│
└── frontend/
    ├── index.html      # User interface
    ├── script.js       # Frontend logic
    └── style.css       # Styling



**Execution**
1. Create Virtual Environment
python -m venv venv

Activate it:
Windows:
venv\Scripts\activate

2. Install Dependencies
pip install flask sqlalchemy pymysql flask-cors python-dotenv groq

3. Setup MySQL Database
Create a database:
CREATE DATABASE task_breaker;
AI Model
llama-3.1-8b-instant (via GROQ API)


4. Run Backend (Terminal 1)
python app.py

Backend runs at:
http://127.0.0.1:5000

5. Run Frontend (Terminal 2)
Open frontend/index.html using:
Frontend typically runs at:
http://127.0.0.1:5500


Why Two Terminals?
Because the project uses:
Flask backend server (API + AI + DB)
Static frontend server (HTML/JS)
The frontend communicates with the backend via HTTP requests (fetch()).
CORS is enabled to allow cross-port communication.
