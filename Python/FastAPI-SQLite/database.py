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

    def selectAll(self):
        c.execute(f"SELECT * FROM students ORDER BY student_id")
        return c.fetchall()

    def select(self, student_id):
        c.execute(f"SELECT * FROM students WHERE student_id=:student_id", {'student_id': student_id})
        return c.fetchall()

    def write(self, student_id, student_name, student_class, student_marks):
        c.execute(f"INSERT INTO students VALUES ('{student_id}', '{student_name}', '{student_class}', {student_marks})")
        #         return c.fetchall()

    def delete(self, student_id):
        c.execute(f"DELETE FROM students WHERE student_id=:student_id", {'student_id': student_id})
        #         return c.fetchall()

    def bulkWrite(self, student_list):
        c.executemany(f"INSERT INTO students VALUES (?,?,?,?)", student_list)
        return c.fetchall()


db = SQLiteConnector()
# print(db.select('U100'))
