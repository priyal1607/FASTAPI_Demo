from fastapi import FastAPI , Path
from typing import Optional
from pydantic import BaseModel
import psycopg2
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow Next.js frontend to access the API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = psycopg2.connect(
    dbname="DemoDababase",
    user="postgres",
    password="1234",
    host="localhost"
)

cursor = conn.cursor()
def create_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id  SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        age INT NOT NULL
    );
    """)
    conn.commit()

create_table()  # Ensure the table exists when the app starts


student = []

class data(BaseModel) :
    name : str
    age : int

class dataupdate(BaseModel) :
    name : Optional[str] = None
    age : Optional[int] = None


@app.get("/")
def read_root():
    student = []
    cursor.execute("""
    SELECT * FROM students
     """)
    row = cursor.fetchall();
    for i in row:
        student.append(i)
    
    return student

@app.get("/studentdata/{id}")
def getData(id : int = Path(... ,description = "id you want to showd", gt = 0)):
    student = []
    cursor.execute("""
    SELECT * FROM students WHERE id = %s;
     """ , (id,))
    row = cursor.fetchall();
    for i in row:
        student.append(i)
    
    return student



@app.post("/adddata")
def addData(dt : data):
    cursor.execute("""
    INSERT INTO students (name, age)
    VALUES (%s, %s)
    """ , (dt.name , dt.age))
    conn.commit()
    
    return {"data add successfully"}
    
@app.put("/updatedata/{id}")
def updatedata(id : int , dt : dataupdate):
    cursor.execute("""
        UPDATE students SET name = %s , age = %s WHERE id = %s
    """ , (dt.name ,dt.age , id ) )
    conn.commit()
    return {"data update successfully"}

@app.delete("/delete/{id}")
def deleteData(id : int):
    cursor.execute("""
        DELETE FROM students WHERE id = %s;
    """ , (id , ))
    conn.commit()
    
    return {"student deleted successfully"}



