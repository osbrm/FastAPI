from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2

app = FastAPI()

# Establish a connection to the database
conn = psycopg2.connect(
    host="localhost",
    database="your_database",
    user="your_user",
    password="your_password"
)

# Define a function to get the count of students
def get_student_count():
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM students")
    result = cur.fetchone()
    cur.close()
    conn.commit()
    return result[0]

# Define a function to get a student by id
def get_student_by_id(id: int):
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE id = %s", (id,))
    result = cur.fetchone()
    cur.close()
    conn.commit()
    if result is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return result

# Define a function to update a student
def update_student(id: int, name: str = None, age: int = None, gender: str = None):
    cur = conn.cursor()
    if age and (age > 60 or age < 0):
        return {"Status": "Updation Failed.. invalid age"}
    cur.execute("UPDATE students SET name = %s, age = %s, gender = %s WHERE id = %s", (name, age, gender, id))
    conn.commit()
    cur.close()
    return {"Status": "Successfully Updated"}

# Define a class for student data
class Student(BaseModel):
    name: str = "NULL"
    id: int = 1
    age: int = 0
    gender: str = "NULL"

# Define a function to update a student using an object
def update_student_obj(student: Student):
    cur = conn.cursor()
    age_ = int(student.age)
    if age_ > 60 or age_ < 0:
        return {"Status": "Updation Failed.. invalid age"}
    cur.execute("UPDATE students SET name = %s, age = %s, gender = %s WHERE id = %s", (student.name, student.age, student.gender, student.id))
    conn.commit()
    cur.close()
    return {"Status": "Successfully Updated"}

# Define a class for user data
class Users(BaseModel):
    uname: str = "NULL"
    password: str = "NULL"

# Define a function to authenticate a user
def authenticate_user(uname: str, password: str):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE uname = %s AND password = %s", (uname, password))
    result = cur.fetchone()
    cur.close()
    conn.commit()
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return result

# Define the routes for the API
@app.get("/Get_Student_Count/")
def get_student_count_route():
    return get_student_count()

@app.get("/Get_Student_by_id/{id}")
def get_student_by_id_route(id: int):
    return get_student_by_id(id)

@app.put("/Update_Student/")
def update_student_route(id: int, name: str = None, age: int = None, gender: str = None):
    return update_student(id, name, age, gender)

@app.put("/Update_Students/")
def update_student_obj_route(student: Student):
    return update_student_obj(student)

@app.post("/Login/")
def user_login_route(user: Users):
    return authenticate_user(user.uname, user.password)

@app.get("/Get_Exam_Scheduled_by_Sub")
def get_exam_scheduled_by_sub_route():
    return get_ex