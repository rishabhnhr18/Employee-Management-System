# Employee Management System

A full-stack **Employee Management System** with a modern web UI built on a Flask REST API backed by SQLite.

---

## Features

- **Dashboard** – summary cards (total employees, departments, roles, genders)
- **Employee table** – sortable columns, live search/filter
- **Add / Edit / Delete** employees via modal forms with validation
- **Charts** – bar chart by department, pie chart by role, bar chart by gender (Chart.js)
- **Dark theme** responsive UI

---

## Tech Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Backend  | Python 3, Flask                   |
| Database | SQLite (`Employee.db`)            |
| Frontend | HTML / CSS / Vanilla JS, Chart.js |
| Container| Docker, Docker Compose            |

---

## Running Locally (Python)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
python app.py

# 3. Open browser
http://localhost:5000
```

---

## Running with Docker

```bash
# Build and start
docker compose up --build

# Open browser
http://localhost:5000
```

The SQLite database is persisted in a Docker named volume (`db_data`).

---

## API Endpoints

| Method | Path                   | Description                     |
|--------|------------------------|---------------------------------|
| GET    | `/api/employees`       | List all employees              |
| POST   | `/api/employees`       | Add a new employee              |
| PUT    | `/api/employees/<id>`  | Update an existing employee     |
| DELETE | `/api/employees/<id>`  | Delete an employee              |
| GET    | `/api/stats`           | Aggregated counts               |
| GET    | `/api/meta`            | Valid departments/roles/genders |

### Employee JSON shape

```json
{
  "id":         "EMP001",
  "name":       "Alice Smith",
  "department": "Software",
  "role":       "Developer",
  "gender":     "Female"
}
```

---

## Desktop GUI (original)

The original tkinter desktop application is still available in `lab.py`:

```bash
pip install customtkinter matplotlib
python lab.py
```
