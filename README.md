Mini Enterprise 
Mini Enterprise is a comprehensive full-stack enterprise task management and SaaS subscription platform built using FastAPI and React.js. It supports role-based access control, task workflows, approvals, notifications, Stripe subscriptions, WebSockets, analytics, AI insights, and modern dashboard features.

```
Tech Stack

Backend

Technology	Purpose
Framework	FastAPI
Database	MySQL
ORM	SQLAlchemy
Authentication	JWT + Bcrypt
Validation	Pydantic
Database Migration	Alembic
File Handling	Python Multipart
API Documentation	Swagger / OpenAPI
Real-Time Communication	WebSockets
Caching	Redis
Payment Gateway	Stripe / Razorpay
Background Tasks	FastAPI Background Tasks
AI Processing	Python AI Services



Frontend



Technology	Purpose
Framework	React.js
Routing	React Router DOM
HTTP Client	Axios
Charts & Analytics	Recharts
Drag & Drop	React Beautiful DnD
Styling	Tailwind CSS + Inline CSS
State Management	React Context API
Real-Time Updates	WebSocket Client
Notifications	Toast Notifications
UI Components	Custom Enterprise UI Components
=======
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



Security Features

JWT Authentication
Refresh Token Mechanism
Bcrypt Password Hashing
Google OAuth Login
Role-Based Access Control (RBAC)
Protected APIs
Input Validation & Sanitization
API Rate Limiting
Token Expiry Handling
Secure Password Reset Flow
SQLAlchemy ORM Protection
Multi-Tenant Data Isolation
```



Project Structure

```
MINI ENTERPRISE/
=======
Mini-Enterprise/
│
├── backend/
│   │
│   ├── venv/
│   │
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── README
│   │
│   ├── app/
│   │   │
│   │   ├── __pycache__/
│   │   │
│   │   ├── core/
│   │   │   ├── __pycache__/
│   │   │   ├── cache.py
│   │   │   ├── config.py
│   │   │   ├── dependencies.py
│   │   │   ├── limiter.py
│   │   │   ├── permissions.py
│   │   │   ├── security.py
│   │   │   ├── sla_scheduler.py
│   │   │   ├── stripe_config.py
│   │   │   └── subscriptions.py
│   │   │
│   │   ├── middleware/
│   │   │   └── sanitize.py
│   │   │
│   │   ├── websocket/
│   │   │   ├── __pycache__/
│   │   │   ├── manager.py
│   │   │   └── notifications.py
│   │   │
│   │   ├── models/
│   │   │   ├── __pycache__/
│   │   │   ├── __init__.py
│   │   │   ├── approval_delegation.py
│   │   │   ├── approval_escalation.py
│   │   │   ├── approval.py
│   │   │   ├── audit.py
│   │   │   ├── billing.py
│   │   │   ├── comment.py
│   │   │   ├── document.py
│   │   │   ├── employee.py
│   │   │   ├── notification_preferences.py
│   │   │   ├── notification.py
│   │   │   ├── organization.py
│   │   │   ├── sla.py
│   │   │   ├── subscription.py
│   │   │   ├── task.py
│   │   │   └── user.py
│   │   │
│   │   ├── repositories/
│   │   │   ├── __pycache__/
│   │   │   ├── ai_repo.py
│   │   │   ├── analytics_repo.py
│   │   │   ├── approval_delegation_repo.py
│   │   │   ├── approval_escalation_repo.py
│   │   │   ├── approval_repo.py
│   │   │   ├── audit_repo.py
│   │   │   ├── auth_repo.py
│   │   │   ├── comment_repo.py
│   │   │   ├── dashboard_repo.py
│   │   │   ├── document_repo.py
│   │   │   ├── notification_preferences_repo.py
│   │   │   ├── subscription_repo.py
│   │   │   └── task_repo.py
│   │   │
│   │   ├── routers/
│   │   │   ├── __pycache__/
│   │   │   ├── ai.py
│   │   │   ├── analytics_router.py
│   │   │   ├── approval_delegations.py
│   │   │   ├── approval_escalations.py
│   │   │   ├── approvals.py
│   │   │   ├── audit.py
│   │   │   ├── auth.py
│   │   │   ├── billing_routes.py
│   │   │   ├── comments.py
│   │   │   ├── dashboard.py
│   │   │   ├── documents.py
│   │   │   ├── kanban.py
│   │   │   ├── notification_preferences.py
│   │   │   ├── notifications.py
│   │   │   ├── payment_routes.py
│   │   │   ├── sla_routes.py
│   │   │   ├── subscription_routes.py
│   │   │   ├── tasks.py
│   │   │   ├── users.py
│   │   │   ├── websocket_routes.py
│   │   │   └── websocket.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __pycache__/
│   │   │   ├── analytics.py
│   │   │   ├── approval_delegation.py
│   │   │   ├── approval_escalation.py
│   │   │   ├── approval.py
│   │   │   ├── audit.py
│   │   │   ├── comment.py
│   │   │   ├── dashboard.py
│   │   │   ├── document.py
│   │   │   ├── kanban.py
│   │   │   ├── notification_preferences.py
│   │   │   ├── notification.py
│   │   │   ├── sla.py
│   │   │   ├── subscription.py
│   │   │   ├── task.py
│   │   │   └── user.py
│   │   │
│   │   ├── services/
│   │   │   ├── __pycache__/
│   │   │   ├── activity_service.py
│   │   │   ├── ai_service.py
│   │   │   ├── analytics_service.py
│   │   │   ├── approval_delegation_service.py
│   │   │   ├── approval_escalation_service.py
│   │   │   ├── approval_service.py
│   │   │   ├── audit_service.py
│   │   │   ├── auth_service.py
│   │   │   ├── comment_service.py
│   │   │   ├── dashboard_service.py
│   │   │   ├── document_service.py
│   │   │   ├── email_service.py
│   │   │   ├── notification_preferences_service.py
│   │   │   ├── notification_service.py
│   │   │   ├── payment_service.py
│   │   │   ├── sla_service.py
│   │   │   ├── subscription_service.py
│   │   │   ├── task_service.py
│   │   │   ├── websocket_service.py
│   │   │   └── workflow_service.py
│   │   │
│   │   ├── uploads/
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
│   ├── uploads/
│   │
│   ├── .env
│   ├── alembic.ini
│   └── requirements.txt
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
│   │
│   ├── src/
│   │   │
│   │   ├── api/
│   │   │   └── axios.js
│   │   │
│   │   ├── components/
│   │   │   ├── ForgotPassword.jsx
│   │   │   ├── Navbar.jsx
│   │   │   ├── PrivateRoute.jsx
│   │   │   ├── ResetPassword.jsx
│   │   │   └── UIComponents.jsx
│   │   │
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── AIInsights.jsx
│   │   │   ├── Analytics.jsx
│   │   │   ├── ApprovalDelegations.jsx
│   │   │   ├── ApprovalEscalations.jsx
│   │   │   ├── Approvals.jsx
│   │   │   ├── AuditLogs.jsx
│   │   │   ├── Billing.jsx
│   │   │   ├── BillingCancel.jsx
│   │   │   ├── BillingSuccess.jsx
│   │   │   ├── CreateTask.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── DashboardStats.jsx
│   │   │   ├── DocumentManagement.jsx
│   │   │   ├── EditTask.jsx
│   │   │   ├── KanbanBoard.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── notification-preferences.jsx
│   │   │   ├── NotificationCenter.jsx
│   │   │   ├── OAuthSuccess.jsx
│   │   │   ├── Pricing.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── SlaDashboard.jsx
│   │   │   ├── SLARules.jsx
│   │   │   ├── Subscription.jsx
│   │   │   └── TaskComments.jsx
│   │   │
│   │   ├── services/
│   │   │   └── WebSocketClient.js
│   │   │
│   │   ├── App.css
│   │   ├── App.js
│   │   ├── App.test.js
│   │   ├── index.css
│   │   ├── index.js
│   │   ├── logo.svg
│   │   ├── reportWebVitals.js
│   │   └── setupTests.js
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
│   ├── .gitignore
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   └── tailwind.config.js
│
├── .gitignore
├── README.md
└── LICENSE
=======
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
Database Models

Core Models:

User
Task
Approval
ApprovalHistory
Comment
Notification
Document
AuditLog
SLARule
SLATracking
ApprovalEscalation
ApprovalDelegation
NotificationPreferences
Organization
Subscription
Billing



```
Project Completion Checklist
#-----------------------------#
Phase 1 — Authentication & Task Management

Implemented:

JWT Authentication
Role-Based Access Control
Task CRUD APIs
Task Assignment
Dashboard
Protected Routes
Roles
Role	Access
Admin	Full system access
Manager	Task & workflow management
Employee	Assigned tasks only


Phase 2 — Workflow & Collaboration System

Implemented:

Kanban Board
Workflow Status Rules
Approval System
Comments Module
Dashboard Analytics
Activity Tracking
Workflow
TODO → IN_PROGRESS → REVIEW → DONE

Invalid transitions are blocked.

Phase 3 — Enterprise Features & Intelligence Layer

Implemented:

Document Management
Audit Logs
Notification System
AI Insights
Activity Feed


Phase 4 — Strengthening Current Implementation

Implemented:

Advanced Authentication:
JWT Refresh Tokens
Password Reset Flow
Google OAuth Login

Security Enhancements
Role-Based Middleware
API Rate Limiting
Input Validation
Sanitization Middleware


Performance Optimization
Pagination APIs
Redis Caching
Query Optimization
Database Indexing


Phase 5 — Enterprise-Level Enhancements

Implemented:

Real-Time Features
WebSocket Notifications
Live Kanban Updates
Activity Tracking

Tracks:

Task Updates
Approval Changes
Document Uploads
User Actions
Role-Based Dashboards
Employee Dashboard
Assigned Tasks
Requests
Notifications
Manager Dashboard
Team Progress
Approvals
SLA Monitoring
Admin Dashboard
Analytics
Audit Logs
System Monitoring

Phase 6 — Intelligent Features

Implemented:

 AI Task Insights
High-priority pending tasks
Delay risk detection
SLA breach prediction
Smart Task Assignment

Based on:

User workload
Historical performance
Priority handling capability


Phase 7 — SaaS-Level Enhancements

Implemented:
Multi-Tenant Architecture
Supports multiple organizations.
Subscription System

Plans:
Basic
Silver
Gold
Billing Integration

Integrated:
Stripe
Credit-Based Usage

Organizations consume credits for AI and advanced features.

Phase 8 — Enterprise Workflow Governance

Implemented:

SLA Rule Management
Create SLA rules
Configure escalation policies
Priority-based SLA timing
 SLA Tracking

Track:

Active SLA
Breached SLA
Escalated SLA
Completed SLA

Approval Escalation
Escalate delayed approvals
Resolve escalations
Escalation history

Approval Delegation
Delegate approvals temporarily
Manager leave delegation
 Notification Preferences

Users can configure:

Email notifications
In-app notifications
Task alerts
Approval alerts
Enhanced Audit Logs

Tracks:

Old/New Data
IP Address
User Agent
Module Name
Action Type
```

```
API Endpoints
#-------------#
Authentication APIs

Method	Endpoint	Description
POST	/auth/register	Register new user
POST	/auth/login	Login user
POST	/auth/refresh	Refresh JWT token
POST	/auth/forgot-password	Send password reset email
POST	/auth/reset-password	Reset password using token
GET	/auth/google/login	Google OAuth login
GET	/auth/google/callback	Google OAuth callback
GET	/auth/me	Get current logged-in user
POST	/auth/logout	Logout user
GET	/auth/verify	Verify JWT token


👥 User APIs
Method	Endpoint	Description
GET	/users/	List all users
GET	/users/{id}	Get user details


📋 Task APIs
Method	Endpoint	Description
GET	/tasks/	List tasks
POST	/tasks/	Create task
GET	/tasks/{task_id}	Get task details
PUT	/tasks/{task_id}	Update task
DELETE	/tasks/{task_id}	Delete task



🗂 Kanban APIs
Method	Endpoint	Description
GET	/tasks/kanban	Get Kanban board data
PATCH	/tasks/{id}/status	Update task status



💬 Comment APIs
Method	Endpoint	Description
POST	/tasks/{task_id}/comments	Add comment to task
GET	/tasks/{task_id}/comments	List task comments



✅ Approval APIs
Method	Endpoint	Description
GET	/approvals/	List approvals



📊 Dashboard APIs
Method	Endpoint	Description
GET	/dashboard/summary	Dashboard summary
GET	/role-dashboard	Role-based dashboard
GET	/dashboard/ai-summary	AI insights summary



📄 Document APIs
Method	Endpoint	Description
GET	/documents/	List documents
POST	/documents/upload	Upload document
GET	/documents/download/{id}	Download document
DELETE	/documents/{id}	Delete document



📜 Audit Log APIs
Method	Endpoint	Description
GET	/audit-logs/	List audit logs


🔔 Notification APIs
Method	Endpoint	Description
GET	/notifications/	List notifications
GET	/notifications/unread	Get unread notification count
PATCH	/notifications/{id}/read	Mark notification as read



🤖 AI APIs
Method	Endpoint	Description
GET	/dashboard/ai-summary	AI task insights


📈 Analytics APIs
Method	Endpoint	Description
GET	/analytics/summary	Analytics summary
GET	/analytics/task-status	Task status analytics
GET	/analytics/user-tasks	User task analytics


💳 Subscription APIs
Method	Endpoint	Description
GET	/subscriptions/	List subscriptions
GET	/subscriptions/current	Current subscription details


💰 Billing APIs
Method	Endpoint	Description
GET	/billing/checkout/{plan}	Stripe checkout session
POST	/billing/webhook	Stripe webhook



⏱ SLA Rule APIs
Method	Endpoint	Description
POST	/sla-rules/	Create SLA rule
GET	/sla-rules/	List SLA rules
GET	/sla-rules/{rule_id}	Get SLA rule
PUT	/sla-rules/{rule_id}	Update SLA rule
DELETE	/sla-rules/{rule_id}	Disable SLA rule



📌 SLA Tracking APIs
Method	Endpoint	Description
POST	/sla-tracking/tasks/{task_id}	Start SLA for task
POST	/sla-tracking/approvals/{approval_id}	Start SLA for approval
PUT	/sla-tracking/{sla_id}/complete	Complete SLA
GET	/sla-tracking/active	Active SLA records
GET	/sla-tracking/breached	Breached SLA records
GET	/sla-tracking/record/{module_name}/{record_id}	Get SLA record details



🚨 Approval Escalation APIs
Method	Endpoint	Description
GET	/approval-escalations/	List escalations
POST	/approval-escalations/	Create escalation
GET	/approval-escalations/pending	Pending escalations
GET	/approval-escalations/approval/{approval_id}	Approval escalation history
PUT	/approval-escalations/{id}/resolve	Resolve escalation
PUT	/approval-escalations/{id}/cancel	Cancel escalation



👥 Approval Delegation APIs
Method	Endpoint	Description
POST	/approval-delegations/	Create delegation
GET	/approval-delegations/me	My delegations
GET	/approval-delegations/active	Active delegations
PUT	/approval-delegations/{id}/cancel	Cancel delegation
⚙ Notification Preference APIs
Method	Endpoint	Description
GET	/notification-preferences/me	Get my notification preferences
PUT	/notification-preferences/me	Update notification preferences
POST	/notification-preferences/default/{user_id}	Create default preferences


🌐 Default APIs
Method	Endpoint	Description
GET	/	Root endpoint
GET	/health	Health check
🔌 WebSocket Endpoint
Protocol	Endpoint	Description
WS	/ws	Real-time notifications & live updates


🔐 Authentication Header

Use JWT token in headers:

Authorization: Bearer <your_token>

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

```




=======



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

>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
