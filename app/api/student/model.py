#encoding:utf8

from sqlalchemy import Column, String, Integer
import sys
sys.path.append('../../')
from db import Base

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer(), primary_key=True, nullable=False)
    student_name = Column(String(64), nullable=False)
    gender = Column(Integer())
    id_card_num = Column(Integer(), nullable=False)
    phone_num = Column(Integer(), nullable=False)
    job_title = Column(String(64))
    enter_time = Column(Integer())
    class_id = Column(Integer())
    class_name = Column(String(64))
    theory_result = Column(Integer())
    practise_result = Column(Integer())

    def info(self):
        return dict(id=self.id,
                    student_name=self.student_name,
                    gender=self.gender,
                    id_card_num=self.id_card_num,
                    phone_num=self.phone_num,
                    job_title=self.job_title,
                    enter_time=self.enter_time,
                    class_id=self.class_id,
                    class_name=self.class_name,
                    theory_result=self.theory_result,
                    practise_result=self.practise_result
                    )
