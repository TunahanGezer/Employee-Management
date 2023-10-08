import sqlite3

def create_table():
    conn=sqlite3.connect('employee.db')
    cursor=conn.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS employee(
                   id TEXT PRIMARY KEY,
                   name TEXT,
                   role TEXT,
                   gender TEXT,
                   status TEXT
                   date_of_birth TEXT)'''
                   )
    conn.commit()
    conn.close()

def get_employee_by_id(employee_id):
    try:
        connection=sqlite3.connect('employee.db')
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM employee WHERE id = ?", (employee_id,))
        employee = cursor.fetchone()
        if employee:
            return employee
        else:
            return None
    except sqlite3.Error as error:
        print("Veritaban hatasi",error)
        return None
    finally:
        if connection:
            connection.close()
            
def fetch_employees():
    conn=sqlite3.connect('employee.db')
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM employee')
    employee=cursor.fetchall()
    conn.close()
    return employee

def insert_employee(id, name, role, gender, status, date_of_birth):
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO employee (id, name, role, gender, status, date_of_birth) VALUES (?, ?, ?, ?, ?, ?)',
                   (id, name, role, gender, status, date_of_birth))
    conn.commit()
    conn.close()

def delete_employee(id):
    conn=sqlite3.connect('employee.db')
    cursor=conn.cursor()
    cursor.execute("DELETE FROM employee WHERE id=?",(id,))
    conn.commit()
    conn.close()

def update_employee(new_name,new_role,new_gender,new_status,new_date_of_birth,id):
    conn=sqlite3.connect('employee.db')
    cursor=conn.cursor()
    cursor.execute("UPDATE employee SET name=?,role=?,gender=?,status=?,date_of_birth=? WHERE id=?",
                   (new_name,new_role,new_gender,new_status,new_date_of_birth,id))
    conn.commit()
    conn.close()

def id_exists(id):
    conn=sqlite3.connect('employee.db')
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*)FROM employee WHERE id=?",
                   (id,))
    result=cursor.fetchone()
    conn.close()
    return result[0]>0

create_table()