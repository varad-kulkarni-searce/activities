

from fastapi import FastAPI
import uvicorn
import sqlite3

app = FastAPI()

conn = sqlite3.connect('StudentsDatabase.db', check_same_thread=False)
c = conn.cursor()


# c.execute("""CREATE TABLE students (
#     student_id text,
#     student_name text,
#     student_class text,
#     student_marks integer
# )""")
# c.execute("Insert INTO students VALUES ('U100','Varad','10th', 90)")
# c.execute("Insert INTO students VALUES ('U200','Rohit','10th', 80)")

class Students:
    @app.get('/get_student_detail_by_id/{student_id}')
    def get_student_details_by_id(self, student_id):
        c.execute(f"SELECT * FROM students WHERE student_id=:student_id", {'student_id': student_id})
        return c.fetchall()

    @app.get('/get_students_data')
    def get_students_data(self):
        c.execute(f"SELECT * FROM students ORDER BY student_id")
        return c.fetchall()

    @app.post('/add_student/{student_id}/{student_name}/{student_class}/{student_marks}')
    def add_student(self, student_id, student_name, student_class, student_marks):
        c.execute(f"INSERT INTO students VALUES ('{student_id}', '{student_name}', '{student_class}', {student_marks})")
        return c.fetchall()

    @app.delete('/delete_student_by_id/{student_id}')
    def delete_student_by_id(self, student_id):
        c.execute(f"DELETE FROM students WHERE student_id=:student_id", {'student_id': student_id})
        return c.fetchall()

    #
    # @app.put('/update_details_by_student_id/{student_id}')
    # def update_details_by_student_id(student_id):
    #     c.execute(f"UPDATE students SET student_id = 'U200', student_name = 'Rohit', student_class = '10th', student_marks = 89 WHERE student_id =: student_id", {'student_id': student_id})
    #     return c.fetchall()

    #
    # @app.post('/add_multiple_students')
    # def add_multiple_students():
    #     student_list = [("U300", "Sachin", "10th", 99),
    #                     ("U400", "Virat", "10th", 89),
    #                     ]
    #     c.executemany(f"INSERT INTO students VALUES (?,?,?,?)", student_list)
    #     return c.fetchall()

    @app.post(
        '/add_multiple_students/{student_id_1}/{student_name_1}/{student_class_1}/{student_marks_1}/student_id_2}/{'
        'student_name_2}/{student_class_2}/{student_marks_2}')
    def add_multiple_students(self, student_id_1, student_name_1, student_class_1, student_marks_1, student_id_2,
                              student_name_2, student_class_2, student_marks_2):
        student_list = [(student_id_1, student_name_1, student_class_1, student_marks_1),
                        (student_id_2, student_name_2, student_class_2, student_marks_2),
                        ]
        c.executemany(f"INSERT INTO students VALUES (?,?,?,?)", student_list)
        return c.fetchall()


if __name__ == "__main__":
    student_obj = Students()
    student_obj.get_students_data()
    uvicorn.run("main:app", reload=True)
