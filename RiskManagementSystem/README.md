# Risk Management System

## Overview

Risk Management System is a backend API project developed using FastAPI, SQLAlchemy, SQLite, and JWT Authentication. The project is designed to manage organizational risks, users, and role-based access permissions.

The application allows administrators, managers, and employees to:

- Create and manage risks
- Assign risks to users
- Track risk status and priority
- Authenticate users securely using JWT tokens
- Control API access using role-based authorization

The project follows a layered architecture using:

- Routers Layer
- Repository Layer
- Schema Layer
- Database Models Layer
- Authentication & Authorization Layer

---

# Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Backend API Framework |
| SQLAlchemy | ORM Database Operations |
| SQLite | Database |
| Pydantic | Data Validation |
| JWT | Authentication |
| Passlib + bcrypt | Password Hashing |
| Uvicorn | ASGI Server |

---

# Project Structure

```text
RiskManagementSystem/
│
├── main.py
├── default.py
├── hashing.py
├── requirements.txt
├── changestodo.txt
│
├── Model/
│   ├── database.py
│   ├── model.py
│   └── database.db
│
├── Repository/
│   ├── risks.py
│   └── users.py
│
├── routers/
│   ├── authenticate.py
│   ├── risks.py
│   ├── users.py
│   └── __init__.py
│
├── Schema/
│   └── schema.py
│
├── Scheme/
│   ├── jwttoken.py
│   ├── oauth2.py
│   └── RoleBasedAccess.py
│
└── __init__.py
```

---

# Architecture Flow

```text
Client Request
      │
      ▼
Router Layer (API Endpoints)
      │
      ▼
Repository Layer (Business Logic)
      │
      ▼
Database Models (SQLAlchemy ORM)
      │
      ▼
SQLite Database
```

Authentication Flow:

```text
Login Request
      │
      ▼
Verify Email & Password
      │
      ▼
Generate JWT Token
      │
      ▼
Protected API Access
      │
      ▼
Role Validation
```

---

# Main Components

## 1. main.py

Main entry point of the FastAPI application.

Responsibilities:

- Creates FastAPI app instance
- Includes all routers
- Starts application server
- Connects APIs together

Expected responsibilities include:

```python
app.include_router(users.router)
app.include_router(risks.router)
app.include_router(authenticate.router)
```

---

# 2. Model Layer

Folder: `Model/`

This layer manages database connection and ORM models.

## database.py

Responsible for:

- Creating SQLite engine
- Creating database sessions
- Providing dependency injection for database access

Key Functions:

```python
engine = create_engine("sqlite:///Model/database.db")
```

```python
get_db()
```

This function provides database sessions to API routes.

---

## model.py

Contains SQLAlchemy ORM Models.

### User Model

Fields:

- user_id
- user_name
- user_role
- user_email
- user_password

Relationships:

- assigned_risk
- allocated_risk
- created_risk

### Risk Model

Fields:

- risk_id
- risk_title
- risk_description
- risk_priority
- risk_status
- risk_type
- risk_category
- created_by
- risk_allocation
- assigned_to
- due_date

Relationships:

- assignee
- allocator
- creator

The project uses SQLAlchemy relationships to connect risks with users.

---

# 3. Schema Layer

Folder: `Schema/`

File: `schema.py`

This layer contains Pydantic models used for:

- Request validation
- Response formatting
- API serialization

Schemas included:

## User Schemas

- User
- UserUpdate
- UserOutput
- UserOutputUpdated

## Risk Schemas

- Risk
- RiskUpdate
- RiskOutput
- RiskOutputUpdated

## Authentication Schemas

- Login
- Token
- TokenData

---

# 4. Repository Layer

Folder: `Repository/`

This layer contains all business logic and database operations.

---

## users.py

Handles all user operations.

Functions:

| Function | Purpose |
|---|---|
| all_users() | Get all users |
| user_by_id() | Get single user |
| add_user() | Create new user |
| update_user() | Update user |
| delete_user() | Delete user |
| risks_assigned() | Fetch assigned risks |

Features:

- Password hashing using bcrypt
- Database CRUD operations
- Error handling using HTTPException

---

## risks.py

Handles all risk operations.

Functions:

| Function | Purpose |
|---|---|
| get_all() | Fetch all risks |
| get_risks_by_id() | Fetch single risk |
| add_risks() | Create risk |
| update_risks() | Update risk |
| delete_risk() | Delete risk |

Features:

- Returns detailed risk data
- Includes related user information
- Handles assignment mapping
- Status-based responses

---

# 5. Router Layer

Folder: `routers/`

This layer defines API endpoints.

---

## authenticate.py

Authentication router.

Endpoint:

```http
POST /login
```

Responsibilities:

- Verifies user credentials
- Checks hashed password
- Generates JWT token
- Returns bearer token

---

## users.py

User management endpoints.

Base Route:

```http
/user
```

Endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | /user/ | Get all users |
| GET | /user/{user_id} | Get user by ID |
| POST | /user/add | Add new user |
| PUT | /user/update/{user_id} | Update user |
| DELETE | /user/delete/{user_id} | Delete user |

---

## risks.py

Risk management endpoints.

Base Route:

```http
/risk
```

Endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | /risk/ | Get all risks |
| GET | /risk/{risk_id} | Get risk by ID |
| POST | /risk/add | Add new risk |
| PUT | /risk/update/{risk_id} | Update risk |
| DELETE | /risk/delete/{risk_id} | Delete risk |

---

# 6. Authentication & Authorization

Folder: `Scheme/`

---

## jwttoken.py

Responsible for:

- JWT token creation
- Token verification
- Token expiration management

Important Variables:

```python
SECRET_KEY
ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
```

Functions:

- create_access_token()
- verifyToken()

---

## oauth2.py

Handles:

- OAuth2 token extraction
- Current user validation

Uses:

```python
OAuth2PasswordBearer
```

---

## RoleBasedAccess.py

Implements role-based authorization.

Access Levels:

| Level | Roles |
|---|---|
| level_1 | Admin |
| level_2 | Admin, Manager |
| level_3 | Admin, Manager, Employee |

Function:

```python
role_required()
```

This function validates whether the logged-in user has permission to access an endpoint.

---

# Password Security

File: `hashing.py`

Uses Passlib and bcrypt for password hashing.

Functions:

```python
bcryptPassword()
verifyPassword()
```

Passwords are never stored in plain text.

---

# Default Data

File: `default.py`

Contains:

- Default users
- Default risks
- Seed/sample data

Useful for:

- Initial testing
- Demo setup
- Development environment

---

# API Workflow

## User Authentication Workflow

```text
1. User sends login credentials
2. System validates email and password
3. Password hash is verified
4. JWT token is generated
5. Token returned to client
6. Client uses token in Authorization header
```

Authorization Header:

```http
Authorization: Bearer <token>
```

---

## Risk Creation Workflow

```text
1. Authenticated user sends risk data
2. Role access is validated
3. Data validated using Pydantic schema
4. Repository layer processes logic
5. SQLAlchemy stores data
6. API returns response
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/linuschoudhary/MenTechPvtLtd.git
```

## Navigate to Project

```bash
cd MenTechPvtLtd/RiskManagementSystem
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Application

```bash
uvicorn main:app --reload
```

Application URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc Documentation:

```text
http://127.0.0.1:8000/redoc
```

---

# Database

Database Used:

```text
SQLite
```

Database File:

```text
Model/database.db
```

The application uses SQLAlchemy ORM for interacting with the database.

---

# Example Login Credentials

The project contains sample users inside `default.py`.

Example:

```text
Email: mohit@gmail.com
Password: mohit123
```

---

# Features

- JWT Authentication
- Role-Based Authorization
- CRUD Operations for Risks
- CRUD Operations for Users
- SQLite Database Integration
- SQLAlchemy ORM Relationships
- Password Hashing
- FastAPI Validation
- Swagger API Documentation
- Modular Folder Structure

---

# Future Improvements

Possible enhancements:

- MySQL/PostgreSQL Support
- Docker Deployment
- Unit Testing
- Logging System
- Email Notifications
- Risk Analytics Dashboard
- Frontend Integration
- Pagination & Filtering
- Environment Variables for Secrets
- Refresh Tokens

---

# Known Issues

- `requirements.txt` contains typo `pydentic` instead of `pydantic`
- Secret key is hardcoded
- SQLite is not ideal for production-scale systems

---

# Learning Concepts Covered

This project demonstrates:

- FastAPI API development
- REST API architecture
- SQLAlchemy ORM
- JWT authentication
- OAuth2 implementation
- Role-based access control
- Repository pattern
- Pydantic schema validation
- Password hashing
- CRUD operations

---

# Author

Developed as a backend risk management system project using FastAPI and SQLAlchemy.
