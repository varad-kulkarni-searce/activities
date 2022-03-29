from fastapi import FastAPI
import uvicorn
from database import db

app = FastAPI()


@app.api_route('/student_access', methods=["GET"])
def student_db(student_id):
    return db.select(student_id)


# def add_student_to_list(student_count):
#     student_list = [(student_id_1, student_name_1, student_class_1, student_marks_1),
#                     (student_id_2, student_name_2, student_class_2, student_marks_2),
#                     ]
#     return student_list


@app.api_route('/student_add_multiple', methods=["POST"])
def add_multiple_students(student_id_1, student_name_1, student_class_1, student_marks_1, student_id_2, student_name_2,
                          student_class_2, student_marks_2):
    student_list = [(student_id_1, student_name_1, student_class_1, student_marks_1),
                    (student_id_2, student_name_2, student_class_2, student_marks_2),
                    ]
    return db.multipleadd(student_list)


@app.api_route('/student_access', methods=['POST'])
def add_student(student_id, student_name, student_class, student_marks):
    return db.write(student_id, student_name, student_class, student_marks)


@app.api_route('/student_access', methods=['DELETE'])
def delete_student(student_id):
    return db.delete(student_id)


@app.api_route('/student_access_all', methods=["GET"])
def all_student_db():
    return db.selectAll()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
