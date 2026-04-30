Mini Enterprise 
The Mini Enterprise Collaboration System is a full-stack enterprise-grade application designed to simulate real-world workflow management systems.
This Phase 2 upgrade transforms the application into a workflow-driven collaboration platform with Kanban tracking, approvals, comments, and analytics.
Tech Stack

Backend:FastAPI, SQLAlchemy, MySQL, JWT, bcrypt  
Frontend:React.js, Axios, React Router DOM  
Tools:Swagger UI, VS Code

Project Structure

```
mini-enterprise/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── dependencies.py
│   │   │   ├── security.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── task.py
│   │   │   ├── comment.py
│   │   │   ├── approval.py
│   │   │   ├── approval_history.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── task.py
│   │   │   ├── comment.py
│   │   │   ├── approval.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   │   ├── task_service.py
│   │   │   ├── comment_service.py
│   │   │   ├── approval_service.py
│   │   │   ├── dashboard_service.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── tasks.py
│   │   │   ├── comments.py
│   │   │   ├── approvals.py
│   │   │   ├── dashboard.py
│   │   │   └── __init__.py
│   │   │
│   │   └── main.py
│   │
│   ├── requirements.txt
│   ├── .env
│   └── .gitignore
│
├── frontend/
│   ├── public/
│   │
│   ├── src/
│   │   ├── api/
│   │   │   └── axios.js
│   │   │
│   │   ├── components/
│   │   │   ├── common/
│   │   │   ├── Kanban/
│   │   │   ├── Approval/
│   │   │   ├── Comments/
│   │   │   └── Dashboard/
│   │   │
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── KanbanBoard.jsx
│   │   │   ├── ApprovalPage.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── TaskDetails.jsx
│   │   │
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   │
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── routes.jsx
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── .gitignore
│
├── README.md
└── .gitignore
```

Prerequisites

- Python 3.10+
- Node.js 18+
- MySQL 8+
- Git



Backend Setup

1. Clone the repository

bash
git clone https://github.com/Aravind1704/mini-enterprise.git
cd mini-enterprise/backend


2. Create and activate virtual environment

bash
python -m venv .venv

Windows
.venv\Scripts\activate

3. Install dependencies

bash
pip install fastapi uvicorn sqlalchemy alembic pymysql python-jose[cryptography] bcrypt==4.0.1 pydantic[email] pydantic-settings python-dotenv


4. Configure environment variables

Create a `.env` file in the `backend/` folder:

env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/taskdb
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30


>Replace `YOUR_PASSWORD` with your MySQL root password.

5. Create MySQL database

```bash
mysql -u root -p
```

```sql
CREATE DATABASE taskdb;
exit;
```

 6. Run the backend server

```bash
uvicorn app.main:app --reload
```

Backend runs at: `http://localhost:8000`  
Swagger UI: `http://localhost:8000/docs`


Frontend Setup

1. Navigate to frontend folder

bash
cd mini-enterprise/frontend


2. Install dependencies

```bash
npm install
```
3. Start the development server

```bash
npm start
```


Task lifecycle:
TODO → IN_PROGRESS → REVIEW → DONE
Drag & drop support (Frontend)
Backend validation for status transitions
Task history tracking

 Workflow Rules
Prevent invalid transitions
 TODO → DONE
 TODO → IN_PROGRESS → REVIEW → DONE

Comments & Collaboration
Add comments to tasks
Internal vs Public notes
Timestamp & user tracking

 Approval System
Multi-level workflow:
Employee → Manager → Admin
Approve / Reject / Hold
Mandatory comments on rejection
Full audit history


  Dashboard
Total tasks
Tasks by status
Pending approvals
Completed tasks
Performance insights


API Authentication

Login via:
POST /auth/login
Copy token
Use Swagger Authorize button
Paste token in Bearer format

Security
Role-based access control
JWT token validation
Protected APIs
Restricted workflow actions


Deliverables
 Backend APIs
 Frontend UI
 Workflow engine
 Approval system
 Dashboard
 GitHub repository

Frontend runs at: `http://localhost:3000`-

Backend Code Placement

1. `core/` → Configuration & Security

```text
app/core/
```

Put here:

* `config.py` → environment variables (.env)
* `database.py` → DB connection
* `dependencies.py` → auth + roles (get_current_user, require_role)
* `security.py` → JWT token creation, password hashing

--

2. `models/` → Database Tables

```text
app/models/
```
Put here:

SQLAlchemy classes

Example:

```python
class Task(Base):
    __tablename__ = "tasks"
```

---

3. `schemas/` → Request & Response

```text
app/schemas/
```

Put here:

* Pydantic models

Example:

```python
class TaskCreate(BaseModel):
    title: str
```

---

4. `services/` → Business Logic (MOST IMPORTANT)

```text
app/services/
```

Put here:

* All logic (NOT in routers)

Examples:

* status validation
* approval rules
* DB operations

Example:

```python
def update_task_status(db, task, new_status):
```

---

5. `routers/` → API Endpoints

```text
app/routers/
```

Put here:

* FastAPI routes only

Example:

```python
@router.post("/tasks")
```

 Router should only call services, not contain logic.

---

 6. `main.py` → Entry Point

```text
app/main.py
```

Put here:

```python
app.include_router(auth.router)
app.include_router(tasks.router)
```

---

FULL FLOW (Understand This)

```text
Client → Router → Service → Model → DB
                 ↑
              Schema
```

---

Example (Complete Flow)

Router

```python
@router.patch("/{task_id}/status")
def update_status(task_id: int, status: str, db: Session = Depends(get_db)):
    return update_task_status(db, task_id, status)
```

---

Service

```python
def update_task_status(db, task_id, status):
    task = db.query(Task).get(task_id)

    validate_status_transition(task.status, status)

    task.status = status
    db.commit()

    return task
```

---

Model

```python
class Task(Base):
    status = Column(String)
```

---

Frontend Code Placement

`src/api/`

Axios config

 `components/`

UI components
Kanban cards, comments, approvals

 `pages/`

Full pages (Dashboard, Login, Kanban)

 `context/`

Auth state

