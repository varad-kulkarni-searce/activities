from typing import Optional, List
from pydantic import BaseModel


# for data validation..

class StudentBase(BaseModel):
    student_name: str
    student_class: str
    student_marks: int


class StudentAdd(StudentBase):
    student_id: str

    class Config:
        orm_mode = True


class Student(StudentAdd):
    id: int

    class Config:
        orm_mode = True

#
# class MultipleStudentAdd(BaseModel):
#     students: List[StudentAdd]


class StudentUpdate(BaseModel):
    student_name: str
    student_class: str
    student_marks: int

    class Config:
        orm_mode = True
