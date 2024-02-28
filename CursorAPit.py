import psycopg2
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


# Establish a connection to the database
conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="Password123.",
    host="localhost",
    port="5432"
)

app = FastAPI()

#CORS origins list
origins = ["*"]

#configuring CORS
cors_options={
    "allow_origins": origins,
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}
#Adding the CORS Middleware
app.add_middleware(
    CORSMiddleware,
    **cors_options
)
#EndPoint to get School list
@app.get("/Get_school_list/")
def Get_School_list_json():
    try:

            cur = conn.cursor()
            cur.execute(f"select school_list_json();")
            results = cur.fetchone()
            cur.close()
            conn.commit()
            return results[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching school info")

#EndPoint to get students' list by page_no
@app.get("/getStudent_list/{pg_no}")
def Get_Student_List_Page_no(pg_no):
    try:
        cur = conn.cursor()
        cur.execute(f"select Students_List({pg_no} :: smallint)")
        results = cur.fetchone()
        cur.close()
        conn.commit()
        if (results[0] != None):
            return results[0]
        else:
            return {"No records..."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching Student info")



#Creating a Student class
class Student(BaseModel):
    name: str="NULL"
    id: int=1
    age: str="NULL"
    gender: str="NULL"

#Endpoint to update student details
@app.put("/Update_Students/")
def Update_Student_obj(student: Student):
    try:
        cur = conn.cursor()
        if (student.age != "NULL"):
            age_ = int(student.age)
            if (age_) > 60 or int(age_) < 0:
                return {"Status": "Updation Failed.. invalid age"}

        if (student.name == ""):
            student.name = "NULL"
        else:
            student.name = f"'{student.name}'"
        if (student.gender == ""):
            student.gender = "NULL"
        else:
            student.gender = f"'{student.gender}'"
        print(
            f"call sp_put_student_details(({student.id} :: smallint),({student.name}::character varying),({student.age}::smallint),({student.gender}::character));")
        cur.execute(
            f"select sp_update_student(({student.id} :: smallint),({student.name}::character varying),({student.age}::smallint),({student.gender}::character))")
        result = cur.fetchone()

        conn.commit()
        if result[0]:
            return {"Status": "Successfully Updated"}
        else:
            return {"Status": "Updation Failed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while updating Student info")


#Creating a User class
class Users(BaseModel):
    uname: str="NULL"
    password: str="NULL"

#Endpoint to validate login
@app.post("/Login/")
def User_Login(user:Users):
    try:
        cur = conn.cursor()
        cur.execute(f"select verify_User('{user.uname}','{user.password}')")
        res = cur.fetchone();
        if res[0]:
            return {"Status": "Login Successful"}
        else:
            return {"Status": "Login Failed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while Login")


#Endpoint to get scheduled exam per subject
@app.get("/Get_Exam_Scheduled_by_Sub")
def Get_Exam_Scheduled_by_Sub():
    try:
        cur = conn.cursor()
        cur.execute("select Get_ExamSched_Sub()")
        results = cur.fetchone()
        cur.close()
        conn.commit()
        return results[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching Scheduled exams info")


#Endpoint to get assessment count
@app.get("/Get_Assessment_Count")
def Get_Exam_Scheduled_by_Sub():
    try:
        cur = conn.cursor()
        cur.execute("select get_assessment_count()")
        results = cur.fetchone()
        cur.close()
        conn.commit()
        return results[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching Assessment info")


#Endpoint to get average score per subject
@app.get("/Avg_Score_Subject")
def Avg_Score_Subject():
    try:
        cur = conn.cursor()
        cur.execute("select avg_score_subject()")
        results = cur.fetchone()
        cur.close()
        conn.commit()
        return results[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching Average score info")


#Endpoint to get grade count per subject
@app.get("/Get_Grade_Subject")
def Get_Grade_Subject():
    try:
        cur = conn.cursor()
        cur.execute("select Get_Grade_Subject();")
        results = cur.fetchone()
        cur.close()
        conn.commit()
        return results[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching Grade Subject info")


##############################################################################################################################################