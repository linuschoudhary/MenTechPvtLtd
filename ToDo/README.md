# 📝 FastAPI Todo List (CRUD Application)

A simple Todo List REST API built using **FastAPI**. This project demonstrates CRUD operations with a clean structure using database and schema separation.

---

## 🚀 Features

- Create a new todo
- Retrieve all todos
- Retrieve a single todo by ID
- Update an existing todo
- Delete a todo
- Automatic API documentation (Swagger & ReDoc)
- Beginner-friendly FastAPI project

---

## 🛠️ Tech Stack

- Python 🐍
- FastAPI ⚡
- Uvicorn 🔥
- SQLite 🗄️

---

## 📂 Project Structure

ToDo/
│
├── Database/
│   ├── sqlitebd.py        # Database connection & operations
│   ├── todolist.db        # SQLite database file
│
├── schema/
│   ├── todo_list_format.py # Pydantic models (validation)
├── main.py                # FastAPI entry point
├── requirements.txt
├── .gitignore
└── README.md

---

## ⚙️ Installation

### Clone the repository
git clone https://github.com/linuschoudhary/todofastapi.git
cd todofastapi

### Create virtual environment
python -m venv todo-env

### Activate virtual environment

Windows:
todo-env\Scripts\activate

Mac/Linux:
source todo-env/bin/activate

### Install dependencies
pip install -r requirements.txt

---

## ▶️ Run the Application

uvicorn main:app --reload

Server will run at:
http://127.0.0.1:8000

---

## 📘 API Documentation

Swagger UI:
http://127.0.0.1:8000/docs

ReDoc:
http://127.0.0.1:8000/redoc

---

## 📌 API Endpoints

| Method | Endpoint        | Description      |
|--------|----------------|------------------|
| GET    | /todos         | Get all todos    |
| GET    | /todos/{id}    | Get todo by id   |
| POST   | /todos         | Create todo      |
| PUT    | /todos/{id}    | Update todo      |
| DELETE | /todos/{id}    | Delete todo      |

---

## 📦 Example Request

{
  "title": "Learn FastAPI",
  "description": "Build a CRUD API",
  "completed": false
}

---

## 🔮 Future Improvements

- Add JWT authentication
- Use SQLAlchemy ORM
- Add Docker support
- Add frontend UI
- Deploy on cloud (Render/Railway/AWS)

---

## 👨‍💻 Author

Your Name  
GitHub: https://github.com/linuschoudhary
