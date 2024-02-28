# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from fastapi import  FastAPI
from sqlalchemy import create_engine
from sqlalchemy.sql import text


def get_stds(pg_no):

    rows = []

    engine = create_engine('postgresql://postgres:Password123.@localhost:5432/postgres')

    stored_procedure = text(f"SELECT * FROM sp_get_students_list(p_pagenum=>({pg_no}::smallint))")
    with engine.connect() as connection:
        result = connection.execute(stored_procedure)

        for row in result:
            rows.append(dict(zip(result.keys(), row)))

        return  rows

def get_schools_list():

    rows = []
    stored_procedure = text(f"SELECT * FROM sp_get_school_list()")
    engine = create_engine('postgresql://postgres:Password123.@localhost:5432/postgres')
    with engine.connect() as connection:
        result = connection.execute(stored_procedure)

        for row in result:
            rows.append(dict(zip(result.keys(), row)))

        return  rows


app=FastAPI()

@app.get("/")
def root():
    return {"Hello":"aleena"}

@app.post("/post")
async def test_fun():
    return {"Test":"Return post"}

@app.get("/get_student/{pg_no}")
async def get_Students(pg_no):
    res = get_stds(pg_no)
    return res

@app.get("/get_school_list/")
async def get_school_list():
    res = get_schools_list()
    return res



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
