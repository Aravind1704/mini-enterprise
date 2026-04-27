Mini Enterprise 

A full-stack enterprise task management system with role-based access control, JWT authentication, and a React dashboard.


ech Stack

Backend:FastAPI, SQLAlchemy, MySQL, JWT, bcrypt  
Frontend:React.js, Axios, React Router DOM  
Tools:Swagger UI, VS Code



Project Structure


Mini Enterprise/

├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── dependencies.py
│   │   │   └── security.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   └── task.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   └── tasks.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   └── task.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   └── task_service.py
│   │   ├── database.py
│   │   └── main.py
│   ├── .env
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── api/
    │   │   └── axios.js
    │   ├── context/
    │   │   └── AuthContext.jsx
    │   ├── pages/
    │   │   ├── Login.jsx
    │   │   ├── Register.jsx
    │   │   ├── Dashboard.jsx
    │   │   ├── CreateTask.jsx
    │   │   └── EditTask.jsx
    │   ├── components/
    │   │   └── PrivateRoute.jsx
    │   └── App.jsx
    └── package.json




Prerequisites

- Python 3.10+
- Node.js 18+
- MySQL 8+
- Git



Backend Setup

1. Clone the repository

bash
git clone https://github.com/your-username/mini-enterprise.git
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


### 2. Install dependencies

```bash
npm install
```

### 3. Start the development server

```bash
npm start
```

Frontend runs at: `http://localhost:3000`

---

Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | MySQL connection string | `mysql+pymysql://root:1234@localhost:3306/taskdb` |
| `SECRET_KEY` | JWT signing key | `your-super-secret-key` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry | `30` |

---

User Roles

| Role | Permissions |
|------|-------------|
| **Admin** | Full access — manage all users and tasks |
| **Manager** | Create and assign tasks, manage own tasks |
| **Employee** | View and update status of assigned tasks only |

---

API Endpoints

 Authentication

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/auth/register` | Register new user | Public |
| POST | `/auth/login` | Login and get JWT token | Public |
| GET | `/auth/me` | Get current logged-in user | Authenticated |

Users

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/users/` | List all users | Admin only |
| GET | `/users/{id}` | Get user by ID | Authenticated |

Tasks

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/tasks/` | Create a task | Admin, Manager |
| GET | `/tasks/` | List tasks (role-filtered) | Authenticated |
| GET | `/tasks/{id}` | Get task by ID | Authenticated |
| PUT | `/tasks/{id}` | Update task | Authenticated |
| DELETE | `/tasks/{id}` | Delete task | Admin, Manager |
| PATCH | `/tasks/{id}/assign` | Assign task to user | Admin, Manager |

---

API Test Values

Register Users




Business Rules

- Email must be unique
- Passwords are hashed with bcrypt
- Task title is required
- Default task status is `todo`
- Default task priority is `medium`
- Employees cannot assign or delete tasks
- Employees can only see their assigned tasks
- Managers can only see tasks they created
- Admins can see all tasks



Running Both Servers

Open two terminals:

Terminal 1 — Backend:
bash
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload


Terminal 2 — Frontend:
bash
cd frontend
npm start




Acceptance Criteria

-  User can register and login
-  JWT authentication works
-  Protected APIs are secured
-  Roles are enforced correctly
-  Tasks can be created
-  Tasks can be assigned
-  Tasks can be updated and deleted
-  Employee sees only assigned tasks
-  Dashboard displays tasks
-  Frontend and backend are integrated
