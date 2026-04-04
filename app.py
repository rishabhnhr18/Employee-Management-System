import os
import re
import sqlite3

from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="static", static_url_path="")

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Employee.db")


def _connect():
    return sqlite3.connect(DB_PATH)


# Override database connections to use the absolute path
def fetch_employees():
    conn = _connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employees")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "department": r[2], "role": r[3], "gender": r[4]} for r in rows]


def insert_employee(emp_id, name, department, role, gender):
    conn = _connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Employees(id, name, department, role, gender) VALUES(?, ?, ?, ?, ?)",
        (emp_id, name, department, role, gender),
    )
    conn.commit()
    conn.close()


def update_employee(emp_id, name, department, role, gender):
    conn = _connect()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Employees SET name=?, department=?, role=?, gender=? WHERE id=?",
        (name, department, role, gender, emp_id),
    )
    conn.commit()
    conn.close()


def delete_employee(emp_id):
    conn = _connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Employees WHERE id=?", (emp_id,))
    conn.commit()
    conn.close()


def id_exists(emp_id):
    conn = _connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Employees WHERE id=?", (emp_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] > 0


def ensure_table():
    conn = _connect()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Employees(
            id TEXT PRIMARY KEY,
            name TEXT,
            department TEXT,
            role TEXT,
            gender TEXT)"""
    )
    conn.commit()
    conn.close()


ensure_table()

NAME_RE = re.compile(r"^[A-Za-z\s]+$")

DEPARTMENTS = ["Software", "Accounts & Finance", "HR", "Purchase & Sales", "Marketing", "Production & Logistics"]
ROLES = ["Manager", "Team Lead", "Head of Dept", "Officer", "Owner", "Director", "Clerk", "Developer", "Consultant"]
GENDERS = ["Male", "Female", "others"]


# ── Routes ──────────────────────────────────────────────────────────────────


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/employees", methods=["GET"])
def get_employees():
    return jsonify(fetch_employees())


@app.route("/api/employees", methods=["POST"])
def add_employee():
    data = request.get_json(force=True)
    emp_id = (data.get("id") or "").strip()
    name = (data.get("name") or "").strip()
    department = (data.get("department") or "").strip()
    role = (data.get("role") or "").strip()
    gender = (data.get("gender") or "").strip()

    if not all([emp_id, name, department, role, gender]):
        return jsonify({"error": "All fields are required"}), 400
    if not NAME_RE.match(name):
        return jsonify({"error": "Name should only contain alphabets"}), 400
    if department not in DEPARTMENTS:
        return jsonify({"error": "Invalid department"}), 400
    if role not in ROLES:
        return jsonify({"error": "Invalid role"}), 400
    if gender not in GENDERS:
        return jsonify({"error": "Invalid gender"}), 400
    if id_exists(emp_id):
        return jsonify({"error": "Employee ID already exists"}), 409

    insert_employee(emp_id, name, department, role, gender)
    return jsonify({"message": "Employee added successfully"}), 201


@app.route("/api/employees/<emp_id>", methods=["PUT"])
def update_employee_route(emp_id):
    if not id_exists(emp_id):
        return jsonify({"error": "Employee not found"}), 404

    data = request.get_json(force=True)
    name = (data.get("name") or "").strip()
    department = (data.get("department") or "").strip()
    role = (data.get("role") or "").strip()
    gender = (data.get("gender") or "").strip()

    if not all([name, department, role, gender]):
        return jsonify({"error": "All fields are required"}), 400
    if not NAME_RE.match(name):
        return jsonify({"error": "Name should only contain alphabets"}), 400
    if department not in DEPARTMENTS:
        return jsonify({"error": "Invalid department"}), 400
    if role not in ROLES:
        return jsonify({"error": "Invalid role"}), 400
    if gender not in GENDERS:
        return jsonify({"error": "Invalid gender"}), 400

    update_employee(emp_id, name, department, role, gender)
    return jsonify({"message": "Employee updated successfully"})


@app.route("/api/employees/<emp_id>", methods=["DELETE"])
def delete_employee_route(emp_id):
    if not id_exists(emp_id):
        return jsonify({"error": "Employee not found"}), 404
    delete_employee(emp_id)
    return jsonify({"message": "Employee deleted successfully"})


@app.route("/api/stats", methods=["GET"])
def get_stats():
    employees = fetch_employees()
    dept_count: dict = {}
    role_count: dict = {}
    gender_count: dict = {}

    for emp in employees:
        dept_count[emp["department"]] = dept_count.get(emp["department"], 0) + 1
        role_count[emp["role"]] = role_count.get(emp["role"], 0) + 1
        gender_count[emp["gender"]] = gender_count.get(emp["gender"], 0) + 1

    return jsonify(
        {
            "total": len(employees),
            "departments": dept_count,
            "roles": role_count,
            "genders": gender_count,
        }
    )


@app.route("/api/meta", methods=["GET"])
def get_meta():
    return jsonify({"departments": DEPARTMENTS, "roles": ROLES, "genders": GENDERS})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
