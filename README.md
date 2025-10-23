🏗️ SiteFlow API – Construction Project Communication & Issue Tracking Platform

SiteFlow API is a professional, web-based construction management platform that centralizes communication, tracks site issues, and ensures accountability among all stakeholders.

As a Construction Manager by profession, I’ve experienced firsthand how fragmented tools like WhatsApp, SMS, and paper records slow down workflows and cause miscommunication.

SiteFlow solves this by offering a structured, audit-ready system that organizes projects, trades, issues, and communications — all in one place.

📘 Table of Contents

Problem Statement

Solution Overview

Core Features

Tech Stack

System Architecture

Data Models

API Endpoints

Authentication & Authorization

Search, Filtering & Pagination

Audit Trail System

Setup Instructions ⚙️

Testing & Documentation 🧪

Development Roadmap 🗓️

Future Enhancements 🚀

Author ✍️

License 📜

🧩 Problem Statement

Construction sites often rely on fragmented and informal tools such as WhatsApp, Excel, and verbal communication.

These disjointed systems lead to:

❌ Lost issue records and unclear accountability

⚠️ Miscommunication between trades

🕐 Delayed resolutions and incomplete follow-ups

📉 Lack of historical data and compliance reports

✅ Solution Overview

SiteFlow introduces a unified, structured platform that:

Organizes Projects → Trades → Issues hierarchically

Defines clear user roles (Admin, Project Manager, Site Officer, Subcontractor)

Provides a searchable, auditable issue-tracking system

Keeps everyone accountable with real-time updates and audit trails

This improves communication, reduces delays, and enhances transparency across construction projects.

💡 Core Features
🏗️ Project & Admin Management

Create and manage multiple projects

Assign trades (e.g., plumbing, electrical, structural)

Control user access based on assigned roles

🧱 Issue Tracking

Log issues with title, description, trade, priority, due date

Attach photos, PDFs, or supporting documents

Assign issues to specific users or trades

Track progress through open → in-progress → closed workflow

💬 Communication

Comment threads per issue with timestamps

Trade-level sub-boards and leadership main boards

🔐 Role-Based Access Control (RBAC)
Role	Permissions
Admin	Global project visibility
Project Manager	Manage projects, trades, and assignments
Site Officer	Report and update issues
Subcontractor	View assigned tasks and update progress
📊 Dashboard

View total issues, open issues, and overdue tasks

Highlight critical priorities for leadership

🛠️ Tech Stack
Layer	Technology
Backend Framework	Django + Django REST Framework
Database	PostgreSQL
Authentication	JSON Web Tokens (JWT)
Deployment	Heroku / Render / PythonAnywhere
Documentation	Swagger / OpenAPI Specification
Frontend (Optional)	HTML, CSS, JS
🧱 System Architecture
Frontend (React/HTML)
        ↓
   Django REST API
        ↓
   PostgreSQL Database
        ↓
     JWT Auth Layer


Django REST Framework handles endpoints and business logic

JWT ensures secure authentication

PostgreSQL provides scalability and reliability

🗃️ Data Models
Model	Fields
User	id, username, email, password_hash, role (PM, Site Officer, CEO, Subcontractor)
Project	id, title, description, start_date, end_date
Trade	id, name, project_id
Issue	id, title, description, trade_category, priority, status, assigned_to, due_date, project_id
Comment	id, issue_id, user_id, content, timestamp
Attachment	id, issue_id, file_url, uploaded_at
IssueHistory	id, issue_id, user_id, action, old_value, new_value, timestamp
🔗 API Endpoints
🧑‍💼 Authentication & User Management
Endpoint	Method	Description
/api/auth/register/	POST	Register a new user
/api/auth/login/	POST	Obtain JWT access and refresh tokens
/api/auth/profile/	GET	Retrieve logged-in user profile

🏗️ Projects & Trades
Endpoint	Method	Description
/api/projects/	GET	List all projects for authenticated user
/api/projects/	POST	Create new project (PM only)
/api/projects/{project_id}/add_trade/	POST	Add a trade to a project
/api/trades/	GET/POST	Manage trades (Admin/PM only)
/api/test-assigned-projects/	GET	Returns assigned projects per user
/dashboard/	GET	Project overview dashboard

🧱 Issues Management
Endpoint	Method	Description
/api/issues/	GET/POST	List or create issues
/api/projects/{project_id}/issues/	GET/POST	List or create project-specific issues
/api/issues/{issue_id}/	GET	Retrieve a single issue with details
/api/issues/{issue_id}/assign/	POST	Assign issue to user or trade
/api/issues/{issue_id}/upload/	POST	Upload attachment (image/PDF)
/api/issues/{issue_id}/comments/	POST	Add a comment to issue
💬 Comments & Attachments
Endpoint	Method	Description
/api/comments/	GET/POST	Manage comments
/api/attachments/	GET/POST	Manage attachments

🔐 Authentication & Authorization

JWT-based secure login system

Role-based permission checks

Example header:

Authorization: Bearer <your_jwt_token>

🔍 Search, Filtering & Pagination
GET /api/issues/?search=leak&status=open&priority=high&trade=plumbing&assigned_to=john
GET /api/issues/?page=2&page_size=20


✅ Enables:

Project managers to find all high-priority electrical issues

Site officers to view only their assigned issues

🧾 Audit Trail System

Tracks every change for accountability:

class IssueHistory(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


💡 Why It Matters:

Maintains transparency

Aids compliance, safety, and dispute resolution

⚙️ Setup Instructions
1️⃣ Clone Repository
git clone https://github.com/<your-username>/siteflow.git
cd siteflow

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate     # On Windows
source venv/bin/activate  # On macOS/Linux

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment Variables

Create a .env file:

SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://username:password@localhost:5432/siteflow

5️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Run Development Server
python manage.py runserver


Access the API at 👉 http://127.0.0.1:8000/api/

🧪 Testing & Documentation

Use Postman or Swagger UI for API testing

Swagger docs: /swagger/

Postman collection: /docs/postman_collection.json

Includes:

Authentication guide

Example responses

Error handling

🗓️ Development Roadmap
Week	Goals
Week 1	Setup Django project, configure JWT auth
Week 2	Implement User, Project, Trade models + endpoints
Week 3	Implement Issues, Comments, and Sub-board system
Week 4	Add file uploads, filtering, pagination
Week 5	Testing, documentation, and deployment
🚀 Future Enhancements

🔔 Real-time notifications (via WebSockets/Channels)

📊 Analytics Dashboard for issue trends & KPIs

📱 Mobile App Integration (Flutter/React Native)

🧾 Automated PDF project reports

🌍 Multi-language support

🔒 Two-Factor Authentication for admins
