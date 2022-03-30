import sqlite3

conn = sqlite3.connect('StudentsDatabase.db', check_same_thread=False)
c = conn.cursor()


# c.execute("""CREATE TABLE students (
#     student_id text,
#     student_name text,
#     student_class text,
#     student_marks integer
# )""")

class SQLiteConnector:

    @staticmethod
    def select_all():
        c.execute(f"SELECT * FROM students ORDER BY student_id")
        return c.fetchall()

    @staticmethod
    def select(student_id):
        c.execute(f"SELECT * FROM students WHERE student_id=:student_id", {'student_id': student_id})
        return c.fetchall()

    @staticmethod
    def write(student_id, student_name, student_class, student_marks):
        c.execute(f"INSERT INTO students VALUES ('{student_id}', '{student_name}', '{student_class}', {student_marks})")
        #         return c.fetchall()

    @staticmethod
    def delete(student_id):
        c.execute(f"DELETE FROM students WHERE student_id=:student_id", {'student_id': student_id})
        #         return c.fetchall()

    @staticmethod
    def bulk_write(student_list):
        c.executemany(f"INSERT INTO students VALUES (?,?,?,?)", student_list)
        return c.fetchall()

    @staticmethod
    def update(student_id, student_name, student_class, student_marks):
        sqlite_update_query = """Update students set student_name = ?, student_class = ?, student_marks = ? where 
        student_id = ? """
        column_values = (student_name, student_class, student_marks, student_id)
        c.execute(sqlite_update_query, column_values)


db = SQLiteConnector()
# print(db.select('U100'))
