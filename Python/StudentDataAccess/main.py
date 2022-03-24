from email.policy import HTTP

from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from typing import List
import models, crud, schema
from database import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


app = FastAPI()



# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/retrieve_all_students_details', response_model=List[schema.Student])
def retrieve_all_students_details(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    all_students = crud.get_student_details(db=db, skip=skip, limit=limit)
    print(all_students)
    return all_students


@app.post('/add_student', response_model=schema.StudentAdd)
def add_student(student: schema.StudentAdd, db: Session = Depends(get_db)):
    student_id = crud.get_student_details_by_student_id(db=db, student_id=student.student_id)
    if student_id:
        raise HTTPException(status_code=400,
                            detail=f"Movie id {student.student_id} already exist in database: {student_id}")
    return crud.add_students_details_to_db(db=db, students=student)


@app.put('/get_student_details_by_student_id', response_model=schema.Student)
def get_student_details_by_student_id(student_id: str, db: Session = Depends(get_db)):
    details = crud.get_student_details_by_student_id(db=db, student_id=student_id)
    if not details:
        raise HTTPException(status_code=404, detail=f"No record found to update")

    return crud.get_student_details_by_student_id(db=db, student_id=student_id)
# @app.get("/student/{student_id}")
# def studentDetails(student_id : int):
#     return{"Student Id": student_id,
#            "Student Name": "",
#            "Class": "",
#            "Marks": ""}

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
