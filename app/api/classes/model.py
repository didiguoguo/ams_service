#encoding:utf8

from sqlalchemy import Column, String, Integer
import sys
sys.path.append('../../')
from db import Base

class Classes(Base):
    __tablename__ = 'class'
    id = Column(Integer(), primary_key=True, nullable=False)
    class_name = Column(String(64), nullable=False)
    begin_address = Column(String(128))
    begin_time = Column(Integer())
    end_time = Column(Integer())
    course_plan = Column(String(128))
    create_time = Column(Integer())

    def info(self):
        return dict(id=self.id,
                    class_name=self.class_name,
                    begin_address=self.begin_address,
                    begin_time=self.begin_time,
                    end_time=self.end_time,
                    create_time=self.create_time,
                    course_plan=self.course_plan,
                    )
