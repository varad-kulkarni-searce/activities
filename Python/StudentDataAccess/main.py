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


class Students:

    # Retrieve details of all the students:
    @app.get('/retrieve_all_students_details', response_model=List[schema.Student])
    def retrieve_all_students_details(self, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
        all_students = crud.get_student_details(db=db, skip=skip, limit=limit)
        print(all_students)
        return all_students

    # Add new student in the database:
    @app.post('/add_student', response_model=schema.StudentAdd)
    def add_student(self, student: schema.StudentAdd, db: Session = Depends(get_db)):
        student_id = crud.get_student_details_by_student_id(db=db, student_id=student.student_id)
        if student_id:
            raise HTTPException(status_code=400,
                                detail=f"Movie id {student.student_id} already exist in database: {student_id}")
        return crud.add_students_details_to_db(db=db, students=student)

    # Add multiple new student in the database:
    # @app.post('/add_multiple_students', response_model=schema.StudentAdd)
    # def add_multiple_students(self, count: int, student: schema.MultipleStudentAdd, db: Session = Depends(get_db)):
    #     for i in range(count):
    #         student_id = crud.get_student_details_by_student_id(db=db, student_id=student.student_id)
    #         if student_id:
    #             raise HTTPException(status_code=400,
    #                                 detail=f"Movie id {student.student_id} already exist in database: {student_id}")
    #         return crud.add_multiple_students_details_to_db(db=db, students=student)

    # Retrieve student details using the student id of that specific student:
    @app.put('/get_student_details_by_student_id', response_model=schema.Student)
    def get_student_details_by_student_id(self, student_id: str, db: Session = Depends(get_db)):
        details = crud.get_student_details_by_student_id(db=db, student_id=student_id)
        if not details:
            raise HTTPException(status_code=404, detail=f"No record found to update")

        return crud.get_student_details_by_student_id(db=db, student_id=student_id)

    # Delete student details from the database using the id:
    @app.delete('/delete_student_by_id')
    def delete_student_by_id(self, sl_id: int, db: Session = Depends(get_db)):
        details = crud.get_students_details_by_id(db=db, sl_id=sl_id)
        if not details:
            raise HTTPException(status_code=404, detail=f"No record found to delete")

        try:
            crud.delete_student_details_by_id(db=db, sl_id=sl_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Unable to delete: {e}")
        return {"delete status": "success"}

    # Delete student details from the database using the student id
    @ app.delete('/delete_student_by_student_id')
    def delete_student_by_student_id(self, student_id: str, db: Session = Depends(get_db)):
        details = crud.get_student_details_by_student_id(db=db, student_id=student_id)
        if not details:
            raise HTTPException(status_code=404, detail=f"No record found to delete")

        try:
            crud.delete_student_details_by_student_id(db=db, student_id=student_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Unable to delete: {e}")
        return {"delete status": "success"}

    # Update the student details using the id:
    @app.put('/update_student_details_by_id', response_model=schema.StudentUpdate)
    def update_movie_details_by_id(self, sl_id: int, update_param: schema.StudentUpdate, db: Session = Depends(get_db)):
        details = crud.get_students_details_by_id(db=db, sl_id=sl_id)
        if not details:
            raise HTTPException(status_code=404, detail=f"No record found to update")

        return crud.update_movie_details_by_id(db=db, details=update_param, sl_id=sl_id)

    # Update the student details using the student id:
    @app.put('/update_student_details_by_student_id', response_model=schema.StudentUpdate)
    def update_movie_details_by_student_id(self, student_id: str, update_param: schema.StudentUpdate, db: Session = Depends(get_db)):
        details = crud.get_student_details_by_student_id(db=db, student_id=student_id)
        if not details:
            raise HTTPException(status_code=404, detail=f"No record found to update")

        return crud.update_movie_details_by_student_id(db=db, details=update_param, student_id=student_id)


if __name__ == '__main__':
    student_obj = Students()        # initialising object "student_obj" of "Students()" class.
    student_obj.add_student()
    student_obj.retrieve_all_students_details()
    student_obj.get_student_details_by_student_id()
    student_obj.delete_student_by_id()
    student_obj.delete_student_by_student_id()
    student_obj.update_movie_details_by_id()
    student_obj.update_movie_details_by_student_id()

    uvicorn.run("main:app", reload=True)
