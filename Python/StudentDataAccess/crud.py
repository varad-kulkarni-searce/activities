import models
from sqlalchemy.orm import Session
import schema
from main import get_db


def get_student_details_by_student_id(db: Session, student_id: str):
    return db.query(models.Students).filter(models.Students.student_id == student_id).first()


def get_student_details(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Students).offset(skip).limit(limit).all()


def get_students_details_by_id(db: Session, sl_id: int):
    return db.query(models.Students).filter(models.Students.id == sl_id).first()


def add_students_details_to_db(db: Session, students: schema.StudentAdd):
    student_details = models.Students(
        student_id=students.student_id,
        student_name=students.student_name,
        student_class=students.student_class,
        student_marks=students.student_marks
    )
    db.add(student_details)
    db.commit()
    db.refresh(student_details)
    # return student_details
    return models.Students(students.dict())
