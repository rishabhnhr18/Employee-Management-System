import sqlite3


def create_table():
    conn=sqlite3.connect('Employee.db')
    cursor=conn.cursor()
    
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS Employees(
                       id TEXT PRIMARY KEY,
                       name TEXT,
                       department TEXT,
                       role TEXT,
                       gender TEXT)'''      
                   )
    conn.commit()
    conn.close()
    
def fetch_employees():
    conn=sqlite3.connect('Employee.db')
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM Employees')
    employees=cursor.fetchall()
    conn.close()
    return  employees
    
def insert_employees(id, name, department, role, gender):
    conn=sqlite3.connect('Employee.db')
    cursor=conn.cursor()
    cursor.execute("INSERT INTO Employees(id, name, department, role, gender) VALUES(?, ?, ?, ?, ?)", (id, name, department, role, gender))
    conn.commit()
    conn.close()
    
def delete_employees(id):
    conn=sqlite3.connect('Employee.db')
    cursor=conn.cursor()
    cursor.execute("DELETE FROM Employees WHERE id=?", (id,))
    conn.commit()
    conn.close()
    
def update_employees(new_name, new_department, new_role, new_gender, id):
    conn=sqlite3.connect('Employee.db')
    cursor=conn.cursor()
    cursor.execute("UPDATE Employees SET name=?, department=?, role=?, gender=?  WHERE id = ?",(new_name, new_department, new_role, new_gender, id))
    conn.commit()
    conn.close()
    
    
def id_exists(id):
    conn=sqlite3.connect('Employee.db')
    cursor=conn.cursor()
    cursor.execute('SELECT COUNT (*) FROM Employees WHERE id = ? ', (id,))
    result=cursor.fetchone();
    conn.close()
    return result[0]>0

create_table()

