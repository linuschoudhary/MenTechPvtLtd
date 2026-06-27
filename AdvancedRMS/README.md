# 🛡️ Advanced Risk Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.138.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1.3.10-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black?style=for-the-badge)
![MCP](https://img.shields.io/badge/MCP-FastMCP_3.4.2-6C4BFF?style=for-the-badge)

**An AI-powered risk management platform built with FastAPI, LangChain, MCP, and a local LLM via Ollama.**

*Developed during Summer Internship at Mentem Technologies Pvt. Ltd. — May 2026*

[Features](#-features) · [Tech Stack](#-tech-stack) · [Architecture](#-system-architecture) · [Setup](#-setup--installation) · [API Reference](#-api-reference) · [Chatbot](#-ai-chatbot)

</div>

---

## 📌 Overview

The **Advanced Risk Management System (ARMS)** is a full-stack backend application that enables organisations to identify, track, assign, and mitigate risks — all through a secure REST API. What sets it apart is an **AI-powered chatbot** that can perform full CRUD operations on risks and users using natural language, powered by a local LLM (Ollama) bridged to the FastAPI backend via the **Model Context Protocol (MCP)**.

The system enforces **role-based access control (RBAC)** with three hierarchical roles — Admin, Manager, and Employee — ensuring that each user can only access what they're authorised for.

> **Created by:** Sunil Choudhary  
> **Date:** 25 May 2026  
> **Organisation:** Mentem Technologies Pvt. Ltd. (Summer Internship)

---

## ✨ Features

- 🔐 **JWT Authentication** — Secure login with OAuth2 password flow and token-based session management
- 👥 **Role-Based Access Control** — Three-tier permission system (Admin → Manager → Employee)
- 📋 **Complete Risk Management** — Create, read, update, and delete risks with detailed metadata
- 👤 **User Management** — Full CRUD operations for managing system users
- 🤖 **AI Chatbot** — Natural language interface powered by a local LLM (Ollama `qwen3.5:4b`) that can interact with the entire system
- 🔧 **MCP Integration** — FastAPI routes are exposed as LLM tools via the Model Context Protocol (FastMCP)
- 🎨 **Streamlit Frontend** — A clean chat UI for interacting with the AI assistant
- 🔒 **bcrypt Password Hashing** — Secure password storage with passlib
- 📦 **SQLite Database** — Lightweight, file-based persistence via SQLAlchemy ORM
- 🗂️ **Default Data Seeding** — Quick-start endpoint to populate the database with sample users and risks
- 📄 **Auto-generated API Docs** — Interactive Swagger UI at `/docs` (provided by FastAPI)

---

## 🧰 Tech Stack

| Layer | Technology | Version |
|---|---|---|
| **Web Framework** | FastAPI | 0.138.0 |
| **ASGI Server** | Uvicorn | 0.49.0 |
| **ORM** | SQLAlchemy | 2.0.51 |
| **Database** | SQLite | Built-in |
| **Data Validation** | Pydantic | 2.13.4 |
| **Authentication** | Python-JOSE (JWT) | 3.5.0 |
| **Password Hashing** | passlib + bcrypt | 1.7.4 / 4.0.1 |
| **AI Framework** | LangChain + LangGraph | 1.3.10 / 1.2.6 |
| **LLM Backend** | Ollama (`qwen3.5:4b`) | 0.6.2 |
| **LLM Interface** | LangChain-Ollama | 1.1.0 |
| **MCP Server** | FastMCP | 3.4.2 |
| **MCP Client** | LangChain-MCP-Adapters | 0.3.0 |
| **Frontend** | Streamlit | 1.58.0 |
| **HTTP Client** | HTTPX / Requests | 0.28.1 / 2.34.2 |
| **Config** | python-dotenv | 1.2.2 |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      CLIENT LAYER                                   │
│   Streamlit UI (app.py)          External API Clients / Swagger     │
└──────────────────────┬──────────────────────┬───────────────────────┘
                       │ HTTP Requests         │ HTTP Requests
                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     FastAPI Application (main.py)                   │
│                                                                     │
│  ┌────────────────┐  ┌──────────────┐  ┌────────────┐  ┌────────┐  │
│  │  /risk Router  │  │  /user Router│  │  /chatbot  │  │ /login │  │
│  │  (risks.py)    │  │  (users.py)  │  │  Router    │  │ Router │  │
│  └───────┬────────┘  └──────┬───────┘  └─────┬──────┘  └───┬────┘  │
│          │                  │                 │             │       │
│  ┌───────▼──────────────────▼─────────────────▼─────────────▼────┐  │
│  │               Authentication Middleware                        │  │
│  │    JWT Verification  +  Role-Based Access Control (RBAC)      │  │
│  └───────────────────────────────────────────────────────────────┘  │
│          │                  │                 │                      │
│  ┌───────▼──────────────────▼─────────┐  ┌───▼──────────────────┐   │
│  │        Database Layer              │  │   Chatbot Engine     │   │
│  │  SQLAlchemy ORM + SQLite           │  │  (chatbot.py)        │   │
│  │  (User & Risk models)              │  └────────┬─────────────┘   │
│  └────────────────────────────────────┘           │                 │
└──────────────────────────────────────────────────┼─────────────────┘
                                                   │
                                     ┌─────────────▼─────────────┐
                                     │        MCP Layer           │
                                     │   FastMCP (mcpserver.py)   │
                                     │   Exposes FastAPI routes   │
                                     │   as LLM-callable tools    │
                                     └─────────────┬─────────────┘
                                                   │ stdio transport
                                     ┌─────────────▼─────────────┐
                                     │     LangChain Agent        │
                                     │  (tool_binding.py)         │
                                     │  Ollama LLM: qwen3.5:4b    │
                                     └───────────────────────────┘
```

### Data Flow — AI Chatbot Request

```
User Message (Streamlit)
        │
        ▼
POST /chatbot  (with Bearer token)
        │
        ▼
Chatbot Router extracts JWT token
        │
        ▼
LangChain Agent is built with Ollama LLM
        │
        ▼
MultiServerMCPClient connects to FastMCP subprocess
        │  (injects JWT token via env variable)
        ▼
LLM decides which MCP tool(s) to call
        │
        ▼
FastMCP calls the corresponding FastAPI endpoint
        │
        ▼
FastAPI processes the request (RBAC-validated)
        │
        ▼
Response bubbles back to the user
```

---

## 📁 Project Structure

```
FinalProject/
├── main.py                    # FastAPI app entry point
├── default.py                 # Default users & risks seed data
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (not committed)
├── .gitignore
│
├── Authentication/            # Auth logic
│   ├── jwttoken.py            # JWT creation and verification
│   ├── oauth2.py              # OAuth2 bearer scheme
│   └── role_based_access.py   # RBAC — level_1, level_2, level_3
│
├── Chatbot/                   # AI Chatbot components
│   ├── chatbot.py             # LangChain agent runner
│   ├── tool_binding.py        # MCP client + agent builder
│   └── app.py                 # Streamlit frontend
│
├── Database/                  # Database layer
│   ├── database.py            # SQLAlchemy engine + session
│   ├── model.py               # ORM models: User, Risk
│   ├── users.py               # User CRUD operations
│   ├── risks.py               # Risk CRUD operations
│   └── RMSDB.db               # SQLite database file (git-ignored)
│
├── Hashing/
│   └── hashing.py             # bcrypt password hashing
│
├── MCP/
│   └── mcpserver.py           # FastMCP server (wraps FastAPI as tools)
│
├── Routers/                   # FastAPI route handlers
│   ├── authenticate.py        # /login endpoint
│   ├── users.py               # /user/* endpoints
│   ├── risks.py               # /risk/* endpoints
│   └── chatbot.py             # /chatbot endpoint
│
└── Schema/
    └── schema.py              # Pydantic models for request/response
```

---

## 👤 Role-Based Access Control

The system has three user roles with hierarchical permissions:

| Role | Level | Access |
|---|---|---|
| `Admin` | level_1, level_2, level_3 | Full access to all endpoints including exclusive Admin routes |
| `Manager` | level_2, level_3 | Risk management endpoints + Chatbot |
| `Employee` | level_3 | Chatbot only |

```
level_1 = ['Admin']                    →  /user/ (list all users)
level_2 = ['Admin', 'Manager']         →  All /risk/* endpoints
level_3 = ['Admin', 'Manager', 'Employee']  →  /chatbot
```

---

## 🗃️ Database Schema

### `user` table

| Column | Type | Description |
|---|---|---|
| `user_id` | INTEGER (PK) | Auto-incremented primary key |
| `user_name` | STRING | Full name of the user |
| `user_role` | STRING | `Admin`, `Manager`, or `Employee` |
| `user_email` | STRING | Used as the login username |
| `user_password` | STRING | bcrypt-hashed password |

### `risks` table

| Column | Type | Description |
|---|---|---|
| `risk_id` | INTEGER (PK) | Auto-incremented primary key |
| `risk_title` | STRING | Short title of the risk |
| `risk_description` | STRING | Detailed description |
| `risk_priority` | STRING | `Critical`, `High`, `Medium`, or `Low` |
| `risk_status` | STRING | `Open`, `In Progress`, `Mitigated`, or `Monitoring` |
| `risk_type` | STRING | `Security`, `Infrastructure`, `Operational`, `Compliance`, `External` |
| `risk_category` | STRING | Sub-category (e.g. `Authentication`, `Database`, `CI/CD`) |
| `created_by` | INTEGER (FK) | User who created the risk |
| `risk_allocation` | INTEGER (FK) | User (Manager) the risk is allocated to |
| `assigned_to` | INTEGER (FK) | User (Employee) the risk is assigned to |
| `due_date` | STRING | Target resolution date (`YYYY-MM-DD`) |

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com/) installed and running locally
- `qwen3.5:4b` model pulled in Ollama

### 1. Clone the Repository

```bash
git clone https://github.com/linuschoudhary/AdvancedRiskManagementSystem.git
cd AdvancedRiskManagementSystem
```

### 2. Create and Activate a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Pull the LLM Model via Ollama

Make sure Ollama is running, then pull the model:

```bash
ollama pull qwen3.5:4b
```

> You can also use a different Ollama model by editing `Chatbot/tool_binding.py` and changing the `model` field in `ChatOllama(...)`.

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **Note:** A default `SECRET_KEY` is already hardcoded in `Authentication/jwttoken.py` for development. Replace it with a strong, randomly-generated key before deploying to production.

### 6. Start the FastAPI Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.  
Interactive API docs: `http://127.0.0.1:8000/docs`

### 7. Seed Default Data (Optional)

Visit the following endpoint once to populate sample users and risks:

```
GET http://127.0.0.1:8000/default
```

Or via curl:

```bash
curl http://127.0.0.1:8000/default
```

### 8. Launch the Streamlit Chatbot Frontend (Optional)

In a separate terminal (with the virtual environment active):

```bash
streamlit run Chatbot/app.py
```

The Streamlit app will open at `http://localhost:8501`.

---

## 📡 API Reference

### Authentication

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/login` | None | Login with email and password; returns a JWT token |

**Login request body** (form data):
```
username = user_email
password = user_password
```

**Login response:**
```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

> All protected endpoints require the header:  
> `Authorization: Bearer <access_token>`

---

### Introduction

| Method | Endpoint | Auth | Role | Description |
|---|---|---|---|---|
| `GET` | `/` | None | Public | System introduction and metadata |
| `GET` | `/default` | None | Public | Seed default users and risks into the database |

---

### Users — `/user`

| Method | Endpoint | Auth | Role | Description |
|---|---|---|---|---|
| `GET` | `/user/` | ✅ | Admin only | Get a list of all users |
| `GET` | `/user/show_by_id?user_id={id}` | ✅ | Any | Get a specific user by ID |
| `POST` | `/user/add_user` | ✅ | Any | Add a new user |
| `PUT` | `/user/update_user?user_id={id}` | ✅ | Any | Update user details (partial update supported) |
| `DELETE` | `/user/delete_user?user_id={id}` | ✅ | Any | Delete a user by ID |

**Add/Update User Schema:**
```json
{
  "user_name": "John Doe",
  "user_role": "Employee",
  "user_email": "john@example.com",
  "user_password": "securepassword"
}
```

---

### Risks — `/risk`

| Method | Endpoint | Auth | Role | Description |
|---|---|---|---|---|
| `GET` | `/risk` | ✅ | Admin, Manager | Get all risks with full user details |
| `GET` | `/risk/id?risk_id={id}` | ✅ | Admin, Manager | Get a specific risk by ID |
| `POST` | `/risk/add_risk` | ✅ | Admin, Manager | Add a new risk |
| `POST` | `/risk/update_risk?risk_id={id}` | ✅ | Admin, Manager | Update an existing risk (partial update supported) |
| `POST` | `/risk/delete_risk?risk_id={id}` | ✅ | Admin, Manager | Delete a risk by ID |

**Add Risk Schema:**
```json
{
  "risk_title": "Server Outage Risk",
  "risk_description": "Primary database server may go offline during peak load.",
  "risk_priority": "Critical",
  "risk_status": "Open",
  "risk_type": "Infrastructure",
  "risk_category": "Scalability",
  "created_by": 1,
  "risk_allocation": 2,
  "assigned_to": 3,
  "due_date": "2026-07-01"
}
```

**Risk Priority values:** `Critical` | `High` | `Medium` | `Low`  
**Risk Status values:** `Open` | `In Progress` | `Mitigated` | `Monitoring`

---

### Chatbot — `/chatbot`

| Method | Endpoint | Auth | Role | Description |
|---|---|---|---|---|
| `POST` | `/chatbot?message={text}` | ✅ | Admin, Manager, Employee | Send a message to the AI assistant |

**Example request:**
```bash
curl -X POST "http://127.0.0.1:8000/chatbot?message=Show%20me%20all%20open%20risks" \
  -H "Authorization: Bearer <your_token>"
```

---

## 🤖 AI Chatbot

### How It Works

The chatbot is the most powerful feature of this system. Here's what happens under the hood when you send a message:

1. **Your message** hits the `/chatbot` FastAPI endpoint along with your JWT token.
2. The endpoint calls `chatbot.py`, which builds a **LangChain agent** with an **Ollama LLM** (`qwen3.5:4b`).
3. A **`MultiServerMCPClient`** spawns the **FastMCP server** (`MCP/mcpserver.py`) as a subprocess via stdio transport.
4. FastMCP wraps the entire FastAPI app and exposes every route as an **MCP tool** with docstrings as tool descriptions.
5. The JWT token is injected into the subprocess environment so MCP tool calls are authenticated automatically.
6. The LangChain agent reads your message, picks the appropriate tool(s), calls them, and returns a natural language response.

### What the Chatbot Can Do

The AI assistant can perform **any operation** that the underlying API supports, including:

- "Show me all risks currently Open"
- "What risks are assigned to Dipesh Soni?"
- "Add a new High priority security risk for the payment gateway"
- "Update the status of risk ID 3 to Mitigated"
- "Delete risk number 7"
- "List all users with the Manager role"
- "Who created the most risks?"

### Chatbot Rules

The LLM is instructed to:
- Only answer risk management related questions
- Always use tools when data is needed (never hallucinate)
- Preserve exact spelling of names and values provided by the user
- Apply user-requested filters itself after fetching data
- Be aware of the current date and time for deadline-related queries

### Streamlit Frontend

The `Chatbot/app.py` provides a simple chat interface:

- **Sidebar login** — authenticates against the FastAPI `/login` endpoint and stores the JWT token in session state
- **Chat input** — sends messages to the `/chatbot` endpoint with the stored Bearer token
- **Chat history** — displays the conversation in a familiar chat bubble format

To launch:
```bash
streamlit run Chatbot/app.py
```

---

## 🌱 Default Data

Running `GET /default` seeds the following data:

### Default Users

| ID | Name | Role | Email | Password |
|---|---|---|---|---|
| 1 | YZA | Employee | YZA@gmail.com | YZA123 |
| 2 | XYZ | Manager | XYZ@gmail.com | XYZ123 |
| 3 | ABC | Manager | ABC@gmail.com | ABC123 |
| 4 | BCD | Employee | BCD@gmail.com | BCD123 |
| 5 | CDE | Admin | CDE@gmail.com | CDE123 |
| 6 | Sunil Choudhary | Admin | sunil@gmail.com | sunil123 |
| 7 | DEF | Employee | DEF@gmail.com | DEF123 |
| 8 | EFG | Employee | EFG@gmail.com | EFG123 |

### Default Risks (Sample)

| Title | Priority | Status | Type |
|---|---|---|---|
| Admin Panel Unauthorized Access Attempt | High | Open | Security |
| Backup System Failure Risk | Critical | In Progress | Infrastructure |
| Delayed Feature Deployment | Medium | Open | Operational |
| Customer Data Exposure Vulnerability | Critical | Mitigated | Compliance |
| Server Overload During Peak Traffic | High | Monitoring | Infrastructure |
| Third-Party API Downtime | Medium | Open | External |
| Phishing Attack on Employees | High | In Progress | Security |
| Payment Gateway Integration Failure | High | Open | Operational |

---

## 🔒 Security Notes

- All passwords are hashed using **bcrypt** before being stored in the database.
- JWT tokens expire after **30 minutes** by default.
- The `SECRET_KEY` in `Authentication/jwttoken.py` is hardcoded for development convenience. **Replace it with a strong secret before any production deployment.**
- The `.env` file and database (`.db`) are excluded from version control via `.gitignore`.
- MCP tool calls inherit the user's JWT token from the environment, ensuring that all AI-driven operations respect the same RBAC rules as direct API calls.

---

## 🛠️ Development Notes

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Accessing the Interactive API Docs

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

### Adjusting the LLM Context Window

In `Chatbot/tool_binding.py`, the LLM context size is set to 32,768 tokens. For more complex multi-step queries, you can increase it:

```python
ChatOllama(
    model="qwen3.5:4b",
    num_ctx=64000,   # increase for larger context
    temperature=0
)
```

### Using a Different Ollama Model

Replace the model name in `Chatbot/tool_binding.py`:

```python
ChatOllama(model="llama3.2:3b", ...)   # example alternative
```

---

## 📦 Key Dependencies

```
fastapi==0.138.0
uvicorn==0.49.0
sqlalchemy==2.0.51
pydantic==2.13.4
python-jose==3.5.0
passlib==1.7.4
bcrypt==4.0.1
python-dotenv==1.2.2
langchain==1.3.10
langgraph==1.2.6
langchain-ollama==1.1.0
langchain-mcp-adapters==0.3.0
fastmcp==3.4.2
mcp==1.28.0
ollama==0.6.2
streamlit==1.58.0
httpx==0.28.1
requests==2.34.2
```

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve the project:

1. Fork the repository
2. Create a new feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## 📄 License

This project was developed as part of a summer internship at **Mentem Technologies Pvt. Ltd.** and is intended for educational and organisational use.

---

## 👨‍💻 Author

**Sunil Choudhary**  
Summer Intern — Mentem Technologies Pvt. Ltd.  
📅 MAY-JUNE 2026

---

<div align="center">
  <i>Built with HATE💔 using my BRAIN🧠</i>
</div>
