from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship

from database import Base


class Students(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    student_id = Column(String, unique=True, index=True, nullable=False)
    student_name = Column(String(255), index=True, nullable=False)
    student_class = Column(String(100), index=True, nullable=False)
    student_marks = Column(Integer, index=True, nullable=False)

