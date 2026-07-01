<div align="center">

# 🛡️ Advanced Risk Management System

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.138.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1.3.10-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-qwen3.5:4b-black?style=for-the-badge)
![FastMCP](https://img.shields.io/badge/FastMCP-3.4.2-6C4BFF?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**An AI-powered risk management backend built with FastAPI, LangChain, MCP, conversation memory, and a fully-local LLM via Ollama.**

*Developed during Summer Internship · Mentem Technologies Pvt. Ltd. · May 2026*

---

[Overview](#-overview) · [What's New](#-whats-new) · [Features](#-features) · [Architecture](#-architecture) · [Project Structure](#-project-structure) · [Setup](#-setup--installation) · [API Reference](#-api-reference) · [RiskBot](#-riskbot-ai-chatbot) · [Logging](#-activity-logging) · [RBAC](#-role-based-access-control) · [Database Schema](#-database-schema) · [Default Data](#-default-data)

</div>

---

## 📌 Overview

The **Advanced Risk Management System (ARMS)** is a production-ready backend that lets organisations identify, track, assign, and mitigate project risks through a secure REST API. It features **RiskBot** — an AI assistant that understands natural language, remembers conversation history per user, and can perform any read or write operation on the system by automatically calling the right API tools.

The system is secured end-to-end with **JWT authentication**, **role-based access control**, and a **structured activity-logging layer** that records every significant action across every endpoint.

> **Author:** Sunil Choudhary · Summer Intern, Mentem Technologies Pvt. Ltd.  
> **Repository:** [github.com/linuschoudhary/AdvancedRiskManagementSystem](https://github.com/linuschoudhary/AdvancedRiskManagementSystem)

---

## 🆕 What's New

The following features and changes have been added since the initial release:

| Area | Change |
|---|---|
| 🗒️ **Activity Logging** | New `Log/` module — every endpoint now writes structured logs to `Log/activity.log` |
| 📋 **Log Viewer** | New `GET /logs` endpoint (Admin-only) returns the full log file content |
| 👤 **Who Am I** | New `GET /whoami` endpoint — returns the currently authenticated user's email and role |
| 🧠 **Conversation Memory** | RiskBot now remembers the chat history per user session via `InMemorySaver` + `thread_id` |
| 🤖 **RiskBot Identity** | Chatbot is now branded as **RiskBot** with a dedicated name and improved system prompt |
| 🙋 **User-Aware Greetings** | RiskBot greets users by their name (derived from their email via JWT) when they say hello |
| 🔐 **Tightened RBAC** | `add_user`, `update_user`, `delete_user` now all require **Admin** role (previously open) |
| 🔐 **RBAC Logging** | `role_required()` now accepts an endpoint name and logs every unauthorized access attempt |
| 🔑 **Token Utility** | New `get_user_from_token()` helper in `jwttoken.py` for extracting user email from JWT |
| 📄 **MIT License** | `LICENSE` file added |
| 🚫 **`.gitignore`** | `*.log` pattern added — log files are now excluded from version control |

---

## ✨ Features

- 🔐 **JWT Authentication** — Secure OAuth2 password flow with 30-minute token expiry
- 👥 **Role-Based Access Control (RBAC)** — Three-tier permission system: Admin → Manager → Employee
- 📋 **Full Risk CRUD** — Create, read (all or by ID), update (partial or full), and delete risks
- 👤 **Full User CRUD** — Manage system users with Admin-level protection on write operations
- 🤖 **RiskBot AI Chatbot** — Natural language risk management assistant powered by a local LLM
- 🧠 **Conversation Memory** — RiskBot remembers your chat history within a session (per-user thread)
- 🔧 **MCP Integration** — All FastAPI routes exposed as LLM tools via FastMCP (Model Context Protocol)
- 🗒️ **Activity Logging** — Structured file-based logging on every endpoint (INFO for normal, WARNING for failures/mutations)
- 📋 **Log Viewer** — Admin-accessible endpoint to inspect the live activity log
- 🎨 **Streamlit Frontend** — Clean chat UI for interacting with RiskBot
- 🔒 **bcrypt Hashing** — All passwords stored as bcrypt hashes
- 📦 **SQLite + SQLAlchemy ORM** — Lightweight relational DB with three foreign-key relationships on the Risk model
- 🗂️ **Data Seeding** — One-call endpoint to seed 8 default users and 8 sample risks
- 📄 **Auto API Docs** — Interactive Swagger UI at `/docs` out of the box

---

## 🏗️ Architecture

### System Diagram

```
┌───────────────────────────────────────────────────────────────────────┐
│                          CLIENT LAYER                                 │
│        Streamlit UI (RiskBot)              REST Clients / Swagger     │
└────────────────────┬──────────────────────────────┬───────────────────┘
                     │ HTTP                          │ HTTP
                     ▼                              ▼
┌───────────────────────────────────────────────────────────────────────┐
│                    FastAPI Application  (main.py)                     │
│                                                                       │
│  ┌─────────────┐ ┌─────────────┐ ┌──────────────┐ ┌───────────────┐  │
│  │ /risk Router│ │ /user Router│ │/chatbot Router│ │  /login  &    │  │
│  │  risks.py   │ │  users.py   │ │  chatbot.py  │ │  /logs Router │  │
│  └──────┬──────┘ └──────┬──────┘ └──────┬───────┘ └──────┬────────┘  │
│         │               │               │                 │           │
│  ┌──────▼───────────────▼───────────────▼─────────────────▼────────┐  │
│  │              Authentication + RBAC Middleware                    │  │
│  │       JWT Verification  ·  Role Checking  ·  Audit Logging      │  │
│  └──────┬───────────────────────────────────────┬──────────────────┘  │
│         │                                       │                     │
│  ┌──────▼──────────────────────┐     ┌──────────▼───────────────┐     │
│  │      Database Layer         │     │     Activity Logger       │     │
│  │  SQLAlchemy ORM + SQLite    │     │   Log/logger.py           │     │
│  │   User  ↔  Risk (3 FKs)     │     │   → Log/activity.log      │     │
│  └─────────────────────────────┘     └──────────────────────────┘     │
└──────────────────────────────────────────┬────────────────────────────┘
                                           │
                            ┌──────────────▼──────────────┐
                            │         MCP Layer            │
                            │   FastMCP  (mcpserver.py)    │
                            │  Exposes FastAPI as tools    │
                            └──────────────┬───────────────┘
                                           │ stdio transport
                            ┌──────────────▼──────────────┐
                            │      LangChain Agent         │
                            │    (tool_binding.py)         │
                            │  Ollama: qwen3.5:4b          │
                            │  Checkpointer: InMemorySaver │
                            └─────────────────────────────┘
```

### RiskBot Request Flow

```
User sends message → POST /chatbot (Bearer token)
        ↓
Extract JWT token from Authorization header
        ↓
Decode token → get user email → used as thread_id (conversation memory key)
        ↓
Build LangChain agent with Ollama LLM + InMemorySaver checkpointer
        ↓
MultiServerMCPClient spawns FastMCP subprocess (JWT injected via env)
        ↓
Agent reasons over system prompt + chat history → selects MCP tool(s)
        ↓
FastMCP calls FastAPI endpoint → RBAC validated → DB operation
        ↓
Result returned to agent → natural language response to user
```

---

## 📁 Project Structure

```
FinalProject/
│
├── main.py                        # App entry point — registers all routers
├── default.py                     # Seed data: 8 users + 8 risks
├── requirements.txt               # All Python dependencies
├── LICENSE                        # MIT License
├── .env                           # Environment variables (git-ignored)
├── .gitignore                     # Ignores: __pycache__, .env, *.db, venv, *.log
│
├── Authentication/                # Security layer
│   ├── jwttoken.py                # JWT create, verify, get_user_from_token()
│   ├── oauth2.py                  # OAuth2PasswordBearer scheme
│   └── role_based_access.py       # RBAC — level_1/2/3, logs unauthorized attempts
│
├── Chatbot/                       # AI assistant
│   ├── chatbot.py                 # Agent runner — thread_id memory, system prompt
│   ├── tool_binding.py            # MCP client + Ollama agent with InMemorySaver
│   └── app.py                     # Streamlit frontend ("RiskBot")
│
├── Database/                      # Persistence layer
│   ├── database.py                # SQLAlchemy engine + session factory
│   ├── model.py                   # ORM models: User, Risk (3 FK relationships)
│   ├── users.py                   # User CRUD functions
│   ├── risks.py                   # Risk CRUD functions
│   └── RMSDB.db                   # SQLite file (git-ignored)
│
├── Hashing/
│   └── hashing.py                 # bcrypt hash + verify via passlib
│
├── Log/                           # Activity logging
│   ├── logger.py                  # logging.basicConfig → Log/activity.log
│   └── activity.log               # Runtime log file (git-ignored)
│
├── MCP/
│   └── mcpserver.py               # FastMCP wraps FastAPI; injects auth token
│
├── Routers/                       # FastAPI route handlers
│   ├── authenticate.py            # POST /login
│   ├── users.py                   # /user/* — full CRUD
│   ├── risks.py                   # /risk/* — full CRUD
│   ├── chatbot.py                 # POST /chatbot, GET /whoami
│   └── read_logs.py               # GET /logs (Admin-only)
│
└── Schema/
    └── schema.py                  # Pydantic models: Users, Risks, UpdateUser, UpdateRisks, Token, TokenData
```

---

## 👥 Role-Based Access Control

The system defines three hierarchical permission levels. Every protected endpoint declares which level is required. Unauthorized access attempts are logged as `WARNING` with the user's email, role, and endpoint name.

| Role | Level | What they can access |
|---|---|---|
| **Admin** | level_1, level_2, level_3 | Everything — including user management, log viewer, and all risk operations |
| **Manager** | level_2, level_3 | All risk operations + chatbot + whoami |
| **Employee** | level_3 | Chatbot + whoami only |

```python
level_1 = ['Admin']                         # /user/ · /user/add_user · /user/update_user
                                            # /user/delete_user · /logs
level_2 = ['Admin', 'Manager']              # /risk · /risk/id · /risk/add_risk
                                            # /risk/update_risk · /risk/delete_risk
                                            # /user/show_by_id
level_3 = ['Admin', 'Manager', 'Employee']  # /chatbot · /whoami
```

When a user is **denied**, `role_required()` logs:
```
WARNING - user@email.com with role Employee tried to access add_new_risk with unauthorized access.
```

---

## 🗃️ Database Schema

### `user` table

| Column | Type | Constraints | Description |
|---|---|---|---|
| `user_id` | INTEGER | PK, auto-increment | Unique user identifier |
| `user_name` | STRING | — | Full display name |
| `user_role` | STRING | — | `Admin` / `Manager` / `Employee` |
| `user_email` | STRING | — | Login credential (username) |
| `user_password` | STRING | — | bcrypt-hashed password |

### `risks` table

| Column | Type | Constraints | Description |
|---|---|---|---|
| `risk_id` | INTEGER | PK, auto-increment | Unique risk identifier |
| `risk_title` | STRING | optional | Short headline for the risk |
| `risk_description` | STRING | required | Detailed description |
| `risk_priority` | STRING | required | `Critical` / `High` / `Medium` / `Low` |
| `risk_status` | STRING | required | `Open` / `In Progress` / `Mitigated` / `Monitoring` |
| `risk_type` | STRING | required | `Security` / `Infrastructure` / `Operational` / `Compliance` / `External` |
| `risk_category` | STRING | required | Sub-category (e.g. `Authentication`, `CI/CD`) |
| `created_by` | INTEGER | FK → user.user_id | User who created this risk |
| `risk_allocation` | INTEGER | FK → user.user_id | Manager the risk is allocated to |
| `assigned_to` | INTEGER | FK → user.user_id | Employee the risk is assigned to |
| `due_date` | STRING | required | Target resolution date (`YYYY-MM-DD`) |

The `Risk` model carries **three independent foreign-key relationships** back to `User`: `creator`, `allocator`, and `assignee`.

---

## 🚀 Setup & Installation

### Prerequisites

| Requirement | Notes |
|---|---|
| Python 3.11+ | |
| [Ollama](https://ollama.com/) | Must be running locally |
| `qwen3.5:4b` model | Pull command below |

### 1 — Clone the Repository

```bash
git clone https://github.com/linuschoudhary/AdvancedRiskManagementSystem.git
cd AdvancedRiskManagementSystem
```

### 2 — Create & Activate a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### 4 — Pull the LLM Model

```bash
ollama pull qwen3.5:4b
```

> To use a different model, edit `model=` in `Chatbot/tool_binding.py`.

### 5 — Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_strong_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> ⚠️ A hardcoded development key exists in `Authentication/jwttoken.py`. **Always replace it with a securely generated secret before any deployment.**

### 6 — Start the API Server

```bash
uvicorn main:app --reload
```

| URL | Description |
|---|---|
| `http://127.0.0.1:8000` | API root |
| `http://127.0.0.1:8000/docs` | Swagger UI (interactive docs) |
| `http://127.0.0.1:8000/redoc` | ReDoc API reference |

### 7 — Seed Default Data *(optional)*

```bash
curl http://127.0.0.1:8000/default
```

### 8 — Launch RiskBot Frontend *(optional)*

In a second terminal:

```bash
streamlit run Chatbot/app.py
```

Opens at `http://localhost:8501`.

---

## 📡 API Reference

### Authentication

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/login` | ❌ | Submit email + password (form data), receive a JWT bearer token |

**Request** (form-encoded):
```
username=user@email.com
password=yourpassword
```

**Response:**
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

All protected endpoints require:
```
Authorization: Bearer <access_token>
```

---

### General

| Method | Endpoint | Auth | Role | Description |
|---|---|---|---|---|
| `GET` | `/` | ❌ | Public | System introduction and metadata |
| `GET` | `/default` | ❌ | Public | Seed the database with default users and risks |

---

### Users — `/user`

| Method | Endpoint | Auth | Role | Description |
|---|---|---|---|---|
| `GET` | `/user/` | ✅ | **Admin** | List all users |
| `GET` | `/user/show_by_id?user_id={id}` | ✅ | Admin, Manager | Get one user by ID |
| `POST` | `/user/add_user` | ✅ | **Admin** | Create a new user |
| `PUT` | `/user/update_user?user_id={id}` | ✅ | **Admin** | Update user (partial update supported) |
| `DELETE` | `/user/delete_user?user_id={id}` | ✅ | **Admin** | Delete a user |

**Create / Update User body:**
```json
{
  "user_name": "Jane Doe",
  "user_role": "Manager",
  "user_email": "jane@company.com",
  "user_password": "securepassword"
}
```
All fields in `UpdateUser` are optional — send only the fields you want to change.

---

### Risks — `/risk`

| Method | Endpoint | Auth | Role | Description |
|---|---|---|---|---|
| `GET` | `/risk` | ✅ | Admin, Manager | List all risks (with full user objects for creator, allocator, assignee) |
| `GET` | `/risk/id?risk_id={id}` | ✅ | Admin, Manager | Get one risk by ID |
| `POST` | `/risk/add_risk` | ✅ | Admin, Manager | Create a new risk |
| `POST` | `/risk/update_risk?risk_id={id}` | ✅ | Admin, Manager | Update a risk (partial update supported) |
| `POST` | `/risk/delete_risk?risk_id={id}` | ✅ | Admin, Manager | Delete a risk |

**Create Risk body:**
```json
{
  "risk_title": "Database Backup Failure",
  "risk_description": "Automated backup job has been failing silently for 3 days.",
  "risk_priority": "Critical",
  "risk_status": "Open",
  "risk_type": "Infrastructure",
  "risk_category": "Database",
  "created_by": 6,
  "risk_allocation": 2,
  "assigned_to": 7,
  "due_date": "2026-07-10"
}
```

`risk_title` is optional. All other fields in `UpdateRisks` are optional for partial updates.

---

### Chatbot & Utility

| Method | Endpoint | Auth | Role | Description |
|---|---|---|---|---|
| `POST` | `/chatbot?message={text}` | ✅ | Admin, Manager, Employee | Send a message to RiskBot |
| `GET` | `/whoami` | ✅ | Admin, Manager, Employee | Returns the current user's email and role |

**Example `/chatbot` request:**
```bash
curl -X POST "http://127.0.0.1:8000/chatbot?message=Show+all+critical+risks" \
  -H "Authorization: Bearer <token>"
```

**`/whoami` response:**
```
"jane@company.com as Manager"
```

---

### Logs

| Method | Endpoint | Auth | Role | Description |
|---|---|---|---|---|
| `GET` | `/logs` | ✅ | **Admin** | Returns the full contents of `Log/activity.log` |

**Sample log output:**
```
27-06-2026 14:32:01 - INFO  - authenticate - login         - Sunil Choudhary logged in with user role Admin
27-06-2026 14:32:15 - INFO  - risks        - show_all_risks - sunil@gmail.com with role of Admin get the details of all risks
27-06-2026 14:33:02 - WARNING - role_based_access - role_checker - dipesh@gmail.com with role Employee tried to access add_new_risk with unauthorized access.
```

---

## 🤖 RiskBot AI Chatbot

### How It Works

RiskBot is powered by a **LangChain agent** running a **local Ollama LLM** (`qwen3.5:4b`) with the FastAPI backend exposed as callable tools via **FastMCP (Model Context Protocol)**. It maintains per-user conversation history using **LangGraph's `InMemorySaver`**.

**Step-by-step flow:**

1. User sends a message to `POST /chatbot` with their Bearer token.
2. The token is decoded to extract the **user email**, which becomes the `thread_id` — the unique key for this user's conversation history.
3. A LangChain agent is built with the Ollama LLM and the `InMemorySaver` checkpointer.
4. A `MultiServerMCPClient` spawns `MCP/mcpserver.py` as a subprocess (via stdio), injecting the JWT into its environment.
5. FastMCP wraps all FastAPI routes as **LLM tools**, using their docstrings as tool descriptions.
6. The agent reasons over the system prompt + full message history → selects tools → calls the API → returns a natural language answer.
7. The conversation state (all messages) is saved under `thread_id` for the next request.

### What RiskBot Can Do

RiskBot can perform any operation the underlying API supports, entirely through natural language:

```
"Show me all open critical risks"
"Who is assigned to risk #4?"
"Add a new High priority security risk about the login system, assigned to Dipesh, due July 15"
"Update risk 3 status to Mitigated"
"Delete risk 7"
"List all users with the Manager role"
"What risks are overdue?"
"Hello!"  →  RiskBot greets you by name from your email
```

### RiskBot System Prompt Rules

The LLM is instructed to follow these rules strictly:

1. Only answer questions related to risk management — users, risks, assignments, priorities, status
2. Always call tools when data is needed — never invent data
3. If data is unavailable, respond: *"Details not found."*
4. Reject off-topic questions with: *"I can only assist with risk management tasks."*
5. Never alter the spelling of names or values given by the user
6. Apply any filters the user requests *after* fetching data, without additional tool calls
7. Always use the current date/time when reasoning about deadlines
8. Do not determine the current logged-in user from log files — only from provided context
9. Greet users by name (derived from their email via `thread_id`) when they say hello

### Conversation Memory

Each user's conversation is stored in memory under their email as `thread_id`:

```python
config = {"configurable": {"thread_id": user_email}}
response = await agent.ainvoke({...messages...}, config=config)
```

This means RiskBot **remembers what you said earlier in the same session** — no need to repeat context. Memory is in-process (`InMemorySaver`) and resets when the server restarts.

### Streamlit Frontend

`Chatbot/app.py` provides a browser-based chat interface titled **RiskBot**:

- **Sidebar** — Login form that calls `POST /login` and stores the JWT in session state
- **Chat input** — Sends messages to `POST /chatbot` with the Bearer token
- **Chat bubbles** — Displays user and AI messages in a conversational layout

```bash
streamlit run Chatbot/app.py
# → http://localhost:8501
```

---

## 🗒️ Activity Logging

All application activity is recorded in `Log/activity.log` using Python's standard `logging` module.

### Log Format

```
DD-MM-YYYY HH:MM:SS - LEVEL - module_name - function_name - message
```

### Log Levels Used

| Level | When it's used |
|---|---|
| `INFO` | Successful logins, data reads, chatbot calls, default data seeding |
| `WARNING` | Failed login attempts, password mismatches, unauthorized access attempts, user/risk mutations (update, delete) |

### What Gets Logged

| Event | Level | Example message |
|---|---|---|
| Successful login | INFO | `Sunil Choudhary logged in with user role Admin` |
| Email not found on login | WARNING | `sunil@gmail.com does not exist` |
| Wrong password | WARNING | `sunil@gmail.com password mismatch` |
| Unauthorized endpoint access | WARNING | `dipesh@gmail.com with role Employee tried to access add_new_risk with unauthorized access.` |
| View all risks | INFO | `sunil@gmail.com with role of Admin get the details of all risks` |
| Add risk | INFO | `sunil@gmail.com ... added a new risk with Details: ...` |
| Update risk | WARNING | `sunil@gmail.com ... updated risk 3 with new detail ...` |
| Delete risk | WARNING | `sunil@gmail.com ... deleted risk 7` |
| Add user | INFO | `sunil@gmail.com ... added new user with details ...` |
| Update user | WARNING | `sunil@gmail.com ... updated the details of user 2 ...` |
| Delete user | WARNING | `sunil@gmail.com ... deleted the user with user id 2` |
| Chatbot message | INFO | `sunil@gmail.com called chatbot with message: Show all risks` |
| Read logs | INFO | `sunil@gmail.com with role Admin accessed 'Log Records'` |
| Watchfiles noise | CRITICAL (suppressed) | Filtered out entirely |

### Logger Configuration

```python
# Log/logger.py
logging.basicConfig(
    filename="Log/activity.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
)
logging.getLogger("watchfiles").setLevel(logging.CRITICAL)   # suppresses hot-reload noise
```

> `Log/activity.log` is excluded from version control via `.gitignore` (`*.log`).

---

## 🌱 Default Data

Call `GET /default` once on a fresh database to populate sample records.

### Default Users

| ID | Name | Role | Email | Password |
|---|---|---|---|---|
| 1 | Abc Bcd | Employee | abc@gmail.com | abc123 |
| 2 | Bcd Cde | Manager | bcd@gmail.com | bcd123 |
| 3 | Cde Def | Manager | cde@gmail.com | cde123 |
| 4 | Def Efg | Employee | def@gmail.com | def123 |
| 5 | Efg Fgh | Admin | efg@gmail.com | efg123 |
| 6 | Sunil Choudhary | Admin | sunil@gmail.com | sunil123 |
| 7 | Fgh Ghi | Employee | fgh@gmail.com | fgh123 |
| 8 | Ghi Hij | Employee | ghi@gmail.com | ghi123 |

### Default Risks

| Title | Priority | Status | Type | Category |
|---|---|---|---|---|
| Admin Panel Unauthorized Access Attempt | High | Open | Security | Authentication |
| Backup System Failure Risk | Critical | In Progress | Infrastructure | Database |
| Delayed Feature Deployment | Medium | Open | Operational | CI/CD |
| Customer Data Exposure Vulnerability | Critical | Mitigated | Compliance | Data Security |
| Server Overload During Peak Traffic | High | Monitoring | Infrastructure | Scalability |
| Third-Party API Downtime | Medium | Open | External | Dependency |
| Phishing Attack on Employees | High | In Progress | Security | Social Engineering |
| Payment Gateway Integration Failure | High | Open | Operational | Payments |

---

## 🧰 Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Web Framework | FastAPI | 0.138.0 |
| ASGI Server | Uvicorn | 0.49.0 |
| ORM | SQLAlchemy | 2.0.51 |
| Database | SQLite | built-in |
| Data Validation | Pydantic | 2.13.4 |
| Authentication | Python-JOSE (JWT) | 3.5.0 |
| Password Hashing | passlib + bcrypt | 1.7.4 / 4.0.1 |
| AI Framework | LangChain + LangGraph | 1.3.10 / 1.2.6 |
| Conversation Memory | LangGraph InMemorySaver | 4.1.1 |
| LLM Runtime | Ollama (`qwen3.5:4b`) | 0.6.2 |
| LLM Interface | LangChain-Ollama | 1.1.0 |
| MCP Server | FastMCP | 3.4.2 |
| MCP Client | LangChain-MCP-Adapters | 0.3.0 |
| Frontend | Streamlit | 1.58.0 |
| HTTP Client | HTTPX / Requests | 0.28.1 / 2.34.2 |
| Config | python-dotenv | 1.2.2 |

---

## 🔒 Security Notes

- All passwords are stored as **bcrypt hashes** — plain-text passwords are never persisted.
- JWT tokens expire in **30 minutes**. Expired tokens are rejected at every protected endpoint.
- The `SECRET_KEY` in `Authentication/jwttoken.py` is hardcoded for development convenience. **Generate a strong random key and move it to `.env` before any production use.**
- `.env` and `*.db` files are excluded from version control.
- MCP tool calls run in a subprocess that inherits the caller's JWT token — all AI-driven operations respect the same RBAC rules as direct API calls.
- Unauthorized access attempts are captured in the activity log as `WARNING` entries, including the attacker's email, role, and the endpoint they tried to reach.

---

## 🛠️ Development Notes

### Running with Auto-Reload

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Increasing RiskBot's Context Window

Edit `Chatbot/tool_binding.py`:

```python
ChatOllama(
    model="qwen3.5:4b",
    num_ctx=64000,    # default is 32768; increase for longer conversations
    temperature=0
)
```

### Switching the LLM Model

```python
ChatOllama(model="llama3.2:3b", ...)   # any model available in your Ollama install
```

### Persistent Conversation Memory

Currently `InMemorySaver` is used, which resets on server restart. To persist conversations across restarts, swap it for a disk-backed checkpointer (e.g. LangGraph's `SqliteSaver`):

```python
from langgraph.checkpoint.sqlite import SqliteSaver
memory = SqliteSaver.from_conn_string("checkpoints.db")
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: describe your change"`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 Sunil Choudhary

---

<div align="center">

**Advanced Risk Management System** · Built with FastAPI, LangChain, MCP & Ollama  
Summer Internship · Mentem Technologies Pvt. Ltd. · May 2026

</div>
