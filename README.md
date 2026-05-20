Mini Enterprise 
Mini Enterprise is a comprehensive full-stack enterprise task management and SaaS subscription platform built using FastAPI and React.js. It supports role-based access control, task workflows, approvals, notifications, Stripe subscriptions, WebSockets, analytics, AI insights, and modern dashboard features.



Tech Stack
Backend

Framework: FastAPI
Database: MySQL
ORM: SQLAlchemy
Authentication: JWT + Bcrypt
File Handling: Python multipart
API Documentation: Swagger/OpenAPI

Frontend

Framework: React.js
Routing: React Router DOM
HTTP Client: Axios
Charts: Recharts
Drag & Drop: React Beautiful DnD
Styling: Inline CSS

Security Features:

JWT Authentication
Bcrypt Password Hashing
Role-Based Access Control
Protected APIs
SQLAlchemy ORM Protection
Token Expiry
Refresh Tokens
Deployment
Tools & Infrastructure

Version Control: Git & GitHub
API Testing: Swagger UI
Development: VS Code
Database: MySQL Workbench
Package Management: npm, pip

Project Structure

```
Mini-Enterprise/
│
├── backend/
│   │
│   ├── venv/
│   │
│   ├── app/
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── dependencies.py
│   │   │   ├── stripe_config.py
│   │   │   ├── websocket_manager.py
│   │   │   └── limiter.py
│   │   │
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── task.py
│   │   │   ├── comment.py
│   │   │   ├── approval.py
│   │   │   ├── document.py
│   │   │   ├── notification.py
│   │   │   ├── audit_log.py
│   │   │   ├── subscription.py
│   │   │   └── payment.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── task.py
│   │   │   ├── comment.py
│   │   │   ├── approval.py
│   │   │   ├── document.py
│   │   │   ├── notification.py
│   │   │   ├── audit_log.py
│   │   │   ├── analytics.py
│   │   │   ├── subscription.py
│   │   │   └── payment.py
│   │   │
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── tasks.py
│   │   │   ├── comments.py
│   │   │   ├── approvals.py
│   │   │   ├── kanban.py
│   │   │   ├── analytics.py
│   │   │   ├── dashboard.py
│   │   │   ├── documents.py
│   │   │   ├── notifications.py
│   │   │   ├── audit_logs.py
│   │   │   ├── ai_insights.py
│   │   │  ├── payment_router.py
│   │   │  ├── subscription_router.py
│   │   │  └── websocket_router.py
│   │   │
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── task_service.py
│   │   │   ├── comment_service.py
│   │   │   ├── approval_service.py
│   │   │   ├── analytics_service.py
│   │   │   ├── document_service.py
│   │   │   ├── notification_service.py
│   │   │   ├── audit_service.py
│   │   │   ├── ai_service.py
│   │   │   ├── websocket_service.py
│   │   │   ├── payment_service.py
│   │   │   └── stripe_service.py
│   │   │
│   │   ├── websocket/
│   │   │   └── connection_manager.py
│   │   │
│   │   ├── database.py
│   │   └── main.py
│   │
│   ├── requirements.txt
│   ├── .env
│   ├── README.md
│   └── alembic/
│
│
├── frontend/
│   │
│   ├── node_modules/
│   │
│   ├── public/
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   ├── logo192.png
│   │   ├── logo512.png
│   │   └── manifest.json
│   │
│   ├── src/
│   │   │
│   │   ├── api/
│   │   │   └── axios.js
│   │   │
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   │
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   └── PrivateRoute.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── CreateTask.jsx
│   │   │   ├── EditTask.jsx
│   │   │   ├── Kanban.jsx
│   │   │   ├── Comments.jsx
│   │   │   ├── Approvals.jsx
│   │   │   ├── Notifications.jsx
│   │   │   ├── Documents.jsx
│   │   │   ├── Analytics.jsx
│   │   │   ├── AuditLogs.jsx
│   │   │   ├── AIInsights.jsx
│   │   │   ├── Pricing.jsx
│   │   │   ├── Success.jsx
│   │   │   └── Cancel.jsx
│   │   │
│   │   ├── services/
│   │   │   ├── WebSocketClient.js
│   │   │
│   │   ├── App.js
│   │   ├── routes.js
│   │   └── index.js
│   │
│   ├── package.json
│   ├── package-lock.json
│   └── README.md
│
├── .gitignore
└── README.md
```

Prerequisites

- Python 3.10+
- Node.js 18+
- MySQL 8+
- Git

Backend Setup
1. Navigate to Backend
bashcd backend
2. Create Virtual Environment
bashpython -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
3. Install Dependencies
bashpip install -r requirements.txt
4. Configure Environment
Create .env file:
envDATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/taskdb
SECRET_KEY=mini-enterprise-super-secret-key-phase3
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
5. Create MySQL Database
bashmysql -u root -p YOUR_PASSWORD
sqlCREATE DATABASE taskdb;
USE taskdb;
ALTER TABLE tasks ADD COLUMN updated_by INT;
exit;
6. Start Backend Server
bashuvicorn app.main:app --reload
Backend URL: http://localhost:8000
Swagger UI: http://localhost:8000/docs

Frontend Setup
1. Navigate to Frontend
bashcd frontend
2. Install Dependencies
bashnpm install
npm install @hello-pangea/dnd recharts
3. Start Development Server
bashnpm start
Frontend URL: http://localhost:3000

User Roles & Permissions
Admin

Full system access
View all tasks
Manage all users
View audit logs
Final approval authority
Access all documents
View all analytics

Manager

 Create and assign tasks
View team tasks
Approve/reject (first level)
Add internal notes
Access team documents
Receive notifications
View analytics

Employee

View assigned tasks
Update task status
Add comments
Submit approval requests
Upload/download documents
Receive notifications
View own analytics


Test Users
Login with these credentials:
json{
  "admin": {
    "email": "admin@example.com",
    "password": "123456"
  },
  "manager": {
    "email": "manager@example.com",
    "password": "manager123"
  },
  "employee": {
    "email": "employee@example.com",
    "password": "employee123"
  }
}

 API Endpoints
Authentication
MethodEndpointDescriptionPOST/auth/registerRegister new userPOST/auth/loginLogin & get JWT tokenGET/auth/meGet current user
Users
MethodEndpointDescriptionGET/users/List all users (Admin)GET/users/{id}Get user details
Tasks
MethodEndpointDescriptionPOST/tasks/Create taskGET/tasks/List tasks (role-filtered)GET/tasks/{id}Get task detailsPUT/tasks/{id}Update taskDELETE/tasks/{id}Delete taskPATCH/tasks/{id}/assignAssign taskPATCH/tasks/{id}/statusUpdate status
Kanban (Phase 2)
MethodEndpointDescriptionGET/tasks/kanbanGet tasks by statusPATCH/tasks/{id}/statusMove task between columns
Comments (Phase 2)
MethodEndpointDescriptionPOST/tasks/{id}/commentsAdd commentGET/tasks/{id}/commentsList comments
Approvals (Phase 2)
MethodEndpointDescriptionPOST/approvals/Submit approvalGET/approvals/List approvalsPATCH/approvals/{id}/actionApprove/RejectGET/approvals/{id}/historyGet history
Documents (Phase 3)
MethodEndpointDescriptionPOST/documents/uploadUpload documentGET/documents/task/{id}Get task documents
Audit Logs (Phase 3)
MethodEndpointDescriptionGET/audit-logs/List all logs (Admin)GET/audit-logs/activityRecent activity
Notifications (Phase 3)
MethodEndpointDescriptionGET/notifications/List notificationsGET/notifications/unreadUnread countPATCH/notifications/{id}/readMark as read
Dashboard (Phase 2 & 3)
MethodEndpointDescriptionGET/dashboard/summaryTask statisticsGET/dashboard/task-distributionTasks by statusGET/dashboard/ai-summaryAI insights (Phase 3)

🎯 Features by Phase
Phase 1 — Foundation
 User authentication with JWT
 Role-based access control
 Task CRUD operations
 Task assignment
 Protected API endpoints
 Basic dashboard
 
Phase 2 — Collaboration
 Kanban board (drag & drop)
 Multi-level approvals
 Comments & activity
 Analytics dashboard
 Status workflows
 Approval history
 
Phase 3 — Enterprise Intelligence
 Document management
 Document versioning
 Audit logging (all actions)
 Notifications system
 Automatic notification triggers
 AI-powered insights
 Activity feed

 Database Models
Users Table
sql- id (PK)
- name
- email (UNIQUE)
- hashed_password
- role (admin, manager, employee)
- is_active
- created_at, updated_at
Tasks Table
sql- id (PK)
- title
- description
- status (todo, in_progress, review, done)
- priority (low, medium, high)
- due_date
- created_by_id (FK)
- assigned_to_id (FK)
- updated_by (FK)
- created_at, updated_at
Comments Table
sql- id (PK)
- task_id (FK)
- user_id (FK)
- content
- is_internal
- created_at
Approvals Table
sql- id (PK)
- title
- description
- requested_by (FK)
- status (pending, approved, rejected)
- current_level (manager, admin)
- created_at, updated_at
Documents Table
sql- id (PK)
- file_name
- file_path
- version
- uploaded_by (FK)
- task_id (FK)
- created_at, updated_at
Audit Logs Table
sql- id (PK)
- user_id (FK)
- action (created, updated, deleted, uploaded)
- entity (Task, User, Document, Approval)
- entity_id
- details
- timestamp
Notifications Table
sql- id (PK)
- user_id (FK)
- message
- action_type (task_assigned, comment_added, approval_requested)
- related_id
- is_read
- created_at

 Testing Workflow
Test Task Assignment Notification

Login as Manager
Go to Dashboard → + New Task
Fill: Title, Description, assign to Employee
Create Task
Go to Notifications → See "Task assigned to you"

Test Comment Notification

Click  Comments on any task
Add: "Please prioritize this task"
Post Comment
Go to Notifications → See comment notification

Test Approval Workflow

Go to  Approvals → + New Request
Fill: Title, Description
Submit Request
Manager sees approval notification
Manager approves/rejects
Employee sees status update

Test Document Upload

Go to  Documents
Select Task ID
Upload file
See document in list
View in Audit Logs

Test AI Insights

Go to  AI
See task counts
See high priority warnings
See overdue alerts


Security Features

 JWT token authentication (30-min expiry)
 Bcrypt password hashing
 Role-based access control (RBAC)
 Protected API endpoints
 CORS enabled for localhost
 SQL injection prevention (ORM)
 Secure password validation
 Token refresh mechanism


 Performance Optimizations

Database query optimization with SQLAlchemy
Role-based filtering at database level
Frontend lazy loading components
Optimized API response payloads
Efficient notification delivery
Caching where applicable


 Troubleshooting
Backend Won't Start
bash# Check .env file exists
cat .env

# Check MySQL is running
mysql -u root -p1234

# Check database exists
USE taskdb; SHOW TABLES;
CORS Errors
Solution: Ensure CORS middleware in main.py with allow_origins=["*"]
401 Unauthorized
Solution: Login again, ensure token is in localStorage
Notifications Not Appearing
Solution: Ensure notifications table exists, backend is running
Charts Not Rendering
Solution: npm install recharts

 Dependencies
Backend (requirements.txt)
fastapi
uvicorn
sqlalchemy
pymysql
python-jose[cryptography]
bcrypt==4.0.1
pydantic[email]
pydantic-settings
python-dotenv
Frontend (package.json)
react
react-router-dom
axios
@hello-pangea/dnd
recharts

 Deployment
Backend Deployment
bashpip freeze > requirements.txt
git add .
git commit -m "Phase 3 Complete"
git push origin main
# Deploy to Heroku/Railway/Render
Frontend Deployment
bashnpm run build
# Deploy build folder to Vercel/Netlify

 Documentation

API Documentation: http://localhost:8000/docs (Swagger)
Backend README: See backend/README.md
Frontend README: See frontend/README.md


 Contributing
This is a complete enterprise project. For modifications:

Create a new branch
Make changes
Test thoroughly
Submit pull request


Project Completion Checklist
Phase 1

 User authentication (JWT)
 Role-based access control
 Task CRUD operations
 Task assignment
 Protected routes
 Basic dashboard

Phase 2

 Kanban board
 Drag & drop functionality
 Approval workflows
 Comments system
 Analytics dashboard
 Charts & statistics

Phase 3

 Document management
 Audit logging
 Notification system
 AI insights
 Activity tracking
 Full enterprise workflow




🚀 Features
✅ Authentication & Security
JWT Authentication
Refresh Token Support
Role-Based Access Control
OAuth Ready
Password Hashing with Bcrypt
Protected Routes
Token-Based Authorization

📋 Task Management
Create Tasks
Edit Tasks
Delete Tasks
Assign Tasks
Task Priorities
Due Dates
Comments System
Task Workflow Management
📊 Dashboard Features
👨‍💼 Admin Dashboard
Total Users
Total Tasks
Approvals
Audit Logs
Full Analytics


👨‍💻 Manager Dashboard
Team Tasks
Pending Approvals
Team Analytics

👤 Employee Dashboard
My Tasks
Pending Tasks
Personal Analytics



🧠 AI Features
AI Task Insights
Delay Detection
High Priority Alerts
Smart Analytics



🔔 Notifications
Real-Time Notifications
WebSocket Support
Activity Feed
Comment Alerts
Approval Alerts




💳 SaaS Subscription System
Subscription Plans
Plan	Price	Credits
Basic	₹499	100
Silver	₹1499	500
Gold	₹3999	2000
Subscription Features
Stripe Checkout Integration
Live Credit Updates
Live Plan Updates
Webhook Support
Subscription Dashboard
Real-Time Credit Tracking



 GitHub repository
 Complete documentation
 API endpoints tested
 Frontend pages tested
 All features working

