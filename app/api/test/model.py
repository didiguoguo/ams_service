#encoding:utf8

from sqlalchemy import Column, String, Integer
import sys
sys.path.append('../../')
from db import Base

class Test(Base):
    __tablename__ = 'test'
    id = Column(Integer(), primary_key=True, nullable=False)
    name = Column(String(64), nullable=False)
    type = Column(String(20))
    work_type = Column(String(20))
    target_name = Column(String(128))
    target_id = Column(Integer())
    start_time = Column(Integer())
    create_time = Column(Integer())
    end_time = Column(Integer())
    duration = Column(Integer())
    times = Column(Integer())
    status = Column(String(10))

    def info(self):
        return dict(id=self.id,
                    name=self.name,
                    type=self.type,
                    work_type=self.work_type,
                    target_name=self.target_name,
                    target_id=self.target_id,
                    start_time=self.start_time,
                    end_time=self.end_time,
                    create_time=self.create_time,
                    duration=self.duration,
                    times=self.times,
                    status=self.status
                    )
